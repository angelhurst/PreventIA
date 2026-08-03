# 0009 — Repository description and topics

**Status:** Accepted
**Date:** 2026-08-03
**Deciders:** Felipe Carvajal Brown

## Context

The repository is public. GitHub's own search ranks primarily on repository name, description and
topics; the README body is not a strong direct ranking factor for it, though it does matter for
Google and for answer engines, and for converting someone who has already landed.

Topic pages are the other half. Google and LLMs surface `github.com/topics/<name>` pages, and those
pages favour star count. GitHub auto-creates a topic page for any slug you invent, so an HTTP 200 is
not evidence a topic is real. Counts have to be checked.

## Decision

**Description**, Spanish, keyword-forward, one sentence:

> Seguimiento diario por WhatsApp a adultos mayores polimedicados: verifica adherencia, detecta
> descompensación temprana y escala al equipo de salud.

Spanish because the README is Spanish, the Lab is Chilean, and the people who most need to find this
read Spanish. The nine topic slugs are English and carry international discovery on their own.

**Topics**, verified counts as of 2026-08-03:

| Topic | Repos | Why |
|-------|-------|-----|
| `ai-agents` | 65,326 | Reach |
| `healthcare` | 13,988 | Reach, on target |
| `conversational-ai` | 2,756 | Describes the product |
| `whatsapp-bot` | 2,721 | Describes the channel |
| `chile` | 868 | Geographic, matches the Lab |
| `digital-health` | 780 | Mid-size, on target |
| `elderly-care` | 135 | Narrow, exact |
| `patient-monitoring` | 82 | Narrow, exact |
| `medication-adherence` | 19 | Narrow, exact |

Three broad for reach, three mid, three narrow enough to rank at the top of immediately. Nine sits
inside the 6 to 10 range where topics still carry relevance instead of diluting it.

## A note for Angel

`medication-adherence` has **nineteen repositories on it**. Nineteen. The topic page that describes
precisely what we are building is close to empty, and the repos sitting on it today are pill
reminder apps, mostly Android: `msarmi9/Sparkle`, `saad2134/dosezy`, `ntpinckney/trackmypills`. Good
software, and a different animal. None of them is a conversational agent that classifies clinical
risk and escalates to a care team.

So we rank at the top of that pond the day we push the topic, and we are plausibly the first Chilean
tool to ever sit on the tag.

**That last claim is unverified.** It is written here as a hunch, not as a fact, and it does not go
into a pitch, a slide or the README until somebody actually reads the nineteen. Checking it is a
five-minute job for whoever gets there first.

## Consequences

- Ranking first on three narrow topics from day one, instead of being invisible on three broad ones.
- Description and topics require admin on `angelhurst/PreventIA`. Felipe has push, not admin, so
  Angel sets them or grants admin.
- Stale repositories are penalised more heavily in this domain than in most. An out-of-date README
  actively costs ranking, so the README is maintained rather than written once.
- The Spanish description costs some reach with English-speaking searchers. Accepted: the topics
  carry that, and the primary audience reads Spanish.

## Alternatives considered

**English description.** Wider reach in GitHub and Google search. Rejected because the README, the
PRD and the Lab are Spanish, and a bilingual mismatch between description and README reads as
careless to the people the project is actually for.

**More topics, up to the maximum.** Rejected: more topics dilutes relevance rather than adding
reach, and unpopulated topic pages contribute nothing.

**Only the high-count topics** (`llm` at 109,514, `mcp` at 58,665). Rejected as the classic mistake.
Maximum reach, zero chance of being seen, and neither describes what this is.
