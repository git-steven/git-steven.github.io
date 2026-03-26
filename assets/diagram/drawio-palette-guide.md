# draw.io Architecture Icon Palette Guide

Purpose: create consistent visual grammar across diagrams.

---

# Core System Icons

| Icon | Meaning |
|---|---|
🧩 | service
📦 | deployable artifact
🔌 | API / port
🔗 | dependency
🗄️ | datastore
📣 | event
🧵 | stream
📊 | metric
🔥 | incident

---

# Layered Architecture

Presentation  
🖥️ UI

Application  
🧠 logic

Domain  
🧬 business rules

Infrastructure  
🗄️ persistence

Example

🖥️ UI  
↓  
🧠 Service Layer  
↓  
🧬 Domain Model  
↓  
🗄️ Database

---

# Microservice Diagram

🧩 Order Service  
🔌 REST API  
🗄 Orders DB  

│  
│ 📣 OrderCreated  
▼  

🧩 Billing Service  
🔌 API  
🗄 Ledger DB  

---

# CQRS Diagram

📥 Command  
↓  
📣 Event  
↓  
📊 Projection

---

# DevOps Pipeline

commit → ⚙ build → 🧪 test → 📦 artifact → 🚀 deploy

---

# Data Pipeline

📥 ingest → 🧹 transform → 🗄 data lake → 📊 analytics

---

# draw.io Palette Groups

Architecture  
Services  
Data  
Messaging  
Pipelines  
Observability

---

# Design Principles

1. Icons represent system roles.
2. Keep icon meanings consistent.
3. Combine icons with short labels.
4. Avoid symbol overload.
