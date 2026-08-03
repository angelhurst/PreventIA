# Research brief

Paste the block below into a fresh session opened in the repository root. It is a research task, not
a build task: its output is evidence that shapes a future revision of `PRD.md`. Phase 1 does not
start until the flag table exists.

**Superseded in part.** All six workstreams below are complete; see `docs/research/README.md` for the
index and the resulting proposals. The original header also made Phase 1 wait on `OLLAMA_MODEL` being
pinned, which ADR-0010 removed when it moved the Lab runtime to Claude.

```
Research task for PreventIA. Read CLAUDE.md, PRD.md, ROADMAP.md and docs/adr/ first.

HARD CONSTRAINTS
- Research and write only. Do NOT write code, scaffold directories, install
  anything, or create the agent. Phase 1 has not started.
- Do NOT edit PRD.md. Your output shapes a future revision of it; you propose,
  Felipe decides.
- Never invent a clinical fact, figure, guideline, threshold or source. If you
  cannot verify something, write "unverified" and say what would verify it.
  A fabricated clinical criterion in this project is worse than a gap.
- Every non-obvious claim carries a source: URL, publisher, and date consulted.
  Prefer Chilean official sources (MINSAL, DEIS, Superintendencia de Salud) over
  general or US-centric ones, and say when you had to fall back.
- Mark anything that needs a clinician's sign-off as REQUIRES CLINICAL REVIEW
  instead of resolving it yourself.

OUTPUT
One markdown file per workstream in docs/research/, named YYYY-MM-DD-topic.md,
English, with a Sources section. Commit each one separately as
docs(research): <topic>, following the conventions in CLAUDE.md.

WORKSTREAMS

1. Self-reportable decompensation signals
   For hypertension, type 2 diabetes and heart failure in older adults: which
   early warning signs can a patient plausibly mention in ordinary conversation,
   without a device and without being asked a clinical question? For each, the
   guideline or literature behind it. This is the raw material for the semaforo
   flag table in clinical/rules/ (ADR-0004). Do not assign colors. Do not build
   the table. Gather candidates and their basis so a clinician can build it.

2. Chilean primary-care reality
   How cardiovascular follow-up actually works in the public system: Programa de
   Salud Cardiovascular, GES guarantees and their legal timeframes, real control
   frequency, who runs follow-up, what happens between controls today. Waiting
   list figures with source, date and methodology, since the PRD currently cites
   2.4 million people, 400+ and 500+ days and those numbers need provenance.

3. Adherence measurement and remote follow-up evidence
   How medication adherence is measured in practice and what validated
   instruments exist. Then: what evidence exists that remote or conversational
   follow-up changes emergency reconsultation or avoidable readmission in older
   adults. Report honestly, including null and weak results. PRD section 10
   makes this claim for the post-Lab horizon and must not overstate it.

4. How Chilean older adults actually use WhatsApp
   Text versus voice notes, typing patterns, literacy and vision constraints,
   what breaks. Feeds the patient-facing copy rules in CLAUDE.md section 8, and
   tells us whether text-first is the right assumption at all.

5. Caja La Araucana and the Lab dataset
   What is publicly known about Caja La Araucana as a health provider and what
   an anonymized, aggregated dataset from them would plausibly contain. The goal
   is to avoid baking assumptions into the SQLite schema that the real data
   cannot satisfy. Flag explicitly where we are guessing.

FINISH WITH
docs/research/README.md: an index, plus a short section listing exactly what you
would change in PRD.md and why, as a proposal. Flag every claim currently in
PRD.md that your research could not substantiate.
```

## Why it is shaped this way

Workstream 1 forbids assigning colors on purpose. ADR-0004 puts the flag table in the hands of the
team's healthcare professional; a research session gathers candidates and their clinical basis, and
the clinician still authors the table. Anything else would be a developer writing clinical criteria.

Workstream 2 points at figures already sitting in `PRD.md`. They came from the Lab's own framing and
will end up on a slide in front of judges who know the real ones, so they need provenance before the
pitch rather than after.
