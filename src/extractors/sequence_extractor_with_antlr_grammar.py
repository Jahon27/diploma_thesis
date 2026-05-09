import os
import sys
import tempfile

SRC_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(SRC_DIR)

from .sequence_to_sqd_extractor import generate_sqd_from_xml

from antlr4 import FileStream, CommonTokenStream
from antlr.SequenceDiagramLexer import SequenceDiagramLexer
from antlr.SequenceDiagramParser import SequenceDiagramParser
from antlr.sequence_model_builder import SequenceModelBuilder
from antlr.sequence_code_generator import generate_sequence_code

def generate_sequence_code_from_sqd(sqd_path: str) -> str:
    input_stream = FileStream(sqd_path, encoding="utf-8")
    lexer = SequenceDiagramLexer(input_stream)
    token_stream = CommonTokenStream(lexer)

    parser = SequenceDiagramParser(token_stream)
    tree = parser.sequence()

    builder = SequenceModelBuilder()
    model = builder.visit(tree)

    return generate_sequence_code(model)


def generate_sequence_code_from_xml(xml_path: str) -> str:
    sqd_code = generate_sqd_from_xml(xml_path)

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".sqd",
        delete=False
    ) as temp_file:
        temp_file.write(sqd_code)
        temp_sqd_path = temp_file.name

    try:
        return generate_sequence_code_from_sqd(temp_sqd_path)
    finally:
        os.remove(temp_sqd_path)