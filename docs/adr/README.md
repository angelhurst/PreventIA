# Architecture Decision Records

One file per significant decision, numbered and immutable.

An Accepted ADR is never edited, extended, or given a new section. A changed decision always gets a
new, next-numbered ADR whose Status reads "Supersedes 00XX"; the only edit ever made to the old one
is flipping its Status line to "Superseded by 00YY".

| # | Title | Status |
|---|-------|--------|
| [0001](0001-strands-agents-sdk-with-agnostic-provider.md) | Strands Agents SDK with a provider-agnostic model layer | Superseded by 0008 |
| [0002](0002-sqlite-clinical-record-file-sessions.md) | SQLite for the clinical record, file sessions for transcripts | Accepted |
| [0003](0003-whatsapp-cloud-api-behind-channel-adapter.md) | WhatsApp Cloud API test number behind a channel adapter | Accepted |
| [0004](0004-deterministic-floor-for-the-semaforo.md) | Deterministic rule floor for the semáforo, model may only escalate | Accepted |
| [0005](0005-three-layer-clinical-guardrail.md) | Three-layer clinical guardrail with an adversarial test suite | Accepted |
| [0006](0006-clinician-triage-queue-as-escalation-surface.md) | Clinician triage queue as the escalation surface | Accepted |
| [0007](0007-synthetic-cohort-with-caja-adapter.md) | Synthetic seed cohort with an adapter for the Caja dataset | Accepted |
| [0008](0008-local-ollama-runtime-claude-as-build-tool.md) | Local Ollama runtime as the default, Claude as the build tool | Accepted |
| [0009](0009-repository-discoverability.md) | Repository description and topics | Accepted |
