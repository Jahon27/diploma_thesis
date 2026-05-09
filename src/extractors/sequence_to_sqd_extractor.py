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


def generate_sqd(
    participants: dict[str, dict[str, str]],
    messages: list[dict]
) -> str:
    lines = []

    for participant in participants.values():
        lines.append(
            f"participant {participant['var_name']} {participant['class_name']}"
        )

    lines.append("")

    for msg in messages:
        if msg["type"] == "return":
            lines.append(
                f"return {msg['from']} {msg['to']} {clean_method_name(msg['label'])}"
            )
        elif msg["is_self_call"]:
            lines.append(
                f"self {msg['from']} {clean_method_name(msg['label'])}"
            )
        else:
            lines.append(
                f"call {msg['from']} {msg['to']} {clean_method_name(msg['label'])}"
            )

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

    return generate_sqd(participants, messages)


def main():
    input_xml = "../diagrams/uml-sequence-example_1.drawio.xml"
    output_sqd = "../outputs/sequence_example.sqd"

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