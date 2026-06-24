import gradio as gr
from safety import classify_safety_tier
from responder import generate_safe_response
from auditor import log_interaction

# ---------------------------------------------------------------------------
# Example questions — 2 safe, 2 caution, 2 clearly refuse, 2 at the boundary
# The "replace outlet" vs "add outlet" pair is the key contrast for Milestone 1
# ---------------------------------------------------------------------------

EXAMPLES = [
    "How do I patch a small hole in drywall?",
    "How do I unclog a slow bathroom drain?",
    "How do I replace a bathroom faucet?",
    "How do I reset a GFCI outlet that won't reset?",
    "Can I replace an electrical outlet that stopped working?",
    "Can I add a new electrical outlet to my garage?",
    "Can I upgrade my electrical panel to 200 amps myself?",
    "How do I fix a gas line that smells like it's leaking?",
]

# ---------------------------------------------------------------------------
# Tier display config
# ---------------------------------------------------------------------------

TIER_CONFIG = {
    "safe": {
        "color": "#16a34a",
        "icon": "✅",
        "label": "SAFE TO DIY",
        "note": "This is a routine repair most homeowners can handle.",
    },
    "caution": {
        "color": "#d97706",
        "icon": "⚠️",
        "label": "PROCEED WITH CAUTION",
        "note": "This repair is doable, but mistakes have real cost. Read carefully.",
    },
    "refuse": {
        "color": "#dc2626",
        "icon": "🚫",
        "label": "PROFESSIONAL REQUIRED",
        "note": "This repair requires a licensed professional. Do not attempt DIY.",
    },
    "unknown": {
        "color": "#64748b",
        "icon": "⚙️",
        "label": "NOT YET CLASSIFIED",
        "note": "Complete Milestone 1 to enable safety classification.",
    },
}


def _tier_html(tier: str, reason: str) -> str:
    cfg = TIER_CONFIG.get(tier, TIER_CONFIG["unknown"])
    color = cfg["color"]
    icon = cfg["icon"]
    label = cfg["label"]
    note = cfg["note"]
    reason_block = (
        f'<p style="margin:8px 0 0 0;color:#374151;font-size:0.9em;">'
        f'<strong>Why:</strong> {reason}</p>'
        if reason and tier in ("safe", "caution", "refuse")
        else ""
    )
    return (
        f'<div style="font-family:sans-serif;padding:14px 18px;'
        f'border-left:5px solid {color};background:#f9fafb;'
        f'border-radius:0 8px 8px 0;margin-bottom:4px;">'
        f'  <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">'
        f'    <span style="font-size:1.25em;">{icon}</span>'
        f'    <span style="background:{color};color:white;padding:3px 14px;'
        f'border-radius:12px;font-weight:700;font-size:0.9em;letter-spacing:0.06em;">'
        f'{label}</span>'
        f'  </div>'
        f'  <p style="margin:4px 0 0 0;color:#6b7280;font-size:0.85em;">{note}</p>'
        f'  {reason_block}'
        f'</div>'
    )


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------

def handle_question(question: str):
    if not question.strip():
        return (
            "<p style='color:#9ca3af;font-style:italic;'>Ask a repair question to see the safety tier.</p>",
            "",
        )

    # Milestone 1: classify
    tier_result = classify_safety_tier(question)
    tier = tier_result.get("tier", "unknown")
    reason = tier_result.get("reason", "")

    # Milestone 2: generate response
    response = generate_safe_response(question, tier)

    # Milestone 3: log
    log_interaction(question, tier, response)

    return _tier_html(tier, reason), response


# ---------------------------------------------------------------------------
# Tier guide content (loaded once at startup)
# ---------------------------------------------------------------------------

def _load_tier_guide() -> str:
    try:
        with open("data/repair_tiers.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "_Tier guide not found. Make sure `data/repair_tiers.md` exists._"


TIER_GUIDE_CONTENT = _load_tier_guide()


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

THEME = gr.themes.Soft(
    primary_hue="orange",
    secondary_hue="red",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
)

CSS = """
#ask-btn { background: #ea580c; color: white; font-weight: 600; }
#ask-btn:hover { background: #c2410c; }
"""

with gr.Blocks(title="RepairSafe") as demo:

    gr.Markdown(
        """
# 🔧 RepairSafe
**AI201 Lab 4 — Home Repair Safety Assistant**

Ask any home repair question. RepairSafe classifies the risk before answering —
not every repair should come with a confident "here's how."

Before the safety layer works, complete the milestones:
- **Milestone 1:** Implement `classify_safety_tier()` in `safety.py`
- **Milestone 2:** Implement `generate_safe_response()` in `responder.py`
- **Milestone 3:** Implement `log_interaction()` in `auditor.py`
        """
    )

    with gr.Tabs():

        with gr.Tab("Ask a Question"):
            with gr.Row():

                with gr.Column(scale=2):
                    question_box = gr.Textbox(
                        label="Your repair question",
                        placeholder="e.g. How do I replace a bathroom faucet?",
                        lines=3,
                    )
                    ask_btn = gr.Button("Ask RepairSafe →", elem_id="ask-btn")

                    gr.Markdown("---")
                    gr.Markdown("#### Try an example")
                    with gr.Row():
                        for ex in EXAMPLES:
                            short = ex[:40] + "…" if len(ex) > 40 else ex
                            btn = gr.Button(short, size="sm")
                            btn.click(fn=lambda e=ex: e, outputs=question_box)

                with gr.Column(scale=2):
                    gr.Markdown("#### Safety Classification")
                    tier_display = gr.HTML(
                        value="<p style='color:#9ca3af;font-style:italic;'>Result will appear here.</p>"
                    )
                    gr.Markdown("#### Response")
                    response_box = gr.Textbox(
                        label="",
                        lines=10,
                        interactive=False,
                        show_label=False,
                        placeholder="Response will appear here after Milestone 2 is complete.",
                    )

            ask_btn.click(
                fn=handle_question,
                inputs=question_box,
                outputs=[tier_display, response_box],
            )
            question_box.submit(
                fn=handle_question,
                inputs=question_box,
                outputs=[tier_display, response_box],
            )

        with gr.Tab("Tier Guide"):
            gr.Markdown(
                """
Use this reference while building your classifier. The taxonomy here defines
what each tier means, gives concrete examples for each, and walks through the
edge cases where the **caution/refuse boundary** is most easily confused.

Your `classify_safety_tier()` prompt in `safety.py` needs to capture these
distinctions — especially the "replacing existing" vs. "adding new" contrast.
                """
            )
            gr.Markdown(TIER_GUIDE_CONTENT)

if __name__ == "__main__":
    demo.launch(theme=THEME, css=CSS)
