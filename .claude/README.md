# .claude

Repository-scoped Claude Code configuration. Everything here is committed and shared between the two
developers on this project. It applies only inside this repository; nothing here changes anyone's
global setup.

## What goes where

| Path | What it is | Committed |
|---|---|---|
| `skills/<name>/SKILL.md` | A repo-scoped skill. Loads on demand when its frontmatter `description` matches what is being worked on, and costs nothing until then. | Yes |
| `settings.json` | Shared settings: permission allowlists, hooks, environment defaults that both developers should have. | Yes |
| `settings.local.json` | Personal overrides. Machine-specific paths, individual permission grants. | No, gitignored |

## Skills

A skill is the right home for knowledge that is specific to this project and only needed some of the
time. The test is whether it would otherwise be re-derived from scratch in a future session.

Candidates worth discussing, none of them written yet:

- The clinical boundary and how to test it, so the guardrail rules in `CLAUDE.md` section 2 do not
  have to be restated in every session that touches `clinical/`.
- WhatsApp Cloud API setup and the 24-hour window rule, so the demo runbook in `CLAUDE.md` section 11
  is executable rather than descriptive.
- The semáforo's floor-and-raise contract, so nobody reimplements de-escalation by accident.
- Patient-facing copy rules: Chilean Spanish, usted, short sentences, never demand typing.

A skill's `description` must name concrete trigger words. A skill that never fires is worse than no
skill, because it looks like coverage.

## What does not go here

Anything that must happen deterministically belongs in a hook in `settings.json`, not in a skill or a
rule. A rule can be forgotten; a hook runs regardless.

Project rules that apply to every session belong in the root `CLAUDE.md`, which is loaded eagerly.
Keep it short for the same reason: every rule added makes every other rule slightly less likely to be
followed.
