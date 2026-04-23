# icon-lexicon.v6.md
Semantic emoji lexicon for architecture, AI systems, and technical diagrams.

Icons function as **semantic anchors**—a visual DSL for system design.

---

# 🧭 Design Principles

- Icons are **semantic, not decorative**
- Prefer **one canonical meaning per icon**
- Allow **composability** (e.g. ☁️ + ⚙️ = “machine in cloud”)
- Separate:
  - **Artifact vs Action vs State**
- Optimize for:
  - diagrams
  - markdown
  - infographics

---

# ⭐ Canonical Icons (v6)

| Icon | Meaning | Notes |
|------|--------|------|
| 📜 | **Model (ML / AI)** | ✅ Canonical — promoted |
| 📦 | Software Package / Artifact | Static deliverable |
| ⛴ | Ship / Deliver / Release | Human-scale shipping metaphor |
| 🚀 | Deploy (system action) | Use sparingly |
| 🏁 | Release Complete / Milestone | Terminal state |
| ☁️ | Cloud / Infra | Combine for richer meaning |
| ⚙️ | Machine / Runtime / Engine | Combine with ☁️ |
| 🧠 | Learning / Intelligence | |
| 🤖 | Autonomous Agent | |
| 👥 | Governance / Humans | |
| 🔄 | Loop / Cycle | |
| ⛓️‍💥 | Broken Loop / Boundary | |
| 📊 | Metrics / Observability | |
| 🧬 | Training / Model evolution | |
| 🧪 | Testing / Validation | |
| ⚖️ | Governance / Tradeoff | |
| 🚰 | Bottleneck | |
| 🌊 | Flow | |
| 🔗 | Dependency | |
| ⛓️ | Coupling | |
| 🔌 | Interface / Port | |
| 🧵 | Stream / pipeline thread | |
| 📣 | Event / signal emission | |

---

# 🧠 Canonical Patterns

## ☁️⚙️ Machine in Cloud
Represents deployed runtime compute.

Variants:
- ☁️📜 = model in cloud
- ☁️⚙️ = runtime
- ☁️🧠 = learning system

---

## 📦 Delivery Flow

📦 → ⛴ → ☁️⚙️ → 🏁

---

# 🧩 Categories

## Architecture
🏛️ 🏢 🏦 🏰 🏚️ 🧱 🗿 🪨 ⚓

## Components
🧩 📦 🗂️ 🔌 🔗 🧷 ⛓️ ⛓️‍💥

## AI / ML
📜 🧠 🤖 🧬 🧪 🧫 🦠 ⚗️ ⚛️

## People
👤 👥 🤝 🧑‍💻 🧑‍🔬 🧑‍🏫 🕵️

## Flow
🌀 🌊 🔄 🧵 🎛️ 📣 📨 🛰️

## Metrics
📊 📈 📉 🧾 🔍 🔎 🔬

## Engineering
⚙️ 🧰 🛠️ 🔧 🔩 🔨

## Infra
☁️ 🖥️ 💻 🗄️ 📡

## Security
🛡️ 🔐 🔒 🗝️ 🪪

## Risk
🔥 ⚡ 💥 🚨 🐞

## Time
⏱️ ⏲ ⏳ 🕒 🕰

---

# 🧠 HITL Patterns

| Concept | Icon |
|--------|------|
| Model | 📜 |
| Inference | 📜 → ⚙️ |
| Runtime | ☁️⚙️ |
| Feedback Loop | 🔄 |
| Governance | 👥 |
| Boundary | ⛓️‍💥 |
| Training | 🧬 |
| Autonomous | 🤖 |

---

# 🏁 Summary

Core mental model:

📦 Artifact  
⛴ Ship  
☁️⚙️ Runtime  
📜 Model  
👥 Governance  
⛓️‍💥 Boundary
