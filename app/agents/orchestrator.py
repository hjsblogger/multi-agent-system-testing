import json
from app.model import model

def orchestrator(state):
    r=model.invoke(f'''You are the Orchestrator of a multi-agent assistant.
Conversation history: {state.get("conversation", [])}
Current user request: {state["user_message"]}
Return JSON only: {{"needs_planning":true/false,"needs_research":true/false,"needs_coding":true/false}}
Complex requests need planning. Factual requests need research. Code/config requests need coding. Avoid unnecessary specialists.''')
    try: d=json.loads(r.content)
    except Exception:
        d={"needs_planning":True,"needs_research":True,"needs_coding":any(x in state["user_message"].lower() for x in ["code","python","yaml","config","docker"])}
    if not state.get("plan") and d["needs_planning"]: nxt="planner"
    elif not state.get("research") and d["needs_research"]: nxt="researcher"
    elif d["needs_coding"] and not state.get("code"): nxt="coder"
    elif d["needs_coding"] and not state.get("verifier_passed"): nxt="verifier"
    else: nxt="finalize"
    return {**d,"next_step":nxt,"trace":state.get("trace",[])+[{"agent":"orchestrator","action":"route","target":nxt,"status":"completed"}]}
