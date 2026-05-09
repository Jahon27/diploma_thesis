import re
import html
import xml.etree.ElementTree as ET

from src.helper import clean_name, to_class_name

def to_attr_name(text: str) -> str:
    text = html.unescape(text or "").strip()
    text = re.sub(r"<[^>]+>", "", text)

    if text and text[0] in "+-#/":
        text = text[1:].strip()

    if ":" in text:
        text = text.split(":", 1)[0].strip()

    return clean_name(text)

def to_method_name(text: str) -> str:
    text = html.unescape(text or "").strip()
    text = re.sub(r"<[^>]+>", "", text)

    if text and text[0] in "+-#/":
        text = text[1:].strip()

    if "(" in text:
        text = text.split("(", 1)[0].strip()

    return clean_name(text)

def is_class_cell(cell: ET.Element) -> bool:
    style = cell.get("style", "")
    value = cell.get("value", "")
    vertex = cell.get("vertex")

    return vertex == "1" and "swimlane" in style and bool(value.strip())

def is_separator_cell(cell: ET.Element) -> bool:
    style = cell.get("style", "")
    vertex = cell.get("vertex")
    return vertex == "1" and "line;" in style

def is_attribute_text(value: str) -> bool:
    value = html.unescape(value or "").strip()
    return ":" in value and "(" not in value and ")" not in value

def is_method_text(value: str) -> bool:
    value = html.unescape(value or "").strip()
    return "(" in value and ")" in value

def get_y(cell: ET.Element) -> float:
    geometry = cell.find("mxGeometry")
    if geometry is None:
        return 0.0

    y = geometry.get("y", "0")
    try:
        return float(y)
    except ValueError:
        return 0.0

def extract_classes(xml_path: str) -> dict[str, str]:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    classes = {}

    for cell in root.findall(".//mxCell"):
        if is_class_cell(cell):
            class_id = cell.get("id")
            class_name = to_class_name(cell.get("value", ""))

            if class_id and class_name not in classes.values():
                classes[class_id] = class_name

    return classes

def build_children_map(cells: list[ET.Element]) -> dict[str, list[ET.Element]]:
    children_by_parent: dict[str, list[ET.Element]] = {}
    for cell in cells:
        parent = cell.get("parent")
        if parent:
            children_by_parent.setdefault(parent, []).append(cell)
    return children_by_parent

def extract_attributes(xml_path: str, classes: dict[str, str]) -> dict[str, list[str]]:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    cells = root.findall(".//mxCell")
    result = {class_name: [] for class_name in classes.values()}
    children_by_parent = build_children_map(cells)

    for class_id, class_name in classes.items():
        children = children_by_parent.get(class_id, [])
        children.sort(key=get_y)

        separator_y = None
        for child in children:
            if is_separator_cell(child):
                separator_y = get_y(child)
                break

        for child in children:
            value = child.get("value", "").strip()
            if not value or is_separator_cell(child):
                continue

            child_y = get_y(child)

            if separator_y is not None and child_y >= separator_y:
                continue

            if is_attribute_text(value):
                attr_name = to_attr_name(value)
                if attr_name and attr_name not in result[class_name]:
                    result[class_name].append(attr_name)

    return result

def extract_methods(xml_path: str, classes: dict[str, str]) -> dict[str, list[str]]:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    cells = root.findall(".//mxCell")
    result = {class_name: [] for class_name in classes.values()}
    children_by_parent = build_children_map(cells)

    for class_id, class_name in classes.items():
        children = children_by_parent.get(class_id, [])
        children.sort(key=get_y)

        separator_y = None
        for child in children:
            if is_separator_cell(child):
                separator_y = get_y(child)
                break

        for child in children:
            value = child.get("value", "").strip()
            if not value or is_separator_cell(child):
                continue

            child_y = get_y(child)

            if separator_y is not None and child_y < separator_y:
                continue

            if is_method_text(value):
                method_name = to_method_name(value)
                if method_name and method_name not in result[class_name]:
                    result[class_name].append(method_name)

    return result

def generate_python_code(
    class_attributes: dict[str, list[str]],
    class_methods: dict[str, list[str]],
    inheritance_map: dict[str, str]
) -> str:
    lines = []

    all_class_names = list(class_attributes.keys())

    for class_name in all_class_names:
        attributes = class_attributes.get(class_name, [])
        methods = class_methods.get(class_name, [])

        parent_class = inheritance_map.get(class_name)

        if parent_class:
            lines.append(f"class {class_name}({parent_class}):")
        else:
            lines.append(f"class {class_name}:")

        if not attributes and not methods:
            lines.append("    pass")
            lines.append("")
            continue

        if attributes:
            lines.append("    def __init__(self):")
            for attr in attributes:
                lines.append(f"        self.{attr} = None")
            lines.append("")

        for method in methods:
            lines.append(f"    def {method}(self):")
            lines.append("        pass")
            lines.append("")

    return "\n".join(lines)

def main():
    input_xml = "../diagrams/uml-class-example_1.drawio.xml"
    output_py = "../outputs/uml-class-example_1.py"

    classes = extract_classes(input_xml)
    class_attributes = extract_attributes(input_xml, classes)
    class_methods = extract_methods(input_xml, classes)
    inheritance_map = extract_inheritance(input_xml, classes)
    code = generate_python_code(class_attributes, class_methods, inheritance_map)

    with open(output_py, "w", encoding="utf-8") as f:
        f.write(code)

    print("Classes found:")
    for class_id, class_name in classes.items():
        print(f"- {class_name} (id={class_id})")

    print("\nAttributes found:")
    for class_name, attrs in class_attributes.items():
        print(f"- {class_name}: {attrs}")

    print("\nMethods found:")
    for class_name, methods in class_methods.items():
        print(f"- {class_name}: {methods}")

    print(f"\nPython file saved at: {output_py}")

def is_inheritance_edge(cell: ET.Element) -> bool:
    if cell.get("edge") != "1":
        return False

    style = cell.get("style", "")
    return "endArrow=block" in style and "endFill=0" in style

def extract_inheritance(xml_path: str, classes: dict[str, str]) -> dict[str, str]:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    inheritance_map = {}

    for cell in root.findall(".//mxCell"):
        if not is_inheritance_edge(cell):
            continue

        source = cell.get("source")
        target = cell.get("target")

        if not source or not target:
            continue

        if source in classes and target in classes:
            child_class = classes[source]
            parent_class = classes[target]
            inheritance_map[child_class] = parent_class

    return inheritance_map

def generate_class_code_from_xml(xml_path: str) -> str:
    classes = extract_classes(xml_path)
    class_attributes = extract_attributes(xml_path, classes)
    class_methods = extract_methods(xml_path, classes)
    inheritance_map = extract_inheritance(xml_path, classes)
    code = generate_python_code(class_attributes, class_methods, inheritance_map)
    return code

if __name__ == "__main__":
    main()