# How Chilean older adults actually use WhatsApp

Workstream 5 of the Phase 0 research brief.

Consulted 3 August 2026. Author: Felipe Carvajal Brown. Archived copies of every source that could be
downloaded are in `docs/research/sources/`.

## Headline: text-first is defensible at 60, and not at 80

Two Chilean official sources agree on the shape and disagree on nothing that matters.

Among Chileans aged 60 and over, **60% used a phone for chat or WhatsApp in the last month**. Broken
down by age, that figure is **78% at 60-69, 51% at 70-79 and 22% at 80 and over**. Over the same
bands, using a phone **to talk to another person** runs at **96%, 90% and 73%**.

So the gap between voice and text is small at 60 and enormous at 80. And 80 is not the edge of
PreventIA's population — the PSCV's own frailty criteria start at "mayor de 75 años" (workstream 2),
which puts the modal patient this product is designed for in the bands where WhatsApp chat is a
coin-flip or worse.

**This does not say text is the wrong choice.** It says text-first is a scoping decision with a
measurable cost, that the cost is concentrated in exactly the patients workstream 1 already
identified as least able to self-report, and that the PRD does not currently acknowledge it.

The brief says not to resolve the scope question, and this document does not. It sets out what each
modality would demand and hands the decision back.

---

## 1. What the two Chilean sources are

**SUBTEL's XI Encuesta de Acceso, Usos y Usuarios de Internet**, fieldwork 2024, published February
2025, run by Cadem for the telecommunications regulator. National, urban and rural, population 15 and
over. Its oldest age band is **"60 años o más"** — one band for everyone from 60 to 100.

**The Sexta Encuesta Nacional de Calidad de Vida en la Vejez 2022**, UC-Caja Los Andes, published
August 2023, coordinated by the Centro UC de Estudios de Vejez y Envejecimiento with fieldwork by
DESUC. Population 60 and over, reported in **three bands: 60-69, 70-79, 80 and over**, and by
education level.

The second is the one that matters, because the first cannot see inside the group we care about.
Note also whose survey it is: Caja **Los Andes**, the largest CCAF, not La Araucana. That it exists
at all is evidence that a Chilean caja de compensación considers the technology habits of older
adults its business, which bears on workstream 6.

---

## 2. What they have

From the UC-Caja Los Andes survey, 2022, population 60+:

| | % |
|---|---|
| Has a mobile phone of any kind | **89%** |
| Has none | 11% |
| Says it is a smartphone | 50% |
| Says it is a conventional phone | 23% |
| Has one but does not know which type | **15%** |
| **"Usuario de smartphone"** — actually uses it for chat, social networks, trámites or information | **65%** (was 46% in 2019) |

That 15% who cannot say what kind of phone they own is worth pausing on. It is the reason the survey
constructed the functional definition in the last row rather than trusting the self-report, and the
report's own commentary draws the conclusion: **35% of Chilean older adults are still outside the
digital world**, and the split is by age and education, consistently across every wave since 2013.

Access is strongly stratified:

| | Has a phone | Is a smartphone user |
|---|---|---|
| 60-69 | 95% | 82% |
| 70-79 | 89% | 57% |
| 80+ | **66%** | **27%** |
| Educación básica | 90% | 45% |
| Educación media | 96% | 72% |
| Educación superior | 87% | 83% |

And education is not a minority condition in this population. Drawing on CASEN, the same report
states that **45,2% of Chilean older adults had educación básica or less in 2020** (down from 57,8%
in 2009), with average schooling of 8,3 years in 2017.

Put those two tables together and the modal PreventIA patient — over 75, básica education,
polymedicated — is more likely than not **outside** the smartphone-user definition.

SUBTEL's national numbers are consistent, with the coarser band: **84,0%** of people 60+ use a
smartphone daily against 95,5% at 45-59; **85,9%** use the internet daily; only **20,3%** used a
computer in the last week; **65,0%** say they know how to check social networks including WhatsApp,
against 80,6% overall; **67,6%** say they can make a video call; **36,5%** can do a bank transaction
online.

## 3. What they do with it, and the finding that argues for the product

The UC-Caja Los Andes question is "durante el último mes, ¿ha usado el celular para...?", asked of
people who have a phone.

| Activity | Total 60+ | 60-69 | 70-79 | 80+ |
|---|---|---|---|---|
| Hablar con otra persona | 91% | 96% | 90% | 73% |
| **Mensajes o llamadas de chat (WhatsApp u otro)** | **60%** | **78%** | **51%** | **22%** |
| Sacar fotos o hacer video | 51% | 68% | 40% | 18% |
| Comunicarse por videollamada | — | 67% | 40% | 21% |
| Buscar noticias o información | 42% | 55% | 35% | 13% |
| Hacer trámites por internet | 23% | 34% | 13% | **4%** |

The totals in the first column are quoted from the report's own prose. **The age-band columns were
read off a bar chart on p.70 whose labels and values `pdftotext` extracted separately**; the
row-to-value mapping is my reconstruction, cross-checked against the printed totals and against a
second chart on the same question by gender. It holds together, but if any of these numbers is going
on a slide, someone should open the PDF and look at the chart. The one age-band figure I can quote
directly from the prose is trámites: "no supera el 5% entre los mayores de 80 años".

The trend is the encouraging part. Chat and social network use each **rose 16 percentage points
between 2019 and 2022**, and the smartphone-user share went from 46% to 65% in three years. The 2022
data is already four years old.

**And here is the finding that argues for building this at all.** SUBTEL groups internet activities
into categories and reports them by age band:

| Activity category | Total | 16-29 | 30-44 | 45-59 | **60+** |
|---|---|---|---|---|---|
| **Comunicaciones** | 86,2 | 85,0 | 87,1 | 86,9 | **85,9** |
| Obtener información | 75,5 | 86,5 | 83,9 | 70,2 | 53,6 |
| Actividades recreativas | 66,4 | 74,9 | 74,5 | 61,2 | 48,5 |
| Comercio electrónico | 59,2 | 64,9 | 69,9 | 56,2 | 38,4 |
| Trámites con el Estado | 39,8 | 43,2 | 49,4 | 36,4 | 24,5 |
| Actividad laboral | 22,7 | 21,7 | 31,2 | 23,5 | 10,0 |

SUBTEL's own comment, verbatim:

> Con la sola excepción de las actividades de comunicación que tienen una declaración sin grandes
> diferencias entre segmentos etarios, en los otros ámbitos se observa una tendencia a encontrar
> mayor nivel de uso de internet en los segmentos menores de 45 años, siendo los de 60 o más años el
> grupo con menor declaración de las actividades presentadas.

**Communication is the one thing older Chilean internet users do at the same rate as everyone else.**
Every other category falls away with age; that one does not. A product that reaches an older adult
through a conversation is working with the grain. A product that reached them through a portal, a
form or an app would not be — and note that among the same population, only **23% do any trámite
online at all**, and **13%** have ever used Zoom or Meet.

That is a strong, sourced, official argument for the channel choice in ADR-0003 and it is not
currently anywhere in the PRD.

## 4. Text versus voice notes: an honest gap

The brief asks specifically about voice notes. **I could not find any Chilean or Latin American
survey that separates written messages from voice notes among older adults.** Both national surveys
ask about "mensajes o llamadas de chat (WhatsApp u otro)" as a single item, which merges the two
modalities into one number. Searches on 3 August 2026 for research on older adults' voice-note use
surfaced only popular-psychology journalism with no data behind it.

**Unverified, and this is a genuine hole in the middle of the question the brief asked.** What would
verify it: the UC-Caja Los Andes microdata, if it separates the item, or a question added to a future
wave; failing that, a small structured observation with real patients, which is a day's work for the
clinical teammate and worth more than any survey to us.

What can be said without inventing anything:

- **Typing is the harder skill and the survey structure hints at it.** The functional smartphone-user
  definition requires chat, social networks, trámites or information — none of which a voice note
  requires. The gap between 91% who talk on the phone and 60% who use chat is where the modality
  question lives.
- **Voice notes are inside the same WhatsApp conversation.** A patient who sends one is not switching
  channel, which is not true of a phone call.
- Whether the same 80-year-old who does not write would send an audio is **exactly the thing nobody
  has measured**, and it is the question that decides whether the 22% figure is a ceiling or an
  artefact of asking about the wrong thing.

## 5. Literacy and vision

**Literacy.** Chile's result in the OECD PIAAC assessment of adult skills, published 2024 for the
2023 cycle: **218 points in comprensión lectora against an OECD average of 260**, and the worst
performance of any age band assessed was **55 to 64 year olds**.

The limitation is severe and needs stating: **PIAAC assesses adults aged 16 to 65**. Its oldest band
is the youngest edge of PreventIA's population. The honest reading is that literacy in this
population is at least as constrained as the worst band PIAAC measures, and probably more so, and
that no instrument I found measures it directly in Chileans over 65. **Unverified.** What would
verify it: a Chilean study of functional literacy or health literacy in adults over 65.

**Vision.** I found no Chilean population figure for visual impairment in older adults. The
UC-Caja Los Andes survey records cataract **treatment** as one of the conditions asked about, and
notes it fell significantly between 2019 and 2022, but does not report prevalence of visual
difficulty. **Unverified.** What would verify it: the Encuesta Nacional de Salud, which asks about
vision, or the Estudio Nacional de la Dependencia en las Personas Mayores. Neither was read for this
document, and stating a vision figure without one would be inventing it.

**What the same survey does establish about the population**, and which bears on the copy rules:
hypertension in **53%**, diabetes or raised blood sugar in **34%**, high cholesterol in **33%**, and
only **16% take no medication at all**. The report's clinical commentary lists "quejas de memoria" and
"mareos o desmayos" among the indicators showing a significant gender gap. This is the same
population workstream 1 described, from a different direction, and it is a better basis for the
synthetic cohort than anything we would invent.

**Self-perceived digital skill is low even where use is high.** On a 1-to-7 scale, in 2022:

| Skill | % rating themselves 1-3 |
|---|---|
| Using the phone | 31,4% |
| Using the internet to find information or do a trámite | 52,9% |
| Connecting to Zoom, Meet or similar | 61,9% |

A patient who rates their own phone skill at 2 out of 7 is not going to recover from a confusing
message by exploring the interface. **Every failure mode must be recoverable by the system, never by
the patient.** That is a design constraint, and it is not currently written down anywhere.

## 6. What each modality would actually demand

Set out so the scope decision can be made on facts rather than on preference. **This section resolves
nothing.**

### 6.1 Text on WhatsApp — what the prototype assumes today

Already scoped in ADR-0003 and section 11 of `CLAUDE.md`. Nothing new is required. The constraints
already known: the 24-hour customer service window, five test recipients, the System User permanent
token.

The demand it places on the **patient** is the one this document adds: composing written Spanish on a
phone keyboard. That is the skill 40% of the 60+ population does not exercise in a month, rising to
78% of those over 80.

### 6.2 Voice notes on WhatsApp — a real option, with a real addition

Meta's Cloud API does support audio, verified against Meta's own developer documentation on 3 August
2026:

- Supported formats: AAC, AMR, MP3, MP4 audio, and OGG **with OPUS codecs only, mono input only**.
- Maximum file size **16 MB**.
- A **voice message** specifically requires `.ogg` encoded with OPUS; a plain audio message does not
  get voice-message rendering. The play icon appears only for files of 512 KB or less.

Two things follow.

**Receiving is the easy half and sending is the fussy half.** An inbound patient audio arrives as a
media id to download. An outbound reply that should look like a voice note has to be OGG/OPUS, mono,
and small.

**Speech to text is a new component, and it is not in ADR-0001.** Nothing in the Strands stack
transcribes audio. Adding it means a new model in the pipeline, a new failure mode — a mis-transcribed
symptom — and a new question for the guardrail suite, because `clinical/guardrails.py` currently
inspects text. **This is the honest cost of voice notes and it is more than an afternoon.**

The transcription step also lands directly on the clinical boundary. A transcription error that turns
one symptom into another is a clinical error introduced by an engineering component, and neither the
semáforo's deterministic floor nor the output filter would catch it. **REQUIRES CLINICAL REVIEW** on
whether transcribed audio may feed the extraction layer at all, or whether a transcript must be
treated as lower-confidence than typed text.

### 6.3 A voice call — a different product, not a channel option

The project description submitted to the Lab says "WhatsApp o llamada de voz". For the record, and
without arguing either way:

- WhatsApp voice calls run through the **WhatsApp Business Calling API**, which is a separate product
  from the Cloud API messaging endpoints. As of 2026 it is described as available to selected
  businesses through direct Cloud API partnerships and a limited number of enterprise providers;
  broad availability has not rolled out. Business-initiated calls require prior consent and are
  blocked in several countries. **This is from vendor and integrator documentation, corroborated
  across several, not from a single Meta page**, and access for a two-person team in Chile in two
  days should be treated as unlikely until someone confirms it.
- A real-time voice conversation needs speech to text, text to speech, and turn-taking under latency
  — three components, none of which exist in the current architecture.
- The backup ladder in `CLAUDE.md` section 11 has no voice rung.

### 6.4 The scope contradiction, flagged and not resolved

The Lab submission says "WhatsApp o llamada de voz". PRD section 9 puts the voice channel explicitly
out of the two-day prototype, calling it "una decisión, no una omisión", and ROADMAP Phase 3 scopes
only the WhatsApp Cloud API adapter.

**These do not agree, and the disagreement is visible to anyone who reads both.** It is not this
document's decision. What this document adds is that the evidence makes it a substantive question
rather than a wording problem: the modality gap in section 2 is real, large, and concentrated in the
oldest patients.

The narrowest thing that would close it, if the answer is to stay text-first: say so in the pitch, on
the evidence, as a deliberate first-cohort scoping decision — "the prototype targets the 78% of
60-69s and 51% of 70-79s who already use WhatsApp chat, and voice is the next cohort, not an
afterthought." That is a stronger position than being asked about it.

## 7. What this changes for the patient-facing copy rules

`CLAUDE.md` section 8 already requires Chilean Spanish, *usted*, short sentences, plain register, no
jargon, no abbreviations, no English. Nothing found here contradicts any of that. Four additions the
evidence supports:

1. **Never require the patient to type more than a few words.** The chat-use figures say composition
   is the limiting skill. Questions answerable with "sí", "no" or one word should be the default
   shape, with free text always accepted and never demanded.
2. **Never send a message the patient must scroll to finish.** Not sourced to a Chilean study; it
   follows from a population where more than half rate their own internet skill at 3 or below out of
   7, and where the prevalence of visual difficulty is unknown to us rather than known to be low.
   **My inference, marked as such.**
3. **Every failure state must be recoverable by the system.** From the self-perceived skill data in
   section 5. If a message confuses the patient, the next message must repair it without the patient
   needing to do anything except reply.
4. **Accept an inbound voice note gracefully even if the prototype cannot process it.** Patients who
   do not type send audio. A silent failure would look to an 80-year-old exactly like being ignored,
   and this is a product whose entire premise is that somebody is listening. Even a fixed reply
   asking them to write is better than nothing. **This is cheap and should be in scope regardless of
   how the voice question is settled.**

## 8. Open questions

1. **Do Chilean older adults who do not type send voice notes instead?** (4.) Nobody has measured it.
   The single highest-value question in this workstream and answerable by observation, not search.
2. Does the UC-Caja Los Andes microdata separate written messages from voice notes? (4.)
3. What is the prevalence of visual impairment in Chilean adults over 65? (5.) **Unverified**; ENS or
   the dependency study would answer it.
4. Is there any measure of functional or health literacy in Chileans over 65? (5.) PIAAC stops at 65.
5. May transcribed audio feed the extraction layer, and at what confidence? (6.2.) **REQUIRES
   CLINICAL REVIEW.**
6. Is WhatsApp Business Calling API reachable at all for this team? (6.3.) Verifiable in one enquiry
   to Meta, and it settles the voice-call branch of the scope question.
7. Which patients does the first cohort actually target, given section 2? A product question for
   Felipe, and the answer belongs in PRD section 4.

## Sources

All consulted 3 August 2026.

1. Subsecretaría de Telecomunicaciones (SUBTEL) and Cadem. *Estudio Undécima Encuesta sobre acceso,
   usos y usuarios de Internet en Chile — Informe Final*. Fieldwork 2024, published February 2025.
   https://www.subtel.gob.cl/wp-content/uploads/2025/02/Informe-Final-Subtel-Acceso-y-Uso-Internet-2024.pdf
   Archived as `subtel-2024-xi-encuesta-acceso-usos-internet.pdf`. Sections used: 5.1 uso de
   dispositivos, Tabla 7 tareas por grupo etario, Tabla 8 uso de internet por edad, 5.3 actividades
   de uso, Tabla 10, Tabla 12 actividades por tramo etario, 7.4 habilidades digitales.

2. Centro UC Estudios de Vejez y Envejecimiento, Programa Adulto Mayor UC, and Caja Los Andes.
   *Chile y sus mayores. Sexta Encuesta Nacional de Calidad de Vida en la Vejez 2022*. Santiago,
   August 2023. ISBN 978-956-14-3157-7.
   https://encuestacalidaddevidaenlavejez.uc.cl/wp-content/uploads/2023/08/Libro-completo-VI-Encuesta_compressed.pdf
   Archived as `uc-caja-los-andes-2022-vi-encuesta-calidad-vida-vejez.pdf`. Sections used:
   Antecedentes sociodemográficos (p.9), chapter 2 Condiciones de salud commentary (p.23), chapter 4
   Acceso a las TICs in full (p.60-75).

3. Ministerio de Educación (Chile). *PIAAC 2023: Chile mejora puntaje en razonamiento matemático en
   adultos*. https://www.mineduc.cl/piaac-2023-chile-mejora-puntaje-en-razonamiento-matematico-en-adultos/
   Official ministry communication of the OECD result. Web page, not archived. Used for the 218
   against 260 comparison and the statement that 55-64 year olds performed worst. The percentage of
   Chilean adults at proficiency level 1 or below was **not** stated on this page and is therefore
   not quoted here, although several secondary sources give figures for it.

4. Meta for Developers. *Audio messages* — WhatsApp Cloud API documentation.
   https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/audio-messages
   Web page, not archived. Used for the formats, size limits and the audio-versus-voice-message
   distinction in 6.2.

5. Meta for Developers. *Cloud API Calling*.
   https://developers.facebook.com/documentation/business-messaging/whatsapp/calling
   Located but **not read directly**. The availability description in 6.3 comes from integrator and
   vendor documentation consulted on the same date and is corroborated across several of them, not
   taken from Meta. **Partially verified.**

## Verification status summary

| Claim | Status |
|---|---|
| 60% of Chileans 60+ used chat or WhatsApp in the last month | Verified, quoted from source 2 prose |
| 91% used the phone to talk to another person | Verified, quoted from source 2 prose |
| Chat use 78% / 51% / 22% and voice 96% / 90% / 73% by age band | **Read off a chart, mapping reconstructed.** See the caveat in section 3 |
| Trámites online do not exceed 5% among the over-80s | Verified, quoted from source 2 prose |
| 89% have a phone, 65% are functional smartphone users, 35% digitally excluded | Verified from source 2 |
| Phone and smartphone use by age band and education level | Verified from source 2, chart with printed values |
| Chat and social network use each rose 16 points 2019-2022 | Verified, quoted from source 2 commentary |
| 45,2% of older adults had educación básica or less in 2020 | Verified from source 2, citing CASEN |
| Self-perceived skill ratings 31,4% / 52,9% / 61,9% at 1-3 | Verified from source 2 |
| HTA 53%, diabetes 34%, cholesterol 33%, 16% take no medication | Verified from source 2 |
| SUBTEL 60+ figures: 84,0% daily smartphone, 20,3% computer, 65,0% social networks, 36,5% banking | Verified from source 1 |
| Communications is the only activity category without a large age gap | Verified, quoted from source 1 |
| PIAAC Chile 218 vs OECD 260, worst band 55-64 | Verified from source 3 |
| PIAAC assesses only 16-65 | Verified from the OECD programme's own scope |
| Any Chilean or LatAm data separating voice notes from written messages | **Unverified — not found.** Genuine gap |
| Prevalence of visual impairment in Chilean older adults | **Unverified — not found** |
| Any measure of functional literacy in Chileans over 65 | **Unverified — not found** |
| Cloud API audio formats, 16 MB limit, OGG/OPUS voice-message requirement | Verified from source 4 |
| WhatsApp Business Calling API availability in 2026 | **Partially verified** — vendor documentation, not Meta's own page |
| Message length and scrolling guidance | **My inference**, not sourced to a Chilean study |
| The Lab submission and PRD section 9 disagree on the voice channel | Verified by reading both. **Not resolved here, by instruction** |
