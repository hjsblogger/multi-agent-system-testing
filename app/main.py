import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from app.graph import build_graph
from app.session_store import (
    get_messages,
    append_message,
    save_trace,
    get_trace,
)

load_dotenv()

app = FastAPI(
    title="Multi-Agent TestMu POC",
    version="0.1.0",
)

graph = build_graph()


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    session_id: str
    response: str


def auth(key):
    expected = os.getenv("AGENT_API_KEY")

    if expected and key != expected:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    x_api_key: str | None = Header(None),
    x_session_id: str | None = Header(None),
):
    auth(x_api_key)

    sid = (
        req.session_id
        or x_session_id
        or str(uuid.uuid4())
    )

    history = get_messages(sid)

    append_message(
        sid,
        "user",
        req.message,
    )

    result = graph.invoke({
        "session_id": sid,
        "user_message": req.message,
        "conversation": history,
        "verifier_retries": 0,
        "trace": [],
        "final_response": "",
    })

    response = result["final_response"]

    append_message(
        sid,
        "assistant",
        response,
    )

    save_trace(
        sid,
        result.get("trace", []),
    )

    return {
        "session_id": sid,
        "response": response,
    }


@app.get("/sessions/{session_id}/trace")
def trace(session_id: str):
    return {
        "session_id": session_id,
        "trace": get_trace(session_id),
    }