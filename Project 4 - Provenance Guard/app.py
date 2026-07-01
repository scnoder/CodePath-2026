import os
import uuid
import json
import math
import re
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)

_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
LLM_MODEL = "llama-3.3-70b-versatile"
LOG_FILE = "audit_log.json"

# ---------------------------------------------------------------------------
# Confidence thresholds (based on your design decisions)
#   >= 0.70  -> Likely AI-generated
#   0.45–0.69 -> Uncertain (leaning AI)
#   < 0.45   -> Likely human-written
# ---------------------------------------------------------------------------
THRESHOLD_AI = 0.70
THRESHOLD_UNCERTAIN_LOW = 0.45


# ---------------------------------------------------------------------------
# Audit log helpers
# ---------------------------------------------------------------------------

def load_log() -> list:
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_log(entries: list) -> None:
    with open(LOG_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def append_log(entry: dict) -> None:
    entries = load_log()
    entries.append(entry)
    save_log(entries)


# ---------------------------------------------------------------------------
# Signal 1 — LLM-based classification via Groq
# ---------------------------------------------------------------------------

def llm_signal(text: str) -> float:
    """
    Ask the LLM to assess whether the text reads as human or AI-generated.
    Returns a float 0.0–1.0 where 1.0 = definitely AI, 0.0 = definitely human.
    """
    prompt = f"""You are an expert at distinguishing human-written text from AI-generated text.

Analyze the following piece of writing and assess how likely it is to be AI-generated.

Consider:
- AI writing tends to be uniform, well-structured, and avoids personal quirks
- Human writing tends to be irregular, personal, and sometimes inconsistent
- AI writing often uses transitional phrases like "Furthermore", "It is important to note", "In conclusion"
- Human writing often has typos, informal language, or personal anecdotes

Respond ONLY in this exact format:
Score: <a number between 0.0 and 1.0>
Reasoning: <one sentence explanation>

Where 1.0 means definitely AI-generated and 0.0 means definitely human-written.

Text to analyze:
\"\"\"
{text}
\"\"\"
"""
    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )
    reply = response.choices[0].message.content.strip()

    score = 0.5  # default fallback
    for line in reply.splitlines():
        if line.startswith("Score:"):
            try:
                score = float(line.split(":", 1)[1].strip())
                score = max(0.0, min(1.0, score))
            except ValueError:
                pass
    return score


# ---------------------------------------------------------------------------
# Signal 2 — Stylometric heuristics (pure Python)
# ---------------------------------------------------------------------------

def stylometric_signal(text: str) -> float:
    """
    Measures statistical properties of writing that differ between human and AI text.
    Returns a float 0.0–1.0 where 1.0 = likely AI, 0.0 = likely human.

    Metrics used:
    - Sentence length variance (AI = low variance, uniform sentences)
    - Type-token ratio (AI = lower vocabulary diversity)
    - Filler phrase density (AI = more transitional/filler phrases)
    """
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s for s in sentences if len(s.strip()) > 0]

    if len(sentences) < 2:
        return 0.5  # not enough data

    # --- Metric 1: Sentence length variance ---
    lengths = [len(s.split()) for s in sentences]
    mean_len = sum(lengths) / len(lengths)
    variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)
    # Low std_dev = uniform = more AI-like
    # Normalize: std_dev < 3 -> high AI score, std_dev > 12 -> low AI score
    variance_score = max(0.0, min(1.0, 1.0 - (std_dev - 3) / 9))

    # --- Metric 2: Type-token ratio (vocabulary diversity) ---
    words = re.findall(r'\b\w+\b', text.lower())
    if len(words) == 0:
        ttr_score = 0.5
    else:
        ttr = len(set(words)) / len(words)
        # Low TTR = repetitive = more AI-like
        # Normalize: TTR < 0.4 -> high AI score, TTR > 0.7 -> low AI score
        ttr_score = max(0.0, min(1.0, 1.0 - (ttr - 0.4) / 0.3))

    # --- Metric 3: AI filler phrase density ---
    filler_phrases = [
        "it is important to note", "furthermore", "in conclusion",
        "it is worth noting", "in summary", "as previously mentioned",
        "it should be noted", "in today's world", "delve into",
        "it is essential", "needless to say", "at the end of the day",
        "in the realm of", "a testament to", "stands as a",
    ]
    text_lower = text.lower()
    filler_count = sum(1 for phrase in filler_phrases if phrase in text_lower)
    word_count = max(1, len(words))
    filler_density = filler_count / (word_count / 100)
    # Normalize: 0 fillers -> low AI score, 3+ per 100 words -> high AI score
    filler_score = max(0.0, min(1.0, filler_density / 3))

    # Weighted combination
    combined = (variance_score * 0.4) + (ttr_score * 0.35) + (filler_score * 0.25)
    return round(combined, 4)


# ---------------------------------------------------------------------------
# Confidence scoring
# ---------------------------------------------------------------------------

def combine_signals(llm_score: float, stylo_score: float) -> float:
    """
    Combines LLM score (weighted more heavily) and stylometric score
    into a single confidence score (0.0–1.0, higher = more likely AI).
    """
    return round((llm_score * 0.65) + (stylo_score * 0.35), 4)


# ---------------------------------------------------------------------------
# Transparency label
# ---------------------------------------------------------------------------

def generate_label(confidence: float) -> str:
    """
    Maps a confidence score to one of three transparency label variants.

    >= 0.70  -> Likely AI-generated
    0.45-0.69 -> Uncertain origin
    < 0.45   -> Likely human-written
    """
    if confidence >= THRESHOLD_AI:
        return (
            "AI-generated content detected. "
            f"This submission shows strong indicators of AI authorship "
            f"(confidence: {confidence:.0%}). "
            "The creator may submit an appeal if this classification is incorrect."
        )
    elif confidence >= THRESHOLD_UNCERTAIN_LOW:
        return (
            "Origin uncertain. "
            f"This submission shows mixed indicators — it may be human-written, "
            f"AI-generated, or a combination (confidence toward AI: {confidence:.0%}). "
            "Review the content directly to form your own judgment."
        )
    else:
        return (
            "Likely human-written. "
            f"This submission shows few indicators of AI authorship "
            f"(confidence toward AI: {confidence:.0%})."
        )


def attribution_result(confidence: float) -> str:
    if confidence >= THRESHOLD_AI:
        return "likely_ai"
    elif confidence >= THRESHOLD_UNCERTAIN_LOW:
        return "uncertain"
    else:
        return "likely_human"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/submit", methods=["POST"])
@limiter.limit("10 per minute;100 per day")
def submit():
    data = request.get_json(force=True)
    text = data.get("text", "").strip()
    creator_id = data.get("creator_id", "anonymous")

    if not text:
        return jsonify({"error": "text field is required"}), 400

    content_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        llm_score = llm_signal(text)
        stylo_score = stylometric_signal(text)
        confidence = combine_signals(llm_score, stylo_score)
        attribution = attribution_result(confidence)
        label = generate_label(confidence)

        log_entry = {
            "content_id": content_id,
            "creator_id": creator_id,
            "timestamp": timestamp,
            "attribution": attribution,
            "confidence": confidence,
            "llm_score": llm_score,
            "stylometric_score": stylo_score,
            "status": "classified",
            "appeal_reasoning": None,
        }
        append_log(log_entry)

        return jsonify({
            "content_id": content_id,
            "attribution": attribution,
            "confidence": confidence,
            "llm_score": llm_score,
            "stylometric_score": stylo_score,
            "label": label,
            "status": "classified",
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/appeal", methods=["POST"])
def appeal():
    data = request.get_json(force=True)
    content_id = data.get("content_id", "").strip()
    creator_reasoning = data.get("creator_reasoning", "").strip()

    if not content_id:
        return jsonify({"error": "content_id is required"}), 400
    if not creator_reasoning:
        return jsonify({"error": "creator_reasoning is required"}), 400

    entries = load_log()
    found = False
    for entry in entries:
        if entry["content_id"] == content_id:
            entry["status"] = "under_review"
            entry["appeal_reasoning"] = creator_reasoning
            entry["appeal_timestamp"] = datetime.now(timezone.utc).isoformat()
            found = True
            break

    if not found:
        return jsonify({"error": "content_id not found"}), 404

    save_log(entries)

    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": "Your appeal has been received and the submission is now under review.",
    })


@app.route("/log", methods=["GET"])
def get_log():
    entries = load_log()
    return jsonify({"entries": entries[-20:]})  # return most recent 20


if __name__ == "__main__":
    app.run(debug=True)