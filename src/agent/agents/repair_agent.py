from agent.agent_state import AgentState
from agent.repair_generator import repair_code

class RepairAgent:
    def __init__(self, client, model: str):
        self.client = client
        self.model = model

    def run(self, state: AgentState) -> dict:
        repaired_code = repair_code(
            client=self.client,
            model=self.model,
            class_model=state["class_model"],
            sequence_model=state["sequence_model"],
            generated_code=state["generated_code"],
            feedback=state["feedback"],
        )

        new_iteration = state["iteration"] + 1

        output_path = (
            state["output_dir"]
            / f"iteration_{new_iteration:02d}.py")

        output_path.write_text(repaired_code, encoding="utf-8",)

        return {"generated_code": repaired_code, "output_path": output_path, "iteration": new_iteration,}
