# Kit Digital design tokens, retrieved values

**Date:** 5 August 2026
**Author:** Felipe Carvajal Brown
**Supplies:** `docs/adr/0011-kit-digital-tokens-for-the-clinician-dashboard.md`
**Purpose:** transcription source. Somebody copies values out of this file into CSS. It contains no
CSS and proposes no design.

## Method

`curl` with a desktop Chrome user agent against `framework.digital.gob.cl` and `kitdigital.gob.cl`.
The decisive retrieval was the framework's compiled stylesheet, `css/gob.cl.css`, which ends with a
`sourceMappingURL`. The map at `css/gob.cl.css.map` carries `sourcesContent` for **165 source files**,
of which **88 are the government's own SCSS** rather than vendored Bootstrap. That includes the entire
`themes/a11y-contrast` and `themes/a11y-fonts` trees. Nothing was installed and no package manager was
run; every value below was read from a file the government's own web server returned over HTTPS.

Where a value exists only as a Sass variable that emits no CSS, it is reported from the **compiled**
output and labelled as such. Contrast ratios in section 5 are arithmetic I performed on retrieved hex
values, marked `[computed]`, not claims made by any source.

## Honesty statement

Everything ADR-0011 asked for was retrieved except the Figma UI Kit v3.0.1 tokens. Three things did
**not** come back and are marked `UNVERIFIED` throughout: whether the Figma UI Kit's tokens agree with
the framework's; the government's own `$` variable names for the colour and spacing scales, because
variable-only SCSS partials emit no CSS and so are absent from the source map; and the exact value of
`$a11y-scale-base`, which is derived arithmetically rather than read.

**Three findings contradict the premises ADR-0011 was written on.** They are in section 8. The most
consequential is that the npm package the ADR says does not exist, does exist.

---

## 1. Colour tokens

`html` root custom properties, read verbatim from the `:root` block of the compiled stylesheet.
Source for every row: `https://framework.digital.gob.cl/css/gob.cl.css`

### 1.1 Main palette (the nine the government documents as the palette)

The Spanish label and the framework name are from `https://framework.digital.gob.cl/colors.html`.
The hex is confirmed against the compiled CSS.

| Token name | Label | Value | Source URL |
|---|---|---|---|
| `primary` | Primario | `#006FB3` | https://framework.digital.gob.cl/colors.html |
| `secondary` | Secundario | `#FE6565` | https://framework.digital.gob.cl/colors.html |
| `tertiary` | Terciario | `#0A132D` | https://framework.digital.gob.cl/colors.html |
| `accent` | Acentuar | `#A8B7C7` | https://framework.digital.gob.cl/colors.html |
| `neutral` | Neutral | `#EEEEEE` | https://framework.digital.gob.cl/colors.html |
| `gray-a` | Gris oscuro | `#4A4A4A` | https://framework.digital.gob.cl/colors.html |
| `gray-b` | Gris medio | `#8A8A8A` | https://framework.digital.gob.cl/colors.html |
| `black` | Negro | `#111111` | https://framework.digital.gob.cl/colors.html |
| `white` | Blanco | `#FFFFFF` | https://framework.digital.gob.cl/colors.html |

**Caution, documentation error.** The colours page prints an `RGB(...)` caption next to each hex, and
for two of them the caption does not match its own hex. `tertiary #0A132D` is captioned
`RGB(52, 58, 64)`, which is `#343A40`. `accent #A8B7C7` is captioned `RGB(33, 37, 41)`, which is
`#212529`. The **hex values are the correct ones** — they agree with the compiled CSS. Ignore the RGB
captions on that page.

### 1.2 Secondary palette ("Otros colores")

| Token name | Label | Value | Source URL |
|---|---|---|---|
| `purple` | Morado | `#6633CC` | https://framework.digital.gob.cl/colors.html |
| `orange` | Naranjo | `#E0701E` | https://framework.digital.gob.cl/colors.html |
| `orange-light` | Naranjo claro | `#FFA11B` | https://framework.digital.gob.cl/colors.html |
| `green` | Verde | `#2D717C` | https://framework.digital.gob.cl/colors.html |

### 1.3 Complete `:root` custom-property block

Everything the framework exposes as a CSS variable. `#63c` and `#fff` are shorthand in the source and
are reproduced as served.

| Token name | Value | Source URL |
|---|---|---|
| `--blue` | `#006fb3` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--indigo` | `#6610f2` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--purple` | `#63c` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--pink` | `#e83e8c` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--red` | `#fe6565` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--orange` | `#e0701e` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--yellow` | `#f2c728` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--green` | `#2d717c` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--teal` | `#20c997` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--cyan` | `#17a2b8` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--white` | `#fff` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--gray` | `#a8b7c7` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--gray-dark` | `#343a40` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--blue-light` | `#a8b7c7` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--blue-dark` | `#0a132d` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--orange-light` | `#ffa11b` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--black` | `#111` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--primary` | `#006fb3` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--secondary` | `#fe6565` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--success` | `#2d717c` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--info` | `#17a2b8` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--warning` | `#f2c728` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--danger` | `#fe6565` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--light` | `#f8f9fa` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--dark` | `#343a40` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--tertiary` | `#0a132d` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--accent` | `#a8b7c7` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--neutral` | `#eee` | https://framework.digital.gob.cl/css/gob.cl.css |

Note `success` is `#2d717c`, a desaturated teal, not a green; `danger` and `secondary` are the same
value `#fe6565`; there is **no distinct `danger` red**. For a green/yellow/red semáforo this palette
gives you one usable green-ish token and a red that is shared with the general-purpose secondary.

### 1.4 Gray scale

Derived by the framework on top of Bootstrap's. `gray-a`, `gray-b`, `gray-c` are the government's own
additions; `gray-100` through `gray-900` are Bootstrap 4.5 stock and are listed because the contrast
theme inverts them and components use them.

| Token name | Value | Source URL |
|---|---|---|
| `gray-a` | `#4a4a4a` | https://framework.digital.gob.cl/css/gob.cl.css |
| `gray-b` | `#8a8a8a` | https://framework.digital.gob.cl/css/gob.cl.css |
| `gray-c` | `#eee` | https://framework.digital.gob.cl/css/gob.cl.css |
| `gray-100` | `#f8f9fa` | https://framework.digital.gob.cl/css/gob.cl.css |
| `gray-200` | `#e9ecef` | https://framework.digital.gob.cl/css/gob.cl.css |
| `gray-300` | `#dee2e6` | https://framework.digital.gob.cl/css/gob.cl.css |
| `gray-400` | `#ced4da` | https://framework.digital.gob.cl/css/gob.cl.css |
| `gray-500` | `#adb5bd` | https://framework.digital.gob.cl/css/gob.cl.css |
| `gray-600` | `#6c757d` | https://framework.digital.gob.cl/css/gob.cl.css |
| `gray-700` | `#495057` | https://framework.digital.gob.cl/css/gob.cl.css |
| `gray-800` | `#343a40` | https://framework.digital.gob.cl/css/gob.cl.css |
| `gray-900` | `#212529` | https://framework.digital.gob.cl/css/gob.cl.css |
| `body-color` | `#212529` | https://framework.digital.gob.cl/css/gob.cl.css |
| `text-muted` | `#6c757d` | https://framework.digital.gob.cl/css/gob.cl.css |

### 1.5 Documented colour roles

Straight from the colours page, section "Utilización de colores".

| Role | Token | Source URL |
|---|---|---|
| Títulos (headings) | `black` | https://framework.digital.gob.cl/colors.html |
| Párrafos (body copy) | `gray-a` | https://framework.digital.gob.cl/colors.html |
| Íconos | `gray-b` | https://framework.digital.gob.cl/colors.html |
| Fondo (background) | `white` | https://framework.digital.gob.cl/colors.html |
| Bordes | `accent` | https://framework.digital.gob.cl/colors.html |

---

## 2. Typography tokens

### 2.1 Families

| Token name | Value | Source URL |
|---|---|---|
| `$primary-font` (`.font-primary`) | `Roboto, sans-serif` | https://framework.digital.gob.cl/css/gob.cl.css |
| `$accent-font` (`.font-accent`) | `"Roboto Slab", serif` | https://framework.digital.gob.cl/css/gob.cl.css |
| root `font-size` (`html`) | `16px` | https://framework.digital.gob.cl/css/gob.cl.css |

The variable names `$primary-font` and `$accent-font` are verified: they appear in the retrieved
`base/_typography.scss`. Loaded by the documentation site from
`https://fonts.googleapis.com/css?family=Roboto:300,400` and
`https://fonts.googleapis.com/css?family=Roboto+Slab:300,400`, so the weights actually used are
**300 and 400 only**.

Rationale, from the typography page, verbatim: "La tipografía elegida para ser utilizada en este kit
es Roboto, en sus familias Roboto y Roboto Slab. Esta tipografía fue seleccionada por ser una familia
diseñada para facilitar la lectura, sobre todo en móviles, ya que es la tipografía por defecto en
dispositivos con sistema operativo Android." Roboto Slab is restricted to headings: "Sólo debe ser
ocupada en títulos, ya que es una tipografía con un peso visual importante en comparación a Roboto
regular."

**The web framework does not use the gobCL government font.** gobCL is a separate download (section 6)
and appears nowhere in the framework's CSS. Whether the Figma UI Kit v3.0.1 specifies gobCL instead is
`UNVERIFIED`.

### 2.2 Weights

| Token name | Value | Source URL |
|---|---|---|
| `$font-weight-light` | `300` | https://framework.digital.gob.cl/css/gob.cl.css |
| `$font-weight-normal` | `400` | https://framework.digital.gob.cl/css/gob.cl.css |
| `$font-weight-bold` | `700` | https://framework.digital.gob.cl/css/gob.cl.css |

### 2.3 Type scale

The scale is responsive with a single breakpoint at **768px** (`@include media($from: tablet)`).
Both columns are needed. Base applies below 768px; `>= 768px` is the desktop value, and a clinician
workstation is always in the second column.

Source for every row: `https://framework.digital.gob.cl/css/gob.cl.css`, cross-checked against
`https://framework.digital.gob.cl/typography.html` which documents only the `>= 768px` sizes.

| Element | Family | Weight | Size (base) | Line height (base) | Size (>=768px) | Line height (>=768px) |
|---|---|---|---|---|---|---|
| `h1` / `.h1` | Roboto Slab | 400 | `1.5rem` | `2.88rem` | `2.4rem` | `3.6rem` |
| `h2` / `.h2` | Roboto Slab | 400 | `1.25rem` | `1.625rem` | `1.6875rem` | `1.625rem` |
| `h3` / `.h3` | Roboto Slab | 400 | `1.23125rem` | `1.625rem` | `1.4375rem` | `1.625rem` |
| `h4` / `.h4` | Roboto | 300 | `1.0625rem` | `1.4625rem` | `1.25rem` | `1.625rem` |
| `h5` / `.h5` | Roboto Slab | 400 | `1.0625rem` | `1.1875rem` | `1.25rem` | `1.625rem` |
| `h6` / `.h6` | Roboto Slab | 400 | `1rem` | `1.5rem` | `1.125rem` | `1.5rem` |
| `body` | Roboto | 400 | `0.9rem` | `1.35rem` | `1rem` | `1.375rem` |
| `p` | Roboto | 400 | `0.9rem` | `1.35rem` | `1rem` | `1.375rem` |
| `q` | Roboto, italic | 400 | `1rem` | `1.1875rem` | `1rem` | `1.1875rem` |
| `small` | Roboto | 400 | `0.6875rem` | `1.5rem` | `0.6875rem` | `1.5rem` |

Note `h4` is the only heading in Roboto rather than Roboto Slab, and the only one at weight 300.
Note `h4` and `h5` are the same size at both breakpoints and differ only in family and line height.

### 2.4 Named size steps (`.font-level-1` ... `.font-level-8`)

The framework's own size-only scale, decoupled from heading semantics. This is the more useful
transcription target: it lets a queue row use a size without claiming a heading level. Source for
every row: `https://framework.digital.gob.cl/css/gob.cl.css`

| Token name | Size (base) | Line height (base) | Size (>=768px) | Line height (>=768px) | Corresponds to |
|---|---|---|---|---|---|
| `.font-level-1` | `1.5rem` | `2.88rem` | `2.4rem` | `3.6rem` | h1 |
| `.font-level-2` | `1.25rem` | `1.625rem` | `1.6875rem` | `1.625rem` | h2 |
| `.font-level-3` | `1.23125rem` | `1.625rem` | `1.4375rem` | `1.625rem` | h3 |
| `.font-level-4` | `1.0625rem` | `1.4625rem` | `1.25rem` | `1.625rem` | h4 |
| `.font-level-5` | `1.0625rem` | `1.1875rem` | `1.25rem` | `1.625rem` | h5 |
| `.font-level-6` | `1rem` | `1.5rem` | `1.125rem` | `1.5rem` | h6 |
| `.font-level-7` | `0.9rem` | `1.35rem` | `1rem` | `1.375rem` | body, p |
| `.font-level-8` | `0.6875rem` | `1.5rem` | `0.6875rem` | `1.5rem` | small |

Documented as: "corresponden a los font-level, `.font-level-1` a `.font-level-8`, las cuales
implementan sólo el tamaño de la fuente y el alto de la línea de los estilos tipográficos de títulos,
más el body default y párrafos."
(https://framework.digital.gob.cl/typography.html)

### 2.5 Documented text colours

| Role | Colour | Source URL |
|---|---|---|
| Body default | `#212529` | https://framework.digital.gob.cl/typography.html |
| Párrafos | `#4a4a4a` | https://framework.digital.gob.cl/typography.html |
| Links | `#111` | https://framework.digital.gob.cl/typography.html |
| Small | `#212529` | https://framework.digital.gob.cl/typography.html |
| Citas | `#4a4a4a` | https://framework.digital.gob.cl/typography.html |

Links are additionally `text-decoration: underline` by default, and keep the same colour on hover
(`base/_typography.scss`, retrieved via the source map).

---

## 3. Spacing tokens

The spacing scale is **Bootstrap 4.5 stock, unmodified**. The framework adds no steps and changes no
values. I checked the emitted `.m-0`..`.m-5` and `.p-0`..`.p-5` utilities; the ladder stops at 5,
which is the stock `$spacers` map. Source for every row:
`https://framework.digital.gob.cl/css/gob.cl.css`

| Token name | Value | rem | px at 16px root |
|---|---|---|---|
| `$spacers[0]` | `0` | `0` | 0 |
| `$spacers[1]` | `.25rem` | 0.25 | 4 |
| `$spacers[2]` | `.5rem` | 0.5 | 8 |
| `$spacers[3]` | `1rem` | 1 | 16 |
| `$spacers[4]` | `1.5rem` | 1.5 | 24 |
| `$spacers[5]` | `3rem` | 3 | 48 |

Negative margins `-1` to `-5` are emitted at the same magnitudes.

### 3.1 Layout tokens

| Token name | Value | Source URL |
|---|---|---|
| `$grid-gutter-width` | `30px` (`.row` margin `-15px` each side) | https://framework.digital.gob.cl/css/gob.cl.css |
| Container horizontal padding | `15px` | https://framework.digital.gob.cl/css/gob.cl.css |
| `$border-width` | `1px` | https://framework.digital.gob.cl/css/gob.cl.css |
| `$border-color` | `#dee2e6` | https://framework.digital.gob.cl/css/gob.cl.css |
| `$border-radius` | `0` (`.rounded { border-radius: 0 }`) | https://framework.digital.gob.cl/css/gob.cl.css |
| `$button-padding-y` | `18px` | https://framework.digital.gob.cl/css/gob.cl.css |

**`$border-radius` is zero.** The government kit is square-cornered. That is a deliberate token, not
an omission, and it is the single cheapest visual cue that a dashboard follows this system.

### 3.2 Breakpoints

Bootstrap's five plus one government addition, `ss: 375px`.

| Token name | Value | Source URL |
|---|---|---|
| `--breakpoint-xs` | `0` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--breakpoint-ss` | `375px` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--breakpoint-sm` | `576px` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--breakpoint-md` | `768px` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--breakpoint-lg` | `992px` | https://framework.digital.gob.cl/css/gob.cl.css |
| `--breakpoint-xl` | `1200px` | https://framework.digital.gob.cl/css/gob.cl.css |

Container max-widths: `576px -> 540px`, `768px -> 720px`, `992px -> 960px`, `1200px -> 1140px`.

---

## 4. The accessibility themes

This is the section ADR-0011 called "the part that matters clinically". Both themes were retrieved in
full SCSS source from the framework's own source map, plus their compiled output, plus the
documentation page that explains the toggle.

Primary sources:
- `https://framework.digital.gob.cl/accessibility.html` (behaviour, documented by the government)
- `https://framework.digital.gob.cl/css/gob.cl.css.map` (88 SCSS source files including both themes)
- `https://framework.digital.gob.cl/css/gob.cl.css` (resolved values)

### 4.1 How both themes are activated

Identical mechanism for both: **a class on the `<html>` element**. Nothing else. No media query, no
CSS custom property swap, no JavaScript beyond the toolbar that sets the class.

Verbatim, on the font theme: "el framework incluye 3 clases, las cuales son aplicadas al tag `html`
del sitio al momento de activar y el cambio desde el toolbar."

Verbatim, on the contrast theme: "Al activar el modo contraste, siguiendo el mismo mecanismo que en el
aumento del tamaño de la fuente, la clase `.a11y-contrast` es aplicada al tag `html` del sitio."

This is the whole pattern ADR-0011 adopted, and it is cheap: one class on `<html>`, everything else
cascades. It costs nothing to reproduce and does not require any Kit Digital code.

### 4.2 `a11y-fonts` — the font-size theme

**Three steps, not two.** The base is a real named step, which matters: it means the "off" state is
addressable as a class rather than as the absence of one.

| Token name | Root `font-size` | Scale factor vs base | Source URL |
|---|---|---|---|
| `.a11y-font-0` | `16px` | 1.00 | https://framework.digital.gob.cl/accessibility.html |
| `.a11y-font-1` | `20px` | 1.25 | https://framework.digital.gob.cl/accessibility.html |
| `.a11y-font-2` | `24px` | 1.50 | https://framework.digital.gob.cl/accessibility.html |

Verbatim: "Por defecto, los niveles de tamaño son 16px, 20px y 24px". The factors 1.25 and 1.50 are
`[computed]` from those three px values.

**The scaling mechanism is the rem cascade, not a second type scale.** The theme changes the root
font-size and everything expressed in `rem` follows. Verbatim: "el tamaño de la fuente base es
aumentado con lo que el tamaño de todos los textos definidos en `rem` son escalados." I confirmed this
negatively as well: there is **no** `.a11y-font-1 h1`, `.a11y-font-1 p` or `.a11y-font-1 .font-level-N`
rule anywhere in the compiled CSS. The themes contain no font-size declarations for text at all.

The consequence for transcription is the important one: **every size token in section 2 must be
authored in `rem`, never `px`, or the font theme silently does nothing.**

What `themes/a11y-fonts` actually contains is **reflow machinery** — utilities that let a layout
rearrange when text gets bigger, because a queue row that was readable at 16px overflows at 24px.
Four mixins, retrieved from `themes/a11y-fonts/abstracts/_mixins.scss`:

| Mixin | Emits | Purpose |
|---|---|---|
| `make-a11y-columns($base-class)` | `.a11y-font-N-col{-bp}-{1..12}`, `-offset-`, `-order-` | Re-span the grid at a larger size |
| `make-a11y-texts($base-class)` | `.a11y-font-N-text-{left,right,center,...}`, weight and colour utilities | Re-align and re-weight text |
| `make-a11y-spacings($base-class)` | `.a11y-font-N-{m,p}{t,r,b,l,x,y}{-bp}-{0..5}` | Re-space at a larger size |
| `make-a11y-flex($base-class)` | `.a11y-font-N-flex-*`, `justify-content`, `align-*` | Re-flow flex containers |

Documented usage, verbatim: "Para la adaptación de columnas, se puede utilizar la clase
`.a11y-font-1-col-12` para que el texto utilice una columna de 12 espacios al momento de aplicar el
primer aumento de tamaño del texto." There is also an any-step prefix: "cuando requiera aplicar cambios
independiente del nivel de aumento del tamaño de la fuente podrá utilizar el prefijo `.a11y-fonts`.
Por ejemplo, `.a11y-fonts-d-none`."

**Component compensation.** Components shrink their own padding as text grows, so a button does not
become enormous. From `themes/a11y-fonts/components/_buttons.scss`, retrieved verbatim:

```
padding-top: ($button-padding-y - ($a11y-scale-base * $index));
padding-bottom: ($button-padding-y - ($a11y-scale-base * $index));
```

Resolved in the compiled CSS to `18px` at step 0, `14px` at step 1, `10px` at step 2. So
`$button-padding-y = 18px` (verified) and **`$a11y-scale-base = 4px`** — that value is `[derived]`
from the 18/14/10 progression, not read from source, because the variables file emits no CSS.
Marked `UNVERIFIED` as a literal source value; the arithmetic is unambiguous but the declaration was
never seen.

The navbar theme (`themes/a11y-fonts/layout/_navbar.scss`) additionally hides secondary navigation at
steps 1 and 2 (`.nav-behavior { display: none }`, `.nav-separator { display: none }`) and forces the
search field to full width. **That is the pattern worth stealing for a triage queue**: at the largest
step, drop the columns that are not the decision, rather than shrinking everything.

### 4.3 `a11y-contrast` — the contrast theme

**What it substitutes.** Retrieved from `themes/a11y-contrast/base/_base.scss` and
`themes/a11y-contrast/base/_typography.scss`, with values resolved from the compiled CSS.

| Surface | Normal | Contrast mode | Source URL |
|---|---|---|---|
| `body` text | `#212529` | `#eee` | https://framework.digital.gob.cl/css/gob.cl.css |
| `body` background | `#fff` | `#212529` | https://framework.digital.gob.cl/css/gob.cl.css |
| `p` | `#4a4a4a` | `#b5b5b5` | https://framework.digital.gob.cl/css/gob.cl.css |
| `a`, `a:hover` | `#111` | `#eee` | https://framework.digital.gob.cl/css/gob.cl.css |
| `.card` background | `#fff` | `#212529` | https://framework.digital.gob.cl/css/gob.cl.css |

**The full inverted palette.** Every named colour and its contrast-mode counterpart, read from the
resolved `.a11y-contrast .text-{name}` rules. Source for every row:
`https://framework.digital.gob.cl/css/gob.cl.css`

| Token name | Normal | Contrast mode |
|---|---|---|
| `primary` | `#006fb3` | `#ff904c` |
| `secondary` | `#fe6565` | `#019a9a` |
| `tertiary` | `#0a132d` | `#f5ecd2` |
| `accent` | `#a8b7c7` | `#574838` |
| `neutral` | `#eee` | `#111` |
| `success` | `#2d717c` | `#d28e83` |
| `info` | `#17a2b8` | `#e85d47` |
| `warning` | `#f2c728` | `#0d38d7` |
| `danger` | `#fe6565` | `#019a9a` |
| `light` | `#f8f9fa` | `#070605` |
| `dark` | `#343a40` | `#cbc5bf` |
| `black` | `#111` | `#eee` |
| `white` | `#fff` | `#000` |
| `blue` | `#006fb3` | `#ff904c` |
| `blue-dark` | `#0a132d` | `#f5ecd2` |
| `blue-light` | `#a8b7c7` | `#574838` |
| `indigo` | `#6610f2` | `#99ef0d` |
| `purple` | `#63c` | `#9c3` |
| `pink` | `#e83e8c` | `#17c173` |
| `red` | `#fe6565` | `#019a9a` |
| `orange` | `#e0701e` | `#1f8fe1` |
| `orange-light` | `#ffa11b` | `#005ee4` |
| `yellow` | `#f2c728` | `#0d38d7` |
| `green` | `#2d717c` | `#d28e83` |
| `teal` | `#20c997` | `#df3668` |
| `cyan` | `#17a2b8` | `#e85d47` |
| `gray` | `#a8b7c7` | `#574838` |
| `gray-a` | `#4a4a4a` | `#b5b5b5` |
| `gray-b` | `#8a8a8a` | `#757575` |
| `gray-c` | `#eee` | `#111` |
| `gray-dark` | `#343a40` | `#cbc5bf` |
| `gray-100` | `#f8f9fa` | `#070605` |
| `gray-200` | `#e9ecef` | `#161310` |
| `gray-300` | `#dee2e6` | `#211d19` |
| `gray-400` | `#ced4da` | `#312b25` |
| `gray-500` | `#adb5bd` | `#524a42` |
| `gray-600` | `#6c757d` | `#938a82` |
| `gray-700` | `#495057` | `#b6afa8` |
| `gray-800` | `#343a40` | `#cbc5bf` |
| `gray-900` | `#212529` | `#dedad6` |
| `body-color` | `#212529` | `#dedad6` |
| `text-muted` | `#6c757d` | `#938a82` |

**How the substitution is computed, and this is the finding that matters.** Every value above is an
exact per-channel RGB inversion: `255 - channel`. `#006fb3` becomes `#ff904c`; `#f2c728` becomes
`#0d38d7`; `#111` becomes `#eee`. The SCSS confirms it — the theme calls Sass's built-in `invert()`
and wrappers named `invert-color()`, `invert-theme-color()`, `invert-gray()`, over a
`$invert-theme-colors` map.

**The contrast theme is a mathematical colour inversion. It is not a palette tuned to a contrast
ratio.** The one exception is the page background, which is `#212529` rather than the `#000` a strict
inversion of `#fff` would give — so somebody did hand-tune exactly one value.

**What ratio it targets.** The documentation states a target but does not claim conformance. Verbatim:

> "Cabe señalar que los colores a utilizar en el modo contraste deben seguir la recomendación
> mencionada en la documentación de Bootstrap (WCAG 2.0 color contrast ratio of 4.5:1) respecto a la
> razón de contraste de colores."

Read that carefully: it says colours used in contrast mode **ought to** follow a 4.5:1 recommendation,
and it sources the recommendation to Bootstrap's docs rather than to WCAG directly. It is an
instruction to the developer, not a property of the shipped palette. Section 5 shows the shipped
palette does not meet it.

**How a component declares its contrast counterpart.** The pattern is a **mirrored file tree**. For
every component file at `components/X.scss` there is a counterpart at
`themes/a11y-contrast/components/X.scss` that re-declares the same selector with inverted values, and
the whole theme tree is emitted scoped under the `.a11y-contrast` ancestor. Retrieved verbatim, the
entire contents of `themes/a11y-contrast/components/cards/_base.scss`:

```scss
.card {
  background-color: $invert-body-bg;
}
```

And `themes/a11y-contrast/components/_buttons.scss`:

```scss
.btn {
  color: invert($body-color);

  @include hover {
    color: invert($body-color);
  }

  &:focus,
  &.focus {
    box-shadow: $invert-btn-box-shadow;
  }

  @each $color, $value in $invert-theme-colors {
    &.btn-#{$color} {

      @include button-variant($value, $value);
    }
    ...
  }
}
```

The mirrored tree has **31 files** covering base, typography, toolbar, search, ten card variants,
close, collapsibles, buttons, breadcrumb, pagination, social, navtabs, line, navbar, four section
types, footer, forms, custom-forms, sidebar, news, and two vendor integrations. That is the honest
measure of what ADR-0011's "contrast handling has to be built rather than inherited" costs: one
counterpart declaration per component that carries a colour.

**Note a spelling defect in the shipped framework.** The contrast background utility is emitted as
`.a11y-contarst-bg-{color}` — "contarst", transposed — for all 40 colours. The text utility
`.a11y-contrast-text-{color}` is spelled correctly. If anyone copies class names rather than values,
copy the typo or the rule will not match. Source: `https://framework.digital.gob.cl/css/gob.cl.css`.

---

## 5. Contrast ratios of the retrieved palettes `[computed]`

These are my own WCAG 2.x relative-luminance calculations on the hex values above. No source asserts
them. I ran them because ADR-0011 commits the dashboard to WCAG 2.2 AA and the palette has to be
checked before it is transcribed, not after.

AA normal text requires 4.5:1; AA large text (>=18.66px bold or >=24px) requires 3:1.

### 5.1 Normal mode, on white `#fff`

| Foreground | Ratio | AA normal | AA large |
|---|---|---|---|
| `body-color` `#212529` | 15.43 | PASS | PASS |
| `black` `#111` | 18.88 | PASS | PASS |
| `gray-a` `#4a4a4a` | 8.86 | PASS | PASS |
| `primary` `#006fb3` | 5.35 | PASS | PASS |
| `green` / `success` `#2d717c` | 5.58 | PASS | PASS |
| `gray-b` `#8a8a8a` | 3.45 | **FAIL** | PASS |
| `secondary` / `danger` `#fe6565` | 2.89 | **FAIL** | **FAIL** |
| `warning` `#f2c728` | 1.62 | **FAIL** | **FAIL** |

### 5.2 Contrast mode, on `#212529`

| Foreground | Ratio | AA normal | AA large |
|---|---|---|---|
| `black` inverted `#eee` | 13.30 | PASS | PASS |
| `gray-a` inverted `#b5b5b5` | 7.52 | PASS | PASS |
| `primary` inverted `#ff904c` | 6.87 | PASS | PASS |
| `success` inverted `#d28e83` | 5.83 | PASS | PASS |
| `danger` inverted `#019a9a` | 4.47 | **FAIL** (marginal) | PASS |
| `warning` inverted `#0d38d7` | 1.88 | **FAIL** | **FAIL** |

### 5.3 What this means for the semáforo, stated plainly

The three colours a green/yellow/red traffic light needs are the three worst performers in this
palette. `warning` `#f2c728` on white is **1.62:1** — it is unreadable as text and fails even the
non-text 3:1 threshold. `danger` `#fe6565` on white is **2.89:1** and fails at every size. Inverted,
`warning` is **1.88:1**, which is worse than useless in the mode that exists to help people see.

Kit Digital's palette was built for public information sites where yellow and red are decorative
accents, not for a screen where a colour encodes clinical urgency. Transcribing `warning` and `danger`
as semáforo colours would produce a dashboard that fails the accessibility standard the ADR commits
to, while carrying government tokens as the justification.

This is a decision for Felipe, not for the transcriber, and it is the main thing this retrieval turned
up that ADR-0011 could not have anticipated. The options are roughly: keep Kit Digital tokens for
chrome and typography but derive the three semáforo colours separately against a measured 4.5:1;
darken the government values until they pass and document the deviation; or use the government values
only as fills behind AA-passing text and never as the text itself. Section 8 lists this with the other
findings that touch the ADR.

Independently of colour, `CLAUDE.md` section 6's semáforo needs a non-colour encoding anyway. The
SENADIS manual requires it (section 7.2).

---

## 6. The government font, gobCL

Retrieved: `https://kitdigital.gob.cl/archivos/insumos/Tipografia-gobCL.zip` (HTTP 200, 118,030 bytes).
Saved to `assets-staging/kitdigital/Tipografia-gobCL.zip`. Not unpacked into the project.

### 6.1 Contents

| File | Bytes |
|---|---|
| `Tipografía/gobCL/gobCL_Regular.otf` | 36,528 |
| `Tipografía/gobCL/gobCL_Light.otf` | 37,960 |
| `Tipografía/gobCL/gobCL_Bold.otf` | 44,716 |
| `Tipografía/gobCL/gobCL_Heavy.otf` | 44,776 |

**Four weights, OpenType (`.otf`) only.** No `.woff`, no `.woff2`, no `.ttf`. I probed the framework
host for web formats and they do not exist there either: `gobCL_Regular.woff` 404,
`gobCL_Regular.woff2` 404, `gobCL_Regular.ttf` 404, while the four `.otf` files are served at
`https://framework.digital.gob.cl/fonts/gobCL_*.otf` (HTTP 200, identical sizes). Using gobCL on the
web therefore requires converting the OTFs, which is a modification of the files and a separate
licence question.

**The zip contains no licence file, no readme, and no terms document.** Only the four fonts.

### 6.2 Family and weight names, from the OpenType `name` table

Read directly from the binaries.

| File | Family (nameID 1) | Subfamily | Full name | PostScript | Version |
|---|---|---|---|---|---|
| `gobCL_Regular.otf` | `gobCL` | `Regular` | `gobCL` | `gobCL` | not set |
| `gobCL_Light.otf` | `gobCL` | `Light` | `gobCL Light` | `gobCL-Light` | `001.000` |
| `gobCL_Bold.otf` | `gobCL` | `Bold` | `gobCL Bold` | `gobCL-Bold` | `1.000` |
| `gobCL_Heavy.otf` | `gobCL` | `Heavy` | `gobCL Heavy` | `gobCL-Heavy` | `001.000` |

The CSS family name is **`gobCL`**. Designer: Rodrigo Ramirez. Foundry: Frescotype.

### 6.3 Licence text, VERBATIM, not interpreted

This is every licence-bearing string in the four font binaries, reproduced exactly. There is no
`LicenseDescription` (nameID 13) and no `LicenseInfoURL` (nameID 14) record in any of the four files.
The text below is the `Description` record, nameID 10. **A human decides what this permits. I am not
interpreting it and nothing here is legal advice.**

Description (nameID 10) — identical in all four files:

```
Las fuentes gobCL están licenciadas para uso abierto del Gobierno de Chile / gobCL fonts are free licensed for Gobierno de Chile / www.gob.cl
```

Copyright (nameID 0) — `gobCL_Bold.otf`, `gobCL_Light.otf`, `gobCL_Heavy.otf`:

```
(c) 2010 by Rodrigo Ramirez / www.frescotype.com
```

Copyright (nameID 0) — `gobCL_Regular.otf`:

```
©Rodrigo Ramirez, frescotype.com
```

Trademark (nameID 7) — identical in all four files:

```
Gobierno de Chile, 2010
```

Separately, the Kit Digital site footer carries a Creative Commons badge linking to
`http://creativecommons.org/licenses/by/3.0/cl/` (CC BY 3.0 Chile). Observed on
`https://kitdigital.gob.cl/recursos-de-desarrollo/`. Whether that site licence extends to the font
files, which carry their own copyright, is `UNVERIFIED` and is part of the same question for a human.

The npm package that ships the framework declares `"license": "MIT"` (section 8.1). That covers the
framework code, not the gobCL fonts, which are not in it.

---

## 7. Accessibility documents

### 7.1 What was retrieved and saved

| File | Saved as | Bytes | Pages | Source URL |
|---|---|---|---|---|
| Manual de Accesibilidad Web | `assets-staging/kitdigital/Manual-Accesibilidad-Web.pdf` | 17,756,886 | 108 | https://kitdigital.gob.cl/archivos/insumos/nuevos/Manual%20Accesibilidad%20Web.pdf |
| Manual de Accesibilidad Web v2 | `assets-staging/kitdigital/Manual-Accesibilidad-Web-v2.pdf` | 17,799,895 | 108 | https://kitdigital.gob.cl/archivos/Manual%20Accesibilidad%20Web-v2.pdf |
| Recomendaciones para sitios web institucionales | `assets-staging/kitdigital/Recomendaciones-WEB-2026.pdf` | 4,452,237 | 24 | https://kitdigital.gob.cl/archivos/Recomendaciones-WEB-2026.pdf |

**The two manuals are textually identical.** Extracted text matches byte for byte
(md5 `24ea120494d103bc4e0bd4ade90172f5` for both); only the PDF containers differ. `-v2` is the one
currently linked from `https://kitdigital.gob.cl/accesibilidad`; the other path is the one cited in the
earlier research and still resolves. Both were kept so neither provenance is lost. Delete either
freely — `assets-staging/` is in `.gitignore`, so nothing here enters the repository.

The `Recomendaciones-WEB-2026.pdf` turned out **not** to be an accessibility specification. It is
general institutional-web guidance covering objectives, audience, outsourcing, SEO, the gob.cl domain,
cybersecurity, usability, UX/UI and graphic resources. It mentions accessibility only in passing
("accesibilidad de W3C como: lectores de pantalla, aumento y reducción de texto, contraste"). Nothing
in it constrains a table, a status colour or a control. It is not a useful source for this task.

### 7.2 The manual, and what it constrains

Title: *Accesibilidad web en Chile — Guía técnica para la implementación de sitios web accesibles*.
Dated **September 2022**. Developed for SENADIS by Alexandra Cabrera Aravena and Elena Herrera Flores
of Cooperativa Prende Accesibilidad. States "SENADIS, Todos los Derechos Reservados".

**It is written against WCAG 2.1**, with comparison material for 2.0, 2.1 and 2.2 — verbatim, "en sus
pautas de Accesibilidad para el contenido web (WCAG) 2.1". This does not settle open item 2 in the
earlier research about which version Decreto 1/2015 requires; the manual is guidance, not the decree.
ADR-0011's choice of WCAG 2.2 AA remains the way to moot the question.

**Constraints on a data table**, which is what a triage queue is. Verbatim:

> "Las tablas, se usarán para mostrar y organizar datos (`<td>`) y se asociará con sus encabezados
> (`<th>`) de fila y de columna donde se requiera. Los títulos de las tablas (caption) y sus resúmenes
> (summary) deben usarse de forma apropiada."

So: a real `<table>` with `<th>` for both row and column headers where applicable, and a `caption`.
A queue built from `<div>`s does not satisfy this.

**Constraint on status colour.** Criterion 1.4.1, level A, verbatim:

> "1.4.1 Uso del color (A) Evitar el uso de color como única forma de para transmitir el contenido o
> distinguir elementos visuales."

(The doubled "de para" is in the original.) **This binds the semáforo directly.** Green, yellow and red
cannot be the only carrier of the risk level. The level needs a text label, a shape, an icon or a
position as well. Combined with section 5.3, the colour question and the redundant-encoding question
are the same question and should be settled together.

**Contrast thresholds stated in the manual**, all verbatim fragments:

| Requirement | Text |
|---|---|
| Normal text | "contraste de, al menos, 4.5:1, excepto en los siguientes casos" |
| Large text | "tamaño tienen una relación de contraste de, al menos, 3:1" |
| Enhanced (AAA) | "El texto debe tener un contraste con el fondo de al menos una razón de 7:1" |
| Non-text / UI components | "de contraste de al menos 3:1 con los colores adyacentes" |
| Keyboard focus indicator | "una razón de 4.5:1 entre el lugar enfocado con el resto de la" |

Note the last row: the manual asks for **4.5:1 on the focus indicator itself**, and illustrates both a
3:1 and a 4.5:1 example ("Figura 28: contraste 3:1 ... con enfoque de teclado", "Figura 30: contraste
4.5:1 ..."). That is stricter than the WCAG 2.2 AA focus-appearance minimum and it is the kind of
detail a Sandbox reviewer would check.

**Constraints on keyboard-operated controls.** Criterion 2.1.1, level A, verbatim:

> "2.1.1 Teclado Accesible (A) Todas las funciones de las páginas de deberán estar disponibles
> utilizando el teclado o interfaz del teclado (incluye los teclados alternativos), excepto aquellas..."

And the guideline heading: "Directriz 2.1 - Teclado accesible: Poder controlar todas las funciones
desde el teclado."

The manual also covers focus-dependent activation, verbatim: "Activable sólo en enfoque: Si se tiene
una tabla la cual ha sido enfocada, y presionar por ejemplo la tecla 'c' hace que esta se llene de
datos nuevos, pero si no está enfocada, la tecla 'c' no realiza ninguna acción." Relevant if the queue
ever gets keyboard shortcuts for triage actions.

For a triage queue this reduces to: every action on a queue row — open, acknowledge, escalate, mark
resolved — must be reachable and operable by keyboard alone, with a focus indicator meeting 4.5:1.
Reading the queue but only being able to act on it with a mouse fails 2.1.1 at level A, the lowest
level in the standard.

---

## 8. Findings that contradict ADR-0011's premises

ADR-0011 is Accepted and therefore immutable. Nothing here is an edit to it. These are facts that
turned up during retrieval which bear on it, and any change of course is a new ADR and Felipe's call.

### 8.1 The npm package exists

ADR-0011 states "No npm package, CDN or git install path was found" and builds two consequences on it:
"there is no package to install", and the tokens "have to be transcribed by hand".

The framework's own SCSS entry point, served at `https://framework.digital.gob.cl/examples/style.scss`,
is three lines and names the package:

```scss
@import "node_modules/@gobdigital-cl/gob.cl/src/scss/gob.cl";
```

I queried the npm registry HTTP API directly — a plain `GET`, no package manager was run and nothing
was installed:

| Field | Value | Source URL |
|---|---|---|
| Package | `@gobdigital-cl/gob.cl` | https://registry.npmjs.org/@gobdigital-cl%2Fgob.cl |
| Latest version | `3.0.10` | https://registry.npmjs.org/@gobdigital-cl%2Fgob.cl |
| Declared licence | `MIT` | https://registry.npmjs.org/@gobdigital-cl%2Fgob.cl |
| Published versions | 54, from `1.1.2` to `3.0.10` | https://registry.npmjs.org/@gobdigital-cl%2Fgob.cl |
| Repository / homepage | none declared | https://registry.npmjs.org/@gobdigital-cl%2Fgob.cl |

The version numbering is worth noting: latest is **3.0.10**, and the Figma library ADR-0011 points at
is **UI Kit v3.0.1**. The code artefact and the design artefact are on the same major line, and the
code has moved nine patch releases past it.

This does not overturn ADR-0011's decision. The ADR rejected the Framework kit primarily on Bootstrap
4.5 being end-of-life and the kit being marked pending update, and both of those remain true — the
compiled CSS still carries `Bootstrap v4.5.3` in its banner. But the specific reason "there is no
package to install, so it must be hand-transcribed" is not correct, and the global rule against
installing JS dependencies is the operative constraint here regardless.

**Practical consequence: it did not need to be hand-transcribed either way.** The source map gave up
88 SCSS files and the compiled CSS gave up every resolved value, which is how this document was
produced without installing anything.

### 8.2 The contrast theme does not target a ratio, it inverts

ADR-0011 treats the contrast theme as the clinically valuable half of the pattern. The **pattern** is
valuable and it is cheap: one class on `<html>`, a mirrored declaration per component. But the
**palette** the government ships in that mode is an arithmetic inversion, not a tuned high-contrast
set, and section 5.2 shows two of its colours fail AA. Adopting the pattern is sound. Adopting the
inverted values would import the defect.

### 8.3 The semáforo colours are the palette's weakest

Section 5.3. `warning` at 1.62:1 on white and 1.88:1 inverted, `danger` at 2.89:1 on white. Needs a
decision before transcription.

### 8.4 Smaller corrections to the earlier research

- `https://kitdigital.gob.cl/recursos-de-desarrollo/` returns **HTTP 200** with a desktop browser user
  agent, not 404. The page is however effectively empty — it renders a shell with a browser-upgrade
  notice, a privacy-policy link and a Creative Commons badge, and lists no development resources. The
  practical conclusion in the earlier research was right; the status code was not.
- `framework.digital.gob.cl` serves cleanly to a plain fetcher with no user-agent tricks needed.

---

## 9. Icons

**Icon set:** a bespoke icon **font** named `gob-cl`, not a third-party set. Not Font Awesome — that
appears only on the separate `kitdigital.gob.cl` marketing site, not in the framework.

| Property | Value | Source URL |
|---|---|---|
| Font family | `gob-cl` | https://framework.digital.gob.cl/icons.html |
| Usage | `.cl` plus `.cl-{icon-name}` | https://framework.digital.gob.cl/icons.html |
| Glyph count | 53 | https://framework.digital.gob.cl/fonts/gob-cl.svg |
| units-per-em | 1000 | https://framework.digital.gob.cl/fonts/gob-cl.svg |
| Formats served | `.eot` (14,180 B), `.svg` (94,780 B), `.ttf` (14,020 B), `.woff` (9,356 B) | https://framework.digital.gob.cl/fonts/ |

No `.woff2`. Cache-busted in the CSS as `?t=1608124305840`, a timestamp corresponding to December 2020.

**Individual SVGs are retrievable.** The `.svg` format is an SVG *font*, and it contains all 53 glyphs
as individual `<glyph glyph-name="..." d="...">` path elements. Each can be lifted into a standalone
`<svg>` by taking the path and applying the standard SVG-font transform for a 1000 units-per-em,
ascent 1000, descent 0 face. I confirmed the paths are present and named, including `doctor`. The file
is saved to `assets-staging/kitdigital/gob-cl-iconfont.svg` so nobody has to re-fetch it.

Documented extension route, verbatim, and note it is npm-based: "Si es necesario agregar un nuevo
ícono, colocar su svg en la carpeta `src/svg` y correr el comando `npm run build:font`, se creará
nuevamente la font de íconos."

**Complete glyph list**, from `https://framework.digital.gob.cl/icons.html`, confirmed against the
glyph names in the SVG font:

`cl-accessibility`, `cl-add-circle-fill`, `cl-add-circle-line`, `cl-arrow-left`, `cl-arrow-line`,
`cl-arrow-right`, `cl-arrow`, `cl-authority`, `cl-breadcrumb`, `cl-briefcase`, `cl-burger`, `cl-bus`,
`cl-call-info`, `cl-claveunica`, `cl-close-line`, `cl-close`, `cl-computer`, `cl-contrast`,
`cl-currency-cycle`, `cl-decrease-text`, `cl-doctor`, `cl-document-verified`, `cl-download`,
`cl-facebook`, `cl-filter`, `cl-give-letter`, `cl-img-preview`, `cl-increase-text`, `cl-instagram`,
`cl-list`, `cl-login-fill`, `cl-login`, `cl-logout`, `cl-m-arrow-down`, `cl-m-arrow-left`,
`cl-m-arrow-right`, `cl-m-arrow-up`, `cl-messenger`, `cl-moneybox`, `cl-ok`, `cl-pause`, `cl-play`,
`cl-question`, `cl-reading`, `cl-search`, `cl-sound`, `cl-store`, `cl-telephone`, `cl-together`,
`cl-touch-screen`, `cl-twitter`, `cl-woman`, `cl-youtube`

Four of these are directly useful and worth knowing exist: **`cl-accessibility`, `cl-contrast`,
`cl-increase-text`, `cl-decrease-text`** are the exact toolbar affordances for the two a11y themes, and
**`cl-doctor`** is a clinician glyph. There is no icon for a warning, an alert or a status indicator in
the set, which is another reason the semáforo cannot be sourced from Kit Digital.

**Separately**, an illustration set is downloadable from the accessibility page:
`https://kitdigital.gob.cl/archivos/iconos/v0beta_ilustraciones-lleno-personas.zip` (HTTP 200,
4,388,131 bytes), saved to `assets-staging/kitdigital/`. It contains **EPS, Adobe Illustrator and PDF
only — no SVG and no PNG** — so it is print artwork, not web assets, and it is marked `v0beta`. Not
usable for the dashboard without conversion.

---

## 10. What could not be retrieved

| Item | Status | What was tried |
|---|---|---|
| Figma UI Kit v3.0.1 token values | `UNVERIFIED` | `https://www.figma.com/community/file/1319005921039608306/ui-kit-v3-0-1` returns HTTP 200 but serves a JavaScript application shell with no token data in the HTML. Per instructions, not pursued further. Whether the Figma tokens agree with the framework's is unknown |
| Government `$` variable names for the colour and spacing scales | `UNVERIFIED` | `abstracts/_variables.scss` and `themes/a11y-contrast/abstracts/_variables.scss` and `_functions.scss` are referenced by name in the framework's own documentation, but variable-only Sass partials emit no CSS and so carry no source-map entry. All 88 output-producing partials were retrieved; these are not among them. Values are all present from the compiled CSS; only the government's identifiers for some of them are missing |
| `$a11y-scale-base` literal value | `UNVERIFIED`, `[derived]` as `4px` | Derived from the compiled button padding progression 18px / 14px / 10px against the retrieved formula `$button-padding-y - ($a11y-scale-base * $index)`. The declaration itself was never seen |
| Whether the CC BY 3.0 CL site licence covers the gobCL fonts | `UNVERIFIED` | The fonts carry their own copyright and trademark records and ship with no licence file. This is a question for a qualified person, not a retrieval problem |
| `.woff` / `.woff2` builds of gobCL | Do not exist at the published paths | Probed `framework.digital.gob.cl/fonts/gobCL_Regular.{woff,woff2,ttf}` — all 404 |
| A warning / alert / status icon in the `gob-cl` set | Does not exist | Full 53-glyph list enumerated and checked |

---

## 11. URL record

Every URL attempted on 5 August 2026, with its result. All requests sent with the user agent
`Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36`.

### 11.1 framework.digital.gob.cl

| URL | Result |
|---|---|
| https://framework.digital.gob.cl/ | 200, 41,805 B |
| https://framework.digital.gob.cl/development.html | 200, 51,100 B |
| https://framework.digital.gob.cl/colors.html | 200, 50,685 B |
| https://framework.digital.gob.cl/typography.html | 200, 51,978 B |
| https://framework.digital.gob.cl/accessibility.html | 200, 46,691 B |
| https://framework.digital.gob.cl/icons.html | 200, 43,090 B |
| https://framework.digital.gob.cl/utilities.html | 200, 47,619 B |
| https://framework.digital.gob.cl/framework-explanation.html | 200, 43,335 B |
| https://framework.digital.gob.cl/custom-presentation.html | 200, 38,662 B |
| https://framework.digital.gob.cl/tags.html | 200, 37,251 B |
| **https://framework.digital.gob.cl/css/gob.cl.css** | **200, 980,668 B — the compiled framework, richest single source** |
| **https://framework.digital.gob.cl/css/gob.cl.css.map** | **200, 2,024,091 B — 165 sources with `sourcesContent`, 88 government SCSS files** |
| https://framework.digital.gob.cl/css/doc.css | 200, 984,897 B (documentation site CSS, not used) |
| https://framework.digital.gob.cl/examples/style.scss | 200, 80 B (names the npm package) |
| https://framework.digital.gob.cl/js/gob.cl.js | 200, 41,407 B (contains no a11y logic) |
| https://framework.digital.gob.cl/css/style.css | **404** |
| https://framework.digital.gob.cl/scss/style.scss | **404** |
| https://framework.digital.gob.cl/dist/css/gob.cl.css | **404** |
| https://framework.digital.gob.cl/fonts/gob-cl.svg | 200, 94,780 B |
| https://framework.digital.gob.cl/fonts/gob-cl.woff | 200, 9,356 B |
| https://framework.digital.gob.cl/fonts/gob-cl.ttf | 200, 14,020 B |
| https://framework.digital.gob.cl/fonts/gob-cl.eot | 200, 14,180 B |
| https://framework.digital.gob.cl/fonts/gobCL_Regular.otf | 200, 36,528 B |
| https://framework.digital.gob.cl/fonts/gobCL_Bold.otf | 200, 44,716 B |
| https://framework.digital.gob.cl/fonts/gobCL_Light.otf | 200, 37,960 B |
| https://framework.digital.gob.cl/fonts/gobCL_Heavy.otf | 200, 44,776 B |
| https://framework.digital.gob.cl/fonts/gobCL_Regular.woff | **404** |
| https://framework.digital.gob.cl/fonts/gobCL_Regular.woff2 | **404** |
| https://framework.digital.gob.cl/fonts/gobCL_Regular.ttf | **404** |

### 11.2 kitdigital.gob.cl

| URL | Result |
|---|---|
| https://kitdigital.gob.cl/ | 200, 14,686 B |
| https://kitdigital.gob.cl/accesibilidad | 200 |
| https://kitdigital.gob.cl/recursos-de-desarrollo/ | **200, 4,383 B — contradicts the earlier 404; page is empty of resources** |
| https://kitdigital.gob.cl/archivos/insumos/Tipografia-gobCL.zip | 200, 118,030 B, `application/zip` — **saved** |
| https://kitdigital.gob.cl/archivos/insumos/nuevos/Manual%20Accesibilidad%20Web.pdf | 200, 17,756,886 B, `application/pdf` — **saved** |
| https://kitdigital.gob.cl/archivos/Manual%20Accesibilidad%20Web-v2.pdf | 200, 17,799,895 B, `application/pdf` — **saved** |
| https://kitdigital.gob.cl/archivos/Recomendaciones-WEB-2026.pdf | 200, 4,452,237 B, `application/pdf` — **saved** |
| https://kitdigital.gob.cl/archivos/iconos/v0beta_ilustraciones-lleno-personas.zip | 200, 4,388,131 B, `application/zip` — **saved** |

### 11.3 Other hosts

| URL | Result |
|---|---|
| https://registry.npmjs.org/@gobdigital-cl%2Fgob.cl | 200, JSON metadata. Plain HTTP GET; no package manager invoked, nothing installed |
| https://www.figma.com/community/file/1319005921039608306/ui-kit-v3-0-1 | 200, 738,696 B, but a JavaScript application shell containing no token data. Not pursued further |

**No host refused a request and no retry was needed.** Every non-200 above is a genuine 404 for a path
that does not exist, not a block.

---

## 12. Files saved

Under `assets-staging/kitdigital/`. `assets-staging/` is already listed in `.gitignore`, so none of
this can reach the repository. Nothing was unpacked into the dashboard.

| File | Bytes |
|---|---|
| `Tipografia-gobCL.zip` | 118,030 |
| `Manual-Accesibilidad-Web.pdf` | 17,756,886 |
| `Manual-Accesibilidad-Web-v2.pdf` | 17,799,895 |
| `Recomendaciones-WEB-2026.pdf` | 4,452,237 |
| `ilustraciones-lleno-personas.zip` | 4,388,131 |
| `gob-cl-iconfont.svg` | 94,780 |

Roughly 44 MB, of which 35 MB is the duplicated manual. Gitignored, so this is local disk only.
