import os

from dotenv import load_dotenv
from openai import OpenAI

from agent.repair_generator import repair_code
from langgraph.graph import END, START, StateGraph
from agent.agent_state import AgentState
from evaluation.evaluator import evaluate
from agent.feedback_builder import build_feedback
from agent.code_generator import generate_code

load_dotenv()

MODEL = "qwen/qwen3-coder-30b-a3b-instruct"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
def generate_node(state: AgentState) -> dict:
    generated_code = generate_code(
        client=client,
        model=MODEL,
        class_model=state["class_model"],
        sequence_model=state["sequence_model"],
    )

    output_path = (
        state["output_dir"]
        / "iteration_00.py"
    )

    output_path.write_text(
        generated_code,
        encoding="utf-8",
    )

    return {
        "generated_code": generated_code,
        "output_path": output_path,
    }

def evaluate_node(state: AgentState) -> dict:
    evaluation = evaluate(
        state["reference_path"],
        state["output_path"],
    )

    fidelity = evaluation[
        "uml_fidelity"
    ]["overall_uml_fidelity"]

    print(
        f"\n=== EVALUATION: iteration "
        f"{state['iteration']:02d} ==="
    )
    print("UML fidelity:", fidelity)

    feedback = build_feedback(evaluation)

    print("\nDetected problems:")
    print(feedback)

    return {
        "evaluation": evaluation,
    }

def feedback_node(state: AgentState) -> dict:
    feedback = build_feedback(state["evaluation"])

    return {
        "feedback": feedback,
    }

def should_continue(state: AgentState) -> str:
    evaluation = state["evaluation"]

    fidelity = evaluation["uml_fidelity"]["overall_uml_fidelity"]

    if fidelity >= 1.0:
        return "end"

    if state["iteration"] >= state["max_iterations"]:
        return "end"

    return "repair"

def repair_node(state: AgentState) -> dict:
    repaired_code = repair_code(
        client=client,
        model=MODEL,
        class_model=state["class_model"],
        sequence_model=state["sequence_model"],
        generated_code=state["generated_code"],
        feedback=state["feedback"],
    )

    new_iteration = state["iteration"] + 1

    output_path = (
        state["output_dir"]
        / f"iteration_{new_iteration:02d}.py"
    )

    output_path.write_text(
        repaired_code,
        encoding="utf-8",
    )

    return {
        "generated_code": repaired_code,
        "output_path": output_path,
        "iteration": new_iteration,
    }
builder = StateGraph(AgentState)

builder.add_node("generate", generate_node)
builder.add_node("evaluate", evaluate_node)
builder.add_node("feedback", feedback_node)
builder.add_node("repair", repair_node)

builder.add_edge(START, "generate")
builder.add_edge("generate", "evaluate")

builder.add_conditional_edges(
    "evaluate",
    should_continue,
    {
        "repair": "feedback",
        "end": END,
    },
)

builder.add_edge("feedback", "repair")
builder.add_edge("repair", "evaluate")

agent_graph = builder.compile()