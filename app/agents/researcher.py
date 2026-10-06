from app.model import model
KNOWLEDGE='''POC knowledge: NVIDIA B200 is a Blackwell-generation accelerator for demanding AI workloads. LLM serving performance depends on model size, precision, memory capacity/bandwidth, KV-cache requirements, batching, and interconnect/networking. Prefill and decode can have different compute and memory characteristics. Production serving should be validated against model, sequence length, concurrency, and latency/throughput targets.'''
def researcher(state):
    r = model.invoke(f'''You are the Researcher agent.
Conversation history: {state.get("conversation", [])}
User request: {state["user_message"]}
Plan: {state.get("plan", "")}
Use this POC knowledge as source material: {KNOWLEDGE}
Produce concise factual findings. Distinguish facts from recommendations. Do not invent benchmark numbers or pricing.''')
    return {"research": r.content, "trace": state.get("trace", []) + [{"agent":"researcher","action":"research","status":"completed"}]}
