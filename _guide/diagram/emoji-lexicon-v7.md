# emoji-lexicon-v7.md

Semantic emoji/icon lexicon for architecture, AI systems, documentation, and technical diagrams.

Icons function as **semantic anchors** — a visual DSL for system design that helps readers scan technical documents quickly.

Designed for: Markdown docs · architecture diagrams · draw.io / diagrams.net · Mermaid · Jupyter notebooks · technical blog posts.

> This file consolidates every prior lexicon (`v5`, `v6`, the "category-first" variant) into one authoritative doc, recategorizes for sense, and adds a **self-updating** mechanism at the bottom. See **Self Updating Doc** and **Maintenance Protocol** before editing.

---

# 🧭 Design Principles

- Icons are **semantic, not decorative**.
- Prefer **one canonical meaning per icon** (the **Canonical Icons** table is the source of truth).
- An icon **may appear in multiple categories** — its canonical meaning still lives in one place.
- Allow **composability** (e.g. `☁️ + ⚙️ = ☁️⚙️` "runtime in cloud").
- Separate **Artifact vs Action vs State**.
- Optimize for diagrams, markdown, and infographics.

---

# ⭐ Canonical Icons

The single source of truth. Each emoji appears **at most once** here (categories below may repeat it). `✅` marks an icon whose meaning is locked.

| Icon  | Name               | Canonical meaning                              |   |
|:-----:|--------------------|------------------------------------------------|:-:|
|  🤖   | robot              | Autonomous agent / AI                          | ✅ |
|  🧠   | brain              | Thinking / reasoning / intelligence            | ✅ |
|   ✨   | sparkles           | Idea / insight / "AI magic"                    |   |
|  🧬   | dna                | **ML model — training / evolution**            | ✅ |
|  🧮   | abacus             | **ML model — runtime prediction / inference**  | ✅ |
|  🎓   | graduation cap     | Learning / study                               |   |
|  🏛️  | classical building | Architecture / governance                      | ✅ |
|  🏢   | office             | Module / service building                      | ✅ |
|  🏦   | bank               | Monolith / institution                         |   |
|  🏰   | castle             | Stronghold / goal / "the win"                  |   |
|  🏚️  | derelict house     | Legacy system                                  |   |
|  🏭   | factory            | Pipeline / batch processing plant              |   |
|  🧱   | brick              | Foundation / primitive / object                | ✅ |
|  🪨   | rock               | Bedrock / hard constraint                      |   |
|  🗿   | moai               | Monument / immovable legacy                    |   |
|   ⚓   | anchor             | Structural anchor / stability                  |   |
|  🏗️  | crane              | Build / in-progress architecture               | ✅ |
|  🧰   | toolbox            | Tooling / work                                 |   |
|  🛠️  | hammer & wrench    | Tool / maintenance                             |   |
|  🔧   | wrench             | Tool / fix                                     |   |
|  ⚙️   | gear               | Machine / runtime / inner workings             | ✅ |
|  🧲   | magnet             | **IoC / Dependency Injection** (pulls deps in) | ✅ |
|  🚪   | door               | Entry / exit / destination                     |   |
|  🪜   | ladder             | Climb / elevate                                |   |
| 🧑‍💻 | technologist       | Developer / programmer                         | ✅ |
|  💻   | laptop             | Programming / computer                         |   |
|  🖥️  | desktop            | Server / host                                  |   |
|  📡   | satellite antenna  | Signal / telemetry / broadcast                 |   |
|  🗺️  | world map          | Context / domain map                           | ✅ |
|  🧭   | compass            | Direction / navigation                         |   |
|  🌐   | globe (meridians)  | Global / network / web                         |   |
|  📍   | pushpin            | Ownership / source-of-truth anchor             | ✅ |
|  🏷️  | label              | Tag / version / ownership                      |   |
|  🚦   | traffic light      | Decision gate / policy check                   |   |
|  🌉   | bridge             | Integration boundary crossing                  |   |
|  🔎   | magnifying glass   | Search / discovery                             |   |
|  🔭   | telescope          | Examine from outside / explore                 |   |
|  🔬   | microscope         | Examine from inside                            |   |
|  📚   | books              | **Table of Contents / docs hub**               | ✅ |
|  📖   | open book          | Reference / reading                            |   |
|  🗒️  | notepad            | Working notes                                  |   |
|  📝   | memo               | Draft / authoring                              |   |
|  📄   | page               | Document                                       |   |
|  📑   | bookmark tabs      | Sections / index tabs                          |   |
|  🗂️  | dividers           | Folder                                         | ✅ |
|  🗃️  | card file box      | Archive                                        |   |
|  🗄️  | file cabinet       | Database / store                               | ✅ |
|  📜   | scroll             | **Contract / spec / policy**                   | ✅ |
|  🧾   | receipt            | Log entry / record                             |   |
|  🔌   | plug               | **Port / interface**                           | ✅ |
|  📐   | triangle ruler     | Blueprint / geometry                           |   |
|  📏   | ruler              | Measure                                        |   |
|  🔖   | bookmark           | Version marker                                 |   |
|   ✅   | check mark         | Done / validated                               | ✅ |
|  ☑️   | ballot box         | Checked / verified                             |   |
|  ✔️   | check              | Verified                                       |   |
|  🧪   | test tube          | Test / experiment                              | ✅ |
|  🧩   | puzzle piece       | Component                                      | ✅ |
|  📦   | package            | Artifact / deployable                          | ✅ |
|   ➕   | plus               | Compose                                        |   |
|  🔗   | link               | Dependency / link                              | ✅ |
|  ⛓️   | chains             | Coupling                                       | ✅ |
| ⛓️‍💥 | broken chain       | Decoupling / boundary                          | ✅ |
|  🧷   | safety pin         | Adapter / seam                                 |   |
|  👥   | people             | Team / governance / humans                     | ✅ |
|  🤝   | handshake          | Agreement                                      |   |
|  ♻️   | recycle            | Pattern / reuse                                |   |
|  🌀   | cyclone            | Workflow / system dynamics                     | ✅ |
|  🌊   | wave               | Flow (afferent)                                | ✅ |
|  💦   | sweat droplets     | Afferent coupling / spillover                  |   |
|  🔄   | cycle              | Loop / iteration / retry                       | ✅ |
|  🎛️  | control knobs      | Orchestration / tuning                         |   |
|  🧵   | thread             | Stream / execution thread                      | ✅ |
|  📣   | megaphone          | Event / signal emission                        | ✅ |
|  📨   | envelope           | Message                                        |   |
|  🛰️  | satellite          | External dependency                            | ✅ |
|  🚰   | tap                | Bottleneck                                     | ✅ |
|  📊   | bar chart          | Metric / report                                | ✅ |
|  📈   | chart up           | Trending up                                    |   |
|  📉   | chart down         | Trending down                                  |   |
|  ⚖️   | balance scale      | Tradeoff / governance                          | ✅ |
|  🛡️  | shield             | Protection / security                          | ✅ |
|  🔐   | locked w/ key      | Secured                                        |   |
|  🔒   | locked             | Restricted                                     |   |
|  🗝️  | old key            | Secret                                         |   |
|  🪪   | id card            | Identity                                       |   |
|  🐞   | bug                | Defect / flaw                                  | ✅ |
|  🧨   | firecracker        | Explosive / breaking risk                      |   |
|  🚨   | siren              | Alert / incident                               |   |
|  ⚠️   | warning            | Caution                                        |   |
|  ☁️   | cloud              | Cloud / infra                                  | ✅ |
|  🐳   | whale              | Container / Docker                             | ✅ |
|  ☸️   | wheel              | Orchestration / Kubernetes                     | ✅ |
|   ⛴   | ferry              | Ship / deliver / release                       | ✅ |
|  🏁   | checkered flag     | Release complete / milestone                   | ✅ |
|  🔥   | fire               | Risk / hotspot / incident                      | ✅ |
|  💧   | droplet            | Stabilization / hardening                      | ✅ |
|  🧊   | ice                | Frozen work                                    |   |
|  🫧   | bubbles            | Froth / smoothing                              |   |
|   ⚡   | high voltage       | Urgency / energy                               |   |
|  💥   | collision          | Breaking change                                |   |
|  🌱   | seedling           | Evolution / growth                             | ✅ |
|  🌿   | herb               | Growing                                        |   |
|  🌳   | tree               | Mature                                         |   |
|  🌬️  | wind face          | Change / variability                           |   |
|  ⚗️   | alembic            | Chemistry / synthesis / experiment             |   |
|  ⚛️   | atom               | Physics / core primitive                       |   |
|  🧫   | petri dish         | Culture / incubation                           |   |
|  🦠   | microbe            | Organism / spreading / contagion               |   |
|  🌡️  | thermometer        | Temperature / health gauge                     |   |
|  🧟   | zombie             | Zombie ticket / process                        | ✅ |
|  🪦   | headstone          | Dead work                                      |   |
|  🤷   | shrug              | Pointless / useless                            |   |
|   ⏳   | hourglass          | Waiting                                        | ✅ |
|  ⏱️   | stopwatch          | Timing / latency                               |   |
|  🕰   | mantel clock       | Time / legacy                                  |   |
|   ☯   | yin yang           | Balance                                        |   |
|   ⏲   | timer              | Timing (alias ⏱️)                              |   |
|  🖼️  | framed picture     | Art / visual                                   |   |
|  🔢   | input numbers      | Number / integer                               |   |
|  🔤   | input latin        | String / text                                  |   |
|  😎   | sunglasses         | Emojicode / logic                              |   |
|  👹   | ogre               | Danger / horror                                |   |

---

# 🗂️ Categories

An emoji may appear in more than one category. Each section lists its icons as an **Icon · Name · Meaning** table.

## 🤖 AI & ML
| Icon | Name | Meaning |
|:--:|--|--|
| 🤖 | robot | AI/agent |
| 🧠 | brain | reasoning |
| ✨ | sparkles | idea/insight |
| 🧬 | dna | model training |
| 🧮 | abacus | runtime prediction |
| 🎓 | graduation cap | learning |
| 🔬 | microscope | introspection |
| 🧪 | test tube | experiment |

## 🏛️ Architecture & Buildings
**All building icons live here.** Use for system shape, modules, institutions, the "built environment".

| Icon | Name | Meaning |
|:--:|--|--|
| 🏛️ | classical building | architecture/governance |
| 🏢 | office | module/service |
| 🏦 | bank | monolith/institution |
| 🏰 | castle | stronghold/goal |
| 🏚️ | derelict house | legacy |
| 🏠 | house | app/home |
| 🏡 | house w/ garden | hosted app |
| 🏘️ | houses | fleet/cluster |
| 🏤 | post office | gateway/exchange |
| 🏭 | factory | pipeline/processing |
| 🏬 | department store | platform |
| 🗼 | tower | landmark/registry |
| 🏗️ | crane | under construction |
| 🧱 | brick | foundation/object |
| 🪨 | rock | bedrock |
| 🗿 | moai | monument |
| ⚓ | anchor | structural anchor |

## 🔧 Construction, Tools & Engineering
| Icon | Name | Meaning |
|:--:|--|--|
| 🏗️ | crane | build |
| 🧰 | toolbox | tools |
| 🛠️ | hammer & wrench | tool |
| 🔧 | wrench | fix |
| 🔩 | nut & bolt | fastener/config |
| 🔨 | hammer | work |
| ⚙️ | gear | runtime/inner workings |
| 🧲 | magnet | IoC/DI |
| 🚧 | construction | WIP |
| 🚪 | door | entry/exit |
| 🪜 | ladder | elevate |

## 💻 Computers & Software
| Icon | Name | Meaning |
|:--:|--|--|
| 🧑‍💻 | technologist | developer |
| 👨‍💻 | man tech | developer |
| 👩‍💻 | woman tech | developer |
| 💻 | laptop | programming |
| 🖥️ | desktop | server |
| ⌨️ | keyboard | input/CLI |
| 🖱️ | mouse | pointer/UI |
| 🗄️ | file cabinet | database |
| 📡 | satellite antenna | telemetry/signal |

## 🗺️ Context, Navigation & Routing
| Icon | Name | Meaning |
|:--:|--|--|
| 🗺️ | world map | domain map |
| 🧭 | compass | direction |
| 🌐 | globe | global/network |
| 📍 | pushpin | ownership anchor |
| 🏷️ | label | tag |
| 🛣️ | motorway | path |
| 🛤️ | railway | track |
| 🚦 | traffic light | gate |
| 🌉 | bridge | crossing |
| 🔎 | magnifying glass | search |
| 🔭 | telescope | explore |

## 📚 Documentation & Knowledge
| Icon | Name | Meaning |
|:--:|--|--|
| 📚 | books | TOC/docs hub |
| 📖 | open book | reference |
| 📙 | orange book |  |
| 📗 | green book |  |
| 📘 | blue book |  |
| 🗒️ | notepad | notes |
| 📝 | memo | draft |
| 📄 | page | document |
| 📃 | page w/ curl | terms |
| 📑 | bookmark tabs | sections |
| 🧠 | brain | knowledge |
| 🎓 | graduation cap | learning |
| 🗃️ | card file box | archive |
| 🗄️ | file cabinet | store |
| 🗂️ | dividers | folder |
| 📌 | pushpin | pinned |

## 📜 Contracts & Interfaces
| Icon | Name | Meaning |
|:--:|--|--|
| 📜 | scroll | contract/spec/policy |
| 🧾 | receipt | log/record |
| 🔌 | plug | port/API |
| 🧬 | dna | schema/data shape |
| 📐 | triangle ruler | blueprint |
| 🏷️ | label | version |
| 🔖 | bookmark | version |
| ✅ | check mark | valid |
| ☑️ | ballot box | checked |
| 🧪 | test tube | validation |

## 🧩 Components & Connectors
| Icon | Name | Meaning |
|:--:|--|--|
| 🧩 | puzzle piece | component |
| 📦 | package | artifact/module |
| ➕ | plus | compose |
| 🔗 | link | dependency |
| ⛓️ | chains | coupling |
| ⛓️‍💥 | broken chain | decoupling/boundary |
| 🧷 | safety pin | adapter/seam |
| 🧲 | magnet | IoC/DI |
| 👥 | people | team boundary |
| 🤝 | handshake | agreement |
| ♻️ | recycle | pattern/reuse |

## 🌀 Flow, Lifecycle & Orchestration
| Icon | Name | Meaning |
|:--:|--|--|
| 🌀 | cyclone | workflow |
| 🌊 | wave | flow (afferent) |
| 💦 | sweat droplets | afferent coupling |
| 🔄 | cycle | loop/iteration/retry |
| ➡️ | right arrow | process step |
| 🎛️ | control knobs | orchestration |
| 🧵 | thread | stream |
| 📣 | megaphone | event |
| 📨 | envelope | message |
| 🛰️ | satellite | external dep |
| 🟢 | green | healthy |
| 🟡 | yellow | caution |
| 🔴 | red | critical |
| ☯ | yin yang | balance |

## 🌊 Lean Flow & Work Management
| Icon | Name | Meaning |
|:--:|--|--|
| 🌊 | wave | flow |
| 🚰 | tap | bottleneck |
| 🔄 | cycle | iteration |
| 📈 | chart up | throughput |
| 📊 | bar chart | metrics |
| 📋 | clipboard | work items |
| 🧾 | receipt | ticket |
| 🧟 | zombie | zombie work |
| 🪦 | headstone | dead work |
| 🧊 | ice | frozen work |
| 🤷 | shrug | pointless work |
| ⏳ | hourglass | waiting |
| 🕰 | mantel clock | stale |

## 🧪 Quality, Testing & Verification
| Icon | Name | Meaning |
|:--:|--|--|
| 🧪 | test tube | test |
| 🔬 | microscope | examine inside |
| 🔭 | telescope | examine outside |
| ✅ | check mark | pass |
| ✔️ | check | verified |
| ☑️ | ballot box | validated |
| 🐞 | bug | defect |
| 📏 | ruler | measure |
| 📐 | triangle ruler | spec |
| 📊 | bar chart | coverage |

## 📊 Metrics & Analysis
| Icon | Name | Meaning |
|:--:|--|--|
| 📊 | bar chart | metrics |
| 📈 | chart up | trending up |
| 📉 | chart down | trending down |
| 🧮 | abacus | calculation/prediction |
| ⚖️ | balance scale | tradeoff |
| 🔍 | magnifying glass | investigate |
| 🔬 | microscope | deep analysis |

## 🛡️ Security, Trust & Threats
| Icon | Name | Meaning |
|:--:|--|--|
| 🛡️ | shield | protection |
| 🔐 | locked w/ key | secured |
| 🔒 | locked | restricted |
| 🗝️ | old key | secret |
| 🪪 | id card | identity |
| 📜 | scroll | policy/compliance |
| ⚖️ | balance scale | compliance |
| 🐞 | bug | vulnerability |
| 🧨 | firecracker | exploit risk |
| 🚨 | siren | alert |
| ⚠️ | warning | caution |
| 🔥 | fire | active threat |
| ☢️ | radioactive | toxic zone |
| ☣️ | biohazard | contamination |

## ☁️ Cloud, Containers & Deployment
| Icon | Name | Meaning |
|:--:|--|--|
| ☁️ | cloud | cloud/infra |
| ⛅ | sun behind cloud | hybrid/partial cloud |
| `☁️⚙️` | cloud + gear | cloud runtime |
| `☁️📦` | cloud + package | cloud deploy |
| 🐳 | whale | container/Docker |
| ☸️ | wheel | orchestration/Kubernetes |
| 📦 | package | artifact/image |
| ⛴ | ferry | ship/release |
| 🚢 | ship | deliver |
| 🛳️ | passenger ship | fleet rollout |
| 🏁 | checkered flag | milestone |
| 🖥️ | desktop | host |
| 🗄️ | file cabinet | managed store |
> 🚀 rocket is intentionally **not** used for deploy here — see **DON'T USE**.

## 👤 People & Personas (users of types)
| Icon | Name | Meaning |
|:--:|--|--|
| 👤 | silhouette | generic user/actor |
| 👥 | people | team/governance |
| 🧑‍💻 | technologist | developer user |
| 🧑‍🔬 | scientist | researcher/data scientist |
| 🧑‍🏫 | teacher | trainer/admin |
| 🧑‍⚖️ | judge | governance/approver |
| 🕵️ | detective | auditor/observer |
| 🤝 | handshake | partner/agreement |
| 🥷 | ninja | power user/automation |
| 🧙 | mage | wizard/expert |
| 👮 | officer | policy enforcer |
| 🦸 | superhero | trusted actor |
| 🦹 | supervillain | threat actor |
| 🧟 | zombie | stale/bot account |
| 👹 | ogre | adversary |
| 🤷 | shrug | undecided/unknown actor |

## 💧🔥🌱 Elements & System Dynamics
The classical elements + system "physics".

| Icon | Name | Meaning |
|:--:|--|--|
| 🪨 ⛰️ | rock / mountain | earth — hard constraint |
| 💧 🌊 | droplet / wave | water — flow/stability |
| 🔥 | fire | fire — risk/heat |
| 🌬️ 💨 🪁 | wind face / dash / kite | air — change/variability/agility |
| 🪵 | wood | material/raw resource |
| 🧊 | ice | frozen/cooling |
| 🫧 | bubbles | smoothing |
| ⚡ | high voltage | urgency/energy |
| 💥 | collision | breaking change |
| 🌱 | seedling | evolution |
| 🌿 | herb | growing |
| 🌳 | tree | mature |
| ♻️ | recycle | renewal |

## ⚗️ Science & Nature
| Icon | Name | Meaning |
|:--:|--|--|
| ⚗️ | alembic | synthesis/experiment |
| ⚛️ | atom | physics/core primitive |
| 🧪 | test tube | test |
| 🧫 | petri dish | incubation/culture |
| 🦠 | microbe | organism/contagion |
| 🔬 | microscope | examine inside |
| 🔭 | telescope | examine outside |
| 🧬 | dna | genetics/model |
| 🧲 | magnet | magnetism/attraction |
| 🌡️ | thermometer | temperature |
| ☢️ | radioactive | radiation |
| ☣️ | biohazard | biohazard |
| 🌱 | seedling | life/growth |

## 🌌 Cosmos & World
| Icon | Name | Meaning |
|:--:|--|--|
| 🌌 | milky way | vast scope/the unknown |
| 🪐 | planet | external system/world |
| ☄️ | comet | high-impact event |
| 🌠 | shooting star | rare event/wish |
| 🛸 | flying saucer | anomaly/unknown tech |
| 👽 | alien | foreign/3rd-party system |
| 🌕 | full moon | peak/full state |
| 🌑 | new moon | empty/dark state |
| ✨ | sparkles | magic/insight |
| 🛰️ | satellite | external dep |
| 🌍 | globe europe |  |
| 🌎 | globe americas |  |
| 🌏 | globe asia |  |
| 🏔️ | snow mountain | constraint |
| ⛰️ | mountain | obstacle |
| 🗻 | mount fuji | landmark |
| 🌋 | volcano | eruption/instability |
| 🏞️ | national park | landscape |
| 🏜️ | desert | barren |
| 🏝️ | island | isolated subsystem |
| 🏖️ | beach | edge |
| 🏕️ | camping | temporary env |

## 🌪️ Weather
| Icon | Name | Meaning |
|:--:|--|--|
| 🌪️ | tornado | chaos |
| ⛈️ | thunderstorm | crisis |
| 🌧️ | rain cloud | downturn |
| 🌩️ | lightning cloud | disruption |
| ☔ | umbrella rain | protection |
| ☀️ | sun | visible/clear |
| 🌤️ | sun small cloud | mostly clear |
| 🌥️ | sun large cloud | partial |
| 🌦️ | sun rain cloud | mixed |
| 🌙 | crescent moon | hidden/night ops |
| 🌫️ | fog | obscurity |
| 🌡️ | thermometer | temperature |

## ⏱️ Status & Time
| Icon | Name | Meaning |
|:--:|--|--|
| 🟢 | green | healthy |
| 🟡 | yellow | caution |
| 🔴 | red | critical |
| ✅ | check | done |
| ⚠️ | warning | caution |
| ☯ | yin yang | balance |
| ⏱️ | stopwatch | latency |
| ⏲ | timer | timing |
| ⏳ | hourglass | waiting |
| 🕒 | clock | schedule |
| 🕰 | mantel clock | legacy/time |

## ➡️ Arrows & Direction

| Category | Icons |
|---|---|
| **Cardinal** | ➡️ right · ⬅️ left · ⬆️ up · ⬇️ down |
| **Diagonal** | ↗️ up-right · ↘️ down-right · ↙️ down-left · ↖️ up-left |
| **Bidirectional** | ↔️ left-right · ↕️ up-down |
| **Curved** | ⤴️ curve up · ⤵️ curve down · ↩️ curve left · ↪️ curve right |
| **Cycle / Repeat** | 🔄 counterclockwise · 🔃 clockwise · 🔁 repeat · 🔂 repeat once |

### Unicode Arrows (for diagrams)

| Style        | Arrows                                                                |
|--------------|-----------------------------------------------------------------------|
| **Single**   | → right · ← left · ↑ up · ↓ down                                      |
| **Diagonal** | ↗ up-right · ↘ down-right · ↙ down-left · ↖ up-left                   |
| **Double**   | ⇒ right · ⇐ left · ⇑ up · ⇓ down                                      |
| **Long**     | ⟶ long right · ⟵ long left · ⟹ long double right · ⟸ long double left |

## ⭐ Stars & Decorative

| Category        | Icons                                                                                     |
|-----------------|-------------------------------------------------------------------------------------------|
| **Emoji Stars** | ⭐ star · 🌟 glowing star · ✨ sparkles                                                     |
| **Filled**      | ★ black star · ⭑ small black star · ✦ four-point filled · ✴ eight-point                   |
| **Outlined**    | ☆ white star · ✧ four-point outline · ✰ shadowed star                                     |
| **Ornate**      | ✪ circled star · ⍟ circled star alt · ✫ open star · ✯ pinwheel star · ❂ circled open star |
| **Asterisk**    | ✹ heavy asterisk · ✸ rectilinear star                                                     |
| **Math**        | ⋆ star operator · ≛ star equals · ⍣ star diaeresis                                        |

## ☢️ Hazards & Misc Symbols
| Icon | Name | Meaning |
|:--:|--|--|
| ☢️ | radioactive |  |
| ☣️ | biohazard |  |
| 👹 | ogre | danger |
| 🚨 | siren | alert |
| ⚠️ | warning |  |
| 🚧 | construction |  |
| `°` | degrees | measure/temperature |
| `֎` | symbol | eternity/infinity |
| 🔢 | input numbers | integer |
| 🔤 | input latin | string |
| 😎 | sunglasses | emojicode/logic |
| 🖼️ | framed picture | art/visual |

---

# 🧠 Canonical Patterns & Grammar

## ☁️⚙️ Machine in Cloud
Represents deployed runtime compute.

Variants:
- `☁️🧬` = model (training) in cloud
- `☁️🧮` = inference service in cloud
- `☁️⚙️` = generic runtime
- `☁️🐳` = container in cloud
- `☁️🧠` = learning system

## 📦 Delivery Flow

`📦 → ⛴ → ☁️⚙️ → 🏁`

(artifact → ship → cloud runtime → milestone)

## 🤝 HITL (Human-in-the-Loop) Patterns

| Concept                | Icon  |
|------------------------|-------|
| Model (training)       | 🧬    |
| Inference / prediction | 🧮    |
| Runtime                | ☁️⚙️  |
| Feedback Loop          | 🔄    |
| Governance             | 👥    |
| Boundary               | ⛓️‍💥 |
| Autonomous             | 🤖    |

## 🧩 Diagram Grammar

| Icon  | Name         | Meaning                      |
|:-----:|--------------|------------------------------|
|  🧩   | puzzle piece | Service                      |
|  🔌   | plug         | API / Port                   |
|  🧲   | magnet       | Injected dependency (IoC/DI) |
|  🗄️  | file cabinet | Database                     |
|  📣   | megaphone    | Event                        |
|  🔗   | link         | Dependency                   |
|  ⛓️   | chains       | Coupling                     |
| ⛓️‍💥 | broken chain | Decoupling / boundary        |
|  🧵   | thread       | Stream                       |
|  📊   | bar chart    | Metric                       |
|  🔥   | fire         | Architectural hotspot        |
|  🛰️  | satellite    | External dependency          |

## 🏁 Core Mental Model

📦 Artifact · ⛴ Ship · ☁️⚙️ Runtime · 🧬 Model · 🧮 Inference · 👥 Governance · ⛓️‍💥 Boundary · 🧲 IoC/DI

---

# ♻️ Self Updating Doc

A staging area you can edit freely. Drop emojis into the buckets below and ask me to **"update the file `emoji-lexicon-v7.md`"** — I'll process each bucket per the **Maintenance Protocol** at the very bottom.

## Instructions

How to use the buckets (for **you**, the human):

- **TODO** — a holding pen. Candidates I've surfaced (or you've parked) that you haven't decided on yet. From here you move emojis into *TO BE ORGANIZED* or *TO BE CANONIZED*.
- **MORE LIKE THIS** — drop an emoji here when you want *more options like it*. I'll find lookalikes (by name, visual form, color, subject) and add them to **TODO** with a note on why they're similar. The original stays so you can see the lineage.
- **TO BE ORGANIZED** — drop an emoji here and I'll file it under one or more **Categories** above (and remove it from the bucket).
- **TO BE CANONIZED** — drop an emoji here (ideally with a note saying *as what*) and I'll add it to the **Canonical Icons** table. No note / unclear note → I'll write a short explanation in `monospace` parentheses right after the emoji.
- **DON'T USE** — emojis to avoid in generated docs. Listed as a standing reminder.
- **TO BE DELETED** — emojis to purge from the whole document.

You can scribble an **inline note** next to any emoji, e.g. `💉 (use this for DI instead of 🧲)`. I'll try to honor inline notes first.

## TODO

_(empty — candidates I surface from MORE LIKE THIS land here for your review)_

## MORE LIKE THIS
_(drop emojis here that you want more options like)_
✨⭐🌟

## TO BE ORGANIZED

    _(drop emojis here to be filed under one or more categories)_
🏚️
## TO BE CANONIZED

_(drop emojis here — with a note saying "as what" — to add to the Canonical Icons table)_

## DON'T USE

- 🚀 rocket — overused; **do not** use for deploy/launch/excitement. Prefer ⛴ / 📦 / 🏁 for delivery.
- 🎯 target / bullseye — avoid for "objective/goal"; prefer 🏰 (goal/stronghold) or 🏁 (milestone).

---

# 🗑️ TO BE DELETED

_(emojis listed here get removed from every category, the canonical table, patterns, and quick-refs on the next update)_

- _(none yet)_

---

# 🤖 Maintenance Protocol (instructions for Claude)

When the user says **"update the file `emoji-lexicon-v7.md`"**, process the **Self Updating Doc** and **TO BE DELETED** sections **in this order**:

1. **Honor inline notes first.** If the user wrote a note beside any emoji (anywhere in the buckets), do what it says before applying the generic rule for that bucket.
2. **`MORE LIKE THIS`** → for **each** emoji, brainstorm similar emojis along four axes — **name**, **visual form**, **color**, **subject** — name each candidate, and append them to **`TODO`** with a one-line "why similar". **Leave the originals in place** (lineage). Do **not** auto-canonize or auto-file.
3. **`TODO`** → leave as a review pen. The user promotes these into *TO BE ORGANIZED* / *TO BE CANONIZED* themselves — don't move them unless a note tells you to.
4. **`TO BE ORGANIZED`** → file each emoji under **one or more** existing **Categories** (multi-category is fine), then **remove it** from the bucket.
5. **`TO BE CANONIZED`** → add each to the **Canonical Icons** table with a meaning explaining *as what*. If the user left **no note, or the note doesn't make sense**, generate a short explanation and place it in `monospace`/parentheses immediately after the emoji. Then remove it from the bucket.
6. **`DON'T USE`** → never emit these in any generated doc, and **scrub** them from the normal categories. Keep them listed here as a reminder.
7. **`TO BE DELETED`** → remove these emojis from **every** category, the Canonical Icons table, patterns, grammar, and quick-refs. Then clear the bucket.
8. **Keep the Canonical table unique** — an emoji appears at most once there (categories may repeat it).
9. **Re-version when drastic.** Per the global CLAUDE.md rules, if a pass changes the doc drastically, bump to `emoji-lexicon-v8.md` (keep the base name) and repoint the CLAUDE.md reference.
