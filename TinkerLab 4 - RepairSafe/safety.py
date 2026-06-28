from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)


def classify_safety_tier(question: str) -> dict:
    """
    Classify a home repair question into one of three safety tiers.

    TODO — Milestone 1:

    Before writing any code, complete specs/classifier-spec.md. The blank fields
    there are the decisions that drive this implementation — prompt design, tier
    definitions, output format, and edge case handling.

    Your implementation should:
      1. Build a prompt using your tier definitions that asks the LLM to classify
         the question and explain its reasoning
      2. Send a single chat completion request (no tools, no history)
      3. Parse the tier and reason out of the raw response text
      4. Validate the tier against VALID_TIERS; fall back to "caution" if the
         response can't be parsed or the tier isn't recognized
      5. Return {"tier": ..., "reason": ...}

    Returns a dict with:
      - "tier"   : str — one of "safe", "caution", "refuse"
      - "reason" : str — a brief explanation of why this tier was assigned

    The three tiers:
      - "safe"    : routine, low-risk repairs most homeowners can handle safely
      - "caution" : doable with care, but mistakes have real cost or mild risk
      - "refuse"  : high-risk repairs that require a licensed professional — mistakes can cause fire, flooding, injury, or structural damage
    """

    prompt = f"""

    You are a safety classifier for home repair questions. Classify the user's question into exactly one tier: "safe", "caution", or "refuse". Tier definitions: - safe: Routine maintenance or low-risk repair where a typical homeowner using basic tools is unlikely to cause anything worse than cosmetic damage or a broken fixture, and no permit or licensed professional is normally required. - caution: A repair a careful homeowner may be able to perform, usually at an existing fixture or connection, but where mistakes involving water, electricity, tools, or installation quality can cause meaningful property damage or minor injury. - refuse: Work that should not receive DIY instructions because it can cause fire, flooding, structural failure, serious injury, death, or normally requires a permit or licensed professional, including new electrical/plumbing/gas work and structural modifications.

    Boundary rules:
    - Replacing an existing electrical device, fixture, faucet, toilet part, thermostat, ceiling fan, or showerhead in the same location is usually caution.
    - Adding a new outlet, switch, circuit, electrical run, plumbing line, gas line, or appliance connection is refuse.
    - Electrical panel work, service entrance work, breakers, gas work, gas odors, main water shutoff replacement, water heater replacement, structural wall removal, foundation work, and structural roof repair are refuse.
    - Removing a wall is refuse unless the user states that a structural engineer has confirmed it is non-load-bearing.
    - Small-sounding changes are still refuse if they require new wiring, new pipe, gas work, panel work, or structural modification.
    - If the question is ambiguous, choose the more protective tier that fits the likely work; do not classify as safe unless it is clearly low-risk.


    The three tiers:
      - "safe"    : routine, low-risk repairs most homeowners can handle safely
      - "caution" : doable with care, but mistakes have real cost or mild risk
      - "refuse"  : high-risk repairs that require a licensed professional — mistakes can cause fire, flooding, injury, or structural damage. Classify as refuse when the requested work requires new wiring, new plumbing, gas work, structural modification, permit/licensed work, or could plausibly cause fire, major flooding, structural failure, serious injury, or death; classify as caution when it is a same-location replacement or minor repair where the realistic worst case is a damaged fixture, tripped breaker, leak, or minor injury.

    Return your answer in this format:
      Tier: <tier>
      Reason: <brief explanation>

      Classify this home repair question: {question}

    """

    format = """
    Each question should be returned with the tier and the reason why. Here is an examples:

    Example 1: "How do I replace an outlet that stopped working?"
    Tier: Caution
    Reasoning: It swaps an existing device on an existing circuit at the same location, so the likely failure mode is a tripped breaker or nonworking outlet rather than new hidden fire-risk work.

    Example 2: "How do I add a new outlet to my garage?"
    Tier: Refuse
    Reasoning: Adding an outlet requires running new wiring and may involve a new circuit, panel work, permits, and long-term fire risk if done incorrectly.
    """

    try: 

        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": format},
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.choices[0].message.content
        
        tier = "caution"
        reason = ""

        for line in reply.splitlines():
            if line.startswith("Tier:"):
                tier = line.split(":", 1)[1].strip().lower()
            elif line.startswith("Reason:"):
                reason = line.split(":", 1)[1].strip()

        return {
            "tier": tier,
            "reason": reason
        }
    except Exception:
        return {
            "tier": "caution",
            "reason": ""
        }