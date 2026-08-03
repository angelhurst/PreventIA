# 0008 — Local Ollama runtime as the default, Claude as the build tool

**Status:** Accepted. Supersedes 0001
**Date:** 2026-08-03
**Deciders:** Felipe Carvajal Brown

## Context

ADR-0001 recorded the model layer as provider-agnostic with `kimi-k3` as the configured default and
Claude as "what runs the Lab demo". That last part conflated two different things.

Claude is the tool the team builds the software **with**. It is not the model that answers a
patient. The Impact Lab's requirement is satisfied by building with Claude; it does not dictate what
the deployed agent runs on.

Separately, Angel has a Mac Studio available to serve a local open-weights model, which changes what
the intended runtime is rather than merely adding an option.

## Decision

**The runtime is model-agnostic, and the default is a local model served by Ollama on the Mac
Studio.** `PREVENTIA_MODEL_PROVIDER` unset means Ollama. `kimi` and `anthropic` remain registered
alternatives behind the same seam.

**Claude is the build tool and is documented as such.** No code assumes Anthropic is answering.

Ollama is chosen over llama.cpp for the local runtime because Strands ships a first-class
`OllamaModel` provider, because Ollama runs as a daemon with an HTTP API that is straightforward to
expose to another machine, and because since v0.19 it runs models through Apple's MLX on Apple
Silicon by default. On a machine that is not ours and cannot be debugged in person, least setup
wins.

Install: `pip install 'strands-agents[ollama,openai,anthropic]'`.

`OLLAMA_MODEL` deliberately has no default. The model depends on the Mac Studio's unified memory and
on how well the candidate handles tool calling, and it is agreed with Angel before Phase 1 rather
than guessed here.

## Consequences

- What gets developed against every day is what is intended to run, instead of a hosted stand-in.
- No per-token cost for the default path, and patient conversations never leave a machine the team
  controls. That is a real argument in a health pitch, not just an engineering preference.
- The default depends on a machine that belongs to someone else being reachable. When it is not,
  `PREVENTIA_MODEL_PROVIDER=kimi` or `=anthropic` is the manual fallback. Automatic failover was
  considered and rejected as one more thing to debug during a two-day build.
- Open-weights models vary in tool-calling reliability. This is the strongest test the deterministic
  semáforo floor (ADR-0004) and the output filter (ADR-0005) will get, and running those suites
  against the local model is how the clinical-safety claim stops depending on any vendor's
  alignment work.
- Serving to a second machine means the Mac Studio's Ollama has to listen beyond localhost, which is
  a network exposure decision on hardware that is not ours. Angel decides how it is reached.

## Alternatives considered

**Keep `kimi-k3` as the default, register Ollama as the planned runtime.** Always answers, nobody is
blocked by a machine being off. Rejected because it means developing against something other than
the target, and the gap surfaces late.

**Local Ollama first with automatic fallback to Kimi.** The eventual right answer. Rejected for now:
it is more code, and it creates a state where nobody can tell which model answered without reading
logs, which is exactly the ambiguity to avoid while establishing clinical behaviour.

**llama.cpp via `llama-server`.** More control over quantization, context and sampling, no daemon in
the way. Rejected as hand-configured server work on a machine we cannot touch, reached through the
generic OpenAI provider instead of a native one.
