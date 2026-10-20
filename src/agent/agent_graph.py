import os

from dotenv import load_dotenv
from openai import OpenAI
from langgraph.graph import START, END, StateGraph

from agent.agent_state import AgentState
from agent.agents.generator_agent import GeneratorAgent
from agent.agents.repair_agent import RepairAgent

from evaluation.evaluator import evaluate
from agent.feedback_builder import build_feedback

load_dotenv()

GENERATOR_MODEL = "qwen/qwen3-coder-30b-a3b-instruct"
REPAIR_MODEL = "deepseek/deepseek-chat"

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"],)

generator_agent = GeneratorAgent(client, GENERATOR_MODEL)
repair_agent = RepairAgent(client, REPAIR_MODEL)

def evaluate_node(state: AgentState) -> dict:
    evaluation = evaluate(state["reference_path"], state["output_path"],)

    fidelity = evaluation["uml_fidelity"]["overall_uml_fidelity"]

    print(f"\n=== EVALUATION: iteration " f"{state['iteration']:02d} ===")
    print("UML fidelity:", fidelity)

    feedback = build_feedback(evaluation)

    print("\nDetected problems:")
    print(feedback)

    return {"evaluation": evaluation,}

def feedback_node(state: AgentState) -> dict:
    feedback = build_feedback(state["evaluation"])
    return {"feedback": feedback,}

def should_continue(state: AgentState) -> str:
    fidelity = state["evaluation"]["uml_fidelity"]["overall_uml_fidelity"]

    if fidelity >= 1.0:
        return "end"

    if state["iteration"] >= state["max_iterations"]:
        return "end"

    return "repair"

builder = StateGraph(AgentState)

builder.add_node("generator", generator_agent.run,)
builder.add_node("evaluator",  evaluate_node,)
builder.add_node("feedback", feedback_node,)
builder.add_node("repair", repair_agent.run,)
builder.add_edge(START, "generator")
builder.add_edge("generator", "evaluator")
builder.add_conditional_edges("evaluator", should_continue,{"repair": "feedback", "end": END,},)
builder.add_edge("feedback", "repair")
builder.add_edge("repair", "evaluator")

agent_graph = builder.compile()