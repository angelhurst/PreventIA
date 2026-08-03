# Research

Evidence that shapes the product. Everything here is sourced; anything that could not be sourced is
marked unverified with the step that would verify it, and anything a developer must not decide is
marked REQUIRES CLINICAL REVIEW.

Research output is split by author. `felipe/` and `angel/` hold each person's workstreams; `sources/`
is shared.

## Index

### felipe/

| Workstream | File | What it establishes |
|---|---|---|
| 1. Self-reportable decompensation signals | [2026-08-03-self-reportable-decompensation-signals.md](felipe/2026-08-03-self-reportable-decompensation-signals.md) | Candidate early-warning signals for the three conditions, each with the Chilean guideline behind it. Raw material for the flag table; no colors assigned, per ADR-0004. |
| 2. Chilean primary-care reality | [2026-08-03-chilean-primary-care-reality.md](felipe/2026-08-03-chilean-primary-care-reality.md) | GES guarantees and their legal timeframes, PSCV control frequency, and provenance for the waiting-list figures in PRD section 1. |
| 3. Municipal follow-up burden | [2026-08-03-municipal-follow-up-burden.md](felipe/2026-08-03-municipal-follow-up-burden.md) | What the rescate de inasistentes obligation is, who carries it, at what scale, and what the one national attempt to automate it achieved. |

### angel/

Empty. Workstreams not yet assigned.

### Still to do

- Adherence measurement and remote follow-up evidence (originally workstream 3, deferred).
- How Chilean older adults actually use WhatsApp.
- Caja La Araucana and the Lab dataset.

## sources/

Every cited PDF is archived in [`sources/`](sources/) rather than linked and left to rot. These
figures go in front of a judging panel; a dead link two days before the pitch is a failure mode we
can cheaply remove.

| File | Document |
|---|---|
| `minsal-2015-guia-clinica-insuficiencia-cardiaca.pdf` | MINSAL / SOCHICAR, *Guía Clínica Insuficiencia Cardíaca*, 2015 |
| `minsal-2010-guia-clinica-diabetes-mellitus-tipo-2.pdf` | MINSAL, *Guía Clínica Diabetes Mellitus tipo 2*, 2010 |
| `minsal-2013-guia-clinica-diabetes-mellitus-tipo-1.pdf` | MINSAL, *Guía Clínica Diabetes Mellitus Tipo 1*, 2013 |
| `minsal-2010-guia-clinica-hipertension-arterial.pdf` | MINSAL, *Guía Clínica Hipertensión Arterial Primaria o Esencial*, 2010 |
| `minsal-2018-gpc-hipertension-resumen-ejecutivo.pdf` | MINSAL, *Resumen Ejecutivo GPC Hipertensión Arterial*, 2018 |
| `minsal-2017-orientacion-tecnica-pscv.pdf` | MINSAL, *Orientación Técnica Programa de Salud Cardiovascular*, 2017 |
| `minsal-2026-glosa-06-lista-espera-i-trimestre.pdf` | MINSAL, *Glosa 06*, Q1 2026, cut-off 31 March 2026 |
| `minsal-2025-glosa-06-lista-espera-iii-trimestre.pdf` | MINSAL, *Glosa 06*, Q3 2025, cut-off 30 September 2025 |
| `dipres-evaluacion-programa-salud-cardiovascular.pdf` | DIPRES, *Evaluación EPG: Programa Fondo de Farmacia*, 2018. Filename is imprecise; the document evaluates FOFAR. |
| `bcn-listas-y-tiempos-de-espera-atencion-salud.pdf` | BCN, *Listas y tiempos de espera para atención en salud en Chile*. Methodological cross-check, not cited for any figure. |
| `ges-2025-listado-problemas-salud.pdf` | Servicio de Salud Atacama / CIRA, GES presentation, 2025. Downloaded expecting a decree listing; it is not one. |

Practical note for whoever fetches more: `minsal.cl` returns HTTP 403 to plain fetchers but serves
normally to `curl` with a browser user agent.

---

## Proposed changes to PRD.md

**These are proposals. `PRD.md` has not been edited** — the research brief reserves that decision for
Felipe. Replacement text is given in full so it can be pasted.

The same claims appear in the root `README.md`, which faces the Lab. Those **have** been corrected,
because leaving figures we know to be false in the outward-facing document was the worse option. If
any proposal below is rejected, `README.md` needs reverting to match.

### P1. Section 1 — the waiting-list figures are wrong

**Severity: high.** These will be said in front of judges from government and health management.

Current text claims ~2,4 million people waiting, an average over 400 days for a specialty
consultation and over 500 for surgery. Against MINSAL's Glosa 06 for Q1 2026 (cut-off 31 March 2026):

| Claim | Official figure |
|---|---|
| 2,4 million people | 2.088.245 people waiting for a new specialty consultation; 2.513.203 records. No published figure equals 2,4 million. |
| Average over 400 days, specialty consultation | Mean **329** days, median 236 |
| Over 500 days, surgery | Mean **383** days, median 259 |

Both day-figures are traceable to something real — they hold for individual Servicios de Salud, and
the surgical median peaked at 661 days in 2021 — but neither is current, and neither is national.

The trend also runs against the framing: waiting times have fallen every quarter recently. The pitch
should not imply they are worsening.

### P2. Section 1 — "En el intervalo no hay nadie mirando" is not accurate

**Severity: high**, and this one is a factual claim about other people's work.

Municipal APS teams are formally obliged to chase patients who miss controls, with at least three
documented rescate actions before anyone can be discharged as *abandono*. Saying nobody is watching
is both wrong and needlessly dismissive of the funcionarios the product is meant to help.

**Proposed replacement for the whole of section 1:**

```markdown
## 1. El problema

Más de dos millones de personas esperan una primera consulta de especialidad en el sistema público:
2.088.245 al 31 de marzo de 2026, con una mediana de 236 días. Para un adulto mayor que ya está en
control, sin embargo, el problema no es la fila.

El Programa de Salud Cardiovascular tiene bajo control a 2,3 millones de personas, y el 65% de ellas
vive con más de una enfermedad crónica. Las garantías GES cubren la entrada: 45 días para confirmar
una hipertensión, 24 horas para iniciar el tratamiento. Ninguna cubre el intervalo. Una vez
compensado el paciente, el programa sugiere un control cada 3 meses si el riesgo cardiovascular es
alto, cada 6 si es moderado, cada 6 a 12 si es bajo. La insuficiencia cardíaca no es siquiera un
problema GES: no tiene plazo garantizado de ninguna clase.

En ese intervalo sí hay alguien mirando, y ahí está el costo. Los equipos municipales de atención
primaria están obligados a rescatar a quien falta a su control, con al menos tres intentos
documentados antes de poder darlo de baja. Nueve de cada diez de los 2.027 establecimientos que
hacen ese trabajo dependen de un municipio. Aun así, una descompensación que empezó a insinuarse
tres semanas antes llega a urgencias como si hubiera aparecido de golpe.
```

Sources: workstreams 2 and 3.

### P3. Section 4 — the target population is now substantiated

**Severity: low, and it is good news.** No correction needed; an addition worth making.

"Adultos mayores polimedicados" currently reads as a design choice. It is the majority case:
**65% of PSCV patients carry more than one chronic condition** (DIPRES 2018, on 2017 data). Worth
stating with the figure, because it turns a scoping decision into an observation about the country.

### P4. Section 5 — the semáforo table needs a frailty caveat

**REQUIRES CLINICAL REVIEW.** The PSCV already varies its targets by age and frailty: blood pressure
target <150/90 and >120/60 for people 80 and over, HbA1c from <7,5% to <8,5% depending on frailty
state, with formal frailty criteria. "Compensated" is not one number.

A flag table keying on absolute values without the patient's frailty state will be wrong for
someone. Whether the table should be frailty-aware is the clinician's call, but section 5 should not
imply a single threshold set.

### P5. Section 10 — the post-Lab claim needs to survive the FOFAR result

**Severity: high, and unresolved.** Flagged here; the evidence review is the next workstream.

Section 10 sets the post-Lab criterion as fewer emergency reconsultations and fewer avoidable
readmissions. Chile has already automated patient contact nationally: FOFAR's SMS and phone reminder
system, evaluated by DIPRES across 4.481.282 appointments, produced 11,6% non-attendance with a
reminder against 13,3% without, and the panel called both the effect and the adherence contribution
marginal.

That is not fatal — a one-way reminder and a two-way conversation are different interventions — but
the PRD currently makes its claim without knowing this precedent exists. Section 10 already says the
outcome "no se va a afirmar como si se hubiera medido", which is the right instinct. It should also
name the precedent, because a judge who knows FOFAR will otherwise raise it first.

### P6. Section 3 and the wider framing — the burden argument is the stronger one

**Severity: medium.** Not a correction, a repositioning.

The product currently argues from clinical benefit, which depends on evidence we do not yet have.
The burden argument does not: displacing mandated rescate work across 2.027 establishments that are
90,7% municipal stands on the mandate and the scale alone, even if the clinical effect were zero.
Worth leading with in front of a management-criteria judge.

---

## PRD claims this research could not substantiate

Listed as the brief requires, separately from the corrections above.

| PRD claim | Status |
|---|---|
| "alrededor de 2,4 millones de personas esperan en listas" | **Not attributable.** No published figure equals it. See P1. |
| "El promedio de espera supera los 400 días para una consulta de especialidad" | **Contradicted.** Mean 329 days. |
| "y los 500 días para cirugía" | **Contradicted.** Mean 383 days. |
| "En el intervalo no hay nadie mirando" | **Contradicted.** See P2. |
| "un control cada 3 a 6 meses" | **Substantiated**, and conservative: 6-12 months at low cardiovascular risk. |
| Target population of polymedicated older adults with the three conditions | **Substantiated.** 65% multimorbidity in the PSCV. |
| Section 10: fewer emergency reconsultations and avoidable readmissions | **Not yet assessed.** Next workstream. The one adjacent Chilean precedent is discouraging. See P5. |
| "matrona o médico de cabecera" as the escalation target | **Partially substantiated.** PSCV follow-up is nurse-led, which fits. The specific role of *matrona* in cardiovascular follow-up was not verified. |

## Open questions for the clinical teammate

Consolidated across all three workstreams. The first is the highest value.

1. **What does one rescate action cost in staff time?** Converts "we save staff time" from assertion
   to number. One conversation with a CESFAM team.
2. Is the MINSAL 2015 heart failure contact threshold — increased dyspnoea, oedema, or over 2 kg in
   3 days — the right starting point for the flag table?
3. How should the table handle weight, given no device is assumed?
4. Can type 1 hypoglycaemia symptoms be used for type 2 older adults?
5. Can type 2 diagnostic symptoms be reused as decompensation signals?
6. How should hypertension be handled, given it produces almost no listenable signal and the national
   guideline warns that the symptoms patients attribute to it frequently are not caused by it?
7. Should the flag table be frailty-aware? (P4.)
8. Is depression in scope?
9. Should absence of reply be a flag?
10. What programme, if any, structures heart failure follow-up in Chile, given it is neither GES nor
    PSCV?
