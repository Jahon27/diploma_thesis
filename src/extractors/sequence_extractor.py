import xml.etree.ElementTree as ET

from src.helper import to_class_name, clean_text, parse_xml

def is_lifeline_cell(cell: ET.Element) -> bool:
    style = cell.get("style", "")
    vertex = cell.get("vertex")
    return vertex == "1" and "shape=umlLifeline" in style

def extract_participants(cells: list[ET.Element]) -> dict[str, str]:
    participants = {}

    for cell in cells:
        if is_lifeline_cell(cell):
            cell_id = cell.get("id")
            value = clean_text(cell.get("value", ""))

            if cell_id:
                participants[cell_id] = value

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
    participants: dict[str, str],
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

def extract_messages(
    cells: list[ET.Element],
    participants: dict[str, str],
    parent_map: dict[str, str],
    lifeline_geometry: dict[str, dict[str, float]]
) -> list[dict]:
    messages = []

    for cell in cells:
        if not is_message_edge(cell):
            continue

        source = cell.get("source")
        target = cell.get("target")
        label = clean_text(cell.get("value", ""))

        source_lifeline = None
        target_lifeline = None

        # 1. Пытаемся определить source/target через id, как раньше
        if source:
            source_lifeline = resolve_lifeline_id(source, participants, parent_map)

        if target:
            target_lifeline = resolve_lifeline_id(target, participants, parent_map)

        # 2. Если чего-то не хватает — используем fallback по координатам
        endpoints = get_edge_endpoints(cell)

        if not source_lifeline:
            source_lifeline = resolve_lifeline_by_x(
                endpoints["source_x"],
                lifeline_geometry
            )

        if not target_lifeline:
            target_lifeline = resolve_lifeline_by_x(
                endpoints["target_x"],
                lifeline_geometry
            )

        # 3. Если даже после fallback ничего не нашли — пропускаем
        if not source_lifeline or not target_lifeline:
            print(
                "Skipped edge after fallback:",
                cell.get("id"),
                "label=", label,
                "source=", source,
                "target=", target,
                "endpoints=", endpoints
            )
            continue

        message_type = "return" if is_return_message(cell) else "call"

        messages.append({
            "type": message_type,
            "from_id": source_lifeline,
            "to_id": target_lifeline,
            "from_name": participants[source_lifeline],
            "to_name": participants[target_lifeline],
            "label": label,
            "is_self_call": source_lifeline == target_lifeline,
            "y": get_message_y(cell),
        })

    messages.sort(key=lambda msg: msg["y"])
    return messages

def get_message_y(cell: ET.Element) -> float:
    geometry = cell.find("mxGeometry")
    if geometry is None:
        return 0.0

    # 1. Пробуем sourcePoint
    for point in geometry.findall("mxPoint"):
        y = point.get("y")
        if y:
            try:
                return float(y)
            except ValueError:
                pass

    # 2. Пробуем точки внутри Array
    for array in geometry.findall("Array"):
        for point in array.findall("mxPoint"):
            y = point.get("y")
            if y:
                try:
                    return float(y)
                except ValueError:
                    pass

    return 0.0

def extract_lifeline_geometry(
    cells: list[ET.Element],
    participants: dict[str, str]
) -> dict[str, dict[str, float]]:
    lifeline_geometry = {}

    for cell in cells:
        cell_id = cell.get("id")
        if cell_id not in participants:
            continue

        geometry = cell.find("mxGeometry")
        if geometry is None:
            continue

        try:
            x = float(geometry.get("x", "0"))
        except ValueError:
            x = 0.0

        try:
            width = float(geometry.get("width", "0"))
        except ValueError:
            width = 0.0

        center_x = x + width / 2

        lifeline_geometry[cell_id] = {
            "x": x,
            "width": width,
            "center_x": center_x,
        }

    return lifeline_geometry

def get_edge_endpoints(cell: ET.Element) -> dict[str, float | None]:
    geometry = cell.find("mxGeometry")
    if geometry is None:
        return {
            "source_x": None,
            "source_y": None,
            "target_x": None,
            "target_y": None,
        }

    source_x = None
    source_y = None
    target_x = None
    target_y = None

    for point in geometry.findall("mxPoint"):
        point_role = point.get("as")

        if point_role == "sourcePoint":
            try:
                source_x = float(point.get("x")) if point.get("x") is not None else None
            except ValueError:
                source_x = None

            try:
                source_y = float(point.get("y")) if point.get("y") is not None else None
            except ValueError:
                source_y = None

        elif point_role == "targetPoint":
            try:
                target_x = float(point.get("x")) if point.get("x") is not None else None
            except ValueError:
                target_x = None

            try:
                target_y = float(point.get("y")) if point.get("y") is not None else None
            except ValueError:
                target_y = None

    return {
        "source_x": source_x,
        "source_y": source_y,
        "target_x": target_x,
        "target_y": target_y,
    }

def resolve_lifeline_by_x(
    x_value: float | None,
    lifeline_geometry: dict[str, dict[str, float]]
) -> str | None:
    if x_value is None:
        return None

    closest_lifeline_id = None
    min_distance = None

    for lifeline_id, geom in lifeline_geometry.items():
        center_x = geom["center_x"]
        distance = abs(x_value - center_x)

        if min_distance is None or distance < min_distance:
            min_distance = distance
            closest_lifeline_id = lifeline_id

    return closest_lifeline_id

def parse_participant_value(value: str) -> dict[str, str]:
    value = clean_text(value)

    if ":" in value:
        left, right = value.split(":", 1)
    else:
        left = ""
        right = value

    var_name = left.strip()
    class_name = right.strip()

    # если имя переменной отсутствует
    if not var_name:
        var_name = class_name.lower()

    # чистим имена
    var_name = clean_text(var_name)
    var_name = var_name.replace(" ", "_")

    class_name = to_class_name(class_name)

    return {
        "var_name": var_name,
        "class_name": class_name,
    }

def build_sequence_objects(participants: dict[str, str]) -> dict[str, dict[str, str]]:
    sequence_objects = {}
    used_var_names = {}

    for participant_id, participant_value in participants.items():
        parsed = parse_participant_value(participant_value)

        var_name = parsed["var_name"]
        class_name = parsed["class_name"]

        if var_name in used_var_names:
            used_var_names[var_name] += 1
            var_name = f"{var_name}_{used_var_names[var_name]}"
        else:
            used_var_names[var_name] = 1

        sequence_objects[participant_id] = {
            "var_name": var_name,
            "class_name": class_name,
        }

    return sequence_objects

def extract_method_name(label: str) -> str:
    label = clean_text(label)

    if "(" in label:
        label = label.split("(", 1)[0].strip()

    label = label.replace(" ", "_")
    return label

def generate_sequence_code(
    sequence_objects: dict[str, dict[str, str]],
    messages: list[dict]
) -> str:
    lines = []

    lines.append("def run_sequence():")

    # создание объектов
    for participant_id, obj in sequence_objects.items():
        var_name = obj["var_name"]
        class_name = obj["class_name"]
        lines.append(f"    {var_name} = {class_name}()")

    lines.append("")

    # вызовы методов
    for msg in messages:
        if msg["type"] == "return":
            continue

        receiver_id = msg["to_id"]
        receiver = sequence_objects.get(receiver_id)

        if not receiver:
            continue

        method_name = extract_method_name(msg["label"])
        if not method_name:
            continue

        lines.append(f"    {receiver['var_name']}.{method_name}()")

    if len(lines) == 2:
        lines.append("    pass")

    return "\n".join(lines)

def generate_sequence_code_from_xml(xml_path: str) -> str:
    cells = parse_xml(xml_path)
    participants = extract_participants(cells)
    lifeline_geometry = extract_lifeline_geometry(cells, participants)
    parent_map = build_parent_map(cells)
    messages = extract_messages(cells, participants, parent_map, lifeline_geometry)
    sequence_objects = build_sequence_objects(participants)
    sequence_code = generate_sequence_code(sequence_objects, messages)
    return sequence_code

def main():
    input_xml = "../diagrams/uml-sequence-example_1.drawio.xml"

    cells = parse_xml(input_xml)
    participants = extract_participants(cells)
    parent_map = build_parent_map(cells)
    lifeline_geometry = extract_lifeline_geometry(cells, participants)
    messages = extract_messages(cells, participants, parent_map, lifeline_geometry)
    sequence_objects = build_sequence_objects(participants)
    sequence_code = generate_sequence_code(sequence_objects, messages)

    print("Participants found:")
    for participant_id, participant_name in participants.items():
        print(f"- {participant_id}: {participant_name}")

    print("\nTesting parent resolution:")

    for cell in cells[:10]:  # первые 10 для проверки
        cell_id = cell.get("id")
        if not cell_id:
            continue

        resolved = resolve_lifeline_id(cell_id, participants, parent_map)

        if resolved:
            print(f"{cell_id} → {participants[resolved]}")

    print("\nMessages found:")
    for msg in messages:
        kind = "self-call" if msg["is_self_call"] else msg["type"]

        print(
            f"- y={msg['y']:.1f} | {kind}: "
            f"{msg['from_name']} -> {msg['to_name']} : {msg['label']}"
        )

    print("\nLifeline geometry:")
    for participant_id, geom in lifeline_geometry.items():
        print(
            f"- {participants[participant_id]}: "
            f"x={geom['x']}, width={geom['width']}, center_x={geom['center_x']}"
        )

    print("\nEdge endpoints:")
    for cell in cells:
        if is_message_edge(cell):
            endpoints = get_edge_endpoints(cell)
            print(
                f"- {cell.get('id')} | label={clean_text(cell.get('value', ''))} | "
                f"source_x={endpoints['source_x']}, source_y={endpoints['source_y']} | "
                f"target_x={endpoints['target_x']}, target_y={endpoints['target_y']}"
            )

    print("\nResolve by X:")
    test_x_values = [90.0, 95.0, 220.0, 269.5, 270.0]

    for x in test_x_values:
        resolved_id = resolve_lifeline_by_x(x, lifeline_geometry)
        resolved_name = participants[resolved_id] if resolved_id else None
        print(f"x={x} -> {resolved_name}")

    print("\nParsed participants:")

    for pid, val in participants.items():
        parsed = parse_participant_value(val)
        print(f"{val} -> {parsed}")

    print("\nSequence objects:")
    for participant_id, obj in sequence_objects.items():
        print(f"- {participant_id}: {obj}")

    print("\nGenerated sequence code:\n")
    print(sequence_code)

if __name__ == "__main__":
    main()