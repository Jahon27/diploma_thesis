from pathlib import Path
from typing import TypedDict

class AgentState(TypedDict):
    class_model: str
    sequence_model: str

    reference_path: Path
    output_dir: Path
    output_path: Path

    generated_code: str
    evaluation: dict
    feedback: str

    iteration: int
    max_iterations: int