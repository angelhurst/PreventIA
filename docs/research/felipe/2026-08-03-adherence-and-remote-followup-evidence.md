# Adherence measurement and remote follow-up evidence

Workstream 4 of the Phase 0 research brief. Originally listed as workstream 3 and deferred once, for
the reason given in the municipal follow-up document.

Consulted 3 August 2026. Author: Felipe Carvajal Brown. Archived copies of downloadable sources are
in `docs/research/sources/`.

## Headline

Two findings, and the second is the one that changes what the PRD can claim.

**On measurement.** The PSCV already mandates an adherence instrument, the Test de Morisky Green
Levine-4, so PreventIA does not need to invent one. But three things about it need saying before
anyone embeds it: I could not find a Chilean validation of the 4-item instrument itself, the
instrument family is **copyrighted and licensed for a fee**, and every self-report instrument sits
under the same ceiling — self-report overestimates adherence by a median of 17% against electronic
monitoring. PreventIA is a self-report instrument by construction.

**On effect.** No study I could find establishes that a **conversational agent** reduces emergency
reconsultation or avoidable readmission in older adults. The evidence that does exist is for
adjacent things: nurse-led structured telephone support and device telemonitoring, where a 2015
Cochrane review reports real reductions, and two of the largest individual trials report nothing at
all. What separates the positive trials from the null ones is not the technology. It is whether the
contact terminated in a clinical service that could act.

That last sentence is the most useful thing in this document for the pitch, and it is the argument
for the triage queue in ADR-0006 rather than an argument the PRD currently makes.

---

## 1. How adherence is measured, and what PreventIA can borrow

### 1.1 What the PSCV already mandates

Established in workstream 2 and repeated here because it is the starting point: the MINSAL 2017 PSCV
Orientación Técnica names the **Test de Morisky Green Levine-4** in Anexo 11 and recommends it
explicitly, verbatim:

> En el seguimiento de los pacientes, siempre se debe evaluar y fomentar la adherencia a la terapia.
> En la fase inicial de compensación este aspecto se vuelve crucial, para esto se recomienda utilizar
> el Test de Morisky Green Levine – 4.

The instrument is four yes/no questions about forgetting doses, taking them at the right time,
stopping when feeling better, and stopping when feeling worse. Scoring in Chilean practice is
strict: the patient is adherent only at 0 points.

**Why this matters to the product.** Aligning to the instrument the clinical team already uses is
cheaper and far more credible than a bespoke adherence score. A number a nurse already knows how to
read beats a number we invented, even if ours is better.

### 1.2 Is it validated in Chile? Not that I could establish

This is the question the brief asked, and the honest answer is no, with a near miss.

**What I could not find:** a Chilean validation study of the **4-item** Morisky Green Levine test.
Searches on 3 August 2026 across SciELO Chile, SciELO regional and the general literature surfaced
Chilean studies that **use** the instrument, and a systematic review stating the purpose of
validating it in Chile, but no completed Chilean validation of MGL-4 itself. **Unverified.** What
would verify it: a search of the Chilean thesis repositories and Rev Med Chile back-issues by
someone with library access, or asking a PSCV academic directly.

**The psychometrics quoted in Chilean practice are borrowed.** The largest Chilean study to use the
instrument (Sandoval et al. 2014, below) states, verbatim:

> El test de Morisky-Green-Levine posee un valor alfa de Cronbach de 0,61; especificidad de 94% y
> valor predictivo positivo de 91,6%

and attributes those figures to its references 11-13, not to its own data. So the numbers Chilean
clinicians cite for this instrument are not Chilean numbers.

**What does exist in Chile, for the 8-item sibling.** Valencia-Monsalvez, Mendoza-Parra and
Luengo-Machuca evaluated the **MMAS-8** in **330 hypertensive adults aged 65 and over** in the
cardiovascular programme of a primary care centre in **Cabrero**, mean age 73,6 years, on oral
antihypertensives for at least six months, against blood pressure and pill count as reference
standards:

| Metric | vs blood pressure | vs pill count |
|---|---|---|
| Sensitivity | 86% | 85% |
| Specificity | 56% | 58% |
| Positive predictive value | 60% | 65% |
| Negative predictive value | 84% | 81% |
| Cronbach's alpha | 0,646 | — |

Non-adherent by MMAS-8: **62,1%**. Non-adherent by pill count: 47,6%. Blood pressure ≥140/90: 43%.

This is as close to our population as Chilean evidence gets — older adults, hypertensive, in a
Chilean APS cardiovascular programme — and it is a different instrument from the one the PSCV
mandates. Read it as: the instrument family **rules out** non-adherence reasonably well (sensitivity
85-86%, NPV 81-84%) and **rules it in** badly (specificity 56-58%). A screening tool, not a
measurement.

**REQUIRES CLINICAL REVIEW** on whether MMAS-8 evidence may stand in for MGL-4 in our reasoning. It
is the same kind of extrapolation flagged for the type 1 hypoglycaemia list in workstream 1, and the
same answer applies: a developer should not make it.

### 1.3 The licensing problem, which is a real risk and not a footnote

The Morisky scales are **copyrighted commercial instruments**. The rights holder's own site states
that use is protected by US copyright law, that permission is required, and that the scales "may not
be modified, sold, translated into another language or adapted for another medium without a
license". Published pricing at the time of consulting: **USD 4 per administration for MMAS-4, USD 7
for MMAS-8**, subscription licences from USD 1.000 per year, translations USD 250 and USD 500.

Enforcement is not theoretical. The literature contains a published *Corrigendum and Editorial
Warning Regarding Use of the MMAS-8 Scale*, attached to a paper about a medication-adherence app,
which is precisely the use case PreventIA occupies.

Three consequences, and none of them are engineering decisions:

1. **"Adapted for another medium" describes exactly what a conversational agent would be doing.** An
   agent that asks the four questions in Chilean Spanish inside a WhatsApp conversation is an
   adaptation and a translation at once.
2. **A per-administration fee is structurally hostile to a daily check-in.** The instrument was
   priced for a questionnaire administered at a clinic visit, not for something asked every morning.
3. **The naming is muddled and does not protect us.** "Test de Morisky Green Levine-4", the name the
   MINSAL document uses, and "MMAS-4", the trademarked name, refer to the same four questions. Using
   the MINSAL wording does not make the instrument public domain.

**Unverified:** whether MINSAL, or Chilean primary care generally, holds a licence covering routine
PSCV use, and whether such a licence would extend to a third party building a tool. What would
verify it: a direct question to MINSAL or to the rights holder. **This is a decision for Felipe, not
a research finding** — the options are to license, to not use the instrument, or to align to it
conceptually without reproducing its items, and only the last of those is free.

### 1.4 The ceiling every self-report instrument sits under

El Alili and colleagues reviewed **117 articles containing 251 comparisons** of the Medication Event
Monitoring System against other adherence measures. The result, verbatim:

> median adherence was grossly overestimated by 17% using self-report, by 8% using pill count and by
> 6% using rating

Only 35% of the comparisons met the review's own methodological standards, which the authors say
plainly. But the direction is not in dispute and the size is large.

**PreventIA is a self-report instrument.** It asks the patient whether they took the pill and
believes the answer. Nothing in the architecture in `CLAUDE.md` changes that, and nothing should:
the alternative is a device, and the product's premise is no device.

This is a limitation to state in the pitch rather than have found. The defensible framing is that
PreventIA measures **reported** adherence, daily, longitudinally, in the patient's own words, and
that this is more information than a nurse currently has at a control three months later — not that
it measures adherence.

One genuine difference, and it is mine rather than a source's: MGL-4 is a **recall** instrument
asking about a period already past, whereas a daily check-in is closer to a **prospective diary**.
Recall bias should be smaller. Social desirability bias, which is most of the 17%, should not be,
and might be worse with a system the patient knows reports to their nurse. **Unvalidated.** What
would verify it: a study comparing daily conversational self-report against pill count in the same
patients. Nobody has done it that I could find.

### 1.5 What the one large Chilean adherence study found

Sandoval and colleagues studied **513 hypertensive patients** drawn from a universe of 1.484 in the
PSCV of two primary care centres in the Región Metropolitana, aged 30 to 68, at least 12 months in
the programme, adherence by MGL-4.

**Adherence: 36,6%.** Higher in women, 38,4% against 28,9% in men.

After multivariate analysis, non-adherence was associated with:

| Factor | Odds ratio (95% CI) |
|---|---|
| High emotional stress and depressive symptoms (GHQ-12 ≥7) | **1,93 (1,27-2,94)** |
| Male gender | 1,76 (1,21-2,56) |
| Low education (under 8 years) | 1,72 (1,18-2,53) |
| Inadequate patient-physician relationship | 1,56 (1,13-2,27) |

Three things follow for PreventIA.

**First, the depression question from workstream 1 gets sharper.** The strongest single predictor of
non-adherence in the only large Chilean study of this is emotional distress and depressive
symptoms. Workstream 1 asked whether depression is in scope on clinical grounds; this says it is
also in scope on **adherence** grounds, which is squarely inside the PRD's stated purpose. Still
**REQUIRES CLINICAL REVIEW**, and still a product decision for Felipe alongside it.

**Second, the quality of the patient-clinician relationship is a measured risk factor.** That cuts
both ways for a conversational agent and I am not going to pretend it only cuts our way. A daily
companion might strengthen the relationship, or might be experienced as the health system replacing
a person with a machine. **Unverified**, and it is the kind of thing a Chilean 80-year-old's
reaction settles, not a literature search.

**Third, the study lost 443 of 956 sampled patients to contact failure**, of which **245 were
"error en la información de contacto"**. Roughly one in four people sampled from a live PSCV
register could not be reached because the register's contact data was wrong.

That is the third time this failure mode appears in this research. FOFAR's unreminded group was
unreminded because their contact data was wrong. A rescate action escalates to a home visit
precisely when the phone number fails. And here, a university research team with funding lost a
quarter of its sample the same way.

**For PreventIA this is the single most underrated deployment risk and it is not in the PRD at all.**
The product assumes a working WhatsApp number for the patient. The Chilean evidence says the health
system frequently does not have one, and that the patients whose numbers are wrong are systematically
the ones most likely to decompensate unobserved.

---

## 2. Does remote follow-up change outcomes?

The brief asks specifically about emergency reconsultation and avoidable readmission in older
adults, because PRD section 10 claims them. This section reports what I found, including the results
that go against us.

### 2.1 The meta-analytic answer: yes, modestly, for heart failure

The Cochrane review by Inglis and colleagues, 2015, covers **41 studies and 13.192 participants**
with chronic heart failure — 25 studies of structured telephone support, 18 of non-invasive
telemonitoring, 2 testing both.

| Intervention | Outcome | Risk ratio (95% CI) | Participants |
|---|---|---|---|
| Structured telephone support | All-cause mortality | 0,87 (0,77-0,98) | 9.222 |
| Structured telephone support | HF-related hospitalisation | 0,85 (0,77-0,93) | 7.030 |
| Non-invasive telemonitoring | All-cause mortality | 0,80 (0,68-0,94) | 3.740 |
| Non-invasive telemonitoring | HF-related hospitalisation | 0,71 (0,60-0,83) | 2.148 |

All four rated **moderate-quality evidence** under GRADE.

This is the strongest evidence in the whole document and it is worth being precise about what it
is. "Structured telephone support" in these trials means a **nurse** calling on a schedule, with
protocols, working inside a heart failure service. It is not an automated message and it is not a
chatbot. Citing it as support for PreventIA without saying that would be dishonest.

### 2.2 The two largest individual trials of telemonitoring found nothing

**Tele-HF.** Chaudhry and colleagues, NEJM 2010, **1.653 patients** recently hospitalised for heart
failure, randomised to a telephone-based interactive voice-response system collecting daily symptoms
and weight, reviewed by clinicians. Readmission for any reason or death within 180 days: **52,3%
against 51,5%, P=0,75**. Authors' conclusion, verbatim:

> Among patients recently hospitalized for heart failure, telemonitoring did not improve outcomes.
> The results indicate the importance of a thorough, independent evaluation of disease-management
> strategies before their adoption.

That last sentence should be read twice by anyone building this product.

**BEAT-HF.** Ong and colleagues, JAMA Internal Medicine 2016, older adults hospitalised for heart
failure, pre-discharge education plus post-discharge telephone nurse coaching plus home
telemonitoring of weight, blood pressure, heart rate and symptoms. Readmission at 30 days 22,7%
against 21,6%, P=0,63; at 180 days 50,8% against 49,2%, P=0,39; 180-day mortality 14,0% against
15,8%, P=0,26. No difference anywhere.

**And the reason offered matters more to us than the result.** At most **61,4%** of intervention
patients were adherent to more than half of the calls and telemonitoring in the first 30 days. The
intervention was largely not received. A remote follow-up product can fail not because the idea is
wrong but because patients stop answering — which is a design problem PreventIA inherits whole, and
which the PRD's daily cadence makes harder rather than easier.

### 2.3 The largest positive trial, and what was different about it

**TIM-HF2.** Koehler and colleagues, Lancet 2018, **1.571 patients** in Germany, NYHA class II-III,
hospitalised for heart failure within the previous 12 months, ejection fraction ≤45% or on oral
diuretics, **major depression excluded**. Primary outcome, percentage of days lost to unplanned
cardiovascular hospital admission or all-cause death: **4,88% against 6,64%, ratio 0,80 (0,65-1,00),
p=0,0460**. All-cause mortality 7,86 against 11,34 per 100 person-years, **HR 0,70 (0,50-0,96),
p=0,0280**.

Three features of this trial are the ones to take, and none of them are the technology:

1. **A tightly defined population.** Recent HF admission, specified NYHA class, specified ejection
   fraction. Not "older adults with chronic conditions".
2. **A telemedical centre.** Daily transmissions went to a staffed service that communicated with
   the cardiologist and the general practitioner. Somebody was on the other end with the authority
   to act.
3. **Depression was an exclusion criterion**, in a trial reporting a positive result, while the
   Chilean adherence study reports depression as the strongest predictor of non-adherence. Those two
   facts sitting next to each other is not comfortable and I am not going to smooth it over.

The p-value is 0,046 and the confidence interval on the primary outcome touches 1,00. This is a
positive trial, not a decisive one.

### 2.4 Messaging specifically: small effects at best

**StAR.** Bobrow and colleagues, Circulation 2016, **1.372 adults** with high blood pressure in South
Africa, randomised three ways to information-only SMS, interactive SMS, or usual care. At 12 months,
adjusted systolic blood pressure change against usual care: **-2,2 mm Hg (95% CI -4,4 to -0,04)**
for information-only and **-1,6 mm Hg (-3,7 to 0,6)** for interactive. Odds of reaching <140/90:
1,42 and 1,41. Authors' conclusion, verbatim:

> we found a small reduction in systolic blood pressure control compared with usual care at 12
> months. There was no evidence that an interactive intervention increased this effect.

The second sentence is the uncomfortable one. StAR is the closest thing in the literature to a
controlled test of "does two-way beat one-way", and it says no. The distinction PreventIA leans on —
that FOFAR was a reminder and we are a conversation — is not supported by StAR. It is not refuted
either, since StAR's "interactive" arm was scripted SMS and not a conversational agent, but it
should stop us from asserting the distinction as though it were established.

**FOFAR**, established in workstream 3: 11,6% non-attendance with reminder against 13,3% without
across 4.481.282 appointments, panel calling both the effect and the adherence contribution
marginal, on a confounded comparison.

### 2.5 Conversational agents specifically: the field is not ready to be cited

**The one trial that is genuinely close.** A randomised clinical trial of voice-based conversational
AI for basal insulin management in type 2 diabetes, JAMA Network Open 2023, four primary care
clinics at an academic medical centre, 8-week follow-up. Time to optimal insulin dose **median 15
days against more than 56**; insulin adherence **83% against 50%**; better glycaemic control and
lower diabetes-related emotional distress.

Those are large effects, and there are two reasons not to lean on them.

**It enrolled 32 people.** That is a pilot.

**And the intervention does the one thing PreventIA has forbidden itself.** The system provided
updated insulin dosing instructions after a daily check-in conversation. Section 3 of the PRD and
section 2 of `CLAUDE.md` prohibit exactly that. So the strongest signal available for a
conversational agent in chronic disease comes from an agent that titrates a drug — and the
plausible mechanism for its effect is the titration, not the conversation.

This is worth saying out loud in the pitch rather than avoiding. The clinical boundary is not free.
It rules out the mechanism with the best evidence behind it. What it buys is a product that a health
service can actually deploy, and that trade is defensible; pretending there is no trade is not.

**The systematic reviews say the field is immature.** Schachner, Keller and von Wangenheim, JMIR
2020, reviewed AI-based conversational agents for chronic conditions and found **10 studies: 2
randomised controlled trials, 7 quasi-experimental, 1 proof of concept**. Their conclusion, verbatim:

> The literature on AI-based conversational agents for chronic conditions is scarce and mostly
> consists of quasi-experimental studies with chatbots in prototype stage.

A more recent review — Han, Lee and Son, *DIGITAL HEALTH* 2026, covering January 2010 to November
2025 across seven databases — was located but **not read**: the publisher returned HTTP 403 to every
fetch attempt on 3 August 2026. **Unverified.** What would verify it: institutional access, or the
PubMed record once indexed. Its existence is noted so a later session does not conclude the 2020
review is the current state of the art.

**No study I found reports emergency reconsultation or avoidable readmission as an outcome of a
conversational agent in older adults.** That is the specific claim in PRD section 10, and the
evidence base for it is empty rather than negative.

---

## 3. What this means for PRD section 10

The pattern across everything above is not about modality. Sorted by result:

| Intervention | Human on the other end? | Result |
|---|---|---|
| Structured telephone support (Cochrane, 25 studies) | Yes, nurse | Mortality and HF admissions down |
| Telemonitoring in a telemedical centre (TIM-HF2) | Yes, staffed centre | Days lost and mortality down, p≈0,05 |
| Telemonitoring reviewed by clinicians (Tele-HF) | Yes, but no defined service | Null |
| Nurse coaching plus telemonitoring, largely not received (BEAT-HF) | Yes, in principle | Null |
| Automated SMS, interactive or not (StAR) | No | -2,2 mm Hg, interactive no better |
| Automated SMS and calls at national scale (FOFAR) | No | Marginal, on a confounded comparison |

Read down that column and the reminder-versus-conversation distinction the project has been leaning
on is not the axis that separates the results. **Whether the contact terminated in a clinical service
that could act** tracks the outcomes much better.

If that reading is right — and it is my reading of six studies, not a published meta-regression, so
mark it as such — then the most defensible thing PreventIA does is not the conversation. It is
ADR-0006: the ranked triage queue that puts a summarised case in front of a named clinician who can
act on it. The clinical non-negotiable that every escalation terminates at a human was written as an
ethical constraint. The evidence suggests it is also the load-bearing part.

**Proposed rewrite of PRD section 10's post-Lab criterion is in `docs/research/README.md`, P5.**

What section 10 must not say:

- That remote follow-up reduces readmissions in older adults. The two largest individual trials of
  it are null, and the positive meta-analysis is of nurse-delivered telephone support.
- That a two-way conversation beats a one-way reminder. StAR tested that directly and found no
  difference.
- That there is evidence for conversational agents in this population. There are ten studies of
  prototypes and one 32-person pilot that does something we have forbidden.

What section 10 can say, and should:

- That Chile has tried automated one-way contact at national scale with a marginal result, which is
  a reason to build something that is not a reminder rather than a reason not to build.
- That the evidence which is positive is for contact embedded in a clinical service, which is what
  the triage queue makes PreventIA.
- That the burden argument from workstream 3 does not depend on any of this.

---

## 4. Open questions

1. **Does MINSAL or Chilean primary care hold a Morisky licence, and would it cover a third-party
   tool?** (1.3.) Blocks any decision to embed the instrument. **For Felipe, with legal advice —
   this document does not give any.**
2. Is there a Chilean validation of the **4-item** MGL, or only of MMAS-8? (1.2.) **Unverified.**
3. May MMAS-8 Chilean evidence stand in for MGL-4 in our reasoning? (1.2.) **REQUIRES CLINICAL
   REVIEW.**
4. Is depression in scope, now that it is the strongest predictor of non-adherence in the Chilean
   data? (1.5.) **REQUIRES CLINICAL REVIEW**, and a product decision.
5. **How does a CESFAM know a patient's current phone number, and how often is it wrong?** (1.5.)
   This is the deployment risk nobody has costed, and it is the same conversation that answers the
   rescate-time question from workstream 3.
6. What does Han, Lee and Son 2026 actually report? (2.5.) Not read.
7. Does any evaluation exist of two-way or conversational follow-up in Chile or Latin America?
   Carried over from workstream 3 and **still not found**. Searches on 3 August 2026 surfaced
   Spanish and Costa Rican programmes and a Chilean COVID tele-rehabilitation observational study,
   none of them conversational follow-up in chronic disease.

## Sources

All consulted 3 August 2026.

1. Ministerio de Salud (Chile), Subsecretaría de Redes Asistenciales. *Orientación Técnica Programa
   de Salud Cardiovascular*. Santiago, 2017.
   https://redcronicas.minsal.cl/wp-content/uploads/2017/08/OT-PROGRAMA-DE-SALUD-CARDIOVASCULAR_05.pdf
   Archived as `minsal-2017-orientacion-tecnica-pscv.pdf`. Section used: Anexo 11 and the adherence
   recommendation quoted in 1.1.

2. Valencia-Monsalvez F, Mendoza-Parra S, Luengo-Machuca L. *Evaluación de la escala Morisky de
   adherencia a la medicación (MMAS-8) en adultos mayores de un centro de atención primaria en
   Chile*. Rev Peru Med Exp Salud Publica. 2017;34(2). doi:10.17843/rpmesp.2017.342.2206
   http://www.scielo.org.pe/scielo.php?script=sci_arttext&pid=S1726-46342017000200012
   Chilean study in a Peruvian journal. Setting: Cabrero, Región del Biobío. Web page, not archived.

3. Sandoval D, Chacón J, Muñoz R, Henríquez Ó, Koch E, Romero T. *Influencia de factores
   psicosociales en la adherencia al tratamiento farmacológico antihipertensivo. Resultados de una
   cohorte del Programa de Salud Cardiovascular de la Región Metropolitana, Chile*. Rev Méd Chile.
   2014;142(10). doi:10.4067/S0034-98872014001000003
   https://www.scielo.cl/scielo.php?script=sci_arttext&pid=S0034-98872014001000003
   Web page, not archived. Note: `scielo.cl` returns HTTP 403 to plain fetchers and serves normally
   to `curl` with a browser user agent, the same behaviour as `minsal.cl`.

4. El Alili M, Vrijens B, Demonceau J, Evers SM, Hiligsmann M. *A scoping review of studies comparing
   the medication event monitoring system (MEMS) with alternative methods for measuring medication
   adherence*. Br J Clin Pharmacol. 2016;82(1):268-279. doi:10.1111/bcp.12942
   https://pubmed.ncbi.nlm.nih.gov/27005306/

5. Morisky Scale / MMAS Research LLC. *MMAS License Pricing* and *MMAS-4 & MMAS-8 — The Morisky
   Scales*. https://www.moriskyscale.com/mmas-license-pricing.html and
   https://www.moriskyscale.com/about-the-morisky-scale---mmas-4--mmas-8-the-morisky-scales.html
   Rights holder's own commercial pages. Cited for the licence terms and prices in 1.3. Prices as
   published on the date consulted; they are not guaranteed current.

6. *Corrigendum and Editorial Warning Regarding Use of the MMAS-8 Scale (The Health Buddies App as a
   Novel Tool to Improve Adherence and Knowledge in Atrial Fibrillation Patients: A Pilot Study)*.
   https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6304217/
   Cited only as evidence that enforcement against app-based use has happened.

7. Inglis SC, Clark RA, Dierckx R, Prieto-Merino D, Cleland JGF. *Structured telephone support or
   non-invasive telemonitoring for patients with heart failure*. Cochrane Database Syst Rev. 2015 Oct
   31;2015(10):CD007228. https://pubmed.ncbi.nlm.nih.gov/26517969/

8. Chaudhry SI, Mattera JA, Curtis JP, et al. *Telemonitoring in patients with heart failure*. N Engl
   J Med. 2010 Dec 9;363(24):2301-9. doi:10.1056/NEJMoa1010029
   https://pubmed.ncbi.nlm.nih.gov/21080835/

9. Ong MK, et al. *Effectiveness of Remote Patient Monitoring After Discharge of Hospitalized
   Patients With Heart Failure: The Better Effectiveness After Transition-Heart Failure (BEAT-HF)
   Randomized Clinical Trial*. JAMA Intern Med. 2016;176(3):310-318.
   Figures taken from secondary summaries of the trial rather than from the JAMA Internal Medicine
   full text, which was not reachable. **Partially verified** — the 30-day, 180-day and mortality
   figures and the 61,4% intervention-adherence figure should be checked against the primary paper
   before any of them is put on a slide.

10. Koehler F, Koehler K, Deckwart O, et al. *Efficacy of telemedical interventional management in
    patients with heart failure (TIM-HF2): a randomised, controlled, parallel-group, unmasked trial*.
    Lancet. 2018;392(10152):1047-1057. doi:10.1016/S0140-6736(18)31880-4
    https://pubmed.ncbi.nlm.nih.gov/30153985/

11. Bobrow K, Farmer AJ, Springer D, et al. *Mobile Phone Text Messages to Support Treatment
    Adherence in Adults With High Blood Pressure (SMS-Text Adherence Support [StAR]): A Single-Blind,
    Randomized Trial*. Circulation. 2016;133(6):592-600. doi:10.1161/CIRCULATIONAHA.115.017530
    https://pubmed.ncbi.nlm.nih.gov/26769742/

12. Nayak A, Vakili S, Nayak K, Nikolov M, Chiu M, Sosseinheimer P, Talamantes S, Testa S,
    Palanisamy S, Giri V, Schulman K. *Use of Voice-Based Conversational Artificial Intelligence for
    Basal Insulin Prescription Management Among Patients With Type 2 Diabetes: A Randomized Clinical
    Trial*. JAMA Netw Open. 2023;6(12):e2340232. doi:10.1001/jamanetworkopen.2023.40232
    https://pmc.ncbi.nlm.nih.gov/articles/PMC10692866/

13. Schachner T, Keller R, von Wangenheim F. *Artificial Intelligence-Based Conversational Agents for
    Chronic Conditions: Systematic Literature Review*. J Med Internet Res. 2020;22(9):e20701.
    doi:10.2196/20701 https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7522733/

14. Han GI, Lee HJ, Son YJ. *Natural language processing-based chatbots for chronic disease
    self-management: A systematic review of implementation and health outcomes*. DIGITAL HEALTH.
    2026. doi:10.1177/20552076261450385
    https://journals.sagepub.com/doi/10.1177/20552076261450385
    **Not read.** Publisher returned HTTP 403. Listed so its absence is visible.

15. Dirección de Presupuestos (DIPRES). *Informe Final de Evaluación EPG: Programa Fondo de Farmacia*.
    2018. Archived as `dipres-evaluacion-programa-salud-cardiovascular.pdf`. Cited here only for the
    FOFAR figures established in workstream 3.

## Verification status summary

| Claim | Status |
|---|---|
| PSCV mandates the Test de Morisky Green Levine-4 | Verified, quoted from source 1 |
| MMAS-8 psychometrics in 330 Chilean hypertensive 65+ | Verified from source 2 |
| MGL-4 psychometrics quoted in Chile are borrowed from non-Chilean references | Verified, quoted from source 3 |
| A Chilean validation of MGL-4 exists | **Unverified — not found.** See 1.2 |
| Morisky scales are copyrighted and licensed for a fee, at the prices stated | Verified from source 5, on the date consulted |
| A published corrigendum and editorial warning exists over app use of MMAS-8 | Verified, source 6 |
| Whether Chilean public health holds a Morisky licence | **Unverified** |
| Self-report overestimates adherence by a median of 17% vs MEMS | Verified, quoted from source 4 |
| Daily prospective self-report has less recall bias than MGL-4 recall | **My inference, unvalidated** |
| Cochrane 2015 effect sizes for STS and telemonitoring | Verified from source 7 |
| Tele-HF null result and authors' conclusion | Verified, quoted from source 8 |
| BEAT-HF null result and 61,4% intervention adherence | **Partially verified** — secondary sources only, see source 9 |
| TIM-HF2 primary outcome, mortality, and depression exclusion | Verified from source 10 |
| StAR effect sizes and "no evidence that an interactive intervention increased this effect" | Verified, quoted from source 11 |
| Voice-based conversational AI insulin trial, n=32, results | Verified from source 12 |
| Conversational-agent literature is scarce and mostly quasi-experimental | Verified, quoted from source 13 |
| No study reports reconsultation or readmission for a conversational agent in older adults | **Verified as an absence in the searches run**, which is weaker than a systematic search |
| Sandoval adherence 36,6% and the four odds ratios | Verified from source 3 |
| 245 of 956 sampled patients unreachable due to wrong contact data | Verified, from source 3 |
| "Human on the other end" explains the pattern of results better than modality | **My reading of six studies.** Not a published analysis |
| A Chilean or Latin American evaluation of conversational follow-up exists | **Unverified — not found** |
