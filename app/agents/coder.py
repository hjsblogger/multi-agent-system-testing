from app.model import model
def coder(state):
    revision = ""
    if state.get("needs_revision"):
        revision = f'''
Your previous attempt:
{state.get("code", "")}
The Verifier rejected it with this feedback:
{state.get("verifier_feedback", "")}
Fix every problem in the feedback.'''
    r = model.invoke(f'''You are the Coder agent.
Conversation history: {state.get("conversation", [])}
User request: {state["user_message"]}
Plan: {state.get("plan", "")}
Research: {state.get("research", "")}
If implementation/configuration is required, produce a small useful example. Do not claim code was executed or deployed. Prefer complete snippets over pseudo-code.{revision}''')
    return {"code": r.content, "needs_revision": False, "trace": state.get("trace", []) + [{"agent":"coder","action":"generate","status":"completed"}]}
