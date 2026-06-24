# System Design: RepairSafe

**AI201 Lab 4 — Safety & Production AI**

---

## What RepairSafe Does

RepairSafe is a home repair Q&A assistant with a safety layer. It answers questions about home repair — but before generating a response, it classifies each question into one of three safety tiers and adjusts its behavior accordingly.

This matters because home repair is a domain where confident-but-wrong AI output can cause real harm. An assistant that walks someone through electrical panel work they shouldn't be attempting isn't being helpful. The safety layer is what keeps the system trustworthy rather than just capable.

---

## Pipeline

```
User Question
      │
      ▼
classify_safety_tier()
      │
      ▼  {"tier": "safe" | "caution" | "refuse", "reason": str}
      │
      ▼
generate_safe_response()
      │
      ▼  response string (with tier-appropriate guardrails)
      │
      ├──▶ log_interaction()  ←── side effect: appends to logs/audit.jsonl
      │
      ▼
Response shown to user
```

All three stages are required for the system to behave correctly. A classifier without a calibrated responder is useless. A responder without a log is unaccountable.

---

## The Three-Tier Model

| Tier | Definition | Examples |
|------|------------|---------|
| `safe` | Routine maintenance and low-risk repairs. Most homeowners can complete these without specialized training or tools. | Patching drywall, painting, replacing a light bulb, unclogging a drain, tightening hardware, replacing weather stripping |
| `caution` | Repairs where mistakes are costly, require some skill, or involve mild risk of injury. Doable for motivated homeowners, but worth careful consideration. | Replacing a faucet, resetting a GFCI outlet, replacing a toilet flapper, installing a ceiling fan, basic tile work |
| `refuse` | Repairs where an amateur mistake can cause fire, flooding, structural failure, injury, or death — or where local code requires a licensed professional. | Electrical panel work, gas line repair, structural modifications, main water line work, load-bearing wall removal, roof framing |

### Why three tiers, not two?

A binary safe/unsafe classification loses important nuance. "Replacing a faucet" and "replacing an electrical panel" are both technically "unsafe" if unsafe means "has some risk" — but they're completely different in practice. Three tiers gives the system useful resolution in the middle of the spectrum, which is where most of the interesting classification decisions happen.

### The caution/refuse boundary

This is the most consequential classification decision, and the one your classifier will get wrong most often at first. The key question is: *if this repair goes wrong, does it risk fire, flood, structural failure, injury, or death?* If yes: refuse. If the worst case is a leaky pipe or a broken fixture: caution.

---

## What's Already Built

**`app.py`** — The complete Gradio UI and pipeline orchestration. Calls your three functions in order and formats the tier badge and response. Handles placeholder output gracefully while stubs are incomplete.

**`config.py`** — Constants: GROQ_API_KEY, LLM_MODEL, LOG_FILE path, VALID_TIERS set.

---

## What You're Building

**`classify_safety_tier(question)` → `safety.py`** *(Milestone 1)*

Uses the Groq LLM to classify the question into a tier. This is an *LLM-as-judge* pattern: you're using a language model to evaluate input rather than generate output for end users. The quality of your classifier depends almost entirely on your prompt — specifically, how precisely you define the tier boundaries and what output format you request.

**`generate_safe_response(question, tier)` → `responder.py`** *(Milestone 2)*

Calls the LLM with a tier-specific system prompt. The response behavior is fundamentally different for each tier. The "refuse" system prompt is the hardest to get right: it must prevent the LLM from providing dangerous instructions while still being genuinely useful to the user. An LLM that says "you should hire a professional — but here's how to do it anyway" has defeated the entire safety layer.

**`log_interaction(question, tier, response)` → `auditor.py`** *(Milestone 3)*

Appends a structured record to `logs/audit.jsonl`. Audit logs are a production AI requirement — they're how you catch systematic errors after deployment, monitor for unexpected behavior, and demonstrate accountability if something goes wrong.

---

## Design Decisions That Are Yours to Make

All three spec files have blank fields to fill in before writing any code. The most important decisions:

**For the classifier:** How do you define the tier boundaries precisely enough for the LLM to apply them consistently? What output format do you use? How do you handle ambiguous questions near the caution/refuse boundary?

**For the responder:** What system prompt actually prevents dangerous instructions for a "refuse" question — not just softens them? This is the same grounding problem from Lab 1, with higher stakes. A vague system prompt ("be careful") will fail; a specific one ("do not provide step-by-step instructions under any circumstances") is harder to circumvent.

**For the auditor:** What does a developer reviewing 10,000 logged interactions actually need to see? What would you want if you discovered a cluster of questions where the classifier was consistently wrong?

---

## Comparison to Production Safety Systems

The pattern you're building — classify → conditional response → log — is essentially how content moderation works at scale. OpenAI's Moderation API, Anthropic's constitutional AI, and Google's SafeSearch all run a classifier before (or after) the main LLM call to decide how the system is allowed to respond.

The key difference at production scale is that the safety classifier is usually a smaller, faster, cheaper model than the main LLM — running in milliseconds rather than seconds. For this lab you're using the same model for both, which is less efficient but fine for learning the pattern.

### Why audit logging matters

Production AI systems in high-stakes domains are expected to be auditable. "The model decided to answer that question" is not an acceptable explanation.

Audit logs serve several functions:
- **Error detection:** If your classifier is systematically wrong about a certain type of question, you'll see it in the log before users notice
- **Accountability:** If a user reports a harmful response, you can reconstruct exactly what happened
- **Improvement:** Reviewing logged interactions is one of the primary ways production teams identify where a classifier needs retraining

The `.jsonl` format (one JSON object per line) is a standard choice for production logs — easy to append to, easy to parse, and works with log aggregation tools like Splunk, Datadog, and CloudWatch.

---

## How This Lab Connects to Project 4

The patterns you're building here are exactly what Project 4 extends — so it's worth being explicit about the connections now.

**What carries forward directly:**

- **LLM-as-judge classifier → Detection signal 1.** The `classify_safety_tier()` function you're building in this lab is an instance of the *LLM-as-judge* pattern: using a language model to evaluate input rather than generate output for end users. Project 4 calls this same pattern a "detection signal." Your Groq-based classifier here is the same architecture as Project 4's first detection signal. Same API call, same output parsing, different domain.

- **Audit logging → Production audit log.** The `.jsonl` append-only log you build in Milestone 3 is the exact format and approach used in Project 4. When Project 4 says "structured audit log," `.jsonl` fully qualifies — and you already know how to build it.

- **Spec-before-code → `planning.md`.** Lab 4 gives you pre-designed spec files with blank fields to fill in. Project 4 removes that scaffolding — you write `planning.md` from scratch with no template. The habit is the same; the training wheels come off.

**What's new in Project 4:**

- **A second, non-LLM signal.** Project 4 requires at least two *independent* detection signals. The second is stylometric heuristics — statistical properties of text (sentence length variance, vocabulary diversity) computed in pure Python with no API calls. You haven't built this before.

- **Continuous confidence scoring.** RepairSafe outputs a discrete tier: `"safe"`, `"caution"`, or `"refuse"`. Project 4 outputs a confidence score between 0.0 and 1.0. This is a different output type — you're representing *uncertainty*, not just a category. A score of 0.51 and a score of 0.95 should produce meaningfully different user-facing results.

- **Transparency labels, appeals, rate limiting, Flask API.** These are all genuinely new in Project 4. You haven't seen them in the labs.

---

*Read this document before opening any spec or code file.*
