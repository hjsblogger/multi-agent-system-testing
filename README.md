# Multi-Agent + TestMu AI POC

A small, runnable multi-agent system designed to expose **one REST endpoint** to TestMu AI Agent Testing while keeping the Planner, Researcher, Coder, and Verifier agents behind an Orchestrator.

## Architecture

```text
TestMu AI Agent Testing
          |
          | POST /chat
          v
+-----------------------+
|     FastAPI API       |
+-----------+-----------+
            |
            v
+-----------------------+
|     Orchestrator      |
+-----------+-----------+
            |
    +-------+-------+----------------+
    |               |                |
    v               v                v
 Planner        Researcher         Coder
                                    |
                                    v
                                Verifier
                                    |
                         PASS ------+------ FAIL
                          |                 |
                          v                 v
                       Final             Coder
                       response            |
                                           +--> Verifier
```

The LLM used by all agents is **Google Gemini**. The default configuration uses `gemini-3.5-flash-lite`. The Gemini API has a free tier with free input/output tokens for eligible models, subject to Google's current rate limits and model availability. Check Google's pricing/model pages if your project does not have access to the configured model.

## 1. Configure Gemini

Create/get your Gemini API key from Google AI Studio, then:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GEMINI_API_KEY=YOUR_GEMINI_KEY
GEMINI_MODEL=gemini-3.5-flash-lite
AGENT_API_KEY=change-me
MAX_VERIFIER_RETRIES=1
```

Do **not** commit `.env` or your API key to Git.

If your key does not have access to `gemini-3.5-flash-lite`, change `GEMINI_MODEL` to a Gemini model available to your project, for example:

```env
GEMINI_MODEL=gemini-2.5-flash
```

## 2. Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 3. Health check

```bash
curl http://localhost:8000/health
```

Expected:

```json
{"status":"ok"}
```

## 4. Test the agent directly

```bash
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: change-me' \
  -d '{
    "session_id":"demo-001",
    "message":"Research B200 GPU serving considerations and create a small Python configuration example."
  }'
```

You should receive:

```json
{
  "session_id": "demo-001",
  "response": "..."
}
```

## 5. Inspect the internal agent trace

```bash
curl http://localhost:8000/sessions/demo-001/trace
```

This is for debugging the POC. TestMu does not need this endpoint.

A typical trace will show routing such as:

```text
orchestrator -> planner
orchestrator -> researcher
orchestrator -> coder
orchestrator -> verifier
finalizer
```

## 6. Test multi-turn context

Use the same `session_id` for every turn:

```bash
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: change-me' \
  -d '{"session_id":"demo-002","message":"I want to deploy an LLM."}'

curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: change-me' \
  -d '{"session_id":"demo-002","message":"Use B200 GPUs."}'

curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: change-me' \
  -d '{"session_id":"demo-002","message":"Now optimize the architecture for cost."}'
```

## 7. TestMu AI Agent Testing

Deploy this API behind HTTPS. The primary TestMu endpoint is:

```text
POST https://YOUR-DOMAIN/chat
```

Request:

```json
{
  "session_id": "string",
  "message": "string"
}
```

Response:

```json
{
  "session_id": "string",
  "response": "string"
}
```

Configure the endpoint in TestMu's Chat Agent Endpoint Profile. Keep the same `session_id` across turns when testing conversation context.

The POC also accepts the session ID through:

```text
X-Session-ID: demo-001
```

and the API protection key through:

```text
X-API-Key: change-me
```

## Suggested TestMu scenarios

### Scenario 1: Simple research

```text
What is GPU memory bandwidth?
```

Expected high-level path:

```text
Orchestrator -> Researcher -> Final
```

### Scenario 2: Research + coding

```text
Research B200 serving considerations and create a Python configuration example.
```

Expected high-level path:

```text
Orchestrator -> Planner -> Researcher -> Coder -> Verifier -> Final
```

### Scenario 3: Verification

```text
Create a deployment configuration and verify it before giving me the final answer.
```

### Scenario 4: Multi-turn context

```text
Turn 1: I want to deploy an LLM.
Turn 2: Use B200 GPUs.
Turn 3: Now optimize the architecture for cost.
```

### Scenario 5: Ambiguous request

```text
Build the best AI infrastructure for me.
```

The agent should ask for missing requirements rather than inventing them.

## Docker

```bash
docker build -t multi-agent-testmu-poc .
docker run --rm -p 8000:8000 --env-file .env multi-agent-testmu-poc
```

Then expose the service through a public HTTPS URL or the appropriate secure TestMu connectivity mechanism.

## Production improvements

This POC intentionally keeps infrastructure simple. Before production, replace the in-memory session store with Redis/PostgreSQL, add durable LangGraph checkpoints, add request IDs and distributed tracing, add rate limiting, use a proper secret manager, and replace the built-in Researcher knowledge base with a real search/RAG tool.
