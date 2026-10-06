from langgraph.graph import StateGraph, START, END

from app.state import AgentState
from app.agents.orchestrator import orchestrator
from app.agents.planner import planner
from app.agents.researcher import researcher
from app.agents.coder import coder
from app.agents.verifier import verifier
from app.agents.finalizer import finalizer

SPECIALISTS = ["planner", "researcher", "coder", "verifier"]


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("orchestrator", orchestrator)
    builder.add_node("planner", planner)
    builder.add_node("researcher", researcher)
    builder.add_node("coder", coder)
    builder.add_node("verifier", verifier)
    builder.add_node("finalize", finalizer)

    builder.add_edge(START, "orchestrator")

    builder.add_conditional_edges(
        "orchestrator",
        lambda state: state["next_step"],
        {**{name: name for name in SPECIALISTS}, "finalize": "finalize", "end": END},
    )

    # Every specialist reports back to the orchestrator for the next routing decision.
    for name in SPECIALISTS:
        builder.add_edge(name, "orchestrator")

    builder.add_edge("finalize", END)

    return builder.compile()
