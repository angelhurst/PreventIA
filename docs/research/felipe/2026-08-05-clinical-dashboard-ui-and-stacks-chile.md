# Web dashboards in Chilean clinics and hospitals: UI types, configurations and stacks

Consulted 5 August 2026. Author: Felipe Carvajal Brown. Method: 34 web searches and direct page
fetches, listed in section 11. No archived PDFs were added to `sources/` for this workstream; every
citation below is a live URL and is marked where the page is a moving target.

Scope, as requested: what user interfaces, what configurations and what technology stacks are
actually in use in Chilean clinical and hospital web systems. This is a survey of the field
PreventIA's `dashboard/` has to land in. It proposes no decision — section 10 lists what it forces
somebody to decide.

---

## Headline: three findings, and only one of them is about frameworks

**1. There is no Chilean healthcare design system.** There is a *government* one, Kit Digital, and it
is not built for clinical work. Its own site now flags the front-end framework as pending update and
points designers at a Figma library instead. Anyone who tells a judge "we follow the government
design system" is describing a Bootstrap 4.5 SCSS kit for public information sites, not a triage
screen.

**2. The binding constraints are legal and interoperability constraints, not UI constraints.**
Decreto 1/2015 (accessibility, W3C), Ley 21.180 (digital transformation), Ley 21.668 (record
interoperability, FHIR R4), Ley 21.719 (data protection, in force 1 December 2026, requiring an
impact assessment for health data), ISO 27001 at MINSAL. Every one of these will be asked about by a
government or management judge. None of them says anything about React versus anything else.

**3. What clinicians actually use is a browser-delivered, dense, Spanish-language, desktop-width form
screen inside an existing system they did not choose.** Rayen in primary care, TrakCare or Florence
in hospitals, plus a set of separate ministerial web platforms they must also keep open. The relevant
design fact for PreventIA is not what our dashboard looks like on its own. It is that it will be the
*n*th tab, and that nothing about a nurse's day makes room for an *n*+1th.

---

## 1. What is actually deployed, by level of care

### 1.1 Primary care: Rayen

Rayen Salud states presence in **more than 76% of primary care establishments in the country**
([rayensalud.com](https://www.rayensalud.com/)). Its distributor Saydex states the Rayen and Florence
systems together are used in **over 400 establishments**
([EMB Gerencia](https://www.gerencia.cl/proveedores/saydex-innovacion-en-registro-clinico-electronico-en-chile/)).
For a CESFAM pilot such as the one in `docs/diagrams/2026-08-03-flujo-piloto-quinta-normal.excalidraw`,
Rayen is the incumbent by default.

What the product page confirms
([Rayen RCE](https://www.rayensalud.com/servicios/sistemas-y-servicios/rayen-registro-clinico-electro)):

| Element | Finding |
|---|---|
| Modules | Admission, appointment management, morbidity, family file with four layers, interactive odontogram, pharmacy and food warehouse, vaccination integrated with the Registro Nacional de Inmunizaciones |
| Analytics | A named BI layer, **IRIS**, for reporting and analytics — a separate surface from the clinical screen |
| Adjacent products | **Rayen ELOÍSA** for low-to-medium complexity hospitals; a self-service **tótem** product |
| Stated capability | Telehealth, remote professional access, and **risk stratification**, "with security certification" ([Rayen APS overview](https://www.rayensalud.com/)) |
| Certifications | ISO 9001:2015 and ISO/IEC 27001:2022 for the company's management system |
| Deployment model | **Not stated.** The page says "sistema de información colaborativo" and nothing about cloud, on-premise, or browser requirements |

**Risk stratification already exists in Rayen and is already governed as an algorithm.** Chile's
public algorithm register lists a "cálculo de factor de riesgo en ficha clínica electrónica Rayen"
project ([algoritmospublicos.cl](https://www.algoritmospublicos.cl/proyecto-algoritmo-factor-riesgo-ficha-clinica-electronica-rayen)).
This matters more than it looks: it means the semáforo is not a novel category to a Chilean health
IT reviewer, and it means there is an existing precedent for how such a thing gets registered.

**Unverified, and I could not close it:** Rayen's browser requirements, screen resolution
assumptions, and whether the clinical screen is a single-page application or server-rendered pages.
The public manuals are the route — `Manual de BOX RAYEN`, version 15.0.0.1, March 2020, hosted by the
Servicio de Salud Tarapacá — and the host refused the connection on 5 August 2026
(`ECONNREFUSED`). Retrieving one manual with a browser user agent would settle the layout and
navigation question in ten minutes. It is the single cheapest open item in this document.

### 1.2 Hospitals: TrakCare, Florence, and a live migration to watch

**InterSystems TrakCare** is in active rollout in the public network. Hospital San Pablo de Coquimbo
began implementing it in 2025 under the local name **"Alma"**, with a **one-year** implementation
covering urgencia, hospitalización, pabellón and atención ambulatoria, starting with the emergency
module including adult, paediatric and gineco-obstetric areas plus laboratory, blood bank, imaging
and pharmacy ([Hospital San Pablo](https://www.hospitalcoquimbo.cl/el-cambio-comienza-aqui-conoce-el-nuevo-sistema-his/),
[training announcement](https://www.hospitalcoquimbo.cl/hospital-de-coquimbo-inicia-las-capacitaciones-de-alma-su-nuevo-sistema-de-ficha-clinica-digital/)).

The published rollout sequence per module is worth copying verbatim, because it is what a Chilean
hospital IT department will expect any new system to go through: **implementación, recolección de
datos, levantamiento de procesos, configuración y parametrización, validación, capacitación,
lanzamiento, acompañamiento.**

Read that against the Lab's judging criterion. A prototype whose adoption story is "it plugs in" is
answering a question no Chilean hospital asks. The question they ask is which of those eight stages
it survives.

**Florence** splits into clinical and financial-management components, with the clinical side capturing
structured information from every hospital clinical process into a single electronic record per
patient ([Neo Puerto Montt](http://www.neopuertomontt.com/InformaticaMedica/Florence/Florence.htm)).

**Cirrus (Ecaresoft)** markets a cloud HIS + ERP + RCM bundle into Chile
([getcirrus.com](https://www.getcirrus.com/comienza/software-para-hospitales-chile)); noted as a
present vendor, with no deployment in the public network verified here.

**In the private sector**, Clínica Alemana runs an in-house record called **Núcleo**, with a web
front (**Núcleo Web**) into which it has integrated an LLM agent, alongside a patient portal, "Mi
Alemana" ([Clínica Alemana](https://www.clinicaalemana.cl/)). Their stack is not published. The
relevant fact for us is directional and it is a good one: **a major Chilean private clinic has
already put a conversational model inside its clinical record web UI.** PreventIA is not proposing an
unprecedented category to a clinical judge.

### 1.3 The national layer: SIDRA

SIDRA is the ministerial strategy that frames all of the above. It is defined as an **ecosystem of
applications, national in scope, flexible and adaptable** to different care networks, integrating
three initiatives — hospital management systems, primary care systems, and referral /
counter-referral — around a **common data repository**
([MINSAL SIDRA](https://www.minsal.cl/SIDRA/), [SSMC](https://ssmc.gob.cl/quienes-somos/mision-vision-funciones/proyecto-sidra/)).

The phrase to take from SIDRA is "ecosystem of applications", not "one system". It is why a clinician
has several tabs open, and it is the doctrine under which a new application is added rather than
rejected.

---

## 2. UI types actually in the field

Seven distinct interface types were identified. They are not variants of one another — they have
different users, different dwell times and different failure modes.

| # | UI type | Where it lives | Defining characteristic |
|---|---|---|---|
| 1 | **Clinical record / box screen** | Rayen, TrakCare, Florence, Núcleo | Dense form entry during a consultation, with the patient in the room. Dwell time is the whole consultation |
| 2 | **Prioritisation / queue panel** | SIGTE — "paneles de visualización" through which priorising physicians access ordered waiting lists ([BCN](https://obtienearchivo.bcn.cl/obtienearchivo?id=repositorio%2F10221%2F36366%2F2%2FBCN_Tiempos_de_espera_para_atencion_en_salud__EG_final.pdf)) | A ranked list a clinician works down. **This is structurally the same object as PreventIA's triage queue** |
| 3 | **Bed / capacity board** | UGCC, and the COVID-era PUC critical-resource system showing live UTI, UCI and ventilator availability ([Ingeniería UC](https://covid19.ing.puc.cl/sistema-de-registro-de-camas-y-reasignacion-de-pacientes/)) | Network-level state, refreshed, read by a coordinator not a treating clinician |
| 4 | **Teleconsultation portal** | Hospital Digital, `interconsulta.minsal.cl` | Asynchronous case handoff between an APS clinician and a specialist, average five-day response ([Departamento de Salud Digital](https://portalsaluddigital.minsal.cl/telemedicina-asincronica/)) |
| 5 | **BI / indicator dashboard** | Rayen IRIS; DEIS public dashboards ([deis.minsal.cl](https://deis.minsal.cl/)) | Aggregate, monthly cadence, management audience. Tied to the REM reporting cycle — data reaches DEIS on the 15th business day of each month |
| 6 | **Patient-facing self-service** | Tótems (Rayen, and the Hospital Militar de Santiago deployment with Transbank payment, [DIVSAL](https://www.divsal.cl/hms-implementa-estacion-de-totems-y-optimiza-la-atencion-a-pacientes/)) | Touch, standing, one task, no training, older users |
| 7 | **Waiting-room caller screen** | LED and display systems across the hospital network ([pled.cl](https://www.pled.cl/portfolio/salas-de-espera-hospitales-chile/)) | Read at distance, no interaction, often paired with voice |

**For PreventIA, type 2 is the target and type 5 is the trap.** ADR-0006 already fixed the triage
queue as the escalation surface. The finding here is that the ranked-queue-worked-top-down pattern is
one a Chilean priorising clinician already performs daily in SIGTE, which is an argument to make in
the pitch. The trap is that a KPI dashboard is easier to build and demos worse: it is type 5, it is
monthly, it is for managers, and it does not satisfy point 4 of `CLAUDE.md` section 12.

---

## 3. The government design system: what it is and what it is not

| Fact | Detail | Source |
|---|---|---|
| Name | **Kit Digital**, run by the Secretaría de Gobierno Digital / Ministerio de Hacienda | [kitdigital.gob.cl](https://kitdigital.gob.cl/) |
| What it contains | Component library — buttons, forms, tables — plus colour, typography and spacing guidelines, on usability and accessibility criteria; distributed to Central Government institutions | [digital.gob.cl launch note](https://digital.gob.cl/media/noticias/subsecretaria-berner-encabezo-lanzamiento-de-kit-para-estandarizar-diseno-de-plataformas-web-del-gobierno/) |
| Current design artefact | **UI Kit v3.0.1**, published as a Figma community library | [Figma community](https://www.figma.com/community/file/1319005921039608306/ui-kit-v3-0-1) |
| Code artefact | **Framework kit**, built on **Bootstrap 4.5**, authored in **SCSS**, mobile-first, with an explicit preference for "HTML and CSS over JavaScript" where possible | [framework.digital.gob.cl](https://framework.digital.gob.cl/development.html) |
| Accessibility themes | Ships `scss/themes/a11y-contrast` and `scss/themes/a11y-fonts`; every component must carry a contrast-mode counterpart and variants for enlarged font sizes | same |
| Component list | Typography, colours, icons, navigation, pagination, tabs, cards, news, profiles, banners, forms, search, buttons, collapsibles, footer | same |
| Status | The Kit Digital site labels the web templates / Framework kit as **pending update** and recommends the UI Kit instead | [kitdigital.gob.cl](https://kitdigital.gob.cl/) |
| Downloads | Government typography (`Tipografia-gobCL.zip`), web accessibility recommendations PDF, inclusive communication guide | same |
| Distribution | **No npm package, CDN or git install path was found.** The development resources index returned HTTP 404 on 5 August 2026 | fetch of `kitdigital.gob.cl/recursos-de-desarrollo/` |

Two honest readings follow, and they point opposite ways.

**Against adopting it:** it is a Bootstrap 4 kit, marked as awaiting update, aimed at public
information sites, with no package distribution and a dead resources page. Bootstrap 4.5 reached end
of life upstream years ago. Building a 2026 clinical prototype on it is inheriting a maintenance
problem to win a talking point.

**For adopting it, or at least its tokens:** the accessibility architecture is the part that is
genuinely good and genuinely Chilean — a mandated contrast theme and a font-size theme per component
is exactly the pair of things a 55-year-old nurse on a shared hospital monitor needs, and exactly the
pair that a hand-rolled Tailwind dashboard skips. Taking the colour, typography and spacing tokens
without the framework is available and cheap.

**Neither is my decision to record here.** See section 10.

---

## 4. Regulation that binds a Chilean clinical web system

This is the section a government-criteria judge will test, so it is given with dates and numbers.

### 4.1 Accessibility — Decreto N°1 de 2015

Approves the technical standard for systems and websites of State administration bodies, promulgated
**2 March 2015**. It requires availability and accessibility of information under W3C accessibility
standards, resting on the 2006 Convention on the Rights of Persons with Disabilities (ratified by
Chile in 2008) and **Ley 20.422** (2010)
([Universidad de Alicante summary](https://accesibilidadweb.dlsi.ua.es/?menu=chile),
[accessibility.cl](https://accessibility.cl/accesibilidad-digital-municipal-chile-decreto-1-ley-21180-ley-20422-edli-overlays/)).

**Which WCAG version applies is contested in the sources.** The decree does not name a version, it
names W3C. One source reads that as WCAG 2.0; a more recent one asserts WCAG 2.2. SENADIS and the Kit
Digital both publish implementation guidance
([SENADIS](https://www.senadis.gob.cl/descarga/i/3676/documento),
[Manual de Accesibilidad Web](https://kitdigital.gob.cl/archivos/insumos/nuevos/Manual%20Accesibilidad%20Web.pdf)).
**Marked unverified.** Building to WCAG 2.2 AA satisfies both readings and removes the question.

One consultancy finding worth carrying because it will come up if anyone proposes a shortcut:
accessibility **overlays do not satisfy the norm**.

### 4.2 Ley 21.180, Transformación Digital del Estado

Published **11 November 2019**, in force **9 June 2022**, with staged implementation deadlines set by
Ley 21.464. Requires State bodies to hold and properly use electronic platforms for electronic
files, complying with security, interoperability, interconnection and cybersecurity standards
([digital.gob.cl](https://digital.gob.cl/transformacion-digital/ley-de-transformacion-digital/),
[BCN](https://www.bcn.cl/leychile/navegar?idNorma=1138479)). The associated **Norma Técnica de
Seguridad de la Información y Ciberseguridad** was promulgated **17 August 2023**. The 2015 technical
standard on systems and websites is described as in the process of being updated.

### 4.3 Ley 21.668, interoperability of clinical records

Published in the Diario Oficial **28 May 2024**. MINSAL must update the clinical-record regulation
within **eighteen months** of entry into force to establish measures allowing electronic records to
interoperate ([MINSAL](https://www.minsal.cl/ley-de-interoperabilidad-de-fichas-clinicas-fue-publicada-en-el-diario-oficial/)).

### 4.4 Ley 21.719, protection of personal data

Published **13 December 2024**, **in force 1 December 2026** — four months after the Lab. Applies to
every public or private organisation processing personal data in Chile regardless of size. **Health
data carries an additional obligation: an Evaluación de Impacto en la Protección de Datos (EIPD)
before implementing any such processing.** Sanctions run to 20.000 UTM, and on repeat offence for
large companies escalate to a percentage of annual revenue, cited at up to 4%. Smaller firms under
Ley 20.416 get written warnings rather than fines during the first twelve months, to 1 December 2027
([Thomson Reuters](https://www.thomsonreuters.cl/es-cl/soluciones-juridicas/biblioteca-contenido-legal/ley-21719-y-la-reconstruccion-del-derecho-chileno-de-proteccion-de-datos-personales),
[preyproject summary](https://preyproject.com/es/blog/ley-de-proteccion-de-datos-en-chile)).

**This is the highest-value line in the whole document for the pitch,** and it is not a UI finding.
Any product touching Chilean patient data that begins operating in 2027 needs an EIPD. `CLAUDE.md`
section 2's rule — no real patient data in the repository, ever — is the thing that lets us say so
without flinching. Naming the EIPD unprompted in front of a government judge signals that we read the
law that lands after the prototype.

**I am not a lawyer and this is not legal advice.** It is a flag for someone qualified.

### 4.5 Security and hosting

MINSAL states it will run continuous improvement grounded in **NCh-ISO 27001:2022**
([MINSAL](https://www.minsal.cl/seguridad_de_la_informacion/)). The Secretaría de Gobierno Digital
publishes **Recomendaciones Técnicas para la adquisición de servicios de Cloud Pública**, requiring
public bodies to weigh efficiency, legality, technological neutrality and security, and noting
explicitly that public cloud "no reconoce territorialidad"
([wikiguias](https://wikiguias.digital.gob.cl/guias/guias/recomendaciones_cloud)).

Data residency is therefore a live question in any Chilean health procurement, not a hypothetical
one. **This is the strongest external evidence for ADR-0010's second half.** The Ollama-on-owned-
hardware deployment path is not a nice-to-have for institutions that "need patient conversations to
stay on hardware they control" — it is an answer to a written government procurement concern. Say it
that way.

---

## 5. The interoperability configuration surface

If the dashboard ever has to exchange anything with a Chilean health institution, this is the fixed
part of the configuration. It is unusually well documented and unusually stable.

| Layer | Standard | Detail |
|---|---|---|
| Syntactic | **HL7 FHIR R4** | MINSAL's stated choice, "la más actualizada y robusta"; the same version used by the EU and the US |
| Imaging | **DICOM** | |
| Terminology, diagnosis | **CIE-10, 2018 edition with 2022 update**; CIE-11 under pilot | |
| Terminology, clinical | **SNOMED CT** | Chile a member of SNOMED International since **1 November 2013**; SNOMED CT Chile is a national reference centre under MINSAL administering national extensions. MINSAL defines it as reference terminology that **may** be used in electronic clinical records — promoted, **not verified as mandatory** |
| Terminology, lab | **LOINC** | |
| Medication | Terminología Farmacéutica Chilena | |
| Formats | JSON, XML, REST | |
| Architecture posture | Service-oriented, elastic; **hybrid centralised-distributed** model for information assets, under transversal governance | |

Sources: [Estándares y Perfiles](https://interoperabilidad.minsal.cl/docs/especificacion-de-la-arquitectura/estandares-perfiles.html),
[Arquitectura](https://interoperabilidad.minsal.cl/docs/especificacion-de-la-arquitectura/arquitectura.html),
[snomed.org/members/chile](https://www.snomed.org/members/chile).

**Named implementation guides**, all published by MINSAL or HL7 Chile:

| Guide | Purpose | Version seen |
|---|---|---|
| **CL Core** | National core profiles (Patient-Cl, Encounter, Organización) | 1.9.3 published as STU3 Draft; 1.9.4 pre-release; MINSAL cited as working on 1.9.4 ([hl7chile.cl](https://hl7chile.cl/fhir/ig/clcore/)) |
| **NID** | Núcleo de Interoperabilidad de Datos — includes the **Índice Maestro de Pacientes (MPI)** and the **Directorio de Prestadores (HPD)** | 0.4.6 |
| **SNRE** | Sistema Nacional de Receta Electrónica | 0.9.5 |
| **EIS** | Norma 820 | — |
| **IPS-CL** | International Patient Summary, Chilean adaptation | build |
| **TEI** | Tiempos de Espera Interoperable | 0.1.6 |

**Note the version numbers.** Every guide except CL Core is below 1.0. This is a national
interoperability programme still in draft, which is an argument for building the FHIR seam and not
the FHIR implementation.

**Authentication is a gap in the published architecture.** The Estándares y Perfiles page names no
identity or authorisation standard — no OAuth 2.0 profile, no SMART on FHIR. Separately, **ClaveÚnica
uses OpenID Connect over OAuth 2.0**, a Presidential Directive requires it for citizen-facing
authenticated procedures, and institutions **may** use it for their own staff on internal platforms
([Manual de Integración](https://wikiguias.digital.gob.cl/Manuales/Integraci%C3%B3n_Clave%C3%9Anica),
[Guía Técnica PDF](https://wikiguias.digital.gob.cl/documentos/guia_tecnica_de_integracion_a_claveunica__8.pdf)).
Credentials are requested through CeroFilas and require certification before production.

For a clinician-facing triage queue, ClaveÚnica is therefore **permitted but not required**, and it
is a real, named, Chilean answer to "how would staff log in" that costs nothing to say and does not
have to be built for the Lab.

---

## 6. What the field says about the environment the dashboard runs in

This section is where the evidence is weakest, and it is labelled accordingly, because guessing here
would be worse than admitting the gap.

| Question | Status |
|---|---|
| Browser and version in a public hospital or CESFAM | **Not verified.** No Chilean source found. The general claim that legacy Internet Explorer persists in corporate environments is not Chile-specific and is not usable |
| Screen resolution at a consultation box | **Not verified.** No source |
| Whether staff work on shared or personal workstations | **Not verified.** Rayen's own materials describe recording consultation data on computers "in the boxes", which implies shared and stationary, not personal and mobile |
| Connectivity | **Partly verified, at regional level.** Over 2.000 rural and conurban localities lack fixed and mobile service. Lowest internet penetration: La Araucanía 33%, Ñuble 33,8%, Maule 37,4% ([DPL News](https://dplnews.com/chile-tiene-un-problema-dramatico-de-conectividad-fija-en-zonas-rurales/)) |
| Hospital-side availability expectations | **Verified for one system.** Hospital Digital's technology architecture is Active/Active high availability across a primary and secondary SONDA site, both connected to the Red MINSAL, with a **committed 99,98% availability** ([DIPRES evaluation](https://www.dipres.gob.cl/597/articles-285478_informe_final.pdf)) |

That last row is the useful one and it cuts against a certain kind of demo. **The reference point for
a national health platform in Chile is a two-site active/active deployment with a contractual
99,98%.** Nothing we build in two days approaches that, and nobody expects it to — but it tells you
what a health-network judge means by "deployable", and it is why the pitch should talk about the
adoption pathway rather than the uptime.

There is also a cautionary case directly on our subject matter. **SIGTE**, the waiting-times platform
whose priorisation panels are the closest existing analogue to our triage queue, has been publicly
criticised for manual operation producing serious errors — patients recorded as attended who were
not, and care records against deceased people — and MINSAL announced a replacement for 2025
([Cooperativa](https://cooperativa.cl/noticias/pais/salud/hospitales/minsal-busca-reemplazar-en-2025-el-actual-sistema-de-gestion-de-listas/2024-08-27/231330.html),
[BioBioChile](https://www.biobiochile.cl/noticias/nacional/chile/2024/09/25/minsal-anuncia-mejora-a-plataforma-de-listas-de-espera-en-medio-de-polemica-por-falsos-fallecidos.shtml)).

**Read that as a design requirement, not as gossip.** The failure was not visual. It was that queue
state could be advanced without the underlying clinical event having happened. A triage queue that
lets a case be marked resolved without recording who resolved it and when is the same class of
system. `CLAUDE.md` section 2 already says every escalation terminates at a human; the SIGTE record
says the queue must also be able to *prove* it did.

---

## 7. Evidence on clinical dashboard design

Restricted to what bears on a risk-ranked queue. Not Chile-specific; flagged as such.

A 2025 scoping review of interface design features in clinical decision support systems for
real-time deterioration detection reports colour prioritisation using **yellow, purple and red**
along with warning icons to signal triage levels
([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1386505625001637)).

Note the palette. It is not green/yellow/red. Purple appears where our semáforo uses green, and the
reason is that **green is not a level in a deterioration system — it is the absence of one.** Our
traffic light is doing two jobs at once: encoding severity and encoding "checked and fine". That is
defensible for a green/yellow/red metaphor a Chilean clinician already knows from GES and triage, but
it is worth knowing the deterioration-detection literature does not do it that way.

On alarm fatigue, consistently across the sources: 93% of participants in one monitoring survey
agreed on the need to reduce alarm frequency, and 95-98% of nurses in another believe false alarms
are frequent, disrupt care and reduce trust, leading nurses to disable alarms inappropriately
([PMC4797660](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4797660/),
[PMC12406432](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12406432/)).

The design rule that follows, and it is the one to hold onto: **reserve the loudest signal for
conditions that change what happens in the next minute, and let everything else sit until someone
goes looking.**

Which lands on an uncomfortable question for us. PreventIA's semáforo can only be raised, never
lowered by the model (ADR-0004). That is right on clinical-safety grounds and it is our best sentence
in front of a clinical judge. It also means **the only pressure on the red count is upward**, and a
queue that fills with red is a queue nobody works. Nothing in the evidence resolves this; the
resolution is operational, not architectural — who clears a red, and how fast. It belongs in the
question list for the clinical teammate.

---

## 8. Stacks: what the Chilean market actually staffs for

Weak evidence, presented as weak. Chilean job listings for full-stack roles at health entities ask
for **CSS, JavaScript, jQuery, React, Angular and Bootstrap**, with some positions specifically
requiring **AngularJS and/or Angular 7 or 11** single-page applications, unit testing in **Karma and
Jasmine**, and the Atlassian toolchain
([Indeed CL](https://cl.indeed.com/q-angular-empleos.html),
[FirstJob](https://firstjob.me/oferta/22690/desarrollador-a-front-end-angular-react)).

Angular 7 and 11 are 2018 and 2020 releases. jQuery and Bootstrap appearing alongside them tells you
the same thing the Kit Digital's Bootstrap 4.5 does: **the installed base is enterprise Angular and
Bootstrap, maintained rather than rewritten.**

That is a fact about hiring, not a reason to pick Angular for a two-day prototype. It is worth
knowing only for one sentence in the pitch, if anyone asks who would maintain this: the skills a
Chilean health institution already staffs are Angular, Bootstrap and jQuery, and anything we build
should be simple enough that this is not a problem.

No evidence was found of **DHIS2, OpenMRS, Bahmni or Odoo** deployments in Chilean public health,
despite their prevalence elsewhere in global health. Searched and not found is not the same as absent,
but Chile's public network is served by commercial vendors under the SIDRA strategy, and the
open-source HMIS ecosystem does not appear in it.

---

## 9. What this establishes for PreventIA

Findings only. Decisions are section 10.

1. **The triage queue has a Chilean precedent by name.** SIGTE's priorisation panels are a ranked
   list a clinician works down. This is worth one sentence in the pitch and it costs nothing.
2. **The strongest regulatory card is Ley 21.719 and the EIPD**, in force 1 December 2026, and our
   no-real-data rule is what lets us play it.
3. **Cloud territoriality is a written government procurement concern**, which upgrades ADR-0010's
   Ollama deployment path from a technical option to a procurement answer.
4. **The interoperability target is FHIR R4 / CL Core**, and every guide except CL Core is
   pre-1.0. Build the seam, not the implementation.
5. **ClaveÚnica is available for staff login**, OpenID Connect over OAuth 2.0, and is a credible
   answer to a question we will be asked without having to build it.
6. **WCAG 2.2 AA removes an ambiguity** in what Decreto 1/2015 requires, and Kit Digital's
   contrast-theme and font-size-theme pattern is the locally idiomatic way to satisfy it.
7. **The deterioration-detection literature does not use green as a level**, and the alarm-fatigue
   literature says an unclearable red queue is a failure mode, not a feature.
8. **The eight-stage hospital rollout sequence** — implementación, recolección de datos, levantamiento
   de procesos, configuración y parametrización, validación, capacitación, lanzamiento,
   acompañamiento — is the shape of the adoption story a health-network judge is listening for.

## 10. Open items and what they need

| # | Item | What would close it |
|---|---|---|
| 1 | Rayen's browser, resolution and navigation structure | Retrieve one public Rayen manual with a browser user agent. Ten minutes. Highest value per minute in this list |
| 2 | Which WCAG version Decreto 1/2015 requires | Read the decree text via `bcn.cl/leychile` XML. Or moot it by building to 2.2 AA |
| 3 | Whether SNOMED CT is mandatory or permitted in an RCE | The MINSAL resolution behind the "may be used" wording |
| 4 | Whether the dashboard adopts Kit Digital tokens, the Kit Digital framework, or neither | **Felipe's decision. Not recorded here** |
| 5 | Who clears a red in the queue, and within what time | The clinical teammate. Adds to the question list in `docs/research/README.md` |
| 6 | Whether the queue records the actor and timestamp of every state change | Follows from the SIGTE failure. Design decision, and it may want an ADR |

## 11. Search record

34 retrievals on 5 August 2026: 30 web searches and 4 direct page fetches. Two fetches failed —
`saludtarapaca.gob.cl` refused the connection, and `kitdigital.gob.cl/recursos-de-desarrollo/`
returned 404. Topics covered: SIDRA; Rayen; hospital HIS vendors; MINSAL interoperability
architecture and standards; CL Core; SNOMED CT Chile; Ley 21.668; Ley 21.719; Ley 21.180; Decreto
1/2015 and accessibility; Kit Digital and the government framework; ClaveÚnica; public cloud
recommendations and ISO 27001; Hospital Digital; SIGTE and waiting lists; UGCC and bed management;
REM/DEIS reporting; tótems and waiting-room screens; TrakCare at Coquimbo; Clínica Alemana; Chilean
front-end job requirements; rural connectivity; open-source HMIS; and clinical dashboard design and
alarm fatigue evidence.

Practical notes for whoever fetches more, extending the list in `docs/research/README.md`:

- `saludtarapaca.gob.cl` refused the connection outright on 5 August 2026. Retry with a browser user
  agent before assuming the document is gone.
- `kitdigital.gob.cl` has broken internal links; the site root lists the resources, the
  `/recursos-de-desarrollo/` path 404s.
- `framework.digital.gob.cl` still serves the full Bootstrap-based documentation even though the Kit
  Digital site describes it as pending update.
- `hl7chile.cl/fhir/ig/clcore/` and `interoperabilidad.minsal.cl` both serve cleanly to plain
  fetchers, unlike `minsal.cl` itself.
