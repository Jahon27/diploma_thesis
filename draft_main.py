# from extractors.class_extractor import generate_class_code_from_xml
# from extractors.sequence_extractor import generate_sequence_code_from_xml
#
# def main():
#     class_xml = "./diagrams/uml-class-example_2.drawio.xml"
#     sequence_xml = "./diagrams/uml-sequence-example_1.drawio.xml"
#     output_py = "./outputs/generated_model3.py"
#
#     class_code = generate_class_code_from_xml(class_xml)
#     # sequence_code = generate_sequence_code_from_xml(sequence_xml)
#
#     full_code1= class_code + "\n\nif __name__ == '__main__':\n    run_sequence()\n"
#     # full_code = class_code + "\n\n" + sequence_code + "\n\nif __name__ == '__main__':\n    run_sequence()\n"
#
#     with open(output_py, "w", encoding="utf-8") as f:
#         f.write(full_code1)
#
#     print(f"Combined Python code saved to: {output_py}")
#
#
# if __name__ == "__main__":
#     main()

