from extractors.class_extractor import generate_class_code_from_xml
from extractors.sequence_extractor_with_antlr_grammar import generate_sequence_code_from_xml
from extractors.sequence_extractor_with_antlr_grammar import generate_sequence_code_from_sqd


def main():
    class_xml = "./diagrams/online-shopping-class.drawio.xml"
    sequence_xml = "./diagrams/online-shopping-sequence.drawio.xml"
    output_py = "./outputs/online_shopping_gen_model.py"

    class_code = generate_class_code_from_xml(class_xml)
    sequence_code = generate_sequence_code_from_xml(sequence_xml)

    print("Generated SQD:")
    print(sequence_code)
    full_code = (
        class_code
        + "\n\n"
        + sequence_code
        + "\n\nif __name__ == '__main__':\n"
        + "    run_sequence()\n"
    )

    with open(output_py, "w", encoding="utf-8") as f:
        f.write(full_code)

    print(f"Combined Python code saved to: {output_py}")


if __name__ == "__main__":
    main()