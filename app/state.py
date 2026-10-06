from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    session_id: str
    user_message: str
    conversation: List[Dict[str, Any]]
    verifier_retries: int
    trace: List[Dict[str, Any]]
    plan: str
    research: str
    code: str
    final_response: str
