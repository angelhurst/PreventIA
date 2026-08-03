# Caja La Araucana and the Lab dataset

Workstream 6 of the Phase 0 research brief.

Consulted 3 August 2026. Author: Felipe Carvajal Brown. Archived copies of every source that could be
downloaded are in `docs/research/sources/`.

## What this document is

ADR-0007 already treats the Lab dataset as untrustworthy in shape, and the brief follows that: the
useful output is **a list of schema assumptions at risk**, not a prediction of what the data will
contain. Section 6 is that list and is the deliverable. Everything before it exists to justify it.

Where I am reasoning rather than reporting, it says so. Section 7 collects every guess in one place
so nobody has to hunt for them.

## Headline

Three findings, in order of how much they should change what we do.

**A caja de compensación is not a health insurer and not a healthcare provider of record.** It is a
social-security entity that administers family allowances, sickness benefit, social credit and
welfare benefits, supervised by the Superintendencia de Seguridad Social. Nothing in its statutory
function requires it to hold a diagnosis, a prescription or a control history. Any expectation that
its dataset contains clinical longitudinal data is an expectation about a **commercial** service it
chose to offer, not about the institution.

**La Araucana already runs a chronic-patient accompaniment service for pensioners.** Its published
benefits list includes "Acompañamiento paciente crónico", plan ilimitado, segment Pensionado,
delivered through free telemedicine. PreventIA is therefore adjacent to something the host institution
already does. That is not a problem, but it is a conversation to have with the organisers before the
pitch rather than a thing to discover during it.

**The word "aggregated" is the one that decides the schema.** If the dataset is genuinely aggregated,
there is no patient-level row in it at all, and `data/caja_adapter.py` cannot populate a `patients`
table with people. It can populate distributions. That is a different piece of software from the one
ADR-0007's wording implies, and it should be built as the smaller one.

---

## 1. What a caja de compensación actually is

Cajas de Compensación de Asignación Familiar are **private non-profit corporations constituted as
entidades de previsión social**, governed by **Ley N° 18.833** of 1989 and supervised by the
**Superintendencia de Seguridad Social (SUSESO)**. There are four in Chile: Los Andes, La Araucana,
Los Héroes and 18 de Septiembre.

SUSESO describes what they administer in two families. **Prestaciones legales**, verbatim:

> pagar a las personas trabajadoras los siguientes beneficios: asignación familiar, subsidios por
> incapacidad común y subsidio por incapacidad laboral temporal, a través las licencias médicas

plus prenatal and postnatal leave, leave for serious illness of a child under one, and unemployment
benefit. And **prestaciones de bienestar social**, verbatim:

> préstamos en dinero hasta por un plazo máximo de 60 meses o 5 años, definidos como créditos
> sociales, y prestaciones adicionales de bienestar social, tales como bonos por fallecimiento,
> matrimonio, nacimiento o escolaridad, becas de estudio, convenios médicos y el uso de centros
> vacacionales o recreacionales

Read that list against what PreventIA's schema needs and the mismatch is immediate. **A CCAF is a
payer of benefits and a lender, with a welfare catalogue attached.** Health appears in it twice: as
*subsidio por incapacidad laboral* administered through medical leave certificates, and as *convenios
médicos*, meaning negotiated discounts.

**The one place a CCAF plausibly holds diagnosis-coded health data is medical leave — and medical
leave is a benefit for workers, not for pensioners.** PreventIA's population is pensioners. The
single most clinically informative dataset a caja holds is about the population we are not targeting.
That asymmetry is the most useful structural thing in this document and I have not seen it stated
anywhere else.

## 2. La Araucana in numbers, from the regulator

From SUSESO's own published statistics, most recent month available (May 2026), archived as
`suseso-2026-afiliados-ccaf.xlsx`:

| CCAF | Affiliated companies | Workers | **Pensioners** | Total affiliates |
|---|---|---|---|---|
| De Los Andes | 54.751 | 3.883.811 | 413.825 | 4.297.636 |
| **La Araucana** | **8.501** | **1.135.591** | **233.332** | **1.368.923** |
| Los Héroes | 9.222 | 484.570 | 636.252 | 1.120.822 |
| 18 de Septiembre | 7.544 | 262.354 | 178.800 | 441.154 |
| **Total** | 80.018 | 5.766.326 | 1.462.209 | 7.228.535 |

La Araucana is the **second largest CCAF by total affiliates** and the **third by pensioners**, behind
Los Héroes and Los Andes. Its pensioner base is roughly **233 thousand people**.

Two cautions on using that number.

**"Pensionado" is not "older adult."** Chilean pensions include invalidity and survivor pensions, so
the pensioner register is not an age register. **Unverified** what the age distribution inside it is.
What would verify it: SUSESO's affiliate statistics broken down by age, if published, or a direct
question to La Araucana.

**233 thousand is not the addressable population either.** Against the 2,3 million people under
control in the PSCV (workstream 3), La Araucana's whole pensioner base is about a tenth, and only some
of those have the three target conditions. Useful for a "pilot inside a defined population" argument,
not for a national-scale claim.

## 3. What La Araucana offers in health

Sourced from a La Araucana benefits presentation hosted on a **Servicio de Salud Metropolitano Sur**
domain, `ssms.gob.cl`, which is a government domain and therefore preferable to the company's own
site. `laaraucana.cl` itself returned a Radware CAPTCHA block to every fetch attempt on 3 August 2026
and could not be read.

Programme **"Tu Salud Más Cerca"**, comprising preventivos, telemedicina, exámenes and medicamentos.
Free telemedicine for the affiliate plus three people of their choosing:

| Service | Frequency | Segment |
|---|---|---|
| Medicina General 24x7 | Ilimitado | Trabajador y Pensionado |
| Psicología, Nutrición, Urología, Ginecología | 1 consulta semanal | Trabajador y Pensionado |
| Pediatría | 1 consulta semanal | Trabajador |
| **Geriatría** | 1 consulta semanal | **Pensionado** |
| **Acompañamiento paciente crónico** | **Plan ilimitado** | **Pensionado** |
| Órdenes de exámenes preventivos | 1 consulta semanal | Trabajador y Pensionado |

Plus dental up to 72% discount, pharmacy through a commercial partner with home delivery, laboratory
sample-taking with Imed coverage and discounts at Bionet centres, opticians, mental health and
orthopaedics. Physical presence: **69 sucursales in 55 cities** and **58 mobile agencies**.

Three things follow.

**The health offering is a benefits catalogue, not a clinical service.** Discounts, negotiated
providers, telemedicine consultations. The clinical record of an affiliate's care stays with FONASA
or their isapre and with whoever treated them.

**Except for two lines.** "Geriatría" and "Acompañamiento paciente crónico" are both pensioner-only,
and the second is unlimited. Whatever data those services generate is the **only** part of La
Araucana's operation that plausibly produces something resembling longitudinal chronic-patient
follow-up. If the Lab dataset contains anything clinically useful to PreventIA, this is where it comes
from.

**And that means PreventIA is adjacent to an existing service of the host institution.** Not
necessarily a conflict — an accompaniment service delivered as scheduled telemedicine consultations is
a different thing from a daily conversational check-in with a deterministic risk floor and an
escalation queue. But a judge who works at La Araucana will know the service exists, and the pitch is
much stronger if it names the service and says how PreventIA relates to it than if it appears not to
know.

**Open question for the organisers, and the highest-value one in this workstream:** what is
"Acompañamiento paciente crónico", how many pensioners use it, and does the Lab dataset come from it?

## 4. Institutional history

Stated plainly and neutrally because it bears on the Phase 5 adoption pathway and someone will raise
it.

From SUSESO's own fiscalización page for La Araucana: SUSESO **declared intervention of La Araucana on
2 November 2015 and terminated it on 25 October 2016**. Sanctions issued on **25 May 2016** totalled
roughly 17.000 UF, including fines against the corporation for failing to report material events
regarding credit-rating downgrades and for internal control deficiencies in the 2014 financial
statements, and individual fines of 150 to 3.000 UF against directors and audit committee members for
"falta de diligencia en el ejercicio de su cargo" in relation to the approval of those statements. All
were recorded as ejecutoriada. The most recent consolidated financial statements listed on the same
page are from September 2025.

Ten years is a long time and the entity has been reporting to its regulator continuously since. The
reason to know this is not to raise it — it is so that nobody on our team is surprised by it, and so
that any claim we make about the institution's stability as a deployment partner is made with the
record in view rather than around it.

## 5. What the Lab actually says about the data

The repository's own account (`CLAUDE.md` section 4, ADR-0007) is that the Lab supplies anonymized,
aggregated health data from Caja La Araucana through MCP servers, available when the Lab starts. Here
is what the Lab's public site says, quoted as read on 3 August 2026.

On the data rule, verbatim:

> Solo datos anonimizados/agregados, fuentes públicas curadas o prospección sintética. Nunca PII de
> pacientes ni re-identificación.

**That is a direct external confirmation of the clinical non-negotiable in `CLAUDE.md` section 2 and
of ADR-0007.** Worth quoting in the pitch: our data rule is not our invention, it is the Lab's rule,
and we built to it from before day one.

On La Araucana's role, verbatim:

> Aporta el problema-país, los datos de salud anonimizados, el venue y la red institucional.

On the curated public sources, the site names **Minsal, Fonasa, DEIS and BCN** — which are the sources
workstreams 2 and 3 have already worked through directly. If the "curated datasets" are these, we are
not waiting on anything.

**And one ambiguity that matters, which I could not resolve.** The site lists "Datasets curados" among
the benefits under a heading reading **"Acceso post-Lab"**, while simultaneously describing La
Araucana as contributing anonymized health data and listing "datos públicos disponibles" per challenge
line. Read one way, the curated datasets arrive during the two days. Read the other, they are part of
the post-Lab adoption pathway for winning teams, and nothing from La Araucana is in our hands on 5
August at all.

**Unverified, and it is the single question whose answer most changes Phase 0.** What would verify it:
one message to the organisers. If the second reading is right, `data/caja_adapter.py` cannot be
exercised during the Lab, ADR-0007's premise that the data is "available when the Lab starts" is
wrong, and the adapter becomes a documented intention rather than a working component — which is
still worth building, but should be described honestly in the pitch as untested against real data.

**Ask before day one.** It costs a message and it changes what Phase 3 has to deliver.

## 6. Schema assumptions at risk

The deliverable. Against the SQLite tables named in `CLAUDE.md` section 3 and ROADMAP Phase 2:
patients, medications, daily check-ins, risk events, escalations.

Risk is my judgement of how likely the assumption is to fail against real Caja data, not a
probability.

| Schema element | Assumption it encodes | Risk | Why |
|---|---|---|---|
| `patients` as **rows about people** | The dataset has one record per person | **Very high** | "Agregado" is in the Lab's own data rule. Aggregated data has no person-level row by construction |
| `patients.age` or date of birth | Age is available per person | **Very high** | Age band at best; a date of birth is PII and the Lab forbids it |
| `patients.sex`, `comuna` | Available | Medium | Standard aggregation dimensions; plausible, still band-level |
| `patients` diagnoses (HTA / DM2 / IC) | The provider knows which conditions a person has | **High** | A CCAF has no statutory reason to hold a pensioner's diagnoses. Only the telemedicine and chronic-accompaniment services plausibly generate them (3.) |
| `medications` — drug, dose, schedule | A per-patient medication list exists | **Very high** | Not a CCAF record at all. The nearest adjacent thing is a pharmacy purchase history held by a commercial partner, which is neither the caja's data nor the same as a prescription |
| `check_ins` — a per-day contact history | Something like it exists to seed from | **Very high** | Nothing in a CCAF's function produces this. The only candidate is "Acompañamiento paciente crónico", and its data is unknown to us |
| `risk_events`, `escalations` | — | None | Entirely generated by PreventIA. No external dependency |
| A phone number to message | A contactable patient can be seeded from the data | **Certain to fail** | Aggregated and anonymized data contains no contact detail, by definition and by the Lab's rule. **The demo can never run against a real Caja patient**, and it was never going to |
| Longitudinal adherence over weeks | The dataset supports a per-person time series | **Very high** | Requires both person-level rows and repeated observation. Aggregation removes the first |
| Frailty state, Barthel, cognitive status | Available to key the rule table on (workstream 2, P4) | **Very high** | These are clinical assessment instruments administered in a health service, not benefit records |

**The consequence for `data/caja_adapter.py`.** ADR-0007 describes an adapter that "reads the Lab's
anonymized dataset over MCP into the same schema". Against genuinely aggregated data, that is not
possible: there is nothing to put in the `patients` table. What *is* possible, and is arguably more
useful, is an adapter that reads the dataset and **calibrates the synthetic cohort** — age
distribution, sex ratio, comuna distribution, condition prevalence, multimorbidity rate — so the
synthetic patients resemble La Araucana's real population instead of our imagination.

That is a smaller, more honest and more defensible piece of software, and the pitch line writes
itself: the cohort is synthetic, its **shape** comes from the institution's own anonymized
aggregates, and we can say exactly which is which. **Proposed as a change to how the adapter is
scoped; it is not written into any ADR and it is Felipe's call.** ADR-0007 is Accepted and immutable,
so if this is adopted it needs a new ADR that supersedes it.

## 7. Everything in this document that is a guess

Collected here so it is impossible to miss.

1. **What the Lab dataset contains.** Nobody outside the organisers knows. Every row of the section 6
   table is reasoning from what the institution's statutory function and published services imply,
   not from having seen the data.
2. **That "agregado" means no person-level rows.** It is what the word means, and the Lab's own rule
   uses it. But the Lab may use "anonimizado/agregado" loosely to mean de-identified, which is a
   different thing and would change section 6 substantially.
3. **The age distribution of La Araucana's 233 thousand pensioners.** Unknown.
4. **Whether the chronic-accompaniment service generates the dataset.** Purely an inference from it
   being the only pensioner-facing longitudinal service in the published catalogue.
5. **When the data arrives.** See 5. Genuinely ambiguous on the public site.
6. **Whether any of this survives contact with what the organisers actually hand over on 5 August.**

## 8. A legal point that is not legal advice

**I am not a lawyer and none of this is legal advice.** It is recorded because the word "anonymized"
is used throughout this repository and it has a specific meaning in Chilean law from December 2026.

**Ley N° 21.719**, promulgated 25 November 2024 and published 13 December 2024, replaces the data
protection regime in Ley 19.628. Two definitions matter, quoted verbatim from the official text on
BCN Ley Chile.

Health data is sensitive personal data:

> g) Datos personales sensibles: tendrán esta condición aquellos datos personales que se refieren a
> las características físicas o morales de las personas o a hechos o circunstancias de su vida
> privada o intimidad, que revelen el origen étnico o racial, la afiliación política, sindical o
> gremial, la situación socioeconómica, las convicciones ideológicas o filosóficas, las creencias
> religiosas, **los datos relativos a la salud**, al perfil biológico humano, los datos biométricos, y
> la información relativa a la vida sexual, a la orientación sexual y a la identidad de género de una
> persona natural.

And anonymisation is defined as irreversible, and distinguished from pseudonymisation:

> k) Anonimización: procedimiento irreversible en virtud del cual un dato personal no puede vincularse
> o asociarse a una persona determinada, ni permitir su identificación, por haberse destruido o
> eliminado el nexo con la información que vincula, asocia o identifica a esa persona. Un dato
> anonimizado deja de ser un dato personal.
>
> l) Seudonimización: tratamiento de datos personales que se efectúa de manera tal que ya no puedan
> atribuirse a un titular sin utilizar información adicional, siempre que dicha información adicional
> figure por separado [...]

On entry into force, the first transitional article, verbatim:

> Las modificaciones a las leyes N° 19.628 [...] entrarán en vigencia el día primero del mes
> vigésimo cuarto posterior a la publicación de esta ley en el Diario Oficial.

Published 13 December 2024, so the twenty-fourth month after publication is December 2026 and the law
takes effect on **1 December 2026** — four months after the Lab, and before any pilot in an AI Health
Sandbox could plausibly run. That derived date is arithmetic on the quoted text, not a quote.

Three things worth carrying:

- **"Anonymized" is a strong word in Chile from December 2026.** Data that can be re-identified is
  pseudonymised and remains personal data with all obligations attached. If the Lab's dataset is
  de-identified rather than irreversibly anonymised, the correct word for it is "seudonimizado", and
  a judge from the health administration may well know the difference.
- **Health data is explicitly sensitive**, which is the strictest category in the new regime.
- **Nothing in this changes what we do at the Lab**, because the repository already holds no real
  patient data of any kind. It changes what Phase 5 would have to answer, and it is a good answer to
  have ready: the architecture was built to a rule stricter than the law before the law arrived.

## 9. A finding that belongs to workstream 2

Not this workstream's question, but it answers its open question 1 and should not be lost.

Workstream 2 could not establish where PRD section 1's "2,4 millones" came from and offered three
hypotheses. **It came from the Lab's own framing.** The Lab site states, verbatim:

> 2,4 millones esperan una consulta, un procedimiento o una cirugía. Algunos llevan más de dos años

and press coverage of the Lab's launch repeats it without attributing it to a source.

The phrasing is the tell: "una consulta, un procedimiento **o una cirugía**" is the sum of the two
waiting lists. At 31 March 2026 that is 2.088.245 people waiting for a specialty consultation plus
398.496 waiting for surgery, which is 2.486.741 — and the Glosa 06 report warns explicitly that these
must not be added, because a person on both lists is counted twice. **The construction is an
inference of mine from the wording; the two component figures are verified.**

This matters exactly as workstream 2 said it would. The figure in PRD section 1 is the Lab's figure.
Correcting it on stage is contradicting the host, which may still be the right call — a panel of
government and health-management judges will know the Glosa 06 numbers — but it is now a deliberate
choice rather than an accident. Carried into `docs/research/README.md`.

## 10. Open questions

1. **When does the Caja dataset arrive, and to whom?** (5.) One message to the organisers. **Highest
   value, and it should be sent before Phase 0 closes.**
2. **What is "Acompañamiento paciente crónico" and does the dataset come from it?** (3.) Same message.
3. What is the age distribution of La Araucana's 233.332 pensioners? (2.)
4. Does the Lab mean "aggregated" strictly, or loosely for de-identified? (7.2.) Decides section 6.
5. Should the adapter calibrate the synthetic cohort rather than populate it? (6.) A decision for
   Felipe, and a new ADR if adopted.
6. Should the pitch use the Lab's 2,4 million figure or the Glosa 06 figures? (9.) A decision for
   Felipe.

## Sources

All consulted 3 August 2026.

1. Superintendencia de Seguridad Social (SUSESO). *Número de trabajadoras(es), pensionadas(os) y
   empresas afiliadas a C.C.A.F.*, statistics for 2026.
   https://www.suseso.gob.cl/608/w3-article-19331.html, spreadsheet at
   https://www.suseso.gob.cl/608/articles-19331_archivo_01.xlsx
   Archived as `suseso-2026-afiliados-ccaf.xlsx`. Figures in section 2 are the May 2026 column, the
   most recent month with data.

2. Superintendencia de Seguridad Social (SUSESO). *¿Qué hacen las Cajas de Compensación?*
   https://www.suseso.gob.cl/606/w3-propertyvalue-34003.html
   Web page, not archived. Source of both verbatim quotations in section 1.

3. Superintendencia de Seguridad Social (SUSESO). *Fiscalización — La Araucana*.
   https://www.suseso.gob.cl/609/w3-propertyvalue-10338.html
   Web page, not archived. Source of the intervention dates and sanctions in section 4.

4. Caja de Compensación La Araucana. *Beneficios*, corporate benefits presentation, undated, hosted by
   the Servicio de Salud Metropolitano Sur.
   https://ssms.gob.cl/wp-content/uploads/2025/02/BENEFICIOS-CAJA-LA-ARAUCANA.pdf
   Archived as `laaraucana-beneficios-via-ssms.pdf`. Used for the whole of section 3.
   Note: `laaraucana.cl` returns a Radware CAPTCHA challenge to `curl` and to WebFetch alike, so the
   company's own pages could not be read. This government-hosted copy is used instead and its
   publication date is not stated in the document.

5. Bendita IA and Anthropic. *Claude Impact Lab · Longevidad — Santiago 2026*.
   https://longevidad.benditaia.cl/es
   Web page, not archived. Source of every quotation in sections 5 and 9. **The "Acceso post-Lab"
   ambiguity described in section 5 is my reading of the page's structure and may be wrong.**

6. Diario Sustentable. *Chile tiene 2,4 millones de personas en lista de espera y una población que
   envejece más rápido que su sistema de salud. Ahora quiere resolverlo con IA*. 24 July 2026.
   https://www.diariosustentable.com/2026/07/chile-tiene-24-millones-de-personas-en-lista-de-espera-y-una-poblacion-que-envejece-mas-rapido-que-su-sistema-de-salud-ahora-quiere-resolverlo-con-ia/
   Press coverage of the Lab launch. Cited in section 9 only as evidence that the 2,4 million figure
   circulates unattributed. Not a source for any figure.

7. Biblioteca del Congreso Nacional de Chile. *Ley N° 21.719, que regula la protección y el
   tratamiento de los datos personales y crea la Agencia de Protección de Datos Personales*.
   Promulgated 25 November 2024, published 13 December 2024.
   https://www.bcn.cl/leychile/navegar?idNorma=1209272
   Full official text retrieved as XML from
   https://www.bcn.cl/leychile/consulta/obtxml?opt=7&idNorma=1209272 — the HTML page returns a
   JavaScript shell to fetchers. All quotations in section 8 are from that official text.

8. Ley N° 18.833, ley orgánica de las Cajas de Compensación de Asignación Familiar, 1989. Referred to
   for the legal frame in section 1; the governing law number and the nature of a CCAF are taken from
   SUSESO (sources 2 and its Compendio index), **not from reading the law itself**.

## Verification status summary

| Claim | Status |
|---|---|
| A CCAF is a private non-profit entidad de previsión social under Ley 18.833, supervised by SUSESO | Verified from source 2 |
| The two benefit families and their contents | Verified, quoted from source 2 |
| Ley 18.833 text itself | **Not read.** Number and remit taken from SUSESO |
| La Araucana affiliate figures, May 2026 | Verified from source 1, the regulator's own spreadsheet |
| La Araucana is second by total affiliates and third by pensioners | Verified by inspecting source 1 |
| Age distribution of La Araucana's pensioners | **Unverified — not published** |
| "Tu Salud Más Cerca" service list including Geriatría and Acompañamiento paciente crónico | Verified from source 4 |
| What "Acompañamiento paciente crónico" consists of | **Unverified.** Only the catalogue line is known |
| SUSESO intervention 2 Nov 2015 to 25 Oct 2016 and the 25 May 2016 sanctions | Verified from source 3 |
| Lab data rule: "Solo datos anonimizados/agregados [...] Nunca PII de pacientes ni re-identificación" | Verified, quoted from source 5 |
| La Araucana "aporta [...] los datos de salud anonimizados, el venue y la red institucional" | Verified, quoted from source 5 |
| Curated public sources are Minsal, Fonasa, DEIS, BCN | Verified from source 5 |
| Whether the Caja dataset is available during the Lab or post-Lab to winners | **Unverified and genuinely ambiguous.** See 5 |
| Every row of the section 6 schema-risk table | **Reasoning, not observation.** See 7 |
| Ley 21.719 dates, sensitive-data definition, anonymisation definition, transitional article | Verified, quoted from the official text, source 7 |
| Entry into force on 1 December 2026 | **Derived** by arithmetic from the quoted transitional article |
| Health data is a dato personal sensible | Verified, quoted |
| The Lab is the origin of the 2,4 million figure | Verified, quoted from source 5 |
| 2,4 million is the sum of the CNE and IQ people-counts | **My inference from the wording.** Components verified in workstream 2 |
