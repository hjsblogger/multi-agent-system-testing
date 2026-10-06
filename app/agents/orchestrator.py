import json
from app.model import model

CODE_HINTS = ["code", "python", "yaml", "config", "docker", "function", "script"]


def _classify(state):
    r = model.invoke(f'''You are the Orchestrator of a multi-agent assistant.
Conversation history: {state.get("conversation", [])}
Current user request: {state["user_message"]}
Return JSON only: {{"needs_planning":true/false,"needs_research":true/false,"needs_coding":true/false}}
Complex requests need planning. Factual requests need research. Code/config requests need coding. Avoid unnecessary specialists.''')
    text = r.content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        d = json.loads(text)
        return {k: bool(d.get(k, False)) for k in ("needs_planning", "needs_research", "needs_coding")}
    except Exception:
        msg = state["user_message"].lower()
        return {"needs_planning": True, "needs_research": True, "needs_coding": any(x in msg for x in CODE_HINTS)}


def orchestrator(state):
    # Classify the request once per turn; later hops route from the stored decision.
    d = {k: state[k] for k in ("needs_planning", "needs_research", "needs_coding") if k in state}
    if len(d) < 3:
        d = _classify(state)

    if d["needs_planning"] and not state.get("plan"): nxt = "planner"
    elif d["needs_research"] and not state.get("research"): nxt = "researcher"
    elif d["needs_coding"] and not state.get("code"): nxt = "coder"
    elif d["needs_coding"] and not state.get("verifier_passed"): nxt = "verifier"
    elif state.get("verifier_passed"): nxt = "end"
    else: nxt = "finalize"

    return {**d, "next_step": nxt, "trace": state.get("trace", []) + [{"agent": "orchestrator", "action": "route", "target": nxt, "status": "completed"}]}
