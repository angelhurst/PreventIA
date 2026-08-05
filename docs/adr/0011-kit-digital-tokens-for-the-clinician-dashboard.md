# 0011 — Kit Digital design tokens for the clinician dashboard

**Status:** Accepted
**Date:** 2026-08-05
**Deciders:** Felipe Carvajal Brown

## Context

ADR-0006 fixed a web dashboard with a triage queue as the escalation surface. It said nothing about
what that dashboard is built on, and the question is not purely an engineering one: the Lab's panel
mixes clinical, government and management judges, and winning prototypes go into an AI Health
Sandbox for adoption evaluation inside a health network. "What standard does your interface follow"
is a question that gets asked in that room.

The research in `docs/research/felipe/2026-08-05-clinical-dashboard-ui-and-stacks-chile.md`
establishes what is actually available to answer with.

There is no Chilean healthcare design system. There is a government one, **Kit Digital**, run by the
Secretaría de Gobierno Digital. Its current design artefact is a Figma library, UI Kit v3.0.1. Its
code artefact, the **Framework kit**, is built on **Bootstrap 4.5** in SCSS, mobile-first, and the
Kit Digital site itself now labels the web templates as pending update and points designers at the
UI Kit instead. No npm package, CDN or git install path was found; the development-resources index
returns HTTP 404.

The part of it that is genuinely valuable is the accessibility architecture. The framework ships
`scss/themes/a11y-contrast` and `scss/themes/a11y-fonts`, and requires every component to carry a
contrast-mode counterpart and variants for enlarged font sizes. That is the pair of things a
clinician on a shared, stationary hospital workstation actually needs, and the pair a hand-rolled
dashboard skips.

The regulation behind it is **Decreto N°1 de 2015**, which requires accessibility under W3C
standards without naming a WCAG version. Sources disagree on whether that means 2.0 or 2.2.

## Decision

The clinician dashboard adopts **Kit Digital's design tokens — colour, typography and spacing — and
its contrast-theme and font-size-theme pattern**, applied over a stack chosen on its own merits.

It does **not** adopt the Kit Digital Framework kit, Bootstrap 4.5, or any Kit Digital code.

The dashboard is built to **WCAG 2.2 AA**, which satisfies both readings of Decreto 1/2015 and
removes the ambiguity rather than betting on it.

The stack itself is left to whoever builds `dashboard/`, subject only to this ADR and to ADR-0006's
constraint that a queue row is readable in seconds.

## Consequences

- The pitch can say the dashboard follows the Chilean State's accessibility criteria, and the claim
  is true and specific rather than decorative.
- No end-of-life dependency enters the project two days before the pitch. Bootstrap 4 is past
  upstream support and the government kit carrying it is marked pending update.
- Contrast and font-size handling has to be built rather than inherited, because we are taking the
  pattern and not the components. This is real work and it is accepted, because it is the part that
  matters clinically.
- The tokens have to be transcribed by hand from the Figma library and the framework's SCSS, since
  there is no package to install. Small, one-off, and it should happen once into a single file
  rather than being scattered.
- WCAG 2.2 AA is a stricter target than anyone will verify at the Lab. Held anyway, because the
  Sandbox evaluation is the audience that would.
- If the government publishes an updated Framework kit later, adopting it becomes a new decision and
  a new ADR, not a silent migration.

## Alternatives considered

**Adopt the Kit Digital Framework kit wholesale.** Strongest conformance claim available, and the
components already exist rather than needing to be written. Rejected on dependency risk: Bootstrap
4.5 is end-of-life upstream, the kit is marked pending update by its own publisher, and with no
install path we would be vendoring a zip of unmaintained SCSS into a project that has two days of
build time. The conformance claim is worth one sentence in the pitch; it is not worth owning that.

**Neither — choose the stack purely on build speed and mention Kit Digital only as something a
production version would adopt.** Cleanest engineering answer and the fastest path to a working
queue. Rejected because it gives away the one thing in this area that costs almost nothing and
answers a judge directly, and because the accessibility pattern is not decoration — it is the
difference between a dashboard a 55-year-old nurse can read on a shared monitor and one they cannot.
