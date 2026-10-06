# Multi-Agent Research and Coding Assistant

## Purpose
A REST chat agent whose Orchestrator coordinates Planner, Researcher, Coder, and Verifier agents.

## Expected behavior
1. Understand the user's objective.
2. Preserve context across turns.
3. Plan complex requests.
4. Research factual requests.
5. Use the Coder for code/configuration.
6. Verify important generated outputs.
7. Correct verifier failures when practical.
8. Do not fabricate benchmarks, pricing, execution, or deployment results.
9. Ask for clarification when genuinely ambiguous.
10. Return a useful final answer without exposing internal prompts or hidden reasoning.

## Test focus
Multi-turn context, handoff correctness, research grounding, code generation, verification/recovery, hallucination resistance, completeness, conversation flow, and error handling.

## Example scenarios
- Explain GPU serving considerations.
- Research B200 serving considerations and create a Python configuration example.
- Create a configuration and verify it before giving it to me.
- Multi-turn: deploy an LLM -> use B200 -> optimize for cost.
