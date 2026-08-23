import html
import xml.etree.ElementTree as ET


def clean_text(text: str) -> str:
    return html.unescape(text or "").strip()


def parse_xml(xml_path: str) -> list[ET.Element]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return root.findall(".//mxCell")


def is_lifeline_cell(cell: ET.Element) -> bool:
    style = cell.get("style", "")
    return cell.get("vertex") == "1" and "shape=umlLifeline" in style


def parse_participant_value(value: str) -> dict[str, str]:
    value = clean_text(value)

    if ":" in value:
        var_name, class_name = value.split(":", 1)
        return {
            "var_name": var_name.strip(),
            "class_name": class_name.strip()
        }

    return {
        "var_name": value.strip().lower(),
        "class_name": value.strip()
    }


def extract_participants(cells: list[ET.Element]) -> dict[str, dict[str, str]]:
    participants = {}

    for cell in cells:
        if is_lifeline_cell(cell):
            cell_id = cell.get("id")
            value = cell.get("value", "")

            if cell_id:
                participants[cell_id] = parse_participant_value(value)

    return participants


def build_parent_map(cells: list[ET.Element]) -> dict[str, str]:
    parent_map = {}

    for cell in cells:
        cell_id = cell.get("id")
        parent_id = cell.get("parent")

        if cell_id and parent_id:
            parent_map[cell_id] = parent_id

    return parent_map


def resolve_lifeline_id(
    cell_id: str,
    participants: dict[str, dict[str, str]],
    parent_map: dict[str, str]
) -> str | None:
    current_id = cell_id

    while current_id:
        if current_id in participants:
            return current_id

        current_id = parent_map.get(current_id)

    return None


def is_message_edge(cell: ET.Element) -> bool:
    return cell.get("edge") == "1"


def is_return_message(cell: ET.Element) -> bool:
    style = cell.get("style", "")
    return "dashed=1" in style


def get_message_y(cell: ET.Element) -> float:
    geometry = cell.find("mxGeometry")
    if geometry is None:
        return 0.0

    for point in geometry.findall("mxPoint"):
        y = point.get("y")
        if y:
            return float(y)

    for array in geometry.findall("Array"):
        for point in array.findall("mxPoint"):
            y = point.get("y")
            if y:
                return float(y)

    return 0.0


def get_point(cell: ET.Element, point_name: str) -> tuple[float | None, float | None]:
    geometry = cell.find("mxGeometry")
    if geometry is None:
        return None, None

    point = geometry.find(f"mxPoint[@as='{point_name}']")
    if point is None:
        return None, None

    x = point.get("x")
    y = point.get("y")

    return (
        float(x) if x is not None else None,
        float(y) if y is not None else None
    )


def extract_lifeline_geometry(
    cells: list[ET.Element],
    participants: dict[str, dict[str, str]]
) -> dict[str, dict[str, float]]:
    geometry_by_id = {}

    for cell in cells:
        cell_id = cell.get("id")

        if cell_id not in participants:
            continue

        geometry = cell.find("mxGeometry")
        if geometry is None:
            continue

        x = float(geometry.get("x", "0"))
        width = float(geometry.get("width", "0"))
        center_x = x + width / 2

        geometry_by_id[cell_id] = {
            "x": x,
            "width": width,
            "center_x": center_x
        }

    return geometry_by_id


def resolve_lifeline_by_x(
    x: float | None,
    lifeline_geometry: dict[str, dict[str, float]]
) -> str | None:
    if x is None:
        return None

    closest_id = None
    closest_distance = float("inf")

    for lifeline_id, geometry in lifeline_geometry.items():
        distance = abs(x - geometry["center_x"])

        if distance < closest_distance:
            closest_distance = distance
            closest_id = lifeline_id

    return closest_id


def extract_messages(
    cells: list[ET.Element],
    participants: dict[str, dict[str, str]],
    parent_map: dict[str, str],
    lifeline_geometry: dict[str, dict[str, float]]
) -> list[dict]:
    messages = []

    for cell in cells:
        if not is_message_edge(cell):
            continue

        label = clean_text(cell.get("value", ""))
        if not label:
            continue

        source = cell.get("source")
        target = cell.get("target")

        source_lifeline = resolve_lifeline_id(source, participants, parent_map) if source else None
        target_lifeline = resolve_lifeline_id(target, participants, parent_map) if target else None

        if source_lifeline is None:
            source_x, _ = get_point(cell, "sourcePoint")
            source_lifeline = resolve_lifeline_by_x(source_x, lifeline_geometry)

        if target_lifeline is None:
            target_x, _ = get_point(cell, "targetPoint")
            target_lifeline = resolve_lifeline_by_x(target_x, lifeline_geometry)

        if source_lifeline is None or target_lifeline is None:
            print("Skipped message:", label)
            continue

        message_type = "return" if is_return_message(cell) else "call"

        messages.append({
            "type": message_type,
            "from_id": source_lifeline,
            "to_id": target_lifeline,
            "from": participants[source_lifeline]["var_name"],
            "to": participants[target_lifeline]["var_name"],
            "label": label,
            "is_self_call": source_lifeline == target_lifeline,
            "y": get_message_y(cell),
        })

    messages.sort(key=lambda msg: msg["y"])
    return messages


def clean_method_name(label: str) -> str:
    label = clean_text(label)

    if "(" in label:
        label = label.split("(", 1)[0]

    return label.strip()

def is_fragment_cell(cell: ET.Element) -> bool:
    value = clean_text(cell.get("value", "")).lower()
    style = cell.get("style", "")

    return (
        cell.get("vertex") == "1"
        and value in {"alt", "loop"}
        and "shape=mxgraph.sysml.package" in style
    )


def extract_fragments(cells: list[ET.Element]) -> list[dict]:
    fragments = []

    for cell in cells:
        if not is_fragment_cell(cell):
            continue

        geometry = cell.find("mxGeometry")
        if geometry is None:
            continue

        x = float(geometry.get("x", "0"))
        y = float(geometry.get("y", "0"))
        width = float(geometry.get("width", "0"))
        height = float(geometry.get("height", "0"))

        fragments.append({
            "id": cell.get("id"),
            "type": clean_text(cell.get("value", "")).lower(),
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "end_x": x + width,
            "end_y": y + height,
            "conditions": [],
            "children": [],
            "items": [],
            "parent": None,
        })

    return fragments


def contains_fragment(parent: dict, child: dict) -> bool:
    return (
        parent["id"] != child["id"]
        and parent["x"] <= child["x"]
        and parent["y"] <= child["y"]
        and parent["end_x"] >= child["end_x"]
        and parent["end_y"] >= child["end_y"]
    )


def contains_message(fragment: dict, msg: dict) -> bool:
    return fragment["y"] <= msg["y"] <= fragment["end_y"]


def build_fragment_tree(fragments: list[dict]) -> list[dict]:
    for fragment in fragments:
        containers = [
            candidate for candidate in fragments
            if contains_fragment(candidate, fragment)
        ]

        if containers:
            parent = min(
                containers,
                key=lambda f: f["width"] * f["height"]
            )
            fragment["parent"] = parent["id"]
            parent["children"].append(fragment)

    root_fragments = [
        fragment for fragment in fragments
        if fragment["parent"] is None
    ]

    return root_fragments


def is_condition_text(cell: ET.Element) -> bool:
    value = clean_text(cell.get("value", ""))

    return (
        cell.get("vertex") == "1"
        and value.startswith("[")
        and value.endswith("]")
    )


def clean_condition(value: str) -> str:
    value = clean_text(value)
    value = value.strip("[]").strip()

    parts = value.split()
    if not parts:
        return "condition"

    return parts[0] + "".join(part.capitalize() for part in parts[1:])


def add_fragment_conditions(
    fragments: list[dict],
    cells: list[ET.Element]
) -> None:
    X_TOLERANCE = 30.0
    Y_TOLERANCE = 25.0

    for cell in cells:
        if not is_condition_text(cell):
            continue

        geometry = cell.find("mxGeometry")
        if geometry is None:
            continue

        x = float(geometry.get("x", "0"))
        y = float(geometry.get("y", "0"))

        condition = clean_condition(cell.get("value", ""))

        containing = [
            fragment
            for fragment in fragments
            if fragment["x"] - X_TOLERANCE <= x <= fragment["end_x"] + X_TOLERANCE
            and fragment["y"] - Y_TOLERANCE <= y <= fragment["end_y"]
        ]

        if not containing:
            print(
                f"Warning: condition '{condition}' "
                f"at ({x}, {y}) was not assigned to any fragment"
            )
            continue

        # Nested fragment gets priority
        fragment = min(
            containing,
            key=lambda f: f["width"] * f["height"]
        )

        fragment["conditions"].append({
            "y": y,
            "condition": condition
        })

    for fragment in fragments:
        fragment["conditions"].sort(
            key=lambda c: c["y"]
        )

def find_innermost_fragment(
    msg: dict,
    fragments: list[dict]
) -> dict | None:
    containing = [
        fragment for fragment in fragments
        if contains_message(fragment, msg)
    ]

    if not containing:
        return None

    return min(containing, key=lambda f: f["width"] * f["height"])


def assign_items_to_fragments(
    messages: list[dict],
    fragments: list[dict]
) -> list[dict]:
    root_items = []

    for msg in messages:
        fragment = find_innermost_fragment(msg, fragments)

        if fragment is None:
            root_items.append({
                "kind": "message",
                "y": msg["y"],
                "data": msg
            })
        else:
            fragment["items"].append({
                "kind": "message",
                "y": msg["y"],
                "data": msg
            })

    for fragment in fragments:
        if fragment["parent"] is None:
            root_items.append({
                "kind": "fragment",
                "y": fragment["y"],
                "data": fragment
            })
        else:
            parent = next(
                f for f in fragments
                if f["id"] == fragment["parent"]
            )
            parent["items"].append({
                "kind": "fragment",
                "y": fragment["y"],
                "data": fragment
            })

    for fragment in fragments:
        fragment["items"].sort(key=lambda item: item["y"])

    root_items.sort(key=lambda item: item["y"])
    return root_items


def message_to_sqd_line(msg: dict, indent: int = 0) -> str:
    prefix = "    " * indent

    if msg["type"] == "return":
        return f"{prefix}return {msg['from']} {msg['to']} {clean_method_name(msg['label'])}"

    if msg["is_self_call"]:
        return f"{prefix}self {msg['from']} {clean_method_name(msg['label'])}"

    return f"{prefix}call {msg['from']} {msg['to']} {clean_method_name(msg['label'])}"


def emit_items(items: list[dict], indent: int = 0) -> list[str]:
    lines = []

    for item in items:
        if item["kind"] == "message":
            lines.append(message_to_sqd_line(item["data"], indent))

        elif item["kind"] == "fragment":
            lines.extend(emit_fragment(item["data"], indent))

    return lines


def emit_fragment(fragment: dict, indent: int = 0) -> list[str]:
    prefix = "    " * indent
    lines = []

    if fragment["type"] == "loop":
        condition = "condition"

        if fragment["conditions"]:
            condition = fragment["conditions"][0]["condition"]

        lines.append(f"{prefix}loop {condition}")
        lines.extend(emit_items(fragment["items"], indent + 1))
        lines.append(f"{prefix}end")
        return lines

    if fragment["type"] == "alt":
        conditions = fragment["conditions"]

        main_condition = (
            conditions[0]["condition"]
            if len(conditions) >= 1
            else "condition"
        )

        else_condition = (
            conditions[1]["condition"]
            if len(conditions) >= 2
            else None
        )

        split_y = (
            conditions[1]["y"]
            if len(conditions) >= 2
            else None
        )

        then_items = []
        else_items = []

        for item in fragment["items"]:
            if split_y is not None and item["y"] >= split_y:
                else_items.append(item)
            else:
                then_items.append(item)

        lines.append(f"{prefix}alt {main_condition}")
        lines.extend(emit_items(then_items, indent + 1))

        if else_condition:
            lines.append(f"{prefix}else {else_condition}")
            lines.extend(emit_items(else_items, indent + 1))

        lines.append(f"{prefix}end")
        return lines

    return lines


def generate_sqd(
    participants: dict[str, dict[str, str]],
    messages: list[dict],
    fragments: list[dict] | None = None
) -> str:
    fragments = fragments or []
    lines = []

    for participant in participants.values():
        lines.append(
            f"participant {participant['var_name']} {participant['class_name']}"
        )

    lines.append("")

    build_fragment_tree(fragments)

    root_items = assign_items_to_fragments(messages, fragments)

    lines.extend(emit_items(root_items, indent=0))

    return "\n".join(lines)


def generate_sqd_from_xml(xml_path: str) -> str:
    cells = parse_xml(xml_path)

    participants = extract_participants(cells)
    parent_map = build_parent_map(cells)
    lifeline_geometry = extract_lifeline_geometry(cells, participants)

    messages = extract_messages(
        cells,
        participants,
        parent_map,
        lifeline_geometry
    )

    fragments = extract_fragments(cells)
    add_fragment_conditions(fragments, cells)

    return generate_sqd(participants, messages, fragments)

def main():
    input_xml = "../diagrams/online-shopping-sequence.drawio.xml"
    output_sqd = "../outputs/online_shopping_test_1.sqd"

    sqd_code = generate_sqd_from_xml(input_xml)

    with open(output_sqd, "w", encoding="utf-8") as f:
        f.write(sqd_code)

    print("Generated SQD:")
    print()
    print(sqd_code)
    print()
    print(f"Saved to: {output_sqd}")


if __name__ == "__main__":
    main()