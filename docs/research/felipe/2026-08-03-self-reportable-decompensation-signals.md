# Self-reportable decompensation signals

Workstream 1 of the Phase 0 research brief (`docs/research/PROMPTforANGEL.md`).

Consulted 3 August 2026. Author: Felipe Carvajal Brown. Archived copies of every PDF cited here are
in `docs/research/sources/`.

## What this document is, and what it is not

This is **raw material for the flag table**, not the flag table.

ADR-0004 puts authorship of the rule table in `clinical/rules/` with the team's healthcare
professional. This document does the part that does not require a clinician: it collects candidate
signals that a patient could plausibly say out loud, and attaches to each one the guideline or
literature that mentions it, so the clinician is choosing from sourced material rather than from a
developer's intuition.

Deliberately absent:

- **No colors.** Nothing here is assigned green, yellow or red, and nothing here proposes a
  threshold for escalation. That mapping is the clinician's decision.
- **No combination logic.** Whether two mild signals together outrank one moderate signal is a
  clinical judgement and is not attempted.
- **No claim of completeness.** This is what three Chilean guidelines and their own cited references
  contain. A clinician will know signals these documents omit.

Every candidate below is a signal **a guideline tells patients to report**. That is the narrowest
defensible basis available: it means the source already accepted that a lay person can recognise and
communicate the thing. It does not mean the signal is sensitive, specific, or usable in the
particular way PreventIA wants to use it.

## Source hierarchy actually achieved

The brief asks for Chilean official sources first, and says to declare fallbacks.

| Condition | Chilean official source found | Quality for this purpose |
|---|---|---|
| Heart failure | MINSAL / SOCHICAR, *Guía Clínica Insuficiencia Cardíaca*, 2015 | Strong. Contains an explicit patient-facing alarm list and a patient education table. |
| Type 2 diabetes | MINSAL, *Guía Clínica Diabetes Mellitus tipo 2*, 2010 | Partial. Gives classic hyperglycaemia symptoms; contains no patient-facing hypoglycaemia symptom list. |
| Hypoglycaemia symptom list | MINSAL, *Guía Clínica Diabetes Mellitus Tipo 1*, 2013 | Verbatim list found, but it is the **type 1** guideline. See the caveat in section 3. |
| Hypertension | MINSAL, *Guía Clínica Hipertensión Arterial Primaria o Esencial*, 2010; *GPC HTA* executive summary, 2018 | Weak **by content, not by access**. Neither document contains a patient-facing alarm list. This is a finding, not a gap in the search. See section 4. |

No fallback to US or general international sources was needed for the candidate lists themselves.
The one international reference cited below (Lainscak et al. 2011, Heart Failure Association of the
ESC) is cited because the MINSAL 2015 guide itself cites it as the basis of its education section,
so it is reachable through the Chilean chain rather than substituted for it.

**Currency caveat, stated up front because it will be asked at the Lab.** The MINSAL heart failure
guide states its own "plazo estimado de vigencia: 5 años desde la fecha de publicación" (p.94). It
was published in 2015, so that nominal window closed in 2020. Searches of minsal.cl,
diprece.minsal.cl and the MINSAL digital repository on 3 August 2026 did not surface a later MINSAL
heart failure guideline. **Unverified:** whether a newer Chilean heart failure GPC exists and was
simply not indexed by the searches run. What would verify it: the DIPRECE clinical guidelines index
(https://diprece.minsal.cl/le-informamos/auge/acceso-guias-clinicas/) read directly, or a direct
question to MINSAL. Until then, treat 2015 as the most recent located, not as confirmed current.

## How to read the candidate tables

Each candidate carries three properties that matter to PreventIA specifically, separate from its
clinical weight:

- **Device-free** — can the patient produce this signal with nothing but their own body and memory?
  A signal that needs a scale, a glucometer or a blood pressure cuff is not device-free, and the
  brief asks specifically about signals that are.
- **Plausibly spontaneous** — could this surface in ordinary conversation, rather than only as the
  answer to "¿tiene hinchazón en los tobillos?" This is the property the product actually claims to
  exploit, and it is the softest of the three. It is a judgement about conversation, not about
  medicine, so it is mine and is marked as such where it is doing real work.
- **Source basis** — the document that tells patients to report it.

---

## 1. Heart failure

The strongest source of the three by a wide margin, because the MINSAL guide contains a section
written for exactly this purpose: teaching a patient which of their own symptoms should make them
call someone.

### 1.1 The explicit alarm list

MINSAL / SOCHICAR 2015, section 3.4, p.73, under the heading *Signos y Síntomas de Alerta*, verbatim:

> Los síntomas de alerta en el que los pacientes con IC deben consultar a su médico o enfermera son
> los siguientes:
>
> - Aumento brusco e inexplicable de peso superior a dos kilos en tres días
> - Edema de extremidades superiores e inferiores. Suele localizarse en los tobillos
> - Anuria o poliuria
> - Disnea de pequeños esfuerzos, disnea paroxística nocturna u ortopnea
> - Tos, cansancio generalizado
> - Problemas de memoria o confusión

Broken out with the PreventIA properties:

| Candidate | Device-free | Plausibly spontaneous | Note |
|---|---|---|---|
| Sudden unexplained weight gain over 2 kg in 3 days | **No** — needs a scale | Only if the patient already weighs themselves | See 1.4. This is the single most-cited HF signal and the least compatible with a device-free design. |
| Swelling of upper and lower limbs, usually at the ankles | Yes | Yes | Patients volunteer this readily ("se me hincharon los pies"). |
| Anuria or polyuria | Yes | Partly | A patient is unlikely to use either word. What they can report is a change in how often they urinate. Recognising that phrasing is an extraction problem, not a rule-table problem. |
| Dyspnoea on minimal exertion, paroxysmal nocturnal dyspnoea, orthopnoea | Yes | Yes, in lay phrasing | Patients describe this as tiring on stairs, waking up short of breath, needing more pillows. The guideline's own education table (1.2) restates it as "falta de aire". |
| Cough, generalised tiredness | Yes | Yes | Low specificity. Cough in particular collides with an ACE-inhibitor adverse effect in the same patient population — see 4.2. |
| Memory problems or confusion | Yes | **Reported by others more than by self** | A confused patient is the least likely to report confusion. In a WhatsApp channel this may be observable as a change in how the patient writes rather than as something they say. That is an inference of mine, not a guideline claim, and it is unvalidated. |

### 1.2 The patient education table

Same guide, Tabla 28, p.73, row *Reconocimiento de síntomas y automanejo*, verbatim:

> Reconocer al menos los siguientes síntomas: falta de aire (disnea), tos persistente o sibilancias,
> retención de líquido (edema), cansancio/fatiga, pérdida del apetito o náuseas, aumento de la
> frecuencia cardíaca, que podrían indicar una descompensación de la enfermedad.

and:

> Ante un aumento de la disnea, detección de edema o una ganancia de peso mayor a dos kilos en tres
> días, el paciente debe comunicarse con su enfermera o médico tratante.

This adds two candidates the alarm list on the same page does not carry:

| Candidate | Device-free | Plausibly spontaneous | Note |
|---|---|---|---|
| Loss of appetite or nausea | Yes | Yes | Easily mentioned in passing, including in answer to an unrelated question about the day. |
| Increased heart rate | Partly | Yes, as palpitations | The guideline phrases it as a measurable rate; a patient can report the sensation without counting. Whether the sensation is an acceptable substitute is a clinical question. **REQUIRES CLINICAL REVIEW.** |

Note also that the second quotation is the guideline defining its own **action threshold** — three
specific findings that mean "contact your nurse or doctor". That is the closest thing in any of these
documents to a ready-made escalation rule, and it is the obvious starting point for the clinician
authoring the table. It is offered here as such and no further.

### 1.3 Depression symptoms, listed separately by the same guide

Tabla 28, p.74, row *Depresión*, verbatim:

> El paciente debe ser capaz de reconocer los síntomas de una depresión, tales como tristeza
> constante, decaimiento, irritabilidad, impotencia, frustración, bajo rendimiento en el trabajo, o
> reducción del nivel de actividad habitual. Si estos síntomas se prolongan en el tiempo, el paciente
> debe solicitar una evaluación por el equipo de salud.

Relevant to PreventIA for a reason beyond the clinical one: these are conversational signals almost
by definition, they accumulate over days rather than appearing at once, and a daily check-in is
structurally well placed to notice them. Whether PreventIA should act on them at all is a scope
decision, not just a clinical one — the PRD's stated scope is adherence and decompensation, and
depression is neither. **REQUIRES CLINICAL REVIEW**, and probably a product decision from Felipe
alongside it.

### 1.4 The weight problem, stated plainly

The 2 kg in 3 days rule appears twice in the guide, is the most operationally precise signal in any
of the three conditions, and needs a scale. PreventIA as described in the PRD asks for no device.

Three options exist and this document does not choose between them:

1. Accept that the strongest HF signal is out of reach and rely on the symptom candidates above.
2. Ask the patient whether they own a scale and treat weight as available for the subset who do.
3. Ask about a device-free proxy for fluid retention.

Option 3 is the tempting one and is the one to be careful about. Commonly repeated device-free
proxies — rings, shoes or a belt fitting more tightly — do **not** appear in any of the Chilean
documents consulted here. **Unverified.** What would verify it: the Heart Failure Association
self-care recommendations that MINSAL itself cites (Lainscak et al. 2011), or another guideline,
stating a garment-fit proxy explicitly. Until someone reads that paper, a garment-fit question must
not be written into the rule table on the strength of it being plausible.

---

## 2. Type 2 diabetes — hyperglycaemia

MINSAL 2010, *Guía Clínica Diabetes Mellitus tipo 2*, p.7 and section 3.1, gives the classic
symptom set. Verbatim:

> Síntomas clásicos de diabetes (polidipsia, poliuria, polifagia y baja de peso)

| Candidate | Device-free | Plausibly spontaneous | Note |
|---|---|---|---|
| Polydipsia | Yes | Yes, as unusual thirst | "Ando con mucha sed" is ordinary speech. |
| Polyuria | Yes | Yes | Frequently volunteered by older adults, including at night. |
| Polyphagia | Yes | Partly | Less often noticed as abnormal by the patient. |
| Unexplained weight loss | Partly | Yes | Reportable without a scale as clothes fitting loosely, but vaguely. |

**Important limit on all four.** These are the guideline's **diagnostic** criteria for identifying
undiagnosed diabetes, not a validated list of decompensation warning signs in an
already-diagnosed patient. Using them as decompensation flags is a reasonable-looking extrapolation
that the source does not itself make. **REQUIRES CLINICAL REVIEW.**

### 2.1 Diabetic foot

MINSAL 2010, section 3.5.3, p.27, defines the diabetic foot syndrome and states:

> Al menos 15% de los diabéticos presentará ulceraciones en el pie durante su vida. Se estima que
> 85% de los diabéticos que sufre amputaciones, previamente ha padecido una úlcera.

The guide's education section (section 3.5.3, p.27) states that structured education aims for
patients to "aprender a reconocer y anticipar posibles problemas en sus pies", and includes
self-examination as a taught procedure.

| Candidate | Device-free | Plausibly spontaneous | Note |
|---|---|---|---|
| A wound, sore or ulcer on the foot | Yes | Yes | The guideline explicitly teaches patients to look for it, so recognition is assumed. Whether PreventIA should ask about it proactively rather than wait for it to be mentioned is a design question. |

Note this is the one candidate in the whole document with a natural device-free, high-specificity,
patient-observable character. It is also the one where the guideline's own framing is prevention
over months, not decompensation over days, which may or may not fit a daily check-in.
**REQUIRES CLINICAL REVIEW.**

---

## 3. Type 2 diabetes — hypoglycaemia

The 2010 type 2 guide repeatedly instructs teams to educate patients about hypoglycaemia risk but
does not enumerate the symptoms. The MINSAL 2017 PSCV technical guidance likewise assigns the task
without listing the content: it instructs teams to "Realizar educación a pacientes diabéticos
insulorequirientes sobre técnica de administración de insulina, síntomas de hipoglicemia y hábitos
alimenticios saludables" and to "Reforzar educación a pacientes diabéticos sobre alimentación,
signos y síntomas de hipoglicemia y adherencia a tratamiento".

The enumerated list was found in the **type 1** guideline. MINSAL 2013, *Guía Clínica Diabetes
Mellitus Tipo 1*, section 8.2, verbatim:

> ¿Cuáles son los síntomas de hipoglicemia?
> Los signos y síntomas son:
> a) Autonómicos: palidez, temblor, sudoración fría, taquicardia
> b) Neuroglucopénicos: alteración del juicio y conducta, confusión, compromiso de conciencia,
> visión borrosa, alteración del habla, convulsiones y muerte.
> c) Inespecíficos: irritabilidad, terrores nocturnos, llanto, nauseas, hambre, cefalea, otros.

| Candidate | Device-free | Plausibly spontaneous | Note |
|---|---|---|---|
| Pallor, tremor, cold sweating, tachycardia | Yes | Yes, in lay phrasing | "Me puse a temblar", "sudé frío". Pallor is normally reported by a family member, not the patient. |
| Blurred vision | Yes | Yes | |
| Altered judgement, confusion, altered speech, impaired consciousness | Yes | **No, by construction** | A patient in this state does not self-report. Reachable only through a caregiver or through absence of response. |
| Irritability, nausea, hunger, headache | Yes | Yes | The guideline itself labels these "inespecíficos". |

**Three caveats, all of which need a clinician.**

1. **It is the type 1 guideline.** The counter-regulatory physiology is not condition-specific, but
   the applicability of a type 1 symptom list to older adults on oral hypoglycaemics or insulin for
   type 2 is exactly the kind of extrapolation this project must not make on its own authority.
   **REQUIRES CLINICAL REVIEW.**
2. **Hypoglycaemia unawareness is documented in the same section.** Verbatim: "No, algunos pacientes
   no presentan síntomas. Los síntomas autonómicos dependen de la secreción de hormonas de
   contrarregulación... Los síntomas neuroglucopénicos pueden estar ausentes especialmente en
   pacientes con hipoglicemias frecuentes". A symptom-listening product is structurally blind to the
   patients at highest risk. This belongs in the pitch as a stated limitation rather than being
   discovered by a judge.
3. **Beta blockers mask it.** MINSAL 2010 HTA guide, p.34, on beta blockers: "Enmascara síntomas de
   hipoglicemia". In a polymedicated cohort with both hypertension and diabetes — precisely
   PreventIA's target population — this is a routine combination, not an edge case.

The 2017 PSCV also sets the frailty criteria used to relax glycaemic targets, which bear directly on
who this cohort is: at least one of "Mayor de 75 años, comorbilidades crónicas significativas,
desnutrición (IMC <23), dependencia para las actividades básicas de la vida diaria (Índice de
Barthel ≤ 60), expectativa de vida <5 años, caídas frecuentes, depresión severa, deterioro
[cognitivo]". Worth reading before the synthetic cohort is written, since it describes the real
population better than an invented one will.

---

## 4. Hypertension

### 4.1 The finding: there is almost nothing to listen for

Neither Chilean hypertension document contains a patient-facing alarm list of the kind the heart
failure guide provides. This is not a search failure. The 2018 GPC executive summary is a set of
GRADE treatment recommendations — diagnostic method, blood pressure targets, when to start combined
therapy — and contains no symptom guidance for patients at all. The 2010 full guide discusses
symptoms only in the context of drug adverse effects, secondary hypertension, and hypertensive
crisis.

The reason is the disease. Hypertension between controls is, for most patients most of the time,
silent. **A daily conversational check-in has close to no hypertension-specific symptom signal to
detect.** For the hypertension arm, what PreventIA can actually observe is adherence and drug
tolerance — not decompensation.

This is the single most consequential finding in this workstream for the PRD, and it is carried into
the PRD proposals in `docs/research/README.md`.

### 4.2 What there is instead: adverse effects that drive non-adherence

MINSAL 2010 HTA guide, section on ACE inhibitors, p.30, verbatim:

> Además de la tos (7-15 %), otros efectos colaterales son, cefalea, rash, náuseas, hiperkalemia,
> síntomas de hipotensión arterial.

and on beta blockers, p.34, verbatim:

> Otros efectos colaterales son, bradicardia extrema, bloqueo a-v, Fenómeno de Raynaud, insuficiencia
> vascular periférica, broncoespasmo, fatiga, cefalea, alteraciones del sueño, insomnio, depresión.
> [...] Enmascara síntomas de hipoglicemia. Puede causar o agravar disfunción eréctil y pérdida de la
> líbido.

| Candidate | Device-free | Plausibly spontaneous | Note |
|---|---|---|---|
| Dry cough on an ACE inhibitor | Yes | Yes | Documented 7-15% frequency. Collides directly with cough as a heart failure alarm sign (1.1) in a patient who has both conditions. |
| Symptoms of hypotension | Yes | Yes, as dizziness on standing | Directly relevant: the 2018 GPC panel notes it evaluates "efectos adversos y tolerancia a la terapia antihipertensiva" when setting targets in frail patients and those over 80. |
| Fatigue, headache, insomnia, low mood on a beta blocker | Yes | Yes | Very low specificity; overlaps the HF and depression lists. |

The product-relevant point: these are the symptoms that make an older adult quietly stop taking a
pill, and PreventIA's primary job in the hypertension arm is to notice that happening. A patient who
says "esa pastilla me da tos" has given the care team something actionable, and PreventIA can carry
that to a human **without ever interpreting it** — which is precisely what section 3 of the PRD
permits.

### 4.3 An explicit anti-pattern, from the guideline itself

This is the most useful hypertension finding for the rule table, and it says what **not** to do.
MINSAL 2010, section 3.2.10, p.41, verbatim:

> No constituye una crisis hipertensiva la HTA con cifras tensionales elevadas, PAD >110 mmHg y <130
> mmHg, sin síntomas y sin amenaza de daño a corto plazo de órganos blanco. Frecuentemente estos
> pacientes consultan al Servicio de Urgencia con síntomas inespecíficos, que coexisten con la HTA
> pero no son producidos por ella, tales como epistaxis, vértigo paroxístico benigno, cefaleas
> tensionales o migraña. En estas situaciones, como la HTA se autolimita espontáneamente, puede ser
> peligroso su manejo agresivo en el Box de Urgencia.

Headache, nosebleed and dizziness are the symptoms a Chilean patient is most likely to attribute to
their blood pressure, and the national guideline states they frequently coexist with hypertension
without being caused by it. A naive rule mapping "me duele la cabeza" to a hypertension alarm would
be both wrong and, per the guideline's own warning about aggressive management, pointed in a harmful
direction.

**REQUIRES CLINICAL REVIEW** on the correct handling. The tension is real and this document does not
resolve it: ADR-0004 accepts over-alerting as the safe failure mode, but here the guideline
identifies a specific symptom cluster where over-alerting has a documented downstream harm.

The guide's *urgencia* and *emergencia hipertensiva* cause lists (p.41-42) are reproduced in the
source PDF rather than here. They are lists of clinical conditions — acute left ventricular failure,
acute coronary insufficiency, dissecting aortic aneurysm, intracranial haemorrhage, hypertensive
encephalopathy — not of patient-reportable symptoms, so they do not yield candidates for this table.

---

## 5. Cross-cutting observations

Collected here because they cut across conditions and each one weakens a naive rule table.

1. **Cough belongs to two conditions at once.** A heart failure alarm sign (1.1, 1.2) and a
   documented 7-15% ACE inhibitor adverse effect (4.2), in a cohort likely to have both. Any rule
   keying on cough alone will fire on the wrong cause a substantial fraction of the time.
2. **Fatigue, headache and low mood appear in the HF alarm list, the HF depression list and the beta
   blocker adverse effect list.** They are close to useless as isolated discriminators.
3. **Beta blockers mask hypoglycaemia symptoms** (MINSAL 2010 HTA, p.34), in exactly the
   hypertension-plus-diabetes patient PreventIA targets.
4. **The most severe states are the least self-reportable.** Confusion, impaired consciousness and
   altered speech appear as alarm signs in both the HF and hypoglycaemia lists, and a patient in any
   of those states does not send a WhatsApp message describing it. The reachable signal is silence,
   or a change in how the patient writes. Whether absence of reply should itself be a flag is
   **REQUIRES CLINICAL REVIEW** and is not currently anywhere in the PRD.
5. **The strongest single quantified signal needs a scale** (1.4).

## Open questions for the clinician

Consolidated from the marks above, in the order a clinician would most usefully take them.

1. Is the MINSAL 2015 contact threshold — increased dyspnoea, detected oedema, or over 2 kg gain in
   3 days — the right starting point for the heart failure rows of the table?
2. How should the table handle the weight signal given no device is assumed (1.4)?
3. Is a garment-fit proxy for oedema supportable by any source? (1.4, currently unverified.)
4. Can type 1 hypoglycaemia symptoms be used for type 2 older adults on oral agents or insulin? (3.)
5. Can the type 2 diagnostic symptom set be reused as decompensation signals in already-diagnosed
   patients? (2.)
6. How should hypertension be handled given it produces essentially no listenable decompensation
   signal, and given the guideline's explicit warning about non-specific symptoms? (4.1, 4.3.)
7. Should palpitations substitute for measured heart rate? (1.2.)
8. Is depression in scope at all? (1.3.)
9. Should absence of reply be a flag? (5.4.)
10. Should foot wounds be asked about proactively rather than waited for? (2.1.)

## Sources

All consulted 3 August 2026. Archived copies in `docs/research/sources/`.

1. Ministerio de Salud (Chile) and Sociedad Chilena de Cardiología y Cirugía Cardiovascular.
   *Guía Clínica Insuficiencia Cardíaca*. Santiago, 2015.
   https://www.minsal.cl/wp-content/uploads/2015/11/GUIA-CLINICA-INSUFICIENCIA-CARDIACA_web.pdf
   Archived as `minsal-2015-guia-clinica-insuficiencia-cardiaca.pdf`. Sections used: 3.4 (p.72-75),
   Tabla 28 (p.73-74), 5.6 (p.94).
   Note: direct WebFetch of this URL returns HTTP 403; it downloads normally with a browser user
   agent, which is how the archived copy was obtained.

2. Ministerio de Salud (Chile). *Guía Clínica Diabetes Mellitus tipo 2*. Santiago, 2010.
   https://www.superdesalud.gob.cl/difusion/572/articles-623_recurso_1.pdf
   (hosted by the Superintendencia de Salud). Archived as
   `minsal-2010-guia-clinica-diabetes-mellitus-tipo-2.pdf`. Sections used: diagnostic criteria,
   3.5.3 Pie diabético (p.27-30).

3. Ministerio de Salud (Chile). *Guía Clínica Diabetes Mellitus Tipo 1*. Santiago, 2013
   (1st ed. 2005, 2nd ed. 2011, updated May 2013).
   https://diprece.minsal.cl/wrdprss_minsal/wp-content/uploads/2014/12/Diabetes-Mellitus-tipo-1.pdf
   Archived as `minsal-2013-guia-clinica-diabetes-mellitus-tipo-1.pdf`. Section used: 8.2
   Hipoglicemia.

4. Ministerio de Salud (Chile). *Guía Clínica Hipertensión Arterial Primaria o Esencial en personas
   de 15 años y más*. Santiago, 2010.
   https://diprece.minsal.cl/wrdprss_minsal/wp-content/uploads/2014/12/Hipertensión-Arterial-en-personas-de-15-años-y-más.pdf
   Archived as `minsal-2010-guia-clinica-hipertension-arterial.pdf`. Sections used: pharmacological
   treatment adverse effects (p.30, p.34), 3.2.10 Crisis hipertensiva (p.41-42).

5. Ministerio de Salud (Chile), Subsecretaría de Salud Pública. *Resumen Ejecutivo, Guía de Práctica
   Clínica Hipertensión Arterial Primaria o Esencial en personas de 15 años y más*. Santiago, 2018.
   https://diprece.minsal.cl/wp-content/uploads/2019/05/08.-RE_GPC-HTA-Final_2018v5.pdf
   Archived as `minsal-2018-gpc-hipertension-resumen-ejecutivo.pdf`. Consulted in full; cited here
   for the absence of patient-facing symptom guidance and for the panel's comments on adverse-effect
   tolerance in patients over 70 and over 80.

6. Ministerio de Salud (Chile), Subsecretaría de Redes Asistenciales. *Orientación Técnica Programa
   de Salud Cardiovascular*. Santiago, 2017.
   https://redcronicas.minsal.cl/wp-content/uploads/2017/08/OT-PROGRAMA-DE-SALUD-CARDIOVASCULAR_05.pdf
   Archived as `minsal-2017-orientacion-tecnica-pscv.pdf`. Sections used: glycaemic targets and
   frailty criteria (footnote 5), professional role descriptions (education duties). This document
   is the primary source for workstream 2 and is described more fully there.

7. Lainscak M, Blue L, Clark AL, Dahlström U, Dickstein K, Ekman I, et al. *Self-care management of
   heart failure: practical recommendations from the Patient Care Committee of the Heart Failure
   Association of the European Society of Cardiology.* Eur J Heart Fail 2011;13(2):115-26.
   **Not read for this document.** Cited here only because it is reference 1 of section 3.4 of
   source 1, i.e. the stated basis of the MINSAL education recommendations. Reading it is the
   verification step named in 1.4.

## Verification status summary

| Claim | Status |
|---|---|
| MINSAL 2015 HF alarm list, verbatim | Verified, quoted from archived PDF |
| MINSAL 2015 HF education table and contact threshold | Verified, quoted |
| MINSAL 2013 hypoglycaemia symptom list, verbatim | Verified, quoted; type 1 guideline |
| Hypoglycaemia unawareness | Verified, quoted from source 3 |
| Beta blockers mask hypoglycaemia symptoms | Verified, quoted from source 4 |
| ACE inhibitor cough 7-15% | Verified, quoted from source 4 |
| MINSAL 2010 T2DM classic symptoms | Verified, quoted |
| Diabetic foot 15% lifetime ulceration, 85% of amputations preceded by ulcer | Verified, quoted from source 2 |
| Non-specific symptoms not caused by hypertension | Verified, quoted from source 4 |
| No patient-facing alarm list in either Chilean hypertension document | Verified by reading both in full |
| A newer MINSAL heart failure guideline does not exist | **Unverified** — not found in searches; DIPRECE index not read directly |
| Garment-fit as a device-free oedema proxy | **Unverified** — appears in no source consulted |
| Type 1 hypoglycaemia list applies to type 2 older adults | **Unverified extrapolation** — REQUIRES CLINICAL REVIEW |
| T2DM diagnostic symptoms usable as decompensation flags | **Unverified extrapolation** — REQUIRES CLINICAL REVIEW |
| Change in writing style as a proxy for confusion | **My inference, unvalidated** — no source |
