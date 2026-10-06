import json
import os

from app.model import model

MAX_VERIFIER_RETRIES = int(os.getenv("MAX_VERIFIER_RETRIES", "1"))


def _parse(text):
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        d = json.loads(text)
        return bool(d.get("passed", False)), str(d.get("feedback", "")), str(d.get("answer", ""))
    except Exception:
        # Unparseable reply: treat it as the final answer, as before the retry loop existed.
        return True, "", text


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

Return JSON only:
{{"passed": true/false, "feedback": "...", "answer": "..."}}

- passed: true if the code/configuration is correct and complete.
- feedback: if passed is false, the specific problems the Coder must fix. Otherwise empty.
- answer: the final answer to show the user. If passed is false, give the best corrected answer you can.
""")

    passed, feedback, answer = _parse(r.content)
    retries = state.get("verifier_retries", 0)
    retry = not passed and retries < MAX_VERIFIER_RETRIES

    update = {
        "verifier_passed": passed,
        "trace": state["trace"] + [{
            "agent": "verifier",
            "action": "verify",
            "passed": passed,
            "retry": retry,
            "feedback": feedback,
            "output": answer,
        }],
    }

    if retry:
        # Send the work back to the Coder with the feedback.
        update.update({"needs_revision": True, "verifier_feedback": feedback, "verifier_retries": retries + 1})
    else:
        # Passed, or out of retries: return the best answer we have.
        update["final_response"] = answer

    return update
