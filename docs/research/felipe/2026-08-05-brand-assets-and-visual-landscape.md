# Brand assets: the Chilean visual landscape, the LatAm field, and the asset specifications

**Date:** 5 August 2026
**Author:** Felipe Carvajal Brown
**Supplies:** the `assets/` build
**Purpose:** the record behind the logo and the asset set. Four parallel retrievals plus local
measurement. Nothing here proposes a decision; it records what was found and what was measured.

## Honesty statement

Every hex value in this document was read from a published source, extracted from a PDF or SVG, or
sampled from a rendered logo file. None were invented. Contrast ratios and colour-difference figures
marked `[computed]` are arithmetic I performed locally on retrieved values, not claims made by any
source.

Four things did not come back and are marked `UNVERIFIED` where they appear: Meta's own WhatsApp
business-profile reference pages (HTTP 500 on four URL variants, so every field limit below is
mirrored from BSP documentation rather than from Meta); X/Twitter card dimensions (the spec pages
now redirect or return HTTP 402); IEC 60601-1-8's alarm-colour table (paywalled, three sample PDFs
attempted and all were stubs); and FONASA's current logo (the site blocks automated fetches, so the
description below is of a 2013 asset).

---

## 1. The governing constraint: what reads as the Chilean state

This is the finding that bounds the logo more than any other.

The Marca Gobierno de Chile is defined in a 73-page `Manual de Normas Gráficas`. Its two official
colours are PANTONE 293 C and PANTONE 185 C:

| | PANTONE 293 C | PANTONE 185 C |
|---|---|---|
| RGB | 15, 105, 180 | 235, 60, 70 |
| Hex | `#0f69b4` | `#eb3c46` |

MINSAL's own 2012 brand manual cites the same two Pantones but converts them differently, to
`#006CB7` and `#EF4144`. Both are official depending on which document is cited. This is a real
discrepancy in the government's own documents, not an error to chase.

The manual states the palette's purpose verbatim: *"La paleta cromática se limita a los colores de
nuestra bandera y sus matices. Su función es comunicar institucionalidad y formalidad."* The palette
exists in order to read as the state.

Three devices are therefore off-limits, independent of what colours fill them:

- **The blue-and-red pair.** Side by side, in any proportion, it is the state.
- **The hard-edged rectangular container with a vertical bicolour seam and knockout white type.** This
  is the single most recognisable device in Chilean institutional graphics. The MINSAL logo is exactly
  this: a blue left band carrying white line art, a red right field carrying white type. FONASA used
  the thin blue/red rule under a wordmark for the same reason.
- **The escudo nacional or any fragment of it.** The government symbol is not a star and not a lonko;
  it is the full coat of arms, huemul and condor flanking a shield, redrawn as white line art. The
  lone star exists only inside the shield. No huemul, no condor, no shield, no scroll, no star.

Extended government base palette, from `Lineamientos Gráficos 2024`: `#173277`, `#0F69B4`, `#3CB9F7`,
`#E8385F`, with accents `#215ACE`, `#53CCF4`, `#DDEFFB`, `#EA7A85`.

Government typography is Museo Sans (primary), Museo Display (secondary), Verdana (digital fallback),
gobCL (editorial). All four are state-identity signals and none should be used.

Sources: https://kitdigital.gob.cl/archivos/ManualNormasGra%CC%81ficas2022.pdf ,
https://www.cultura.gob.cl/wp-content/uploads/2023/03/identidad-visual-gobcl.pdf ,
https://www.cultura.gob.cl/wp-content/uploads/2024/05/manual-de-comunicacion-visual-gob-2024.pdf ,
https://www.minsal.cl/wp-content/uploads/2025/12/cd33fa50423bb45ae040010164011269.pdf ,
https://commons.wikimedia.org/wiki/File:Logo_del_Ministerio_de_Salud_de_Chile.svg

## 2. The rest of the Chilean health field

**Superintendencia de Salud** uses `#3cb9f7` and `#173277`, both literally from the 2024 government
base palette. A health regulator adopting the state palette verbatim.
Source: https://www.superdesalud.gob.cl/

**ChileAtiende** uses `#0f69b4` unmodified, with `#0d4d82`, `#12579d`, `#0e4b7e`, red `#da343a`, and
neutrals `#272727`, `#4a4a4a`, `#d4d4d4`, `#f7f7f7`. Roboto for body, Roboto Slab for headings.
Source: https://www.chileatiende.gob.cl/

**FONASA**, from a 2013 asset only. Three abstract rounded human figures beside "Fonasa" in an italic
rounded lowercase sans, over a small blue-and-red bar. Colours sampled from the rendered image, not
from a spec: `#006cb7`, `#00adef`, `#a6ce39`, `#ef4045`. The live site references
`/assets/fonasa2020/img/logo-fonasa.svg`, so the mark has been revised since. Treat as directional.
Source: https://commons.wikimedia.org/wiki/File:Logo_de_Fonasa.jpg

**CESFAM / APS, and this is the one worth remembering.** Under the MAIS model a CESFAM population is
divided into geographic *sectores*, and each sector is identified by a colour. Verified live: "Sector
Azul", "Sector Verde", "Sector Naranjo", "Sector Terraza". The mapping is local, not national. An
older Chilean patient who attends a CESFAM has been taught that a colour means "your team and your
queue". Colour is already load-bearing semantics in their health experience, which cuts both ways: it
makes colour-coding legible to them, and it means an arbitrary brand colour can be misread as a
sector assignment. CESFAM Codegua's own site runs `#008ba8` teal with `#67bce0`.
Source: https://www.cesfamcodegua.cl/

**Caja La Araucana**, a Lab partner. Dominant `#00539B` with `#FFA500` orange; supporting `#0056a4`,
`#0084D1`, `#0096e5`, `#FF9600`, `#fc8a00`. The logo is a dark blue rounded-rectangle frame holding
"La Araucana" in a wide geometric rounded lowercase sans, with "más cerca" in an orange handwritten
script that deliberately breaks through the bottom edge. Warm and informal:
friendly-institutional rather than state-institutional.
Source: https://www.laaraucana.cl/

**Bendita IA.** Near-black `#0a0a0a` / `#1c1c1e`, orange `#d4772c` / `#e8944a` / `#f09433`, violet
`#8b5cf6`, navy `#0a2540`. Led by Felipe Pacheco, Anthropic's Community Ambassador in Chile.

**One discrepancy to check with the organisers, recorded and not resolved.** The English page at
benditaia.cl/en describes a Claude Impact Lab on **financial inclusion**, co-hosted with FinteChile
and the Chile Fintech Forum, 200 builders over 48 hours, with no reference to Longevidad or Caja La
Araucana. These may be two separate Labs, or the page may be stale. This does not contradict
`CLAUDE.md`, which is the team's authority; it is recorded so nobody inherits an assumption.
Source: https://benditaia.cl/en

## 3. Guidance for older adults

Thin. There is no Chilean equivalent of a "design for older adults" standard.

SENAMA's `Guía de Orientaciones para la Inclusión Digital de Personas Mayores`, produced with HelpAge
International, says support materials must be made *"con letra grande, con contraste de color y
lenguaje sencillo"*, and recommends a colour manual with step-by-step instructions and clear
illustrations. Note that it endorses colour and illustration as comprehension aids, not decoration.

SENADIS specifies sans-serif ("palo seco") as the accessible default. The state's own practical
baseline, from the Kit Digital framework, is 16px scaling to 20px and 24px on user request.

Searched for and **not found**: any SENAMA, MINSAL or "Más Adultos Mayores Autovalentes" document
specifying type sizes, colour values or contrast ratios for older-adult health materials. Confidence
that no such published Chilean design norm exists: moderate.

Source: https://www.senama.gob.cl/storage/docs/guiadeorientacionesinclusiondigital.pdf

The Kit Digital framework's own typography rationale transfers directly to our patients, verbatim:
*"Esta tipografía fue seleccionada por ser una familia diseñada para facilitar la lectura, sobre todo
en móviles, ya que es la tipografía por defecto en dispositivos con sistema operativo Android."* The
Chilean state picked Roboto because its citizens read on Android phones. Ours are on Android phones
reading WhatsApp.

## 4. The LatAm digital-health field, and what is exhausted

Inspected directly by fetching stylesheets, downloading logo files, reading SVG source and sampling
rendered images.

| Product | Mark | Colours |
|---|---|---|
| Examedi (CL) | Lowercase geometric wordmark, roof chevron over a medical cross | `#4773ff`, accent `#fdc700` |
| Rayen Salud (CL) | Split wordmark, "RAYEN" grey / "SALUD" blue, over a green-blue swoosh | `#6e6f71`, `#30b5e4`, `#2aa9e0` |
| Imed (CL) | Two-colour wordmark only, viewBox 3.5:1 | `#092f6d`, `#05c08a` |
| Cero (CL) | Pure black four-letter lowercase wordmark, no symbol; avatar is white on a magenta-purple-blue gradient | `#000000`, gradient near `#9e23f7` |
| Hospital Digital / MINSAL | Gobierno de Chile seal, flat white paths | `#5a7b8c`, `#3b6e9e`, `#2d5a7f`, bg `#ecf7fb` |
| Doctoralia | Path-drawn wordmark, viewBox 5.75:1; app icon is an abstract green starburst | `#00A085` |
| 1DOC3 | Rounded wordmark with O's as circles and a `+` substitution; app icon is a white cross in a blue circle | `#4486ff` |
| mediQuo | Near-black wordmark plus a separate square 59x59 speech-bubble avatar | `#0A0A22` |
| Salud Savia (MAPFRE) | Inherits MAPFRE corporate red; Circular Std | `#d81e05` |
| Tucuvi (ES) | The closest functional analogue that exists | `#26666e` teal on `#f8f7f5`, Inter + Lora |

**Tucuvi is worth knowing about.** An AI voice assistant that phones elderly and chronic patients at
home for follow-up and alerts clinicians, deployed with AstraZeneca (AZerca, COPD) and GSK, agent
named "LOLA". Deep teal on warm off-white, and a serif in the type pairing, which is rare in
health-tech and reads warm and editorial rather than clinical-SaaS.

**Cero is the competitor.** Chilean, Y Combinator S21, coordinates appointments and chronic-treatment
adherence over WhatsApp, reportedly 350+ health centres. Their site refused connection; this comes
from YC and Endeavor profiles. "How is this different from Cero" is a pitch question worth an answer.
Sources: https://www.ycombinator.com/companies/cero , https://endeavor.cl/company/cero

**Medication-adherence app icons, viewed at 256px:** MyTherapy is a single crimson capsule; Medisafe
is two interlocking white capsule outlines on a blue gradient; Max is a dog mascot; 1DOC3 is a white
cross in a blue circle; Doctoralia is an abstract green starburst.

### Exhausted, and why each is disqualified

1. **The capsule.** Two of three medication apps use it and nothing else. It says "reminder app",
   which is the smaller thing PreventIA is not. It also promises something the product is
   contractually forbidden from doing: PreventIA never indicates, changes or doses a treatment.
2. **The medical cross**, especially white-in-a-blue-circle. The most generic mark in the sweep. In
   Chile a red cross additionally reads emergency / Cruz Roja.
3. **The swoosh or wave under a wordmark.** Reads as 2010s health-corporate.
4. **Default health blue.** Examedi `#4773ff`, 1DOC3 `#4486ff`, Rayen `#30b5e4`, Imed navy, Hospital
   Digital's blue-greys, and Kit Digital's own `#006fb3`. A blue PreventIA is invisible in this field.
5. **The heartbeat / ECG line.** Not observed in any logo inspected, which itself says it is beneath
   these brands.
6. **The stethoscope, and caring-hands-cradling-something.**
7. **A friendly robot avatar.** It also fights the clinical positioning: PreventIA must never look
   like it is the one making decisions.
8. **A wide horizontal wordmark as the only asset.** Doctoralia at 5.75:1 and Imed at 3.5:1 are
   physically unusable as a WhatsApp profile picture, which for us is the primary surface.
9. **Gradient-mesh AI aesthetics**, neural nodes, glowing brains. Signals "AI startup" to a panel
   that is clinical, governmental and management.

### The "-IA" wordplay: one precedent, and its own warning

`retinIA` by PROSPERiA (Mexico), a diabetic-retinopathy screening tool, solves exactly our problem
with three stacked devices: colour split ("retin" `#0d1d41`, "IA" `#00aec5`, both sampled from the
logo file), case split, and letterform split with a crossbar-less A that repeats in the tagline.

The parent brand is the cautionary half. Counting across their own two sites: `prosperia` lowercase
119 times, `PROSPERiA` 20, plus `Prosperia`, `ProsperIA`, `retinIA`, `RetinIA`, `retiniA`, `retinia`.
**They cannot hold their own casing in running text, and neither will we.** The mark has to survive a
clinician typing "Preventia" in an email.

Searched specifically for other Spanish "-IA" pun brands and found no other verifiable examples. One
well-executed instance is not a trend.

Sources: https://retinia.mx/ , https://www.prosperia.health/

### One further note on avatars

Boti, the Buenos Aires city chatbot on WhatsApp since 2019 with 58M+ conversations, used by the
Ministry of Health for COVID triage, **does not put its character avatar in its WhatsApp profile
photo**. Verbatim: *"si bien el avatar de Boti no aparece en la foto de perfil de la cuenta de
WhatsApp, sí es cierto que en todas las comunicaciones y cartelería que hace el Municipio de Buenos
Aires sobre el asistente, se incluye la identidad visual de Boti."*
Source: https://planetachatbot.com/identidad-visual-chatbot-concepto-y-ejemplos/

## 5. Clinical triage colour, recorded for later

Parked. Not applied to the current asset build, kept because it is the argument a clinical judge will
ask for and re-deriving it costs a day.

**Chile already has the semáforo.** MINSAL adopted an ESI-based five-level categorización in 2018.
Colours extracted from a public patient-facing sheet, Dirección Comunal de Salud, Los Ángeles:

| Category | Colour | Hex | Meaning |
|---|---|---|---|
| C1 | rojo | `#d2232a` | Emergencia con riesgo vital |
| C2 | anaranjado | `#f26921` | Emergencia grave |
| C3 | amarillo | `#fff200` | Emergencia de mediana gravedad |
| C4 | verde | `#40ad49` | No urgente, resolvible en SAPU |
| C5 | azul | `#00aeef` | Consulta de salud general |

The hexes are that publisher's rendering; MINSAL specifies the colours by name only, and no national
hex standard was found. Source: https://www.losangeles.cl/archivos/categoriasurgencia.pdf

**A Chilean clinician already reads rojo/amarillo/verde in our direction.** Our three-state semáforo
is C1/C3/C4 collapsed. Saying that out loud is worth more than any palette argument.

Other systems, for the record: Manchester Triage is five colours (red, orange, yellow, green, blue)
with no published hex spec. **ESI has no colours at all** — I searched all 36 pages of the Fifth
Edition handbook and the only hits are clinical prose. Colour is a presentation layer implementations
add. START/SALT mass-casualty uses red/yellow/green/black, where green means "walking wounded" and
black is a real category; do not import those semantics into chronic-care follow-up.

**NEWS2 is the item to lead with if this is ever revisited.** The Royal College of Physicians
redesigned the NEWS2 chart because, verbatim, *"the red/amber/green scale in the original NEWS chart
was problematic for those with red-green colour-blindness"*. Their fix was not better reds and
greens: they deleted green from the severity scale and replaced hue opposition with a luminance ramp
in one warm hue family. Extracted from a deployed NHS Lothian chart: score 1 `#faf0ab`, score 2
`#feca8b`, score 3 `#f6977f`, strictly ordered by luminance `[computed]` 0.856 / 0.652 / 0.433.
Sources: https://www.rcp.ac.uk/media/a4ibkkbf/news2-final-report_0_0.pdf ,
https://policyonline.nhslothian.scot/wp-content/uploads/2023/03/NEWS_Chart.pdf

Published palettes retrieved from their own npm packages rather than their docs: NHS
`#d5281b` / `#007f3b` / `#ffb81c`; GOV.UK v5 `#d4351c` / `#00703c` / `#ffdd00`; GOV.UK v6 moved green
to `#0f7a52`; IBM Carbon `#da1e28` / `#24a148` / `#f1c21b` light and `#ff8389` / `#42be65` / `#f1c21b`
dark; USWDS `#d54309` / `#00a91c` / `#ffbe2e`; HSE Ireland `#B30638` / `#02A78B` / `#FFDE0E`.
Okabe-Ito, empirically tested and recommended by *Nature Methods*: `#E69F00`, `#56B4E9`, `#009E73`,
`#F0E442`, `#0072B2`, `#D55E00`, `#CC79A7`, `#000000`.

IEC 60601-1-8 assigns red to high-priority alarms, yellow to medium and cyan to low. `UNVERIFIED`
against the standard text, which is paywalled; corroborated across independent secondary sources.
The one directly useful point: in device-alarm grammar green is not an alarm priority at all, it is
"ready for use", which is arguably the correct reading of a check-in with no findings. Independently
of any regulatory question, **do not flash anything**: a red flashing at 1.4-2.8 Hz is a trained
signal meaning "act now at this bedside", and this is an asynchronous review queue.

Whether a colour choice could imply a regulated-device claim is a regulatory and legal question and
is not answered here. Device classification turns on intended purpose and function, not on visual
styling.

## 6. Local measurements of the shipped tokens `[computed]`

Run locally against `preventia/dashboard/static/tokens.css` using the WCAG relative-luminance formula
and Machado/Oliveira/Fernandes 2009 severity-1.0 matrices. Recorded, not acted on.

The `.caso` row rail is `border-left: 0.5rem solid var(--rail)` on `--surface`.

| Rail on white | Contrast |
|---|---|
| `--sem-green` `#2d717c` | 5.58:1 |
| `--sem-red` `#fe6565` | 2.89:1 |
| `--sem-yellow` `#f2c728` | 1.62:1 |

Greyscale luminance ranks green `0.138` < red < yellow, so green is the darkest of the three.

Kit Digital's high-contrast theme is an exact per-channel inversion (`255 - channel`), so under
`html.contrast-high` the red chip renders teal `#019a9a` and the green chip renders salmon `#d28e83`.
The two themes disagree about which colour means escalate; the text label and the sort order are what
carry the meaning across the two.

Green/red separation, CIE76 dE: normal 89.3, protanopia 23.3, deuteranopia 48.2. For reference the
same figure under deuteranopia is 6 for USWDS, 16 for Carbon, 22 for NHS, 23 for the Chilean
categorización and 32 for GOV.UK. Kit Digital's "green" being a desaturated teal rather than a green
is why it performs comparatively well here, by accident rather than by design.

Working scripts are in the session scratchpad and were not committed.

## 7. Asset specifications

### WhatsApp Business profile

All field limits below are mirrored from BSP documentation (360dialog, Bird, Vonage), not from Meta.
Meta's own reference pages returned HTTP 500 on four URL variants. The upload mechanics were verified
against a Meta page that did load.

| Property | Value |
|---|---|
| Shape | Square, maximum edge 640px |
| Recommended | 640 x 640 |
| Minimum | 192 x 192 |
| Max upload | 5 MB |
| Format | JPEG / PNG. The Resumable Upload API accepts exactly `application/pdf, image/jpeg, image/jpg, image/png, video/mp4` |
| Circle crop | Yes. Documented only in BSP and agency material, never in a Meta spec |

Bird's docs say "max size of 63KB" while every other BSP says 5 MB. The likely reconciliation, which I
could not prove: 63 KB is what WhatsApp stores after re-encoding, 5 MB is the input ceiling. Upload a
640x640 PNG and let Meta re-encode rather than hand-optimising.

A circle inscribed in a 640 square discards about 21.5% of the canvas at the corners. There is no
published safe area; keeping load-bearing marks inside a centred 576px circle leaves 32px of bleed.
The avatar also renders at roughly 40-56px in a chat list, which is why it must be the mark alone.

Profile text fields: `about` 1-139 characters, `address` max 256, `email` max 128, `websites` max 2
URLs at 256 characters each and must include the scheme, `vertical` from a fixed enum where ours is
`HEALTH`. **`description` is contested**: 360dialog says 512, Vonage and Bird say 256. Write to 256,
valid under both readings. 360dialog also documents that `vertical` cannot be set back to empty once
created.

These fields are patient-facing. An 80-year-old opens the contact card and reads `about` and
`description`. They are Chilean Spanish, *usted*, plain register, and they must not read as an offer
to diagnose or to manage treatment. Write them with the clinical teammate.

Upload flow, verified: `POST /{APP_ID}/uploads` with `file_length`, `file_name`, `file_type` returns
an upload session id; `POST /{UPLOAD_SESSION_ID}` with header `file_offset: 0` and the **raw bytes as
the body** returns a handle; `POST /{PHONE_NUMBER_ID}/whatsapp_business_profile` with
`profile_picture_handle`. Two gotchas: the upload endpoints use `Authorization: OAuth <token>`, not
`Bearer`, and multipart form data causes validation failures where raw bytes succeed.
Source: https://developers.facebook.com/docs/graph-api/guides/upload

### Favicons

Current Evil Martians recommendation. Note the article's title says "six files"; the body specifies
five icons plus a manifest.

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
```

`sizes="32x32"` on the ICO line is load-bearing: it works around a Chrome bug that otherwise makes
Chrome prefer the ICO over the SVG. The ICO is not legacy cruft either, because some tools request
`/favicon.ico` from the server root and never read the link tags. `apple-touch-icon` needs about 20px
of padding and an opaque background, since iOS handles neither transparency nor its own padding. The
maskable safe zone is a centred circle of radius 40% of the icon width, so 409px diameter at 512.

SVG favicon support: Chrome 80+, Firefox 41+, Edge 80+, Safari only from version 26. Roughly 89%
global, which is why the ICO stays.
Sources: https://evilmartians.com/chronicles/how-to-favicon-in-2021-six-files-that-fit-most-needs ,
https://web.dev/articles/maskable-icon , https://caniuse.com/link-icon-svg

### GitHub and social

Social preview: minimum 640 x 320, "1280 by 640 pixels for best display", under 1 MB, PNG/JPG/GIF, no
required aspect ratio. Open Graph: Facebook recommends 1200 x 630 at 1.91:1, max 8 MB. The ubiquitous
1200x628 figure appears in no primary source I could reach. X's card spec pages now redirect or
return HTTP 402, so no X-specific dimension here is verifiable; 1200x630 satisfies every secondary
reading.

Light/dark swap in a README, GitHub's own GA syntax:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="logo-dark.png">
  <img alt="PreventIA" src="logo-light.png">
</picture>
```

One `<source>` only, for dark; `alt` goes on the `<img>`. The older `#gh-dark-mode-only` fragment
trick still works and, contrary to widespread claims, neither GitHub changelog uses the word
"deprecated".
Sources: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview ,
https://github.blog/changelog/2022-08-15-specify-theme-context-for-images-in-markdown-ga/

### SVG portability

GitHub states plainly: "SVGs don't currently support inline scripting or animation", and "If you are
using the Firefox browser, SVGs on GitHub may not render." That last line is a live risk for a README
logo with no workaround other than a PNG fallback.

`<img src="logo.svg">` in a README works, because GitHub never inspects the referenced file. Raw
inlined `<svg>` in Markdown is stripped: the html-pipeline sanitiser allowlist contains 59 elements
and includes no `svg`, `style`, `script`, `filter`, `mask`, `clipPath`, `use`, `text`, `defs` or
gradient elements, and neither `class` nor `style` appears in its attribute allowlist.

**Why text must become paths.** When an SVG loads via `<img>`, `background-image`, `<picture>` or as a
favicon, MDN's restricted mode applies: JavaScript is disabled and "external resources (e.g., images,
stylesheets) cannot be loaded, though they can be used if inlined through `data:` URLs". So
`@font-face` cannot load. A `<text>` element naming an installed font is not blocked, but it falls
back to whatever the rendering machine has, which differs between a laptop, a reader's browser, a
projector and a video encoder. Inline `<style>` with no external reference is preserved, which is why
the dark-mode favicon technique works.

Keep `viewBox`, omit fixed `width`/`height`, so one file scales from 16px to a banner. Use a square
viewBox for anything used as a favicon; non-square SVGs are letterboxed or cropped inconsistently.

**Google Slides cannot import SVG at all** — "Unsupported image type", confirmed by an open Google
issue tracker entry. PowerPoint supports SVG in Microsoft 365 but rasterises on paste, so use
`Insert > Pictures > This Device`. PNG exports are therefore mandatory, not insurance.

SVGs uploaded as GitHub **Release** assets are served as `application/octet-stream` and refuse to
render. Keep the logo in the repo tree.
Sources: https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files ,
https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image ,
https://issuetracker.google.com/issues/302007844

### Deck and video

A PowerPoint 16:9 slide is 13.333 x 7.5 inches, not a pixel size. **Default image export is 96 dpi,
which yields 1280 x 720, not 1920 x 1080** — an unmodified export is 720p and looks soft in a 1080p
recording. At 144 dpi you get 1920 x 1080.
Source: https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/powerpoint/change-export-slide-resolution

## 8. URL record

Retrievals that failed, so nobody repeats them: `developers.facebook.com` business-profile reference
(HTTP 500, four variants); `developer.x.com` card docs (HTTP 402); `m3.material.io` (empty body,
twice); `fonasa.cl` (SSL rejection on the main host, HTTP 403 on the asset host); `cero.cl`,
`medismart.cl`, `levitamagnetics.com` (refused); `rcp.ac.uk`, `service-manual.nhs.uk`,
`design-system.service.gov.uk` (network-blocked, worked around by reading the published npm packages,
which is a stronger source than the docs); IEC 60601-1-8 sample PDFs from iteh.ai, the ANSI webstore
and an mdcpp mirror (all stubs or missing the colour table).

No evidence was found for "Instapp", "Zerca", "SavIA / Salud Digital Chile" or "Medicato" as branded
products. They are unconfirmed rather than checked and dismissed.
