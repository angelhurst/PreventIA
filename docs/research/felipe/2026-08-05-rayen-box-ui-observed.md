# What Rayen's clinical screen actually looks like, read from the manual

Consulted 5 August 2026. Method: retrieved and read the `Manual de BOX RAYEN`, version **15.0.0.2**,
updated **November 2021**, 128 pages, hosted by the Servicio de Salud Osorno at
[saluddigital.ssosorno.cl](https://saluddigital.ssosorno.cl/Portals/0/adam/Content/NL82SHDUQUu9h4a08EjoPw/Link/Software%20RAYEN%20-%20Manual%20Box.pdf).
The document is image-based, so it was read page by page rather than text-extracted. Everything below
is observed from the manual's own screenshots and prose; quoted strings are verbatim.

This closes **open item 1** of `2026-08-05-clinical-dashboard-ui-and-stacks-chile.md` on navigation
and application type, and leaves the browser and resolution halves of it open, because the manual
states neither.

## Correction to the earlier retrieval note

The earlier document recorded `saludtarapaca.gob.cl` as refusing a plain fetcher and suggested a
browser user agent would settle it in ten minutes. That is wrong. With a Chrome user agent the host
times out on ports 80 and 443 across three hostnames, while `rayensalud.com` and
`framework.digital.gob.cl` answer 200 from the same shell. **The host is down, not filtering.** The
manual was obtained from a different Servicio de Salud, in a revision one version newer than the
15.0.0.1 of March 2020 that the earlier note was chasing. A July 2023 revision is indexed at Tarapacá
for whenever that host returns.

## 1. Application type and entry

**"RAYEN es una aplicación web que contiene diversos subsistemas creados para la gestión clínica y
administrativa"** — stated verbatim in the introduction and repeated in chapter 1. Server-rendered
versus single-page is still not stated, but the vendor's own word for it is `aplicación web`.

Entry is `http://www.rayenaps.cl/`, a **launcher page offering four ámbitos**, each a card with its
own module list and an `Iniciar` button:

| Ámbito | Modules listed on the launcher |
|---|---|
| Administrativo | Admisión, Agenda, Citas, Herramientas, Reportes para la gestión, REM |
| Clínico | Ficha clínica, Ficha odontológica, Ficha familiar, Derivación, Registro de atención |
| Servicios Transversales | Farmacia, Entrega de alimentos, Vacunatorio, Toma de muestra, Derivación administrativa |
| Urgencia | Admisión, Categorización, Registro clínico, Registro de tratamientos |

This is the "ecosystem of applications" doctrine from SIDRA made concrete in one screen, and it is
the clearest evidence yet for the earlier document's point that our dashboard will be the *n*th tab.

## 2. Authentication, and what it means for ClaveÚnica

Three fields: **Ubicación** (an establishment slug, the manual's example is `cesfamrayensalud`),
**Usuario** ("correspondiente al RUN del funcionario prestador"), and **Clave** personal.

**ClaveÚnica does not appear anywhere in the login flow.** The earlier document was right that
ClaveÚnica is permitted rather than required for staff; this is the confirmation that the incumbent
primary-care system does not use it. If we say ClaveÚnica is the credible staff-login answer, we
should say it as what a new system *may* adopt, not as what clinicians already do.

Note also that the login screenshot carries **`Versión: 15.1.0.13`** while the manual itself is
15.0.0.2. The deployed build runs ahead of the documentation, which is worth knowing before anyone
cites a version number in front of a judge.

## 3. Navigation structure

**A dark blue left sidebar**, full height, with collapsible module groups and indented sub-items. The
observed group order is Admisión, Agenda, Citas, Entrega de alimentos, Box, with Box expanded to
Pacientes citados, Agregar documentos, Preparación de pacientes, Administrador de derivaciones,
Visualización de odontograma. The **active sub-item is highlighted in orange** against the dark blue.
A hamburger and the word `Rayen` sit at the top of the sidebar; the logged-in user's name sits at the
top right.

Below the top bar there is a **horizontal action toolbar** whose buttons act on the row currently
selected in the list: `Certificado de Atención`, `Llamar`, `Ingresar Atención`, `Mensajes`,
`Inasistente`, `Espontáneo`, `Actualizar`, `Cerrar`.

So: sidebar for navigation, toolbar for verbs, table for nouns. Not tabs, not a launcher within the
app, not per-row buttons.

## 4. Pacientes Citados, the closest existing analogue to our triage queue

A **dense table, one line per patient**, with these columns in order: `Estado`, `Nombre`,
`Tipo cupo`, `Hora cita`, `Llegada`, `Llamada`, `Razón de la cita`, `Tipo de atención`, `Adjunto`.
A green context strip above the table describes the selected patient in one sentence
("Paciente de 38 años 6 meses 6 días, pertenece al sector Desarrollo"). Clicking a name opens a small
popover with age, RUT, ficha number and sector.

**There is no auto-refresh.** The list is brought up to date by an explicit `Actualizar` button,
documented as covering "cambios de estado, incorporación de pacientes a la lista, registro de
llegada".

**The six states, and how each is set** — this is the part that matters for ADR-0014:

| State | What sets it, verbatim |
|---|---|
| `Agendado` | "No ha sido abierta la ficha del paciente" |
| `Iniciado` | "La ficha del paciente se encuentra abierta" |
| `Completado` | "Ficha de paciente cerrada" |
| `Preparada` | "Registro de llegada y preparación de paciente realizada" |
| `No se Presentó` | "usuario fue registrado como inasistente" |
| `Pendiente` | "Preparación de paciente realizada" |

Read those definitions closely. **Every one of them is defined by a system event, not by an
assertion.** A case is `Iniciado` because a ficha was opened, `Completado` because it was closed.
That is the same principle ADR-0014 adopts and makes explicit: state is a consequence of a recorded
event rather than a field somebody sets. The SIGTE failure recorded in section 6 of the earlier
document is what happens when that principle is not enforced.

## 5. Rayen already has a semáforo, and calls it that

This is the finding that changes how the pitch should be worded.

From the `ESTRATIFICACIÓN DE RIESGO` chapter, verbatim:

> "Este identificador de riesgo tiene la alerta de tipo semáforo, para destacar desde un G0 a un G3."

The chapter illustrates it with three lights, **red, yellow and green**. In the clinical header, next
to the patient's name, sits a chip reading `G2 Riesgo moderado` — an **amber fill with dark text**.
Selecting the chip opens `Información riesgo` showing the start date and the diagnoses that produce
the classification, with a `Ver todos los diagnósticos activos` action opening the full list, where
each chronic diagnosis carries its own chips: `G2`, `No Controlado`, `Confirmado`, plus its CIE-10
code.

Four things follow, and they are all useful:

1. **The word `semáforo` is Rayen's own word for a risk identifier.** PreventIA is not introducing a
   metaphor to Chilean primary care; it is using the incumbent's vocabulary. That is a sentence worth
   saying to a clinical judge, and it costs nothing.
2. **The "click the colour to see why" affordance already exists** and clinicians are trained on it.
   Our patient ficha does the same thing — the rules floor, its reason, and whether the model raised
   it — which means the interaction is familiar rather than novel.
3. **The two semáforos grade different things and do not compete.** Rayen's is *diagnosis-derived* and
   grades the patient's standing risk on four levels, G0 to G3. PreventIA's grades a *single
   check-in* on three levels, from what the person said today. One is a stable attribute of the
   patient; the other is an event. Saying this explicitly forestalls the obvious objection that Rayen
   already does this.
4. **Amber fill with dark text is what Rayen already ships.** The decision to use the Kit Digital
   traffic-light values as fills with measured ink, never as coloured text, lands on the same visual
   pattern a Chilean primary-care clinician already reads daily. That was chosen for WCAG reasons and
   it turns out to be the locally idiomatic answer too.

## 6. Alertas clínicas

A separate feature from the semáforo. A **warning-triangle icon in the clinical toolbar** opens a
dropdown listing administrative and clinical alerts, plus "las atenciones de urgencia del paciente de
los últimos 12 meses, esto con la finalidad de alertar al profesional de estos datos". There is an
`Agregar alerta administrativa` action at the foot of the list.

Two notes. The alert surface is a **dropdown a clinician opens deliberately**, not an interruption —
consistent with the alarm-fatigue evidence in section 7 of the earlier document. And Rayen already
treats "went to urgencias recently" as an alert-worthy fact, which is a reasonable precedent for
PreventIA surfacing longitudinal context rather than only today's colour.

## 7. Visual language observed

Not a design system, just what the screenshots show, and it is consistent across the manual: dark
blue chrome, **orange as the single accent** for the active nav item and for primary buttons
(`Aceptar`, `Salir`, the floating `+`), light blue headers on modals and panels, amber and blue chips
with dark text for status, dense tables with thin rules, and a floating circular action button that
fans out into lettered sub-actions on the evaluation screen.

## 8. Where our dashboard deliberately differs, and why

Worth having straight, because "why doesn't it look like Rayen" is a fair question from a judge who
knows Rayen.

| Rayen | PreventIA | Reason |
|---|---|---|
| Dense table, one line per patient | Stacked severity rows | The font-size theme in ADR-0011 has to work. A nine-column table overflows at 200% type and fails WCAG 2.2 AA reflow |
| Toolbar acts on the selected row | Action lives on the row itself | One nurse working a short ranked list, not a receptionist working a day's appointments |
| Explicit `Actualizar` button | Page load | Same posture, no polling. Worth keeping if the queue ever gets live updates |
| Colour chip plus a `G` code | Colour chip plus the colour word in text | WCAG 1.4.1 and the SENADIS criterion: colour is never the only carrier |
| Risk from diagnoses | Risk from what the person said today | Different object, stated in section 5 above |

## 9. Still not stated, after reading the manual

| Question | Status |
|---|---|
| Browser name or minimum version | **Not stated anywhere in 128 pages** |
| Screen resolution or display requirement | **Not stated** |
| Server-rendered pages versus single-page application | **Not stated.** "Aplicación web" is as specific as the vendor gets |
| Shared or personal workstations | Still inferred, not stated. The `Ubicación` login field and the per-box framing continue to imply shared and stationary |
| Whether the risk stratification algorithm is the one on the public algorithm register | Not addressed by the manual |
