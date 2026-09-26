import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from evaluation.evaluator import evaluate
from agent.feedback_builder import build_feedback
from agent.repair_generator import repair_code


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL = "nvidia/nemotron-3.5-lightning:free"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)


def run_agent(
    class_xml_path: Path,
    sequence_xml_path: Path,
    reference_path: Path,
    original_output_path: Path,
    output_dir: Path,
):
    output_dir.mkdir(parents=True, exist_ok=True)

    class_xml = class_xml_path.read_text(encoding="utf-8")
    sequence_xml = sequence_xml_path.read_text(encoding="utf-8")

    generated_code = original_output_path.read_text(
        encoding="utf-8"
    )

    # -------------------------
    # ITERATION 0
    # -------------------------

    evaluation_before = evaluate(
        reference_path,
        original_output_path
    )

    print("\n=== BEFORE REPAIR ===")
    print(
        "UML fidelity:",
        evaluation_before["uml_fidelity"]["overall_uml_fidelity"]
    )

    feedback = build_feedback(evaluation_before)

    print("\n=== FEEDBACK ===\n")
    print(feedback)

    # -------------------------
    # REPAIR
    # -------------------------

    print("\nSending repair request to LLM...")

    repaired_code = repair_code(
        client=client,
        model=MODEL,
        class_xml=class_xml,
        sequence_xml=sequence_xml,
        generated_code=generated_code,
        feedback=feedback,
    )

    repaired_path = output_dir / "iteration_01.py"

    repaired_path.write_text(
        repaired_code,
        encoding="utf-8"
    )

    # -------------------------
    # EVALUATE AGAIN
    # -------------------------

    evaluation_after = evaluate(
        reference_path,
        repaired_path
    )

    print("\n=== AFTER REPAIR ===")
    print(
        "UML fidelity:",
        evaluation_after["uml_fidelity"]["overall_uml_fidelity"]
    )

    print(
        "\nImprovement:",
        round(
            evaluation_after["uml_fidelity"]["overall_uml_fidelity"]
            - evaluation_before["uml_fidelity"]["overall_uml_fidelity"],
            4
        )
    )


if __name__ == "__main__":
    run_agent(
        class_xml_path=BASE_DIR / "diagrams" / "online-shopping-class.drawio.xml",

        sequence_xml_path=BASE_DIR / "diagrams" / "online-shopping-sequence.drawio.xml",

        reference_path=BASE_DIR / "reference" / "online_shopping_reference.py",

        original_output_path=(
            BASE_DIR
            / "outputs"
            / "ai_generated_output"
            / "ai_online_shopping.py"
        ),

        output_dir=(
            BASE_DIR
            / "outputs"
            / "agent_generated_output"
            / "tc1"
        ),
    )