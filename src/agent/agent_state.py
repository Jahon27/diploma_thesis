
from pathlib import Path
from typing import Literal, TypedDict


class ReviewIssue(TypedDict):
    category: Literal[
        "syntax",
        "uml_structure",
        "behavior",
        "other",
    ]
    severity: Literal["error", "warning"]
    message: str


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

    review_issues: list[ReviewIssue]
    review_passed: bool
