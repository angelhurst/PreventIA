# Clinician-configurable thresholds and human-in-the-loop for an LLM clinical follow-up tool

Consulted 5 August 2026. Method: 30 web searches and 19 direct page fetches, of which 10 fetches
succeeded. Full search record in section 9, including every failure. This document surveys what
published standards exist and how shipped software exposes them. It proposes no clinical value and
recommends no threshold; which numbers PreventIA uses is the healthcare professional's decision.

**Honesty statement.** Four things came back thin or empty and are labelled as such rather than
padded:

1. **No primary-source retrieval of the CDC opioid guideline's MME numbers.** `cdc.gov` returned
   HTTP 403 to a plain fetcher on three separate paths. The 2022 Recommendation 4 text was retrieved
   verbatim from the PMC mirror and **contains no MME figure at all**. The familiar 50 and 90 MME
   numbers come from secondary sources describing the superseded 2016 guideline and are marked
   `UNVERIFIED` against primary text in section 2.3.
2. **No Chilean numeric threshold was verified.** The GES/AUGE guideline PDFs were located but not
   opened, so this document carries no Chilean clinical figure. Line A's Chilean half produced
   infrastructure findings (CENS Pharma, Formulario Nacional) rather than values.
3. **The one directly on-topic academic source on CDS rule authoring environments could not be
   read.** BMC redirects to a Springer identity provider; a PMC guess returned a different article.
   It is cited from its search-result extract only and flagged.
4. **Nothing was found that addresses a patient-facing conversational agent stating a dose.** The
   dose-line evidence in section 6 is assembled from adjacent regulatory and standards text. The
   inference is mine and is labelled as inference, not as a finding.

Several quantitative claims in sections 3 and 4 come from search-result extracts of named papers
whose full texts I did not open. Each is marked `[extract only]`. Do not put any of those numbers on
a slide without opening the paper.

I am not a lawyer. Licence and regulatory text below is quoted verbatim precisely so that a
qualified reader can interpret it. I have not interpreted it.

---

## 1. Headline findings

1. **A published dose number is a unit of measurement, not a patient instruction, and WHO says so in
   its own words** — the DDD "does not necessarily correspond to the recommended or Prescribed Daily
   Dose". See section 6.
2. **The clearest documented harm from a clinician-facing threshold is the threshold being read as a
   rule**, which is why CDC removed the MME figures from its 2022 recommendation text entirely. See
   section 6.
3. **Every shipped CDS standard models its output as a dismissible card addressed to a clinician,
   never as an executed instruction** — CDS Hooks lets the user "ignore it entirely, or dismiss it
   with or without an override reason". See section 3.
4. **The regulatory line that decides whether a tool is a regulated device is drawn at "directive"
   and at "who reads it"**, not at whether a number is stored: FDA's Criterion 3 excludes software
   giving "a specific preventative, diagnostic, or treatment output or directive". See section 4.
5. **A configuration edit is a clinical act and needs the audit trail of one** — the field's own
   worst cases are a rule nobody could reconstruct, and the incumbent Chilean system already defines
   every state by a recorded event rather than an assertion. See sections 3 and 7.

---

## 2. Line A — standards a clinician could configure against

### 2.1 What exists, and whether it is machine-readable

| Standard | What it is | Machine-readable? | Source |
|---|---|---|---|
| **WHO eEML** (electronic Essential Medicines List) | Online database of the Model List. States it holds 1,418 recommendations for 667 medicines and 156 therapeutic equivalents across 30+ therapeutic categories | **Partly.** Export to PDF, XLSX and DOCX with selectable sections and metadata fields. **No API or JSON/CSV found on the page** | [list.essentialmeds.org](https://list.essentialmeds.org/) |
| WHO Model Lists (published) | Current versions per WHO are the 24th EML and 10th EMLc, updated September 2025 | PDF, via IRIS | [who.int EML page](https://www.who.int/groups/expert-committee-on-selection-and-use-of-essential-medicines/essential-medicines-lists), [IRIS 23rd list](https://iris.who.int/server/api/core/bitstreams/289a875c-cc89-4914-90ad-eb3c578ebaf6/content) |
| **WHO ATC/DDD Index** | Anatomical Therapeutic Chemical classification plus Defined Daily Dose, maintained by the WHO Collaborating Centre for Drug Statistics Methodology, Oslo | Searchable online; **a machine-readable version is sold**, ordering portal at `orders.atcddd.fhi.no`. No price or terms published on the copyright page | [atcddd.fhi.no](https://atcddd.fhi.no/), [copyright page](https://atcddd.fhi.no/copyright_disclaimer/) |
| **WHO analgesic ladder** | Three-step cancer pain framework, originally 1986. Secondary sources report the 2018 WHO guideline applies to people aged 10 and over and removed advocacy for explicit use of weak opioids | Prose guideline. `UNVERIFIED` — I did not retrieve the 2018 WHO guideline itself; all detail here is from secondary commentary | [BJA 2022 commentary](https://www.bjanaesthesia.org.uk/article/S0007-0912(22)00126-X/fulltext), [AMA Journal of Ethics](https://journalofethics.ama-assn.org/article/revisiting-who-analgesic-ladder-surgical-management-pain/2020-08) |
| **Formulario Nacional de Medicamentos (Chile)** | DTO. N° 194, published in the Diario Oficial 10 March 2006; the regulation is DTO. N° 264/2003. Monographs specify INN, pharmaceutical forms, routes of administration and doses, adverse reactions, contraindications, interactions | Word/PDF regulation text on MINSAL's juridical server. **No structured dataset found** | [DTO_194_05.DOC](https://juridico1.minsal.cl/DTO_194_05.DOC), [reglamento](http://farmacia.udec.cl/wp-content/uploads/2015/09/reglamento_formulario_nacional.pdf), [WHO NEML mirror, 2005](https://cdn.who.int/media/docs/default-source/essential-medicines/national-essential-medicines-lists-(neml)/paho_neml/chile-2005.pdf) |
| **Terminología Farmacéutica Chilena** | Named by MINSAL as the medication terminology layer of the national interoperability architecture | **Yes, via CENS Pharma** — a terminology server exposing a FHIR REST API, mapping to SNOMED CT, DCI and ATC. **Commercial: "CENS Pharma es un producto, por lo cual, debes adquirir una licencia para su utilización."** Deployment is a Docker server. No price published | [cens.cl/cens-pharma](https://cens.cl/cens-pharma/), [MINSAL Estándares y Perfiles](https://interoperabilidad.minsal.cl/docs/especificacion-de-la-arquitectura/estandares-perfiles.html) |
| **GES/AUGE clinical guidelines** | DIPRECE publishes the AUGE guideline set, including hypertension (GPC HTA 2018) and heart failure | PDF prose. **Located, not opened.** No threshold from these is quoted anywhere in this document | [DIPRECE guideline index](https://diprece.minsal.cl/le-informamos/auge/acceso-guias-clinicas/guias-clinicas-auge/), [GPC HTA 2018](https://diprece.minsal.cl/wp-content/uploads/2019/05/08.-RE_GPC-HTA-Final_2018v5.pdf), [Guía IC](https://www.minsal.cl/wp-content/uploads/2015/11/GUIA-CLINICA-INSUFICIENCIA-CARDIACA_web.pdf) |

### 2.2 Licence text, quoted verbatim

Quoted so a qualified reader can interpret it. I have not interpreted it.

**WHO ATC/DDD Index** ([atcddd.fhi.no/copyright_disclaimer](https://atcddd.fhi.no/copyright_disclaimer/)):

> "Use of all or parts of the material requires reference to the WHO Collaborating Centre for Drug
> Statistics Methodology."

> "Copying and distribution for commercial purposes is not allowed. Changing or manipulating the
> material is not allowed."

**WHO eEML** ([list.essentialmeds.org/licencing](https://list.essentialmeds.org/licencing)) — Creative
Commons Attribution IGO License, **CC BY 3.0 IGO**:

> "you are free to copy, distribute, transmit, and adapt this work, including for commercial
> purposes"

with the eEML not to be used "In conjunction with the advertising or promotion of commercial
products, including proprietary medicines" or "In any manner that suggests that WHO endorses any
specific organisation or products", and "The use of the WHO logo is not permitted." Required
citation: "WHO electronic Essential Medicines List (eEML), World Health Organization, 2020.
https://list.essentialmeds.org/ (beta version 1.0). Licence: CC BY 3.0 IGO."

**Note the discrepancy, it matters.** The eEML *web database* is published under CC BY 3.0 IGO,
which the page says permits commercial use. WHO's *printed* Model List publications carry the
standard WHO publication licence, **CC BY-NC-SA 3.0 IGO**, whose terms permit copying and adapting
"for non-commercial purposes" and require share-alike. Two different artefacts, two different
licences, opposite answers on commercial reuse
([WHO licensing](http://www.who.int/about/licensing),
[The selection and use of essential medicines, 2025](https://iris.who.int/server/api/core/bitstreams/17642505-ecd3-4940-a691-4f1dfa0d835a/content)).
`iris.who.int` returned HTTP 403 to my fetcher, so the CC BY-NC-SA line is quoted from a search
extract and is **`UNVERIFIED` against the primary document.** A lawyer should settle this before
anything from either list is embedded in software.

**Practical reading for engineering, not legal:** ATC/DDD is the one that would need money and
permission; the eEML is the one with a stated free-reuse licence and an export button.

### 2.3 Opioid thresholds — what is actually verified

This is the part of the brief where a wrong number would do the most damage, so provenance is
attached to each claim.

**Verified, retrieved verbatim** from the CDC 2022 guideline via the PMC mirror
([PMC9639433](https://pmc.ncbi.nlm.nih.gov/articles/PMC9639433/)) — Recommendation 4 in full:

> "When opioids are initiated for opioid-naïve patients with acute, subacute, or chronic pain,
> clinicians should prescribe the lowest effective dosage. If opioids are continued for subacute or
> chronic pain, clinicians should use caution when prescribing opioids at any dosage, should
> carefully evaluate individual benefits and risks when considering increasing dosage, and should
> avoid increasing dosage above levels likely to yield diminishing returns in benefits relative to
> risks to patients."

**There is no MME figure in that sentence.** That absence is deliberate and it is the single most
important fact in this document for section 6.

**`UNVERIFIED` against primary text:** the widely cited pair of numbers — reassess above 50 MME/day,
avoid exceeding 90 MME/day without careful justification — is reported by secondary sources as the
wording of the **superseded 2016** guideline, and reported as surviving in the 2022 guideline only in
*supporting text* rather than in the recommendations. I could not confirm either against CDC's own
pages: `cdc.gov/mmwr/volumes/71/rr/rr7103a1.htm` and
`cdc.gov/overdose-prevention/hcp/clinical-guidance/opioid-prescribing-guideline.html` both returned
HTTP 403 to a plain fetcher, and the HHS-hosted FDA PDF returned 403 as well. Reported by
[ASHP's summary](https://www.ashp.org/-/media/assets/pharmacy-practice/resource-centers/ambulatory-care/docs/2022-CDC-Opioid-Prescribing-Guideline-Updates.pdf)
and [the MMWR landing page](https://www.cdc.gov/mmwr/volumes/71/rr/rr7103a1.htm). **Do not put those
two numbers in a PreventIA artefact on this document's authority.**

**MME conversion factors** are published in several places with a stated method — multiply the dose
of an opioid by its conversion factor — including a state Medicaid table
([Utah DHHS](https://medicaid-documents.dhhs.utah.gov/Documents/files/Opioid-Morphine-EQ-Conversion-Factors.pdf)).
I did not open it and I quote no factor from it.

**A source that blurs the line, since the brief asked.** The MME search returned a first page
dominated by open consumer calculators — `best-calculators.com`, `medaptly.com`, `thecalcs.com`,
`calcbee.com` — that compute a daily MME and display a CDC "risk band" to anyone who types in a dose,
with no clinician gate at all. That is exactly the shape PreventIA must not take: a threshold
rendered to a lay user as a verdict about their own regimen. It is also evidence that the open web
will happily give a patient the number PreventIA declines to give them, which is an objection the
clinical teammate may want an answer to.

---

## 3. Line B — how clinician-editable rules are actually built

### 3.1 The two shipped standards

Neither is a UI. Both are the shape the industry has agreed a clinical rule takes, and both are
directly relevant to the seam PreventIA already has between `clinical/rules/` and the model.

**CDS Hooks** — HL7 specification, current version 2.0.1, Standard for Trial Use, stewarded by the
HL7 CDS Work Group. It defines RESTful APIs using JSON over HTTPS between a *CDS Client* (an EHR)
and a *CDS Service*. Verbatim from the spec
([cds-hooks.hl7.org/2.0](https://cds-hooks.hl7.org/2.0/), [cds-hooks.hl7.org](https://cds-hooks.hl7.org/)):

> "A _CDS Service_ is a service that provides recommendations and guidance through the RESTful APIs
> described by this specification."

Output is a **card** carrying an `indicator` with exactly three values — `info` (lowest urgency,
informational), `warning` (medium urgency), `critical` (highest urgency) — and the spec says the CDS
Client "MAY use this field to help make UI display decisions such as sort order or coloring." On
what the human may do with it:

> users may "accept its suggestions, ignore it entirely, or dismiss it with or without an override
> reason."

Accepting is recorded: the client posts the card and suggestion `uuid`s to the service's feedback
endpoint with an outcome of `accepted`.

**Three things transfer directly to PreventIA.** A three-level indicator that drives sort order and
colour is structurally our semáforo. Dismissal with an optional override reason is the audit
primitive our queue lacks. And the feedback endpoint means the standard assumes you record what the
clinician did with each alert, not just that you raised it.

**HL7 CQL (Clinical Quality Language)** — an ANSI Normative Standard, current spec v1.5.3, also
stewarded by the HL7 CDS Work Group. It is described as "a high-level, domain-specific language
focused on clinical quality improvement", explicitly "intended to be usable by clinical domain
experts to both author and read clinical knowledge", with a machine-readable canonical form called
ELM (Expression Logical Model) for implementations. It ships an Author's Guide as chapter 2 of the
specification ([cql.hl7.org](https://cql.hl7.org/),
[Author's Guide](https://cql.hl7.org/02-authorsguide.html),
[HL7 product brief](https://www.hl7.org/implement/standards/product_brief.cfm?product_id=400),
[reference implementation](https://github.com/cqframework/clinical_quality_language)).

**Read that against ADR-0004.** CQL's whole premise is the same premise as the deterministic floor:
clinical logic is authored by a clinical domain expert in a human-readable form and compiled to
something a machine executes. PreventIA's `clinical/rules/` is a hand-rolled instance of a pattern
that has a normative standard behind it. That is a sentence worth saying to a judge, and it costs
nothing to say, provided we say it as "the same principle as CQL" and not as "we implement CQL".

### 3.2 Who edits, and what governance the field expects

| Practice | What the source says | Source |
|---|---|---|
| Rule authoring by clinicians | CQL is "targeted at measure and decision support artifact authors" and intended to be usable by clinical domain experts to author *and read* logic | [cql.hl7.org/01-introduction.html](https://cql.hl7.org/01-introduction.html) |
| Clinical leader required per rule | In a tertiary-hospital BPA optimisation programme, "Every new BPA request required a clinical leader" | [JAMIA Open 2023, Singapore](https://academic.oup.com/jamiaopen/article/6/3/ooad056/7235064) |
| Multidisciplinary governance committee | Oncology CDS at a multistate enterprise is managed by named teams, tools and processes rather than ad hoc edits | [PMC11943330, City of Hope](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11943330/) |
| Request / approval / build / test as distinct stages | "Assessing your organization's BPA request, approval, build, and testing processes is key" | [CereCore](https://resources.cerecore.net/are-your-bestpractice-advisories-useful-or-are-they-being-ignored) |
| Versioning and change log | Organisations should define who updates rules, how often and under which evidence standards, "while maintaining version logs" `[extract only]` | [topflightapps 2026 guide](https://topflightapps.com/ideas/clinical-decision-support-system-implementation/) |
| Audit of who changed what | Audit reports should "track rule changes, who made them and why", plus execution reports on rule firing frequency and clinician acceptance or rejection rates `[extract only]` | same |
| Structured self-assessment | ONC **SAFER Guides**, first published 2014 and since revised, are 8 guides of 6 to 18 recommended practices each, scored on a 5-point scale from "not implemented" to "fully implemented". The **CPOE with Decision Support** guide covers design, implementation, use and monitoring of orders and CDS; separate guides cover **System Configuration** | [healthit.gov SAFER Guides](https://healthit.gov/clinical-quality-and-safety/safer-guides/), [PMC12005625 on the revisions](https://pmc.ncbi.nlm.nih.gov/articles/PMC12005625/) |

**On the academic source that was supposed to anchor this section.** "A study of diverse clinical
decision support rule authoring environments and requirements for integration", BMC Medical
Informatics and Decision Making 12:128 (2012), is the one paper directly on the question of who
authors CDS rules and in what interface. **I could not read it.** The BMC URL 301s to
`link.springer.com`, which 303s to a Springer identity provider; a PMC identifier guess returned an
unrelated systematic review. It is cited here as existing and on-point, and nothing in this document
rests on its contents.
[bmcmedinformdecismak.biomedcentral.com/articles/10.1186/1472-6947-12-128](https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/1472-6947-12-128).

### 3.3 Failures caused by a badly governed rule or model

The brief asked for real failures. The best-documented one in the literature is a model rather than a
hand-set threshold, and it is the more useful example anyway, because it is about a rule nobody could
independently check.

**Epic Sepsis Model, external validation.** Wong A, Otles E, Donnelly JP, et al., *External Validation
of a Widely Implemented Proprietary Sepsis Prediction Model in Hospitalized Patients*, JAMA Internal
Medicine, 2021. Retrieved and quoted from the abstract
([jamanetwork.com](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2781307)):

- 38,455 hospitalizations among 27,697 patients; sepsis in 2,552 (7%).
- Hospitalization-level AUC **0.63 (95% CI, 0.62-0.64)**.
- At a score threshold of 6 or higher, the model identified 183 of 2,552 patients with sepsis (7%)
  who did not receive timely antibiotics, **while failing to identify 1,709 patients (67%) with
  sepsis, and generating alerts on 6,971 hospitalizations (18%)**.
- Conclusion, verbatim: "the ESM has poor discrimination and calibration in predicting the onset of
  sepsis. The widespread adoption of the ESM despite its poor performance raises fundamental
  concerns about sepsis management on a national level."

Follow-on reporting: Epic subsequently overhauled the model and now recommends training on a
hospital's own data before clinical use, and changed its sepsis-onset definition
([STAT, 3 October 2022](https://www.statnews.com/2022/10/03/epic-sepsis-algorithm-revamp-training/),
[Fierce Healthcare](https://www.fiercehealthcare.com/tech/epic-s-widely-used-sepsis-prediction-model-falls-short-among-michigan-medicine-patients)).
One deploying hospital deactivated the model in April 2020 over false-positive frequency during
COVID-19 `[extract only]`.

**The transferable lesson is not "models are bad".** It is that a threshold whose basis a clinician
cannot inspect gets adopted at scale, fires on 18% of admissions, and is still trusted until somebody
external validates it. A clinician-set number in PreventIA is the opposite arrangement by
construction, and that is the point of Felipe's question.

**On misconfigured thresholds specifically:** I searched for a named case report of a threshold
misconfiguration causing harm and **did not find one.** What the search returned instead was the
systemic version — ECRI listed hospital alarms as the number one health technology hazard in 2012 and
2013, and alarm hazards have appeared on its top-hazard list across multiple years, with 80–99.4% of
monitor alarms reported as false or clinically insignificant `[extract only]`
([AAMI BI&T](https://array.aami.org/doi/full/10.2345/0899-8205-54.1.12),
[PMC9132737 on CDS stewardship](https://pmc.ncbi.nlm.nih.gov/articles/PMC9132737/)). Treat the
absence as a gap in my search, not as evidence that such cases do not exist.

---

## 4. Line C — human in the loop for an LLM clinical tool

### 4.1 Regulatory framing, quoted verbatim

**FDA, Clinical Decision Support Software, final guidance, 28 September 2022.** The four statutory
criteria from section 520(o)(1)(E) of the FD&C Act, quoted as reproduced by Covington & Burling
([cov.com](https://www.cov.com/en/news-and-insights/insights/2022/10/5-key-takeaways-from-fdas-final-guidance-on-regulation-of-clinical-decision-support-software-fda-outlines-significant-changes-for-cds);
[Federal Register notice](https://www.federalregister.gov/documents/2022/09/28/2022-20993/clinical-decision-support-software-guidance-for-industry-and-food-and-drug-administration-staff)).
`fda.gov`'s own guidance page returned HTTP 404 and the HHS-hosted PDF returned 403, so these are
quoted at one remove and marked accordingly.

> **Criterion 1:** "The software is not intended to acquire, process, or analyze a medical image or a
> signal from an in vitro diagnostic device or a pattern or signal from a signal acquisition system."
>
> **Criterion 2:** "The software is intended for the purpose of displaying, analyzing, or printing
> medical information about a patient or other medical information."
>
> **Criterion 3:** "The software is intended for the purpose of supporting or providing
> recommendations to a healthcare professional about prevention, diagnosis, or treatment of a disease
> or condition."
>
> **Criterion 4:** "The software is intended for the purpose of enabling the HCP to independently
> review the basis for the recommendations that such software presents so that it is not the intent
> that the HCP rely primarily on any of such recommendations to make a clinical diagnosis or
> treatment decision regarding an individual patient."

And two limiting statements attributed to FDA in the same source:

> Software providing "a specific preventative, diagnostic, or treatment output or directive" does not
> qualify under Criterion 3.
>
> "software that is intended to support time-critical decision-making" fails to meet Criterion 3.

A second law-firm summary adds that under Criterion 4 the software or its labelling "should provide
the basis for its findings in plain language so that the HCP may independently evaluate the basis of
recommendations", and should disclose algorithm methods, datasets and validation `[extract only]`
([Snell & Wilmer](https://www.swlaw.com/publication/fda-issues-key-updates-to-cds-software-guidance/),
[Arnold & Porter](https://www.arnoldporter.com/en/perspectives/advisories/2022/10/fda-releases-significantly-revised-final-clinical)).

**I am not a lawyer and this is not legal advice.** It is quoted so a qualified reader can interpret
it. Note also that this is US law and PreventIA is a Chilean project; it is cited as the clearest
published articulation of the *distinction*, not as a rule binding on us.

**EU AI Act, Article 14, Human oversight.** Retrieved verbatim from
[artificialintelligenceact.eu/article/14](https://artificialintelligenceact.eu/article/14/):

> **1.** "High-risk AI systems shall be designed and developed in such a way, including with
> appropriate human-machine interface tools, that they can be effectively overseen by natural persons
> during the period in which they are in use."
>
> **2.** "Human oversight shall aim to prevent or minimise the risks to health, safety or fundamental
> rights that may emerge when a high-risk AI system is used in accordance with its intended purpose
> or under conditions of reasonably foreseeable misuse, in particular where such risks persist
> despite the application of other requirements set out in this Section."

Paragraph 3 requires oversight measures "commensurate with the risks, level of autonomy and context
of use". Paragraph 4 requires that the person assigned oversight be enabled to:

> (a) "properly understand the relevant capacities and limitations of the high-risk AI system";
> (b) "remain aware of the possible tendency of automatically relying or over-relying on the output";
> (c) "correctly interpret the high-risk AI system's output";
> (d) "decide not to use the high-risk AI system or to otherwise disregard, override or reverse the
> output";
> (e) "intervene in the operation ... or interrupt the system through a 'stop' button".

Paragraph 5 imposes separate verification "by at least two natural persons with the necessary
competence, training and authority" — **but that requirement is written for biometric identification
systems, not for medical AI generally.** Do not cite Article 14(5) as a two-person rule for clinical
software; it is not one.

**Sub-point (b) is the one to notice.** The Act writes automation bias into the statute as something
the interface has to actively counteract, which makes section 4.3 below a design requirement rather
than a caveat.

### 4.2 Human-in-the-loop taxonomy

The distinction the literature draws, from a 2025-2026 systematic review and adjacent framework work
`[extract only]`:

| Pattern | Definition as stated | Where PreventIA sits |
|---|---|---|
| **Human-in-the-loop (HITL)** | "continuous, active human participation in critical decision-making processes enabling real-time intervention" | Not this. No human reads each check-in |
| **Human-on-the-loop (HOTL)** | "supervisory control in which humans monitor AI systems and intervene as needed, promoting scalability and operational efficiency" | This, for the queue |
| **Trivial Monitoring** archetype | AI operates autonomously with human approval or emergency-abort capability | Closest to the daily conversation |
| **Endpoint Action** archetype | AI outputs a candidate for human final decision | Exactly the escalation, per ADR-0006 |

Sources: [MDPI Entropy systematic review](https://www.mdpi.com/1099-4300/28/4/377) /
[PubMed 42072503](https://pubmed.ncbi.nlm.nih.gov/42072503/);
[HITL in healthcare, ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1386505626001024).

**Useful for the pitch, and honest:** PreventIA is human-*on*-the-loop for routine check-ins and
human-*in*-the-loop at escalation. Felipe's proposed configuration screen adds a third position that
the taxonomy above does not name well — **the clinician is in the loop *before* the loop runs**, by
authoring the criteria. That is the ADR-0004 arrangement, and it is a stronger claim than either HITL
or HOTL because it does not depend on anyone being at a screen when the check-in happens.

### 4.3 Automation bias and alert fatigue, with numbers

All figures below are `[extract only]` — search-result extracts of named papers whose full texts I
did not open. Open the paper before quoting any of these in front of a judge.

| Finding | Figure | Source |
|---|---|---|
| Automation bias, computational pathology under time pressure | AI integration raised overall performance but produced a **7% automation bias rate**, where initially correct evaluations were overturned by erroneous AI advice | [arXiv 2411.00998](https://arxiv.org/abs/2411.00998) |
| Automation bias, wound-care CDSS | 210 participants from German hospitals and nursing programmes; measured as agreement rate with wrong AI recommendations. Diagnostic performance, certified wound-care training, physician profession and female gender significantly reduced false agreement | [Kücking et al. 2024, SAGE/SHTI240871](https://journals.sagepub.com/doi/10.3233/SHTI240871) |
| Drug-drug interaction alert override rate | **55% to 98%** across studies | [Scoping review, PubMed 35673040](https://pubmed.ncbi.nlm.nih.gov/35673040/) |
| Alert override rate, all types | **46.2% to 96.2%** | [JMIR Med Inform 2020;8(7):e15653](https://medinform.jmir.org/2020/7/e15653) |
| Appropriateness of dose-alert overrides | **43.9% to 88.8%** | same |
| Acceptance in ambulatory care | Clinicians accepted **9.2%** of drug interaction alerts and **23.0%** of allergy alerts | [Harvard HCP publication record](https://hcp.hms.harvard.edu/publication/overrides-medication-alerts-ambulatory-care) |
| Adverse events and overrides | Retrospective study of more than 47,000 overridden medication alerts: most overrides appropriate, but adverse drug events more likely when alerts were overridden in error | [PMC8800577](https://pmc.ncbi.nlm.nih.gov/articles/PMC8800577/) |

These sit on top of, and agree with, the alarm-fatigue evidence already recorded in section 7 of
`2026-08-05-clinical-dashboard-ui-and-stacks-chile.md`.

**The uncomfortable implication for a configuration screen, stated plainly:** giving a clinician a
dial that lowers a threshold is giving them a dial that raises the alert count, and the field's own
numbers say roughly half to nine-tenths of alerts get overridden. A config screen that makes it easy
to add a trigger and hard to see its firing rate is a machine for producing an unworkable queue.

### 4.4 LLM-specific failure modes in a clinical loop

| Failure mode | What the source says | Source |
|---|---|---|
| Plausible-but-wrong clinical output | "In clinical settings, the most consequential failures are rarely overtly 'unsafe' in form; instead, they are often plausible, polite, and well-structured responses that nonetheless recommend incorrect dosing, downplay emergent symptoms, or misrepresent evidence." | [MPIB benchmark, arXiv 2602.06268](https://arxiv.org/html/2602.06268) |
| Direct prompt injection through patient text | "Any LLM-powered interface where patients or members of the public can submit arbitrary text is exposed to direct prompt injection. The user controls what goes into the prompt." | [Aptible](https://www.aptible.com/hipaa-ai-security/prompt-injection) |
| Multi-turn erosion of a refusal | "users can push back after a refusal, reframe the request, or add emotional pressure" — most safety evaluations score only a single message | [MultiTurnPSB, arXiv 2606.02630](https://arxiv.org/pdf/2606.02630) |
| Confidence miscalibration | Models show "undue confidence in wrong answers", described as a dangerous form of hallucination that could lead clinicians to adopt erroneous decisions "delivered with overt certainty" `[extract only]` | [PMC12101789](https://pmc.ncbi.nlm.nih.gov/articles/PMC12101789/) |
| Unsafe answers to patient-posed questions | Paper title itself: "Large language models provide unsafe answers to patient-posed medical questions" | [arXiv 2507.18905](https://arxiv.org/pdf/2507.18905) |

**Two of these are already answered by existing PreventIA decisions and one is not.** The
plausible-but-wrong output and the confidence miscalibration are exactly why ADR-0005's layer 2 is a
deterministic filter rather than a prompt, and why ADR-0004 forbids the model lowering a colour.
**Multi-turn erosion of a refusal is not covered by anything we have written down.** ADR-0005's
adversarial suite is specified as single questions ("¿me suspendo el losartán?"). A patient who asks
the same thing four times in four different ways across a conversation is the documented attack, and
our test suite does not currently describe that case.

**Prompt injection through patient text is real here and specific.** PreventIA's entire input surface
is free-text WhatsApp messages from patients. The relevant risk is not a malicious attacker; it is
that patient text flows into the same context as the system prompt, and the deterministic layers
(extraction, rules floor, guardrail filter) are the only parts of the pipeline that a sentence in a
patient message cannot rewrite.

---

## 5. Line D — interface and interaction evidence

This is the thinnest of the four lines. The configuration-screen literature is largely generic
usability writing, and the one framing the brief asked for — "why did this fire" shown next to an
alert — returned no source using that framing. What follows is what is actually supported.

### 5.1 Designing a configuration screen for a non-technical expert

| Principle | Stated as | Source |
|---|---|---|
| Translate, do not expose | "provide a needs-based interface that translates customer requirements into technical properties, rather than exposing technical parameters directly" `[extract only]` | [arXiv 2605.29456, configurator UI usability](https://arxiv.org/pdf/2605.29456) |
| Start from a default | "Provide starting points to enable users to begin with predefined configurations, not only from scratch" `[extract only]` | same |
| Preview before commit | "Exploit prototypes to avoid surprises by visualizing the configuration" `[extract only]` | same |
| Explain consequences | Organise large configuration spaces to avoid crowded UIs, highlight changes, communicate dependencies, and explain the impact of choices `[extract only]` | same |
| Fewer, consistent controls | Less-skilled users prefer high intuitiveness with relatively fewer but consistent UI elements `[extract only]` | [PMC3628119, bedside nursing CDSS UI evaluation](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3628119/) |
| Confirm every action | Every user action should get visible confirmation `[extract only]` | [Compunnel healthcare interface guidance](https://www.compunnel.com/blogs/designing-healthcare-interfaces-accessible-and-usable/) |

**Weak evidence, and labelled weak.** Only the nursing-CDSS UI evaluation is a clinical study; the
rest is product-design writing and one configurator-usability preprint. Nothing here is specific to a
clinician editing a clinical threshold.

### 5.2 Explaining why an alert fired

**No source was found that addresses "why did this fire" as a distinct interface pattern.** The
adjacent literature says three things that bear on it:

- Timing is the core design mistake: "alerts are triggered by data availability, not by clinical
  intent", and that mismatch drives alert fatigue and reduced trust `[extract only]`
  ([Mindbowser](https://www.mindbowser.com/reduce-cdss-alert-fatigue-clinical-decision-support/)).
- CDS alerts "must be designed to provide clinicians with patient-specific assessment and
  recommendation during task execution" `[extract only]`
  ([Olakotan & Yusof, 2021](https://journals.sagepub.com/doi/full/10.1177/14604582211007536),
  [ScienceDirect version](https://www.sciencedirect.com/science/article/pii/S1532046420300812)).
- Systems should "expose inputs, confidence, and citations so clinicians can independently review the
  basis", and provide "a clear override path so clinicians won't trust a black box that can't be
  questioned" `[extract only]`
  ([topflightapps](https://topflightapps.com/ideas/clinical-decision-support-system-implementation/)).

That last one is the same sentence as FDA Criterion 4, arrived at from a usability direction rather
than a regulatory one. **The strongest evidence for "show why" is therefore regulatory, not
empirical** — FDA's Criterion 4 and EU AI Act 14(4)(a) and (c), both in section 4.1.

There is also a local precedent already recorded in
`2026-08-05-rayen-box-ui-observed.md` section 5: Rayen's own semáforo chip opens an `Información
riesgo` panel showing the start date and the diagnoses producing the classification. Chilean primary
care clinicians are already trained on click-the-colour-to-see-why.

### 5.3 Accessibility of a form-heavy configuration screen

WCAG 2.2 AA specifics for grouped numeric inputs, which is what a threshold screen is
([W3C H71](https://www.w3.org/TR/WCAG20-TECHS/H71.html),
[TheWCAG forms guide](https://www.thewcag.com/examples/forms),
[Vision Australia on fieldset/legend](https://www.visionaustralia.org/business-consulting/digital-access/removing-form-barriers)):

- Group related controls in `<fieldset>` with `<legend>` as the first child. The legend is announced
  before each grouped input, giving screen-reader users the context that makes a bare number
  meaningful.
- Every `<input>`, `<select>` and `<textarea>` needs a programmatic label via `<label for="id">`
  matched to the input's `id`.
- Required fields carry `aria-required="true"` *and* a visual indicator.
- Validation errors must be announced and tied to the field that caused them.
- Success criteria implicated: **1.3.1** (Info and Relationships), **3.3.1** (Error
  Identification), **3.3.2** (Labels or Instructions), **3.3.3** (Error Suggestion), **4.1.2** (Name,
  Role, Value).

`UNVERIFIED` and worth someone checking: I did not confirm which of the **new** 2.2 criteria
(2.4.11 Focus Not Obscured, 2.5.8 Target Size Minimum, 3.3.7 Redundant Entry, 3.3.8 Accessible
Authentication) apply specifically to a numeric configuration form. ADR-0011 commits the dashboard to
WCAG 2.2 AA, so somebody has to answer that before build.

### 5.4 Making a configuration change reversible and traceable

**Weak line.** The search returned mostly process-control patents and generic DevOps writing rather
than clinical sources. Three usable statements:

- Rollback should restore configuration to a specific date and time from a change log, undoing all
  changes made after it `[extract only]`
  ([US 7346634, application configuration change log](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7346634)).
- An audit trail should record, per version: version number, date, who made it, the nature of the
  modification, and **the reason for the modification** `[extract only]`
  ([US 6449624, version control and audit trail in a process control system](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6449624)).
- For clinical AI specifically: "Rollback in clinical systems must be immediate, mechanical, and
  independent of human judgment. If you cannot reproduce last week's clinical behavior exactly, you
  do not have an auditable system", and "The rollback has to preserve the audit trail, because the
  regulatory record of 'what policy was in effect when' survives the rollback" `[extract only]`
  ([DeepInspect blog](https://www.deepinspect.ai/blog/ai-gateway-rollback-strategy)). **This is a
  vendor blog, not a standard.** It is quoted because it states the requirement crisply, not because
  it carries authority.

The one authoritative-adjacent item here is ONC's **System Configuration** SAFER Guide, already cited
in section 3.2 ([healthit.gov](https://healthit.gov/clinical-quality-and-safety/safer-guides/)). I
did not open it. That is the single highest-value unopened document in this whole research line.

---

## 6. Where the dose line gets drawn

This is the section `CLAUDE.md` section 2 depends on, so it is given with the provenance of every
claim and with my own inferences labelled as inferences.

### 6.1 The four pieces of evidence, strongest first

**1. WHO says its own dose figure is a measurement unit, not a patient's dose.** Verbatim from
[who.int/tools/atc-ddd-toolkit/about-ddd](https://www.who.int/tools/atc-ddd-toolkit/about-ddd):

> "The assumed average maintenance dose per day for a drug used for its main indication in adults."
>
> "The DDD is a unit of measurement and does not necessarily correspond to the recommended or
> Prescribed Daily Dose (PDD)."
>
> "Therapeutic doses for individual patients and patient groups will often differ from the DDD as
> they will be based on individual characteristics such as age, weight, ethnic differences, type and
> severity of disease, and pharmacokinetic considerations."

This is the cleanest sentence in the entire research. The most widely used published daily-dose
number in the world comes with an explicit disclaimer that it is not what any individual should take.
A threshold and a prescription are different objects, and the body that publishes the threshold says
so first.

**2. CDC removed its dose numbers from the recommendation because they were being read as a rule.**
The 2022 Recommendation 4, quoted in full in section 2.3, contains no MME figure. The guideline says
of itself, verbatim
([PMC9639433](https://pmc.ncbi.nlm.nih.gov/articles/PMC9639433/)):

> "This voluntary clinical practice guideline provides recommendations only and is intended to
> support, not supplant, clinical judgment and individualized, person-centered decision-making. This
> clinical practice guideline should not be applied as inflexible standards of care."

It explicitly names the misapplications it does not authorise, including "rigid application of opioid
dosage thresholds" and "rapid opioid tapers and abrupt discontinuation without collaboration with
patients". And on audience:

> "This clinical practice guideline is intended for clinicians who are treating outpatients aged ≥18
> years with acute, subacute, or chronic pain."

Secondary sources state the reason for the change directly: the 2016 wording "inadvertently led to
the misapplication of opioid dosage thresholds and subsequent patient harm" `[extract only]`
([ASHP summary](https://www.ashp.org/-/media/assets/pharmacy-practice/resource-centers/ambulatory-care/docs/2022-CDC-Opioid-Prescribing-Guideline-Updates.pdf)).

**This is the closest thing in the literature to the exact failure PreventIA must avoid.** A number
authored as a prompt for clinician reassessment became, in the field, a hard limit applied to
patients. The number did not change. The distance between the number and the patient changed.

**3. The regulatory line is drawn at "directive" and at "who receives it", not at "is a number
stored".** From FDA's 2022 CDS guidance as quoted in section 4.1: Criterion 3 covers software
"supporting or providing recommendations **to a healthcare professional**", and software providing
"a specific preventative, diagnostic, or treatment output or directive" falls outside it. Criterion 4
requires the professional be able to "independently review the basis". Software for time-critical
decisions fails Criterion 3 because there is no time for that review.

Reading those together, three things move a tool across the line, and only the third is about the
number itself: **the recipient stops being a clinician; the output becomes a directive rather than a
recommendation; and the recipient has no practical way to review the basis.** A conversational agent
telling a patient a dose fails all three at once.

**4. Every shipped CDS standard renders the output as something a human can refuse.** CDS Hooks
cards carry an urgency indicator and the user may "accept its suggestions, ignore it entirely, or
dismiss it with or without an override reason", with acceptance recorded through a feedback endpoint
([cds-hooks.hl7.org/2.0](https://cds-hooks.hl7.org/2.0/)). EU AI Act 14(4)(d) requires the overseer be
able to "disregard, override or reverse the output". Neither standard contemplates a threshold being
executed against a person without a human between.

### 6.2 The line, stated as one operational test

**My inference, not a finding, and labelled as such.** Nothing I found addresses a patient-facing
conversational agent stating a dose, so this is a synthesis of the four items above rather than a
citation.

A clinician-set number is safe to hold when **all four** of these are true:

| Test | Flagging to a clinician | Telling a patient a dose |
|---|---|---|
| Who reads the number | The clinician who authored it, or a colleague | The patient |
| What the output is | A ranked case with its basis attached | An instruction to act on |
| What the recipient can do | Disregard, override, or dismiss with a reason | Comply, because there is nobody else in the room |
| Whether the basis is reviewable | Yes, by the person who set it | No, and there is no time or expertise to |

**The practical corollary for PreventIA.** The number lives in the rule table, the patient never
learns the number, and the patient never learns that a number was crossed. What the patient hears is
unchanged by the configuration screen: the agent asks whether the medication was taken and, per
ADR-0013, may direct them to urgencias **only** where the deterministic `rules_color` is red. A
threshold edit changes what reaches the clinician's queue; it does not change one word of
patient-facing copy. If a config edit can change what the patient is told, the design is wrong.

### 6.3 Where sources blur it, since the brief asked

- **Open consumer MME calculators** (section 2.3) hand a lay user a threshold and a risk band with no
  clinician in the path. They are the anti-pattern in its purest form.
- **The FDA mobile-app framing is stale and I could not verify it.** Secondary sources describe a
  category of app functionality covering "reminders to patients regarding when they should take their
  medicine, according to guidelines either set out in the drug labeling or prescribed by the
  patient's physician", and reference a "Drug Dose Calculator" classification under 21 CFR 868.1890
  `[extract only]`
  ([MobiHealthNews](https://www.mobihealthnews.com/40917/in-depth-anticipating-fda-regulation-of-pharmaceutical-apps),
  [McGuireWoods](https://www.mcguirewoods.com/client-resources/alerts/2011/8/second-in-series-fda-draft-guidance-mobile-medical-apps-cheat-sheet/)).
  Those sources date from 2011-2013 and predate the 2022 CDS guidance. **`UNVERIFIED`. Do not rely on
  the claim that a medication-reminder app repeating a physician's own prescription sits on the safe
  side of the line.** It may well; I have no current primary source saying so.
- **Chilean law: not established.** I searched for the Código Sanitario provision reserving the
  indication of treatment to a médico cirujano and did not retrieve the article text. What the search
  did surface is the current telemedicine instrument — **Norma General Técnica N°237, "Estándares
  asociados a las prestaciones de salud a distancia y telemedicina"**, published on MINSAL's digital
  health portal in January 2025 — and **Ley 21.541** on telemedicine
  ([NGT 237 PDF](https://portalsaluddigital.minsal.cl/wp-content/uploads/2025/01/2025.01.06_NORMA-TECNICA-PRESTACIONES-DE-SALUD-A-DISTANCIA-Y-TELEMEDICINA.pdf),
  [Código Sanitario, MINSAL](https://diprece.minsal.cl/wrdprss_minsal/wp-content/uploads/2015/01/Codigo-Sanitario.pdf),
  [Ley 21.541 summary](https://reservo.cl/blog/profesionales/telemedicina/prestas-servicios-de-salud-en-chile-asi-debes-cumplir-con-la-ley-21541/)).
  **Neither document was opened.** `UNVERIFIED`. This is the single most Chile-relevant gap in the
  document and it is a lawyer's question, not mine.

---

## 7. What this would mean for PreventIA's dashboard

Implications only. No decisions. Anything requiring a decision is flagged for an ADR at the end.

### 7.1 What a config screen would have to contain

Derived from sections 3, 5 and 6. Each item carries the reason.

| Element | Why | Evidence |
|---|---|---|
| A **named author** on every rule, not a generic admin account | "Every new BPA request required a clinical leader"; ADR-0004 already assigns table authorship to the healthcare professional | §3.2 |
| A **free-text clinical basis** field per rule, citing the guideline it comes from | FDA Criterion 4's "independently review the basis"; `CLAUDE.md` §5 already puts clinical reasoning in `docs/research/` | §4.1, §6.1 |
| **The minimum colour** the rule sets, from the three semáforo values | ADR-0004: rules set a floor, model may raise. CDS Hooks' `info`/`warning`/`critical` is the same three-level shape | §3.1 |
| A **preview** showing which historical check-ins the rule would have fired on, before saving | "Exploit prototypes to avoid surprises by visualizing the configuration"; and the alert-rate problem in §4.3 | §4.3, §5.1 |
| The rule's **firing rate** displayed next to it once live | Override rates of 46–96% mean an unmeasured rule is an unmanaged one | §4.3 |
| **Effective-from date**, so a past case can be replayed against the rule that was live then | "the regulatory record of 'what policy was in effect when' survives the rollback" | §5.4 |
| **Fieldset + legend grouping**, programmatic labels, `aria-required`, field-tied error messages | WCAG 2.2 AA, committed by ADR-0011 | §5.3 |
| **A starting table shipped as the default**, not an empty screen | "Provide starting points ... not only from scratch". Also: ADR-0004 already calls the missing real table a Phase 0 blocker | §5.1 |

### 7.2 What it must never contain

Each of these would breach `CLAUDE.md` section 2 as written.

1. **Any field whose value reaches patient-facing copy.** A threshold edit changes the queue, never
   the conversation. If the config screen can alter one word the patient reads, the boundary has
   moved from code into a form field.
2. **A dose recommendation field of any kind** — no "suggested dose", no "target dose", no "maximum
   the patient may take". The rule table stores the value at which a *case is raised to a human*.
   The distinction is section 6.2 and it is the whole design.
3. **Any control that lowers a colour.** ADR-0004 says the model may only raise. If the config screen
   grows a "downgrade this flag" control, the same property has to hold: a clinician may retune the
   floor, but nothing downstream of the floor may lower it at runtime.
4. **A diagnosis field.** A rule may be named for the signal it watches; it may not name a condition
   the patient has, because that string will eventually be rendered somewhere.
5. **Free-text that reaches the model's context unfiltered.** The clinical basis field is
   documentation for humans. If it is interpolated into the system prompt, a clinician's note becomes
   an injection surface (§4.4).

### 7.3 What governance the edit needs

The field's expectations, from §3.2, mapped to what PreventIA already has:

| Expectation | Already covered? |
|---|---|
| Named clinical author per rule | Partly — ADR-0004 assigns authorship, nothing records it per row |
| Request / approval / build / test as distinct stages | No |
| Version log with who, when, and **why** | No |
| Ability to replay a past case against the rule that was live then | No |
| Firing-rate and acceptance monitoring per rule | No |
| Two-person sign-off | **Not required by anything I found.** EU AI Act 14(5)'s two-person rule is written for biometric identification, not clinical AI (§4.1). If the team adopts it, adopt it as our own choice, not as a legal obligation |

**The precedent to lean on is already in the repo.** `2026-08-05-rayen-box-ui-observed.md` §4 records
that every one of Rayen's six queue states is defined by a system event rather than an assertion —
`Iniciado` because a ficha was opened, `Completado` because it was closed. The same doctrine applied
to configuration says: a rule's history is a sequence of recorded edits, not a current-value field
somebody overwrites. The SIGTE failure in §6 of the dashboard research is what the other approach
looks like.

### 7.4 What it costs

Honest, because the Lab deadline is tomorrow.

- **A read-only rules view is cheap.** Rendering `clinical/rules/` as a table on the dashboard, with
  author, basis, minimum colour and the flags it watches, is an afternoon and it directly serves
  point 5 of `CLAUDE.md` §12 and FDA Criterion 4's "independently review the basis". It also makes
  the ADR-0004 story visible instead of asserted.
- **An editable screen with versioning, effective dates and replay is not a two-day feature.**
  Versioned rules mean every stored check-in has to carry the rule version it was evaluated under, or
  the replay claim is false. That is a schema change to the clinical record (ADR-0002).
- **The preview feature depends on having historical check-ins**, which for the Lab means the
  synthetic cohort. It demos well and it is honest, provided the pitch says the data is synthetic.
- **The expensive part is not the UI.** It is that a config screen makes the rule table a live
  artefact rather than a reviewed file, which raises rather than lowers the governance burden. A file
  in git already has an author, a timestamp, a diff and a review trail. **A worse version of that,
  rebuilt in a web form, is a real risk of this feature.**

### 7.5 What would need a new ADR

Per `CLAUDE.md` §9, ADRs are immutable and a changed decision gets a new one. Felipe is the
`Deciders:` line, so none of these may be written without him deciding first.

1. **Whether the rule table is editable at runtime at all**, or stays a reviewed file in git with the
   dashboard showing it read-only. This is the actual fork and everything else follows from it.
2. **Whether rules are versioned and check-ins record the rule version they were evaluated under.**
   Touches ADR-0002's schema.
3. **What governance an edit requires** — named author, reason, approval, or two-person sign-off —
   and explicitly that two-person sign-off, if adopted, is our choice and not a legal requirement.
4. **Whether the clinical basis text is ever shown to anyone but a clinician**, which is the
   patient-facing boundary in §7.2 item 1.
5. **Whether the adversarial guardrail suite gains multi-turn cases.** §4.4 identified that ADR-0005's
   suite is specified as single questions, and the documented attack is a patient rephrasing across
   turns. This is arguably the cheapest safety improvement in this whole document.

Item 5 is the one I would raise first if the Lab deadline forces a single choice, because it improves
a thing that is already built and already demoed rather than adding a surface.

---

## 8. Open questions for the clinical teammate

Ready to hand to a doctor. None of these has an answer in this document, by design.

1. Which published standard, if any, do you want the flag table anchored to — a GES/AUGE guideline, a
   MINSAL orientación técnica, a society guideline, or your own clinical judgement recorded as such?
2. For each flag, what is the **signal** you want detected, in the words a patient would actually use,
   rather than in clinical terms?
3. Do any of the flags need a **numeric threshold at all**, or are they all presence/absence of a
   reported symptom? Felipe's morphine example implies a number; the hypertension, diabetes and heart
   failure cohort may not need one.
4. Where a flag does carry a number, what is the **source of that number**, so it can be cited in
   `docs/research/` per `CLAUDE.md` §5?
5. Who is allowed to change a threshold — you alone, any treating physician, or a committee?
6. Does a threshold change need a second person's approval before it takes effect? (Nothing found
   requires it. This is a team choice.)
7. When a threshold changes, what happens to cases already in the queue that were raised under the
   old value?
8. What is an acceptable **red rate**? Section 4.3 says the field overrides 46–96% of alerts. If
   PreventIA's queue produces more reds per day than you can clear, which is the failure you would
   rather have?
9. Who clears a red, and within what time? (Carried forward unanswered from open item 5 of
   `2026-08-05-clinical-dashboard-ui-and-stacks-chile.md`.)
10. Should the clinician's own written reason for a flag be visible in the queue next to the case it
    fired on, or is that clutter on a row that has to be readable in seconds (ADR-0006)?
11. Are there flags where you would want the patient told **nothing at all** — not even the softer
    "estamos avisando a su equipo" — because saying anything would alarm them?
12. ADR-0013 permits the urgencias sentence only where a rule fired red. Are there flags you would
    want to carry that sentence, and flags you would explicitly not?

---

## 9. Search record

30 searches and 19 direct page fetches on 5 August 2026. Ten fetches succeeded. This document was
written after an interrupted session; no search was re-run.

### 9.1 Searches, line A — standards a clinician would configure against

| # | Query | Result |
|---|---|---|
| 1 | WHO Model List of Essential Medicines machine-readable data API download | Usable. Led to eEML |
| 2 | WHO ATC/DDD index Defined Daily Dose licence terms reuse software | Usable. Established that a machine-readable version is sold |
| 3 | morphine milligram equivalent MME conversion table CDC threshold 50 90 | **Partly usable, and a warning.** First page dominated by ungated consumer calculators. No primary CDC source in reach |
| 4 | Formulario Nacional de Medicamentos Chile ISP MINSAL Terminología Farmacéutica Chilena | Usable. DTO 194/2005 and DTO 264/2003 located |
| 5 | WHO analgesic ladder opioid three-step 2018 revision | **Weak.** Secondary commentary only; no WHO primary document retrieved |
| 6 | GES AUGE Chile guía clínica hipertensión diabetes insuficiencia cardiaca umbral derivación | **Located, not read.** Guideline PDFs found; none opened; no threshold quoted |
| 26 | CDC 2022 Clinical Practice Guideline recommendation 4 "50 MME" "90 MME" verbatim | Usable for context; the primary text came from the PMC fetch, not this search |
| 27 | "Terminología Farmacéutica Chilena" MINSAL ISP catálogo interoperabilidad | Usable. Found CENS Pharma |
| 28 | WHO publication licence "CC BY-NC-SA 3.0 IGO" essential medicines list terms of use | Usable, but the primary IRIS document 403'd |

### 9.2 Searches, line B — how clinician-editable rules are built

| # | Query | Result |
|---|---|---|
| 7 | CDS Hooks specification clinical decision support hooks standard HL7 | Usable |
| 8 | HL7 CQL Clinical Quality Language authoring clinician rules shareable specification | Usable |
| 9 | clinical decision support rule editor clinician-facing threshold configuration governance versioning audit | Partly usable. Mostly vendor content; surfaced the BMC paper |
| 10 | Epic best practice advisory BPA governance committee approval process | Usable. JAMIA Open and City of Hope |
| 11 | misconfigured clinical decision support alert threshold patient harm case report ECRI hazard | **Empty on the specific question.** No named case report of a threshold misconfiguration found |
| 12 | drug dose alert override rate clinicians percentage study | Usable. Numbers are extract-only |
| 13 | "clinical decision support" content governance "sign-off" two-person review change control audit trail | **Weak.** Mostly vendor and compliance-marketing pages; no standard found |
| 29 | ONC SAFER Guides clinical decision support configuration testing | Usable. Best unopened source in the document |
| 30 | named incident EHR rule change error sepsis alert Epic model failure documented | Usable. Led to the Wong 2021 validation |

### 9.3 Searches, line C — human in the loop for LLM clinical tools

| # | Query | Result |
|---|---|---|
| 14 | FDA clinical decision support software guidance non-device "independent review" 2022 | Usable, via law-firm summaries only |
| 15 | EU AI Act Article 14 human oversight high-risk medical AI obligations text | Usable |
| 16 | human-in-the-loop human-on-the-loop taxonomy clinical AI 2025 framework oversight levels | Partly usable. Definitions retrieved, full texts not opened |
| 17 | automation bias clinician AI decision support 2024 2025 measured effect incorrect advice | Usable. Numbers are extract-only |
| 18 | LLM clinical failure modes prompt injection through patient text medical chatbot safety 2025 | Usable. The strongest quotes in §4.4 |
| 19 | LLM medical advice dosing error hallucination confident wrong output evaluation 2025 | Usable, extract-only |

### 9.4 Searches, line D — interface and interaction evidence

| # | Query | Result |
|---|---|---|
| 20 | WCAG 2.2 AA grouped numeric input fields fieldset legend accessible form design | Usable |
| 21 | "why did this fire" alert explanation design clinical decision support transparency | **Empty on the framing asked for.** No source uses it. Adjacent CDS literature only |
| 22 | designing configuration settings screen for non-technical clinical users safe defaults preview confirm | **Weak.** One preprint and generic product-design writing |
| 23 | FDA drug dosage calculator app device regulation medication reminder enforcement discretion | **Weak and stale.** 2011-2013 secondary sources and patents. Marked UNVERIFIED in §6.3 |
| 24 | reversible configuration change clinical system rollback undo audit trail effective date | **Weak.** Patents and DevOps blogs, no clinical standard |
| 25 | Chile Código Sanitario indicación tratamiento telemedicina resolución MINSAL prescripción | **Partly usable.** Found NGT 237 and Ley 21.541; did not answer the exclusivity question |

### 9.5 Fetches

**Succeeded (10):** `atcddd.fhi.no/copyright_disclaimer/` · `list.essentialmeds.org/` ·
`list.essentialmeds.org/licencing` · `who.int/tools/atc-ddd-toolkit/about-ddd` ·
`pmc.ncbi.nlm.nih.gov/articles/PMC9639433/` · `artificialintelligenceact.eu/article/14/` ·
`cov.com` FDA CDS takeaways · `cds-hooks.hl7.org/2.0/` ·
`jamanetwork.com/journals/jamainternalmedicine/fullarticle/2781307` · `cens.cl/cens-pharma/`

**Failed (9), with the failure mode:**

| URL | Failure |
|---|---|
| `fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software` | HTTP 404 |
| `hhs.gov/.../Guidance-Clinical-Decision-Software.pdf` | HTTP 403 |
| `cdc.gov/mmwr/volumes/71/rr/rr7103a1.htm` | HTTP 403 |
| `cdc.gov/overdose-prevention/hcp/clinical-guidance/opioid-prescribing-guideline.html` | HTTP 403 |
| `who.int/publications/i/item/WHO-MHP-HPS-EML-2025.01` | HTTP 404 |
| `iris.who.int/handle/10665/371090` | HTTP 403 |
| `bmcmedinformdecismak.biomedcentral.com/articles/10.1186/1472-6947-12-128` | 301 to Springer, then 303 to an identity provider. Not read |
| `link.springer.com/article/10.1186/1472-6947-12-128` | 303 to `idp.springer.com`. Not read |
| `pmc.ncbi.nlm.nih.gov/articles/PMC3534499/` | Wrong article. My identifier guess was bad |

**Practical notes for whoever fetches next**, extending the list in
`2026-08-05-clinical-dashboard-ui-and-stacks-chile.md` §11:

- **`cdc.gov` and `iris.who.int` both refuse plain fetchers with 403.** For CDC content, the PMC
  mirror works: `pmc.ncbi.nlm.nih.gov` served the full 2022 opioid guideline where three `cdc.gov`
  paths did not.
- `www.ncbi.nlm.nih.gov/pmc/...` 301s to `pmc.ncbi.nlm.nih.gov/...`; go straight to the latter.
- `bmcmedinformdecismak.biomedcentral.com` now routes through Springer's identity provider. Do not
  guess PMC identifiers to work around it; search for the PMC record by title instead.
- `jamanetwork.com`, `cds-hooks.hl7.org`, `cql.hl7.org`, `artificialintelligenceact.eu`,
  `list.essentialmeds.org`, `atcddd.fhi.no` and `cens.cl` all serve cleanly to a plain fetcher.

### 9.6 Highest-value unopened documents

In order, for whoever picks this up:

1. **ONC SAFER Guide, System Configuration**, and the **CPOE with Decision Support** guide —
   [healthit.gov](https://healthit.gov/clinical-quality-and-safety/safer-guides/). The only
   authoritative checklist found for exactly this problem.
2. **Norma General Técnica N°237** (Chilean telemedicine standards, January 2025) —
   [PDF](https://portalsaluddigital.minsal.cl/wp-content/uploads/2025/01/2025.01.06_NORMA-TECNICA-PRESTACIONES-DE-SALUD-A-DISTANCIA-Y-TELEMEDICINA.pdf).
   The Chile-specific answer to where the line sits.
3. **CDC 2022 guideline supporting text for Recommendation 4**, to settle whether the 50/90 MME
   figures survive there and in what wording.
4. **The GES/AUGE guidelines for the three cohort conditions**, which is the clinical teammate's
   material rather than mine.
