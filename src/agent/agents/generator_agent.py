
from openai import OpenAI

from agent.agent_state import AgentState
from agent.code_generator import generate_code

class GeneratorAgent:
    """Generates Python source code from UML models."""

    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model

    def run(self, state: AgentState) -> dict:
        print("\n=== GENERATOR AGENT ===")
        generated_code = generate_code(client=self.client, model=self.model, class_model=state["class_model"], sequence_model=state["sequence_model"],)

        if not generated_code or not generated_code.strip():
            raise RuntimeError("Generator Agent returned empty code.")

        output_path = (state["output_dir"] / "iteration_00.py")
        output_path.parent.mkdir(parents=True, exist_ok=True,)
        output_path.write_text(generated_code, encoding="utf-8",)
        return {"generated_code": generated_code, "output_path": output_path,}
