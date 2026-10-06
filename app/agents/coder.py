from app.model import model
def coder(state):
    r = model.invoke(f'''You are the Coder agent.
User request: {state["user_message"]}
Plan: {state.get("plan", "")}
Research: {state.get("research", "")}
If implementation/configuration is required, produce a small useful example. Do not claim code was executed or deployed. Prefer complete snippets over pseudo-code.''')
    return {"code": r.content, "trace": state.get("trace", []) + [{"agent":"coder","action":"generate","status":"completed"}]}
