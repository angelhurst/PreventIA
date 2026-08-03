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
| 4. Adherence and remote follow-up evidence | [2026-08-03-adherence-and-remote-followup-evidence.md](felipe/2026-08-03-adherence-and-remote-followup-evidence.md) | What instrument the PSCV already mandates and what it costs to use, the ceiling on any self-report measure, and the outcome evidence PRD section 10 depends on, including the null results. |
| 5. WhatsApp use among Chilean older adults | [2026-08-03-whatsapp-use-chilean-older-adults.md](felipe/2026-08-03-whatsapp-use-chilean-older-adults.md) | What this population has, what it does with it, and how far apart voice and text are by age. Sets out what each modality would demand without resolving the scope question. |
| 6. Caja La Araucana and the Lab dataset | [2026-08-03-caja-la-araucana-and-the-lab-dataset.md](felipe/2026-08-03-caja-la-araucana-and-the-lab-dataset.md) | What the host institution is and is not, what it already runs for chronic pensioners, and a list of SQLite schema assumptions at risk against data nobody has seen. |

All six workstreams in the brief (`PROMPTforANGEL.md`) are complete.

### angel/

Empty. Workstreams not yet assigned.

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
| `subtel-2024-xi-encuesta-acceso-usos-internet.pdf` | SUBTEL / Cadem, *XI Encuesta sobre acceso, usos y usuarios de Internet en Chile — Informe Final*, fieldwork 2024, published February 2025 |
| `uc-caja-los-andes-2022-vi-encuesta-calidad-vida-vejez.pdf` | Centro UC Estudios de Vejez y Envejecimiento / Caja Los Andes, *Chile y sus mayores. Sexta Encuesta Nacional de Calidad de Vida en la Vejez 2022*, August 2023 |
| `suseso-2026-afiliados-ccaf.xlsx` | SUSESO, affiliate statistics by CCAF, 2026. Companies, workers, pensioners and totals by month |
| `laaraucana-beneficios-via-ssms.pdf` | Caja La Araucana benefits presentation, undated, hosted by the Servicio de Salud Metropolitano Sur. Used because `laaraucana.cl` blocks fetchers |
| `lab-2026-wiki-datos-salud.txt` | Bendita IA / Caja La Araucana, *Wiki de Datos — Salud*, Claude Impact Lab · Longevidad. Text snapshot of `longevidad.benditaia.cl/es/wiki-legal` as retrieved 3 August 2026. **The authority for the Lab's data and AI rules**, archived because it is a live page with no version marker |

Sources cited but not archived, because they are web pages rather than documents: the
Superintendencia de Salud GES pages, the SUSESO pages on what a CCAF does and on the fiscalización of
La Araucana, the SciELO articles in workstream 4, Meta's WhatsApp Cloud API documentation, the
MINEDUC PIAAC page, and the Lab's own site at `longevidad.benditaia.cl`.

Practical notes for whoever fetches more:

- `minsal.cl` and `scielo.cl` both return HTTP 403 to plain fetchers and serve normally to `curl`
  with a browser user agent.
- `laaraucana.cl` returns a Radware CAPTCHA challenge to everything. The government-hosted copy above
  was the way around it.
- `bcn.cl/leychile` serves a JavaScript shell to fetchers. The official text comes back as XML from
  `https://www.bcn.cl/leychile/consulta/obtxml?opt=7&idNorma=<id>`.
- `journals.sagepub.com` returned HTTP 403 throughout, which is why one 2026 systematic review is
  listed in workstream 4 as located but not read.

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

**Resolved by workstream 6: all four figures are the Lab's, verbatim, and the Lab attributes them to
MINSAL.** Workstream 2 offered three hypotheses and could not settle it. The Lab's *Wiki de Datos —
Salud* lists them as "las cifras sobre las que van a construir los equipos":

> ~2,4 millones de personas — En listas de espera del sistema público
> 330.000–350.000 — Esperando una cirugía
> 400+ días promedio — En consulta de especialidad
> 500+ días promedio — En cirugía — con casos de 3 y 4 años

attributed on the same panel to "Ministerio de Salud" and "DEIS — Estadísticas de salud". Every one
is out of date against Glosa 06 Q1 2026, including a fourth we had not checked: the wiki's
330.000–350.000 waiting for surgery against **398.496** people.

**So PRD section 1 is not sloppy — it copied the brief faithfully, and the brief is stale.** That
changes the register of the correction entirely. Because the wiki names MINSAL as its own source, and
Glosa 06 *is* MINSAL's legally mandated quarterly report to Congress, the pitch is not contradicting
the host. It is citing the host's own source at its most recent cut.

**The line to use:** "las cifras del Lab vienen del Minsal; estas son las del último informe
trimestral del Minsal al Congreso, al 31 de marzo de 2026." Then give the numbers.

The root `README.md` already reads that way, so nothing needs reverting there.

**And note where the waiting-list framing belongs.** The wiki maps waiting lists to the
**Descompresión** challenge line; ours, Continuidad, is mapped to "egresos hospitalarios, datos
agregados de crónicos". PRD section 1 currently opens on the other line's problem statement. That is
a second, independent argument for the P2 pivot below.

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

### P5. Section 10 — the post-Lab claim needs to survive the evidence

**Severity: high. Now resolved by workstream 4, with replacement text.**

Section 10 sets the post-Lab criterion as fewer emergency reconsultations and fewer avoidable
readmissions. Three things are now known about that claim.

**Chile has already automated patient contact nationally and the result was marginal.** FOFAR's SMS
and phone reminders, evaluated by DIPRES across 4.481.282 appointments: 11,6% non-attendance with a
reminder against 13,3% without, panel calling both the effect and the adherence contribution
marginal, on a comparison confounded by contact-data quality.

**The "but a conversation is not a reminder" defence is weaker than it looked.** The StAR trial
randomised 1.372 hypertensive adults three ways — informational SMS, interactive SMS, usual care —
and concluded verbatim: "There was no evidence that an interactive intervention increased this
effect." That is a direct test of two-way against one-way and it found nothing. It does not settle
the question for a conversational agent, since StAR's interactive arm was scripted SMS, but it stops
us asserting the distinction as established.

**And the evidence base for conversational agents specifically is empty rather than negative.** No
study found reports emergency reconsultation or avoidable readmission for a conversational agent in
older adults. The nearest positive evidence is for nurse-led structured telephone support and device
telemonitoring (Cochrane 2015: RR 0,87 and 0,85 for structured telephone support; 0,80 and 0,71 for
telemonitoring, moderate quality), and the two largest individual trials of remote monitoring —
Tele-HF and BEAT-HF — are flatly null.

**What the pattern actually tracks is worth the PRD saying**, because it is an argument for the thing
we built. Across those six studies, the results do not sort by modality. They sort by whether the
contact terminated in a clinical service that could act. That is exactly what ADR-0006's triage queue
makes PreventIA, and the clinical non-negotiable that every escalation ends at a human turns out to
be load-bearing rather than merely ethical. (This reading is mine across six studies, not a published
analysis, and workstream 4 marks it as such.)

**Proposed replacement for the final paragraph of section 10:**

```markdown
Para el producto más allá del Lab, el criterio es otro: menos reconsultas de urgencia y menos
reingresos hospitalarios evitables en población adulta mayor. Eso no se mide en dos días y no se va a
afirmar como si se hubiera medido.

Hay que decir además lo que ya se sabe. Chile automatizó el contacto con pacientes a escala nacional
con el sistema de recordatorios de FOFAR, y la evaluación del propio Estado, sobre 4.481.282 horas,
encontró un efecto marginal. Y el ensayo que comparó de frente mensajes interactivos contra mensajes
de una sola vía en 1.372 hipertensos no encontró diferencia entre ambos. La evidencia que sí es
positiva, en insuficiencia cardíaca, corresponde a seguimiento telefónico estructurado conducido por
enfermería y a telemonitoreo dentro de un servicio clínico.

Eso es precisamente lo que separa a un recordatorio de lo que hace PreventIA: el caso termina en una
persona del equipo de salud que puede actuar sobre él. No prometemos el resultado clínico. Sostenemos
que la arquitectura es la que la evidencia disponible respalda, y que la carga de trabajo que
desplaza el sistema no depende de ese resultado.
```

The last sentence hands the argument to P6, which is the one that does not depend on evidence we do
not have.

### P6. Section 3 and the wider framing — the burden argument is the stronger one

**Severity: medium.** Not a correction, a repositioning.

The product currently argues from clinical benefit, which depends on evidence we do not yet have.
The burden argument does not: displacing mandated rescate work across 2.027 establishments that are
90,7% municipal stands on the mandate and the scale alone, even if the clinical effect were zero.
Worth leading with in front of a management-criteria judge.

Workstream 4 strengthens this: the burden argument is now the **only** one of the two that the
evidence supports without qualification.

### P7. Sections 4 and 9 — name the first cohort, because the modality gap is measurable

**Severity: medium. New, from workstream 5.** Not a correction; the PRD is silent where it should not
be.

Among Chileans aged 60 and over, chat or WhatsApp use in the last month runs at **78% at 60-69, 51%
at 70-79 and 22% at 80 and over**, while using the phone to talk to somebody runs at 96%, 90% and 73%.
The PSCV's own frailty criteria start at 75. So a text-first prototype reaches a shrinking share of
the population as clinical need rises, and PRD section 4 currently describes the target population
without acknowledging it.

Two additions, and neither requires changing scope:

**Section 4** should say which older adults the prototype is for. "Adultos mayores polimedicados" is
substantiated (P3) but silent on channel. A first cohort defined as older adults who already use
WhatsApp is honest, is a majority of the 60-79 population, and turns a limitation into a scoping
decision.

**Section 9** should keep the voice channel out — that decision stands — and say why in one line that
survives being challenged: the modality gap is real, it is largest among the oldest patients, and
voice is the next cohort rather than a nice-to-have. Workstream 5 sets out what voice would actually
cost: a speech-to-text component that is not in ADR-0001 and lands directly on the clinical boundary,
and, for calls, a separate Meta API with limited availability.

**And there is a scope contradiction to settle before the pitch, not by this document.** The project
description submitted to the Lab says "WhatsApp o llamada de voz". PRD section 9 and ROADMAP Phase 3
say WhatsApp only. Anyone reading both will see it.

**One thing that is cheap and should be in scope regardless:** accept an inbound voice note
gracefully. Patients who do not type send audio. A prototype that silently ignores an audio message
looks, to an 80-year-old, exactly like not being listened to — which is the one thing this product
cannot look like. A fixed reply asking them to write is enough.

### P8. Section 7 — two copy rules the evidence supports

**Severity: low. New, from workstream 5.** `CLAUDE.md` section 8 and PRD section 7 already require
Chilean Spanish, *usted*, short sentences and plain register. Nothing found contradicts any of it.
Two additions:

- **Never require the patient to type more than a few words.** Composition is the limiting skill in
  this population, not comprehension. Questions answerable with "sí", "no" or one word should be the
  default shape, with free text always accepted and never demanded.
- **Every failure state must be recoverable by the system, never by the patient.** In 2022, 52,9% of
  Chileans over 60 rated their own ability to use the internet for information or a trámite at 3 or
  below on a scale of 7. A confused patient will not explore the interface to recover; the next
  message has to do the repair.

### P9. Section 8 — the adapter should calibrate the cohort, not populate it

**Severity: medium, and it needs a new ADR if adopted.** New, from workstream 6.

PRD section 8 and ADR-0007 describe an adapter that reads the Lab's anonymized dataset "en el mismo
esquema". Against genuinely **aggregated** data — the Lab's own published rule says "datos
anonimizados/agregados" — that is not possible, because aggregated data has no person-level row to
put in a `patients` table.

What is possible, and is both smaller and more defensible, is an adapter that reads the aggregates and
**calibrates the synthetic cohort**: age distribution, sex ratio, comuna distribution, condition
prevalence, multimorbidity rate. The pitch line follows directly — the cohort is synthetic, its shape
comes from the institution's own anonymized aggregates, and we can say exactly which is which.

Workstream 6 section 6 lists the schema assumptions at risk in full. The ones to know: a per-patient
medication list, a diagnosis per patient, a per-day contact history, and any contactable phone number
are all things a caja de compensación has no statutory reason to hold, and the last is impossible by
the Lab's own data rule.

**ADR-0007 is Accepted and immutable.** If this is adopted it needs a new, next-numbered ADR that
supersedes it, per `CLAUDE.md` section 9 — and per the global rule, Felipe writes the decision, not
the research.

**Blocking question before Phase 0 closes:** the Lab site is ambiguous about whether the Caja dataset
arrives during the two days or post-Lab to winning teams. One message to the organisers settles it,
and if it is the second, ADR-0007's premise is wrong and Phase 3 has to be described differently.

### P10. Anywhere the PRD discusses deployment — contact data is the unnamed risk

**Severity: medium. New, from workstream 4, and it appears nowhere in the PRD.**

The same failure mode has now defeated three separate Chilean efforts to reach this population.
FOFAR's unreminded group was unreminded because its contact data was wrong or missing. A rescate
action escalates to a home visit precisely when the phone fails. And the largest Chilean study of
antihypertensive adherence lost **443 of 956 sampled patients**, of which **245 were "error en la
información de contacto"** — a quarter of a sample drawn from a live PSCV register, unreachable
because the register was wrong.

PreventIA assumes a working WhatsApp number. The Chilean evidence says the health system frequently
does not have one, and that the patients whose numbers are wrong are systematically the ones most
likely to decompensate unobserved. This should be named in the PRD as a deployment precondition, and
it is a much better question to have answered than to be asked.

### P11. Not yet in the PRD, but blocking if the team plans to use Morisky

**Severity: high if it comes up, and it is a legal question this document does not answer.**

The PSCV mandates the Test de Morisky Green Levine-4 for adherence (workstream 2). The Morisky scales
are **copyrighted commercial instruments**: the rights holder publishes prices of USD 4 and USD 7 per
administration and states the scales may not be "modified, sold, translated into another language or
adapted for another medium without a license". A conversational agent asking the four questions in
Chilean Spanish is an adaptation and a translation at once, and a per-administration fee is
structurally hostile to a daily check-in. Enforcement is not theoretical: a published corrigendum and
editorial warning exists over an adherence app's use of MMAS-8.

The PRD does not currently name an adherence instrument, so nothing needs correcting today. It needs
deciding before anything is written into `clinical/`. **I am not a lawyer and this is not legal
advice.** The three options are to license, to not use it, or to align to it conceptually without
reproducing its items.

### P12. The pitch — name the licencias médicas chain as the scale-up path

**Severity: medium, decided.** New, from the Lab's data wiki via workstream 6.

The Lab's own return-on-investment story runs through medical leave, verbatim: "COMPIN valida las
licencias médicas → las Cajas de Compensación (como La Araucana) pagan el subsidio → SUSESO
supervigila. Menos listas de espera → menos licencias → menos gasto → más productividad país", with
La Araucana paying "del orden de mil millones CLP/año" into it.

Medical leave is a **worker** benefit. PreventIA's population is pensioners. So the host institution's
stated economics do not pass through our target population at all — which is exactly the structural
finding workstream 6 reached from the other direction, before this page was read.

**Felipe's decision, 3 August 2026: keep older adults, name the chain as the scale-up path.** No
scope change. The pitch says that the same architecture applied to working-age chronic patients — the
majority of the PSCV's 2,3 million, since the programme covers people from 15 up — lands directly on
the COMPIN–CCAF–SUSESO chain, and that this is what the Phase 5 pilot would measure. It costs
nothing, it shows we read the brief, and it answers the management-criteria judge before the question
arrives.

This sits alongside P6, not instead of it. The municipal burden argument is the one that stands
without any evidence we lack; the licencias chain is the one the host recognises as money.

### P13. Not a PRD change — the ADR-0010 sync. **Done.**

**Severity was high and mechanical.** Recorded here for the trail rather than as a pending item.

ADR-0008's decision was mirrored in four files outside `docs/adr/`. All four were brought into line
on 3 August 2026, on Felipe's instruction:

| File | What changed |
|---|---|
| `CLAUDE.md` section 4 | Claude is the Lab runtime; Ollama named as the documented deployment path; the `OLLAMA_MODEL` open item demoted from a Phase 1 blocker to Phase 4 or later; the suite-per-provider rule made explicit about which provider must pass before demo day |
| `ROADMAP.md` Phase 1 | Provider line updated, the `OLLAMA_MODEL` blocker removed, shaped-by list corrected to ADR-0010 |
| `README.md` stack table | "Modelo: Local vía Ollama por defecto" was the most dangerous instance — it is the Lab-facing document, and it advertised the exact configuration the Lab's rule penalises |
| `docs/research/PROMPTforANGEL.md` | Header no longer makes Phase 1 wait on `OLLAMA_MODEL` |

One sentence in `CLAUDE.md` was deliberately kept: **do not write code that assumes Anthropic is
answering.** The provider seam is what makes both runtimes possible and it is what makes the
deployment story true, so it survives the change of default intact.

**Angel needs telling**, because ADR-0008 put his Mac Studio on the critical path and ADR-0010 takes
it off.

---

## PRD claims this research could not substantiate

Listed as the brief requires, separately from the corrections above.

| PRD claim | Status |
|---|---|
| "alrededor de 2,4 millones de personas esperan en listas" | **Traced to the Lab's own wiki, verbatim, and stale.** No published official figure equals it. See P1. |
| "El promedio de espera supera los 400 días para una consulta de especialidad" | **Contradicted.** Mean 329 days. Also verbatim from the Lab wiki. |
| "y los 500 días para cirugía" | **Contradicted.** Mean 383 days. Also verbatim from the Lab wiki. |
| "En el intervalo no hay nadie mirando" | **Contradicted.** See P2. |
| "un control cada 3 a 6 meses" | **Substantiated**, and conservative: 6-12 months at low cardiovascular risk. |
| Target population of polymedicated older adults with the three conditions | **Substantiated.** 65% multimorbidity in the PSCV; 53% hypertension, 34% diabetes and only 16% taking no medication among Chileans 60+. |
| Section 10: fewer emergency reconsultations and avoidable readmissions | **Not substantiated, and now assessed.** No study reports either outcome for a conversational agent in older adults. The positive evidence is for nurse-led telephone support and telemonitoring; the two largest individual trials are null; the one direct test of interactive against one-way messaging found no difference. See P5. |
| Section 2: that a two-way conversation is a different intervention from a one-way reminder | **Unsupported as an outcome claim.** True as a description; StAR tested the distinction directly and found no added effect. Still not refuted for a conversational agent, which nobody has tested at scale. |
| Section 8: an adapter reading the Lab dataset "en el mismo esquema" | **Probably not possible as written.** Aggregated data has no person-level row. See P9. |
| Section 8: that the anonymized dataset "hace creíble la proyección" | **Plausible, and now narrower than the PRD implies.** The dataset does arrive, but for our line it is hospital discharges and aggregated chronic-patient data, which supports a population-level projection and not a per-patient one. See P9. |
| Section 9: WhatsApp as the channel, voice out of scope | **Substantiated as a decision, silent on its cost.** The modality gap is 78% / 51% / 22% by age band. See P7. Also contradicts the project description submitted to the Lab. |
| "matrona o médico de cabecera" as the escalation target | **Partially substantiated.** PSCV follow-up is nurse-led, which fits. The specific role of *matrona* in cardiovascular follow-up was not verified. |
| Implicit throughout: that patients are reachable | **Contradicted by the deployment record.** Wrong contact data has defeated three separate Chilean efforts to reach this population. See P10. |

## What the Lab's own wiki settled

The organisers are not reachable — Felipe's assessment on 3 August 2026 is that they have enough
disorganisation on their hands that a clarification request will not come back in time. The three
questions this section originally posed have been answered instead by the Lab's *Wiki de Datos —
Salud*, archived as `sources/lab-2026-wiki-datos-salud.txt`.

| Question | Answer |
|---|---|
| When does the Caja dataset arrive, and to whom? | **Closed.** Curated datasets, anonimizados y agregados, "se publican al abrir la convocatoria". My earlier post-Lab reading was wrong |
| What does our challenge line get? | **Egresos hospitalarios, datos agregados de crónicos.** Waiting lists belong to Descompresión |
| Where do the 2,4 million and 400/500-day figures come from? | **The wiki itself**, attributed to Minsal and DEIS. All four are stale against Glosa 06 Q1 2026. See P1 |

**And one thing it settled that nobody had thought to ask.** The wiki states "Claude como motor
principal — Sin llamadas reales a la API de Claude → descalificado", which contradicted ADR-0008's
stated basis for making Ollama the default runtime. Resolved by **ADR-0010**: Claude is the runtime
for the build, demo and pitch; Ollama becomes the documented deployment path. One environment
variable, no module code, disqualification risk removed under either reading of the rule.

Two of the Lab's rules are conditions rather than guidance and are worth knowing: **every team must
include at least one health professional**, and every clinical claim must carry a verifiable source
or say "no sé". The second is why workstream 1 attaches a MINSAL citation to every candidate signal
instead of proposing thresholds.

Still open, and now answerable only on the day or by decision:

1. **What is "Acompañamiento paciente crónico"?** La Araucana runs it — pensioner-only, plan
   ilimitado, by telemedicine. The wiki does not list it among the data sources, so it probably is
   not the dataset, but a judge from the host institution will know it exists and the pitch is
   stronger naming it.
2. Does the Lab mean "agregado" strictly or loosely? Answerable by looking at the data on day one.

## Questions for the clinical teammate

Consolidated across all six workstreams. The first is the highest value.

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
8. **Is depression in scope?** Sharpened by workstream 4: emotional distress and depressive symptoms
   are the strongest predictor of non-adherence in the only large Chilean study of it, at OR 1,93.
   That puts depression inside the PRD's stated purpose on adherence grounds, not only clinical ones.
9. Should absence of reply be a flag?
10. What programme, if any, structures heart failure follow-up in Chile, given it is neither GES nor
    PSCV?
11. May Chilean MMAS-8 evidence stand in for the MGL-4 the PSCV actually mandates? (Workstream 4.)
12. May transcribed audio feed the extraction layer, and at what confidence, if voice notes are ever
    accepted? (Workstream 5.)
13. **How does a CESFAM know a patient's current phone number, and how often is it wrong?** (P10.)
    Same conversation as question 1, and nearly as valuable.

## Note on the impact line

Recorded for awareness, not as a proposal. The Lab publishes three challenge lines. `CLAUDE.md` and
`PRD.md` place PreventIA in **Continuidad y medicina de precisión**, described as "seguimiento
crónico, medicina personalizada, autonomía en envejecimiento", which fits. The **Descompresión** line
is described as "triage clínico por riesgo, match paciente-capacidad, acompañamiento longitudinal",
and the first and third of those are literally what the semáforo and the triage queue do.

The line is already chosen and two days out is not the moment to move. The reason to know this is
that the pitch can honestly say the product serves both, and a judge on the Descompresión panel is
not going to hear a stranger.
