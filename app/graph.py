from langgraph.graph import StateGraph, START, END

from app.state import AgentState
from app.agents.planner import planner
from app.agents.researcher import researcher
from app.agents.coder import coder
from app.agents.verifier import verifier


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("planner", planner)
    builder.add_node("researcher", researcher)
    builder.add_node("coder", coder)
    builder.add_node("verifier", verifier)

    builder.add_edge(START, "planner")
    builder.add_edge("planner", "researcher")
    builder.add_edge("researcher", "coder")
    builder.add_edge("coder", "verifier")
    builder.add_edge("verifier", END)

    return builder.compile()