from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    session_id: str
    user_message: str
    conversation: List[Dict[str, Any]]
    verifier_retries: int
    trace: List[Dict[str, Any]]
    needs_planning: bool
    needs_research: bool
    needs_coding: bool
    next_step: str
    plan: str
    research: str
    code: str
    verifier_passed: bool
    final_response: str
