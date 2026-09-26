from typing import TypedDict

class AgentState(TypedDict):
    class_xml: str
    sequence_xml: str

    generated_code: str
    evaluation: dict
    feedback: str

    iteration: int
    max_iterations: int