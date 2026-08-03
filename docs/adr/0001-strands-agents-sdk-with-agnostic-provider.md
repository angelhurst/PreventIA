# 0001 — Strands Agents SDK with a provider-agnostic model layer

**Status:** Superseded by 0008
**Date:** 2026-08-03
**Deciders:** Felipe Carvajal Brown

## Context

PreventIA needs an agent that holds a daily conversation with a patient, calls tools to read and
write a clinical record, and consumes the MCP servers the Impact Lab exposes over its curated
anonymized datasets. The Impact Lab requires Claude as the engine for the competing prototype and
supplies Anthropic API credits per participant. That requirement governs the Lab; it does not govern
what the project defaults to outside it.

The build window is two days, shared between two developers, one of whom is joining the repository
cold.

## Decision

Use the **Strands Agents SDK** in Python, with the model provider behind an internal seam rather
than hardcoded.

**Kimi `kimi-k3` is the configured default. Claude runs the Lab demo**, selected by setting
`PREVENTIA_MODEL_PROVIDER=anthropic`. Nothing else in the codebase changes between the two.

`kimi-k3` is chosen over `kimi-k2.6` and `kimi-k2.5` for deprecation safety rather than capability:
Moonshot discontinued the entire `kimi-k2` series on 25 May 2026 and closed `kimi-k2.5` to newly
registered users after 31 August 2026, so the current flagship is the one least likely to be
withdrawn mid-project.

Install both providers, Anthropic rather than Bedrock, since the project uses Anthropic API credits
directly and has no AWS account:

```bash
pip install 'strands-agents[anthropic,openai]'
```

Kimi is reached through Strands' OpenAI-compatible provider with `base_url` set to
`https://api.moonshot.ai/v1`, which needs no additional dependency. Model construction lives in
`agent/models.py` and nowhere else.

Consume Lab MCP servers through Strands' own `MCPClient` rather than a separate MCP stack.

## Consequences

- MCP client support and session persistence come from the framework instead of being written by
  hand under time pressure.
- The agent core never learns which model it is talking to, so switching providers is one
  environment variable.
- Two providers means the clinical layer has to be correct under both. This is a feature rather than
  a cost: it forces the guardrail and semáforo suites to be run against each, which is exactly the
  evidence that clinical safety lives in deterministic code and not in one vendor's alignment
  behaviour. It is also two sets of API keys, two failure modes and two bills.
- Neither developer has shipped Strands before. Framework-specific problems will be debugged during
  the Lab, which is the real cost of this decision.

## Alternatives considered

**Raw Anthropic Python SDK with a hand-rolled tool loop.** Fewest unknowns, nothing between the code
and the model, easiest to debug at 2am. Rejected because the tool loop, session storage and MCP
client would all have to be written and debugged in the same two days, the Lab's value is largely in
its MCP-exposed datasets, and it would hardcode a single vendor.

**Claude Agent SDK.** Anthropic's own agent harness, closest to Claude Code's loop. Rejected as
heavier than this problem requires, more opinionated about filesystem context than a WhatsApp
conversation loop needs, and single-vendor by construction.

**Claude as the configured default.** Simpler, one provider, matches what runs on stage. Rejected
because the Lab requirement applies to the competing prototype, not to the project, and building the
provider seam only for the demo would mean discovering its cost after the Lab rather than before.
