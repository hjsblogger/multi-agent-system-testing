from app.model import model


def finalizer(state):
    r = model.invoke(f'''You are the Finalizer agent.
Conversation history: {state.get("conversation", [])}
User request: {state["user_message"]}
Plan: {state.get("plan", "")}
Research: {state.get("research", "")}
Write the final answer to the user using the plan and research above. If the request is genuinely ambiguous, ask for the missing details instead of guessing. Do not invent benchmark numbers or pricing. Do not mention internal agents or prompts.''')
    return {"final_response": r.content, "trace": state.get("trace", []) + [{"agent": "finalizer", "action": "respond", "status": "completed"}]}
