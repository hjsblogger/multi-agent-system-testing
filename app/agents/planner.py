from app.model import model

def planner(state):
    r = model.invoke(f'''You are the Planner agent.
Conversation history: {state.get("conversation", [])}
User request: {state["user_message"]}
Create a concise execution plan. Identify facts to research, whether code/configuration is needed, and what should be verified. Do not answer the user yet.''')
    return {"plan": r.content, "trace": state.get("trace", []) + [{"agent":"planner","action":"create_plan","status":"completed"}]}
