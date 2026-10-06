from pathlib import Path

from extractors.sequence_to_sqd_extractor import generate_sqd_from_xml
from extractors.class_extractor import (
    extract_classes,
    extract_attributes,
    extract_methods,
    extract_inheritance,
)


def build_class_model(xml_path: Path | str) -> str:
    """
    Converts a Draw.io UML class diagram into a compact textual
    representation suitable for sending to an LLM.
    """

    xml_path = str(xml_path)

    classes = extract_classes(xml_path)
    attributes = extract_attributes(xml_path, classes)
    methods = extract_methods(xml_path, classes)
    inheritance = extract_inheritance(xml_path, classes)

    lines = ["CLASS MODEL"]

    for class_name in classes.values():
        lines.append("")
        lines.append(f"class {class_name}")

        parent = inheritance.get(class_name)
        if parent:
            lines.append(f"  extends: {parent}")

        class_attributes = attributes.get(class_name, [])
        if class_attributes:
            lines.append(
                "  attributes: " + ", ".join(class_attributes)
            )
        else:
            lines.append("  attributes: none")

        class_methods = methods.get(class_name, [])
        if class_methods:
            lines.append(
                "  methods: " + ", ".join(class_methods)
            )
        else:
            lines.append("  methods: none")

    return "\n".join(lines)

def build_sequence_model(xml_path: Path | str) -> str:
    """
    Converts a Draw.io UML sequence diagram into the compact
    SQD representation used as LLM context.
    """

    sqd = generate_sqd_from_xml(str(xml_path))

    return (
        "SEQUENCE MODEL\n\n"
        + sqd
    )

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent

    class_xml_path = (
        base_dir
        / "diagrams"
        / "online-shopping-class.drawio.xml"
    )

    sequence_xml_path = (
        base_dir
        / "diagrams"
        / "online-shopping-sequence.drawio.xml"
    )

    class_model = build_class_model(class_xml_path)
    sequence_model = build_sequence_model(sequence_xml_path)

    print(class_model)

    print("\n" + "=" * 60 + "\n")

    print(sequence_model)