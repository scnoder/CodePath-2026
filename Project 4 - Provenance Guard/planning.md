# Provenance Guard — Planning Document

## Architecture Narrative

A piece of text submitted to `POST /submit` flows through two independent
detection signals — an LLM-based classifier (Groq) and a stylometric heuristics
analyzer — whose scores are combined into a single confidence value. That
confidence value drives a transparency label which is returned to the caller
alongside the raw scores. Every submission is written to a structured JSON audit
log. If a creator disputes their classification, they call `POST /appeal` with
their content ID and reasoning; the system updates that log entry to
`"under_review"` and stores their explanation for human review.

## Architecture

```
POST /submit
     │
     ▼
 [Input validation]
     │
     ├──────────────────────────┐
     ▼                          ▼
[Signal 1: LLM]        [Signal 2: Stylometrics]
 Groq llama-3.3         sentence length variance
 Semantic/holistic      type-token ratio
 score: 0.0–1.0         filler phrase density
                        score: 0.0–1.0
     │                          │
     └──────────┬───────────────┘
                ▼
      [Confidence scoring]
       LLM × 0.65 + Stylo × 0.35
       combined score: 0.0–1.0
                │
                ▼
      [Transparency label]
       >= 0.70  → Likely AI-generated
       0.45–0.69 → Uncertain
       < 0.45   → Likely human-written
                │
                ▼
        [Audit log write]
                │
                ▼
        JSON response to caller


POST /appeal
     │
     ▼
 [Look up content_id in audit log]
     │
     ▼
 [Update status → "under_review"]
 [Store creator_reasoning]
     │
     ▼
 [Save audit log]
     │
     ▼
 Confirmation response
```

---

## Detection Signals

### Signal 1 — LLM Classification (Groq)

**What it measures:** Semantic and stylistic coherence holistically. The model
reads the text the same way a human editor would and assesses whether it feels
machine-generated.

**Output:** A float 0.0–1.0 (1.0 = definitely AI).

**Blind spot:** The LLM can be fooled by heavily edited AI output or by formal
human writing (academic papers, legal documents) that happens to resemble AI
style. It also can't detect AI writing in languages it has less training data for.

**Weight in combined score:** 0.65

---

### Signal 2 — Stylometric Heuristics (pure Python)

**What it measures:** Three statistical properties of the text:
1. **Sentence length variance** — AI tends to write uniformly-lengthed sentences.
2. **Type-token ratio** — AI text tends to have lower vocabulary diversity.
3. **Filler phrase density** — AI text overuses transitional phrases like
   "Furthermore", "It is important to note", "In conclusion".

**Output:** A float 0.0–1.0 (1.0 = likely AI).

**Blind spot:** Formal human writing (essays, reports) naturally has lower
sentence variance and vocabulary diversity, which can produce false positives.
Very short texts (under ~50 words) don't have enough data for reliable statistics.

**Weight in combined score:** 0.35

---

## Uncertainty Representation

| Confidence score | Meaning | Label variant |
|---|---|---|
| >= 0.70 | Strong AI indicators | Likely AI-generated |
| 0.45–0.69 | Mixed indicators, leaning AI | Uncertain |
| < 0.45 | Few AI indicators | Likely human-written |

A score of ~0.50 means the signals are disagreeing or both returning near-neutral
results — the system genuinely cannot make a confident determination and leans
slightly toward AI per the design spec.

---

## Transparency Label Variants

**High-confidence AI (>= 0.70):**
> "AI-generated content detected. This submission shows strong indicators of AI
> authorship (confidence: 85%). The creator may submit an appeal if this
> classification is incorrect."

**Uncertain (0.45–0.69):**
> "Origin uncertain. This submission shows mixed indicators — it may be
> human-written, AI-generated, or a combination (confidence toward AI: 58%).
> Review the content directly to form your own judgment."

**Likely human (< 0.45):**
> "Likely human-written. This submission shows few indicators of AI authorship
> (confidence toward AI: 22%)."

---

## Appeals Workflow

- **Who can appeal:** Any creator who submitted content (identified by `creator_id`).
- **What they provide:** The `content_id` from their original submission and a
  plain-language explanation of why they believe the classification is wrong.
- **What the system does:**
  - Updates the log entry's `status` from `"classified"` to `"under_review"`
  - Stores `appeal_reasoning` and `appeal_timestamp` on the entry
  - Returns a confirmation to the creator
- **What a human reviewer sees:** The full log entry via `GET /log`, including
  original scores, the label that was shown, and the creator's reasoning.
- **Automated re-classification:** Not implemented. A human reviewer resolves appeals.

---

## Anticipated Edge Cases

1. **Formal human writing** (academic papers, legal documents): Low sentence
   variance and formal vocabulary will push the stylometric score toward AI even
   for genuine human writing. The LLM signal may partially compensate, but
   false positives are likely here.

2. **Very short submissions** (under 50 words): Stylometric heuristics require
   enough text to compute meaningful statistics. A haiku or short poem will
   produce unreliable scores. The system returns `0.5` as a fallback for
   sentence-level analysis when fewer than 2 sentences are detected.

3. **Lightly edited AI output**: A human who prompts an AI and then edits the
   result may produce text that scores in the uncertain range — neither signal
   will confidently classify it, which is arguably the correct behavior.

---

## API Surface

| Method | Endpoint | Description |
|---|---|---|
| POST | `/submit` | Submit text for attribution analysis |
| POST | `/appeal` | Contest a classification by content_id |
| GET | `/log` | Return the 20 most recent audit log entries |

---

## Rate Limiting

Applied to `POST /submit`:
- **10 per minute** — a real creator submitting their own work would never need
  more than a few submissions per minute. This prevents rapid scripted flooding.
- **100 per day** — generous enough for legitimate multi-submission workflows
  (a platform processing a batch of new posts) while making large-scale abuse
  expensive.

---

## AI Tool Plan

### M3 — Submission endpoint + Signal 1
- Provide: Detection signals section + Architecture diagram
- Ask for: Flask app skeleton with POST /submit stub + LLM signal function
- Verify: Call llm_signal() directly on 3 test inputs and check score range

### M4 — Signal 2 + Confidence scoring
- Provide: Detection signals + Uncertainty representation sections + diagram
- Ask for: Stylometric signal function + combine_signals() logic
- Verify: Run both signals on clearly AI and clearly human text; check scores differ meaningfully

### M5 — Production layer
- Provide: Label variants + Appeals workflow + diagram
- Ask for: generate_label() function + POST /appeal endpoint
- Verify: Submit 3 inputs that hit all 3 label variants; test appeal updates status in /log