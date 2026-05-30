# 🎨 The Manifold — Image Prompts v2 (Calabi–Yau + denizens + locked palette)

> Adds the locked complementary palette (sampled from your swatch), per-color hex ranges,
> the shape-reveal gradient, and the six-view render commands. Supersedes `manifold-image-prompts.md`.

---

## 🌌 The cosmology (read once — it drives every prompt)

**The Manifold** is the universe where architecture comes to life: a **Calabi–Yau** surface
whose *shape determines the laws* (string theory's actual premise → "The Shape of Architecture").

**Its denizens** — borrowed from how a Calabi–Yau is actually populated in physics:

- **Cycles** — glowing **loops** threading the manifold's holes → *data flows, event streams.*
- **Membranes (branes)** — luminous **surface patches** wrapping a region → *services / bounded contexts.*
- **Flux** — **filaments of energy** running in and out through bright nodes → *messages, I/O, traffic.*
- **The mirror manifold** — a faint **dual** twin (mirror symmetry) → *the same system from the other side.*

---

## 🎨 Locked palette (complementary anchors)

Sampled from the uploaded swatch. **These are complementary anchors, not the whole palette** — the art
uses many more shades. Two are locked as brand anchors: **dark turquoise `#365558`** and **purple `#462D57`**
(with **lavender `#C8B3D6`** as the locked *light* purple).

| Swatch | Name | Hex |
|---|---|---|
| 🔒 | **dark turquoise** (slate teal) | `#365558` |
| 🔒 | **purple** (dark plum) | `#462D57` |
| | olive / **dark green** | `#515931` |
| | coffee (dark brown) | `#553F2E` |
| | dusty blue (slate) | `#94ABAE` |
| | sage (pale green) | `#D2D9B6` |
| | tan (beige) | `#D5C3B4` |
| 🔒 | **lavender** (light purple) | `#C8B3D6` |

### Hex ranges (lightest → darkest, with average)

| Color | Lightest | Light | **Average** | Dark | Darkest |
|---|---|---|---|---|---|
| **dark turquoise** | `#AFBBBC` | `#72888A` | **`#365558`** | `#263C3E` | `#162223` |
| **purple** (plum) | `#B5ABBC` | `#7E6C89` | **`#462D57`** | `#31203D` | `#1C1223` |
| **dark green** | `#B9BDAD` | `#858B6F` | **`#515931`** | `#393E22` | `#202414` |
| coffee | `#BBB2AB` | `#88796D` | **`#553F2E`** | `#3C2C20` | `#221912` |
| dusty blue | `#D4DDDF` | `#B4C4C6` | **`#94ABAE`** | `#68787A` | `#3B4446` |
| sage | `#EDF0E2` | `#E0E4CC` | **`#D2D9B6`** | `#93987F` | `#545749` |
| tan | `#EEE7E1` | `#E2D5CA` | **`#D5C3B4`** | `#95887E` | `#554E48` |
| **lavender** | `#E9E1EF` | `#D8CAE2` | **`#C8B3D6`** | `#8C7D96` | `#504856` |

*(Ladder = average mixed 60%/30% toward white for tints, 30%/60% toward black for shades.)*

### Gradients

- **Shape-reveal (for the seed renders):** `#365558` → `#FFFFFF` → `#515931`
  *(dark turquoise → white → dark green; divergent, colored by height — the white band reveals the form).*
- **Glow (luminous teal art):** `#03201F` → `#0A6F66` → `#26E6D2` → `#8FFBEE`.
- **Energy / flux (denizens):** purple range — `#462D57` core → `#B86BFF` / lavender `#C8B3D6` highlights.

---

## 🧰 Which prompts need the manifold render?

| Prompt | Needs the CY render? |
|---|---|
| 1 Header · 2 Full scene · 3 Denizens close-up · 5 Pencil line | **Yes** — render in matplotlib, composite in |
| 4 Two-worlds diptych | No — it shows a *warped world*, not the object |
| 6 Woodpecker · 7 Slingshot-vs-cannon | No — no manifold at all |

---

## 🧊 Six orthographic views + commands (do it yourself)

The seed sheet (`manifold_six_views.png`) shows **N, E, S, W, TOP, BOTTOM**, each framed, camera locked
on `(0,0,0)` with **+y up**, using the shape-reveal gradient. To regenerate or tweak:

```python
from manifold_studio import ManifoldStudio

s = ManifoldStudio(resolution=42)                  # higher = crisper, slower
s.set_gradient(["#365558", "#FFFFFF", "#515931"])  # dark turquoise -> white -> dark green

# all six framed views as one contact sheet:
s.render_six_views("manifold_six_views.png", distance=2.0, frame_color="#365558")

# a single view — axis in {"x","y","z"}, angle in degrees, distance in manifold-lengths:
s.render_image(axis="y", angle=35, distance=2.0, out_path="one_view.png")

# transparent cut-out for compositing into a Gemini scene:
s.render_image(axis="y", angle=35, distance=2.0, out_path="cutout.png", transparent=True)
```

CLI one-liner:

```bash
python3 -c "from manifold_studio import ManifoldStudio as M; s=M(resolution=42); s.set_gradient(['#365558','#FFFFFF','#515931']); s.render_six_views('manifold_six_views.png')"
```

> The same `set_gradient(...)` applies to the spin animation and the denizen renders, so any seed graphic
> can carry the high-contrast gradient instead of the flat glow when you want the shape to read clearly.

---

## 1) Article header — the Manifold and its life

```
A clean, friendly, awe-inspiring header illustration of an alternate universe where software architecture comes to life. At center floats THE MANIFOLD: a smooth, intricate Calabi-Yau surface — many curved petal-like lobes folding through one another — its core a luminescent dark teal (#365558 deepening, brightening toward turquoise) that glows from within, easing to muted teal where it folds back, with deep-turquoise inner faces glimpsed through the gaps. Living on and through it are its denizens: glowing loops threading its holes (data flows), a few luminous membrane patches wrapping its lobes (services), and fine purple-magenta filaments of energy (purple #462D57 to lavender #C8B3D6) running in and out through small bright nodes. Off to one side, an elegant friendly Turing machine — a ribbon of tape with a gentle read/write head — curves toward the horizon. Calm, bright "mirror dimension" mood, wondrous not dark. Clean vector-meets-soft-3D, rounded forms, subtle glow and bloom. Deep-indigo background. Leave clear space in the upper third for a title. No text, letters, logos, or UI.
```

## 2) Full establishing scene — the Manifold over the purple plain

```
A breathtaking alternate-universe landscape. Bottom 38% is an orderly ground plain; top 62% is a vivid deep-purple sky (lavender #C8B3D6 highlights, plum #462D57 depths) with tiny near-black twinkling stars and a few strange beautiful architectural structures drifting far away. Centered in the upper two-thirds floats the Calabi-Yau MANIFOLD — luminescent dark-teal core (#365558), muted-teal folds, deep-turquoise inner faces — alive with denizens: glowing loops (flows) threading it, membrane patches (services) on its lobes, and purple-magenta energy filaments running in and out through bright nodes. High in the sky, faint and inverted, hangs its MIRROR MANIFOLD: a ghostly dual twin. Clean luminous soft-3D illustration, calm wonder, science-museum-poster feel. Clear sky upper third for a title. No text, letters, logos, or UI.
```

## 3) Denizens close-up — the architecture, alive

```
A detailed close-up of life inside the Manifold. A translucent Calabi-Yau surface in luminescent teal (#365558 to bright turquoise) fills the frame; on it the architectural denizens are clearly legible: bright membrane patches resting on its lobes (services), glowing loops looping through its holes (data flows), and several purple-magenta filaments (purple #462D57 to lavender #C8B3D6) threading straight in and out of the form, each ending in a small bright glowing node where energy meets structure. A subtle sense that the loops carry current and the membranes pulse. Clean soft-3D, dark-indigo background, gentle bloom, generous depth. No text, letters, logos, or UI.
```

## 4) Two-worlds diptych — ordered world vs the Manifold

```
A side-by-side diptych of two universes under different rules. LEFT — "the ordinary world": a clean sunlit scene of well-formed modern buildings on green grass, a few distant people, calm and organized, warm daylight. RIGHT — "the Manifold": the SAME buildings, paths, and figures, reorganized by a different physics — gently warped, folded, and looped through non-Euclidean space, still clearly orderly rather than chaotic, lit in deep indigo and teal (#365558) under a deep-purple starlit sky (plum #462D57), faint purple-magenta energy threading the structures. Shared composition so the eye reads them as one place under two sets of laws. Clean soft-3D, friendly, luminous. No text, labels, or UI.
```

## 5) Pencil / ink line version — the Manifold drawn by hand

```
The Calabi-Yau Manifold rendered as a clean hand drawing on paper: a single solid purple (#462D57) contour line tracing the physical edges of its folded, petal-like form, the way someone would ink it on a 2D page. Minimal flat teal shading inside the outline (#365558 light wash) — just enough to read the folds and the soft shadow where the surface passes into itself. A few denizen loops sketched as thin purple lines threading the holes. No fancy 3D tracery or glow — restrained and elegant. Warm off-white paper with a faint tooth. No text, labels, or UI.
```

## 6) Weinberg's Law — the woodpecker

```
A clean, witty illustration of software fragility. A tall tower built entirely out of "software" — stacked translucent blocks shaped like code windows, curly braces, and UI panels, glowing softly in teal (#365558). Perched on one block is a single charming cartoon woodpecker, mid-tap; a hairline crack of light spreads from that one tap, hinting the whole structure could topple from a single small peck. Humorous and light — a wink, not a disaster. Deep-indigo background, teal glow, a touch of purple-magenta (#462D57), clean soft-3D, rounded edges, gentle bloom, generous negative space. The woodpecker is small and endearing beside the tower. No text, letters, logos, or UI.
```

## 7) Cost crystallizer — slingshot vs cannon

```
A clean, witty illustration about right-sizing tools. On one side a small elegant slingshot; on the other an absurdly oversized cannon — both aimed at the very same tiny target: a small floating stack of simple list items / a few lines of glowing code. The slingshot is clearly enough; the cannon is comic overkill. Light, humorous tone — a wink, no explosions, nothing destructive. Deep-indigo background, teal and turquoise glow (#365558), purple-magenta accents (#462D57), warm tan/beige highlights (#D5C3B4), clean soft-3D, rounded style, subtle bloom, generous negative space. No text, letters, logos, or UI.
```
