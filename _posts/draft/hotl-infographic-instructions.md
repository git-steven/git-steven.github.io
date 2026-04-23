# HOTL Infographic Morphing Instructions

> Starting from `hitl-infographic.drawio`, apply the following changes to produce the HOTL version.
> These instructions are temporary — once the infographic is complete, replace this section with a
> textual summary and a side-by-side (or stacked) view of both infographics.

**Color system (established):**
- 🟦 Teal/turquoise fill — automation nodes and inner loop flow arrows
- 🟣 Purple fill — model services (Model Prediction, Model Training)
- 🟩 Green fill — Model Training Service
- 🟧 Orange-dashed border — monitoring overlay nodes (Human Monitor, Circuit Breaker)
- Parchment background, Architects Daughter font, sketchStyle=comic — unchanged

---

## 1. Remove ✅ DONE

- ~~The two orange dashed governance routing paths~~
- ~~The **Curation Team** box~~
- ~~The **Model Governance Team** box~~
- ~~The orange **"GOVERNANCE"** labels~~

---

## 2. Replace (automated equivalents) ✅ DONE

- ~~Curation Team → **🤖 Automated Data Validation** (teal, bottom center)~~
- ~~Model Governance Team → **🚀 Auto-Deploy Models** (teal, top center)~~

Both nodes are in the loop flow, not external overlays. Inner loop ring is visually closed. ✅

---

## 2.5 Verify Loop Ring Is Unbroken ✅ DONE

Inner loop flows continuously with teal arrows. No governance gaps. ✅

---

## 3. Monitoring Overlay Nodes ✅ / ⬜ PARTIALLY DONE

Human Monitor(s) and Circuit Breaker(s) boxes exist with orange-dashed borders. ✅

**Still needed — outer bracket / arc:**

Connect Human Monitor and Circuit Breaker to each other with a bracket or arc at the top of the diagram. Label it: `HUMAN ON THE LOOP`. This makes clear they form a coherent outer oversight layer rather than two orphaned floating boxes.

**Still needed — connection lines:**

These two nodes need thin dashed **read-only observation lines** to specific inner loop nodes. Style these as visually distinct from loop flow arrows — lighter weight, open or hollow arrowhead (suggesting "observes" not "controls").

| Monitoring Node | Observes (draw line to) | Why |
|---|---|---|
| Human Monitor(s) | Product UI/API | Watching user-facing predictions and session outcomes |
| Human Monitor(s) | Data | Watching incoming signal quality |
| Circuit Breaker(s) | Auto-Deploy | Can halt deployment if thresholds breach |
| Circuit Breaker(s) | Model Training | Can halt retraining if drift detected |

**Kill Switch:** Rather than a third standalone node, treat it as an attribute of the Circuit Breaker. Add `· kill switch` to its sub-bullets. The Circuit Breaker IS the kill switch mechanism.

---

## 4. Relabel ✅ / ⬜ MOSTLY DONE

| Element | Status |
|---|---|
| Loop center label → `HOTL System (Human-On-The-Loop) closed-loop learning` | ✅ Done |
| Title → Part 2: From HITL to HOTL | ✅ Done |
| Bottom caption updated | ✅ Done |
| `"Closing the Loop"` explanatory text box | ✅ Done |
| `"New in HOTL"` label near Auto-Deploy | ✅ Done |
| `"replaces Model Governance"` note | ✅ Done |
| Legend: `'Main' Loop: HITL (with Human in it)` | ⬜ Still says HITL — update to `'Main' Loop: HOTL (closed-loop)` |

---

## 5. Developer Training → Emergency Intervention ⬜ TODO

Developer Training existed in HITL as a normal operational bypass for manual tuning. In HOTL it still belongs, but its character changes completely — it is now a **rare emergency path**, not an operational one.

> In HOTL, the developer doesn't disappear. They just stop being part of normal operations and become the person who shows up when the Circuit Breaker fires and automated recovery fails.

**Changes:**
- Relabel node: `🧑‍💻 Emergency Intervention`
- Sub-bullets: `manual override · emergency retraining · bypasses automated gates`
- Restyle border: amber or red to signal "exceptional use only" (distinct from HITL's neutral style)
- Keep the dashed bypass arrow, but add label: `emergency only`

---

## 6. Counter-Rotation: Implying Asynchronous Spin ⬜ TODO

The inner loop (autonomous) and outer monitoring layer operate on completely different cadences. Counter-rotating visual motion conveys this structurally.

**Directional convention:**
- **Inner loop: clockwise (CW)** — already established by teal flow arrows
- **Outer monitoring arc: counter-clockwise (CCW)** — Human Monitor → Circuit Breaker → Human Monitor

**Implying spin in a static diagram (dim-to-bright arrows):**

Place 3–4 arrows along each ring, graduated in opacity in the direction of travel:

| Arrow in sequence | Opacity |
|---|---|
| 1st (trailing) | ~20% |
| 2nd | ~50% |
| 3rd | ~80% |
| 4th (leading) | 100% |

The eye reads brightening as momentum. Inner CW and outer CCW will read as counter-rotating without animation.

Add a small label near the outer arc: `asynchronous oversight`

---

## 6.5 Animation (Optional — Animated GIF Export) ⬜ EXPERIMENTAL

draw.io supports native flow animation on connectors:

1. Select a connector
2. **Format Panel → Connection tab → enable Flow Animation**
3. Inner loop connectors: animate **CW**
4. Outer monitoring arc: animate **CCW** at **slower speed** (reinforces async cadence difference)

**Export as animated GIF:**
- File → Export As → GIF → enable "Animate"
- 3–5 fps — slower is more readable
- ⚠️ Test at reduced canvas size first — GIF export at 2800×1800 can be rough
- ⚠️ Animated GIFs may not render reliably in Jekyll/GitHub Pages — keep a static PNG as the primary blog embed

> If animation proves unreliable, the dim-to-bright static approach (section 6) is the self-contained fallback and likely the more durable choice for longevity.

---

## 7. Legend Cleanup ⬜ PARTIALLY DONE

| Legend Entry | Action |
|---|---|
| `'Main' Loop: HITL (with Human in it)` | ⬜ Update to `'Main' Loop: HOTL (closed-loop)` |
| `Potential Bypass` | ⬜ Relabel to `Emergency Intervention (bypass)` | 
| `Automation Routing` | ✅ Keep |
| `Automation Boundary` | ✅ Keep |
| `'Sub' Loop: Iterative activities` | ✅ Keep |
| AUTOMATION node | ✅ Keep |
| MODEL SERVICES | ✅ Keep |
| PRODUCT UI | ✅ Keep |
| DATA | ✅ Keep |
| MODEL TRAINING SERVICE | ✅ Keep |

**Add to legend:**
- **Orange-dashed border** — Monitoring overlay node (human or automated); observes without gating

---

## 8. Remaining Work — Priority Order

| # | Item | Priority |
|---|---|---|
| 1 | Bracket/arc connecting Human Monitor + Circuit Breaker, labeled `HUMAN ON THE LOOP` | High |
| 2 | Observation lines from both monitoring nodes to inner loop nodes (read-only style) | High |
| 3 | Kill Switch sub-bullet added to Circuit Breaker | Medium |
| 4 | Developer Training → relabel Emergency Intervention, restyle border | Medium |
| 5 | Legend: HITL → HOTL label; Potential Bypass → Emergency Intervention | Medium |
| 6 | Dim-to-bright counter-rotation arrows on inner and outer rings | Low / Polish |
| 7 | `asynchronous oversight` label on outer arc | Low / Polish |
| 8 | Animated GIF export experiment | Optional |
