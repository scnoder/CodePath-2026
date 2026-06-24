# RepairSafe — Home Repair Safety Assistant

**AI201 Lab 4 Starter Repository**

RepairSafe is a home repair Q&A tool with a safety classification layer. Before answering any question, it classifies the request into one of three safety tiers and adjusts its behavior accordingly.

---

## Setup

1. Fork this repo and clone your fork locally
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Mac/Linux
   # or: .venv\Scripts\activate  # Windows
   ```

3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your Groq API key
5. Run the app: `python app.py`

---

## What to Implement

| Milestone | File | Function | Description |
|-----------|------|----------|-------------|
| 1 | `safety.py` | `classify_safety_tier()` | Classify question into safe / caution / refuse |
| 2 | `responder.py` | `generate_safe_response()` | Generate tier-appropriate response |
| 3 | `auditor.py` | `log_interaction()` | Append interaction record to audit log |

Complete each spec in `specs/` before implementing the corresponding function.

---

## Repository Structure

```
ai201-lab4-repairsafe-starter/
├── app.py              ← Gradio UI and pipeline orchestration (pre-built)
├── safety.py           ← Milestone 1: safety tier classifier
├── responder.py        ← Milestone 2: tier-aware response generator
├── auditor.py          ← Milestone 3: audit logger
├── config.py           ← constants (API key, model, log path, valid tiers)
├── data/
│   └── repair_tiers.md ← tier guide shown in the app's Tier Guide tab
├── logs/               ← audit.jsonl written here after Milestone 3
└── specs/
    ├── system-design.md    ← read this first
    ├── classifier-spec.md  ← Milestone 1 spec
    ├── responder-spec.md   ← Milestone 2 spec
    └── auditor-spec.md     ← Milestone 3 spec
```
