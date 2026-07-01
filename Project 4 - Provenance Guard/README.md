# Provenance Guard

A backend system that classifies submitted text as human-written or AI-generated,
returns a confidence score and transparency label, and handles creator appeals.

---

## Setup
Run the server:
```bash
python app.py
```

---

### POST /submit

Accepts a piece of text and returns an attribution result.

**Request:**
```json
{
  "text": "Your poem, story, or blog post here...",
  "creator_id": "user-123"
}
```

**Response:**
```json
{
  "content_id": "3f7a2b1e-...",
  "attribution": "likely_ai",
  "confidence": 0.82,
  "llm_score": 0.87,
  "stylometric_score": 0.72,
  "label": "AI-generated content detected. This submission shows strong indicators of AI authorship (confidence: 82%). The creator may submit an appeal if this classification is incorrect.",
  "status": "classified"
}
```

### POST /appeal

Contest a classification by content_id.

**Request:**
```json
{
  "content_id": "3f7a2b1e-...",
  "creator_reasoning": "I wrote this myself. I am an academic and my writing style is naturally formal."
}
```

**Response:**
```json
{
  "content_id": "3f7a2b1e-...",
  "status": "under_review",
  "message": "Your appeal has been received and the submission is now under review."
}
```

### GET /log

Returns the 20 most recent audit log entries.

---

## Detection Signals

### Signal 1 — LLM Classification (Groq, weight: 65%)

Sends the text to `llama-3.3-70b-versatile` with a structured prompt asking it
to score how likely the text is AI-generated (0.0–1.0). This captures semantic
and stylistic coherence holistically — things like tone consistency, generic
phrasing, and the absence of personal voice.

**Blind spot:** Formal human writing (academic, legal) can resemble AI style and
produce false positives.

### Signal 2 — Stylometric Heuristics (pure Python, weight: 35%)

Computes three statistical properties:
- **Sentence length variance** — AI tends toward uniform sentence lengths
- **Type-token ratio** — AI text has lower vocabulary diversity
- **Filler phrase density** — AI overuses transitional phrases like "Furthermore"

**Blind spot:** Short texts (under ~50 words) don't have enough data for reliable
statistics; the signal defaults to 0.5.

---

## Confidence Scoring

Signals are combined as: `confidence = (llm_score × 0.65) + (stylo_score × 0.35)`

The LLM signal is weighted more heavily because it captures nuance that
heuristics miss. The stylometric signal acts as a structural check — it can catch
AI writing that has been lightly edited to sound more natural.

**Example scores from testing:**

| Input | LLM score | Stylo score | Combined |
|---|---|---|---|
| Clearly AI (formal tech paragraph) | 0.90 | 0.78 | 0.86 |
| Clearly human (casual social post) | 0.12 | 0.21 | 0.15 |
| Borderline (lightly edited AI) | 0.58 | 0.51 | 0.56 |

---

## Transparency Label Variants

All three variants the system can display:

**High-confidence AI (confidence >= 0.70):**
> "AI-generated content detected. This submission shows strong indicators of AI authorship (confidence: 85%). The creator may submit an appeal if this classification is incorrect."

**Uncertain (confidence 0.45–0.69):**
> "Origin uncertain. This submission shows mixed indicators — it may be human-written, AI-generated, or a combination (confidence toward AI: 58%). Review the content directly to form your own judgment."

**Likely human-written (confidence < 0.45):**
> "Likely human-written. This submission shows few indicators of AI authorship (confidence toward AI: 22%)."

---

## Rate Limiting

Applied to `POST /submit`:
- **10 requests per minute**
- **100 requests per day**

A legitimate creator submitting their own work would never need more than a few
submissions per minute. 10/minute prevents automated flooding while remaining
comfortable for any real usage pattern. 100/day is generous for a single creator
but makes large-scale adversarial scraping expensive.

When the limit is exceeded the server returns HTTP `429 Too Many Requests`.

---

## Audit Log

Every submission and appeal is written to `audit_log.json`. Sample entries:

```json
[
  {
    "content_id": "3f7a2b1e-4c9d-4e2a-b123-abc123def456",
    "creator_id": "test-user-1",
    "timestamp": "2025-04-01T14:32:10.123Z",
    "attribution": "likely_ai",
    "confidence": 0.82,
    "llm_score": 0.87,
    "stylometric_score": 0.72,
    "status": "classified",
    "appeal_reasoning": null
  },
  {
    "content_id": "7a1b2c3d-5e6f-7a8b-c901-def456abc789",
    "creator_id": "test-user-2",
    "timestamp": "2025-04-01T14:35:22.456Z",
    "attribution": "likely_human",
    "confidence": 0.15,
    "llm_score": 0.12,
    "stylometric_score": 0.21,
    "status": "classified",
    "appeal_reasoning": null
  },
  {
    "content_id": "3f7a2b1e-4c9d-4e2a-b123-abc123def456",
    "creator_id": "test-user-1",
    "timestamp": "2025-04-01T14:32:10.123Z",
    "attribution": "likely_ai",
    "confidence": 0.82,
    "llm_score": 0.87,
    "stylometric_score": 0.72,
    "status": "under_review",
    "appeal_reasoning": "I wrote this myself. I am an academic and my writing style is naturally formal.",
    "appeal_timestamp": "2025-04-01T15:01:33.789Z"
  }
]
```

---

## Known Limitations

**Formal human writing produces false positives.** Academic papers, legal
documents, and professional reports naturally have low sentence length variance
and formal vocabulary — both properties the stylometric signal associates with AI
writing. A professor submitting their own essay could receive an "uncertain" or
even "likely AI" label. The appeals workflow exists specifically to handle this case.

---

## Spec Reflection

The planning.md spec helped most during confidence scoring — having written out
the exact thresholds (0.70, 0.45) before coding meant the label logic was
straightforward to implement and easy to verify. The one divergence: the original
plan weighted both signals equally, but after testing, the LLM signal was
noticeably more accurate on borderline cases, so the weighting was adjusted to
65/35 in favor of the LLM.

---

## AI Usage

1. **Stylometric signal structure:** Asked Claude to generate a Python function
   that computes sentence length variance and type-token ratio from raw text.
   The generated function used `nltk` for sentence splitting; revised it to use
   `re.split` on punctuation to eliminate the external dependency.

2. **Audit log update logic:** Asked Claude to generate the appeal endpoint's
   log-update loop. The generated version used a list comprehension that
   rebuilt the entire list; replaced with an in-place loop to make the
   "found/not found" logic clearer and to return a 404 correctly.