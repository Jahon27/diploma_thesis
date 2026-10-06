from pathlib import Path

from agent.agent_graph import agent_graph
from agent.uml_context_builder import (
    build_class_model,
    build_sequence_model,
)

BASE_DIR = Path(__file__).resolve().parent.parent

def run_agent(
    class_xml_path: Path,
    sequence_xml_path: Path,
    reference_path: Path,
    output_dir: Path,
    max_iterations: int = 3,
):
    output_dir.mkdir(parents=True, exist_ok=True)

    class_model = build_class_model(class_xml_path)
    sequence_model = build_sequence_model(sequence_xml_path)

    initial_state = {
        "class_model": class_model,
        "sequence_model": sequence_model,

        "reference_path": reference_path,
        "output_dir": output_dir,
        "output_path": output_dir / "iteration_00.py",

        "generated_code": "",

        "evaluation": {},
        "feedback": "",

        "iteration": 0,
        "max_iterations": max_iterations,
    }

    print("\n=== STARTING AGENT ===")

    final_state = agent_graph.invoke(initial_state)

    print("\n=== AGENT FINISHED ===")

    print(
        "Iterations:",
        final_state["iteration"]
    )

    print(
        "Final UML fidelity:",
        final_state["evaluation"]
        ["uml_fidelity"]
        ["overall_uml_fidelity"]
    )

    print(
        "Final output:",
        final_state["output_path"]
    )


if __name__ == "__main__":
    run_agent(
        class_xml_path=(
            BASE_DIR
            / "diagrams"
            / "tc4-class.drawio.xml"
        ),

        sequence_xml_path=(
            BASE_DIR
            / "diagrams"
            / "tc4-sequence.drawio.xml"
        ),

        reference_path=(
            BASE_DIR
            / "reference"
            / "testcase4.py"
        ),

        output_dir=(
            BASE_DIR
            / "outputs"
            / "agent_generated_output"
            / "tc4"
        ),

        max_iterations=3,
    )