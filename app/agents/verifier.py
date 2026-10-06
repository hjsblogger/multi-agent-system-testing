from app.model import model


def verifier(state):
    r = model.invoke(f"""
You are the Verifier agent.

User request:
{state["user_message"]}

Review the work performed by the other agents.

Conversation:
{state["conversation"]}

Plan:
{state.get("plan", "")}

Research:
{state.get("research", "")}

Code / configuration:
{state.get("code", "")}

Execution trace:
{state["trace"]}

Determine whether the work is correct and complete.

If it is correct, provide a concise final answer to the user.

If it is not correct, identify the problem and provide the best corrected answer.

Return ONLY the final answer that should be shown to the user.
""")

    response = r.content

    trace = state["trace"] + [
        {
            "agent": "verifier",
            "output": response
        }
    ]

    return {
        "final_response": response,
        "verifier_passed": True,
        "trace": trace
    }