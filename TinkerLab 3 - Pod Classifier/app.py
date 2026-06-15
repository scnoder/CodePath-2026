import gradio as gr
from classifier import classify_episode, load_labeled_examples
from evaluate import run_evaluation, format_evaluation_report

# ---------------------------------------------------------------------------
# Example descriptions for the UI
# ---------------------------------------------------------------------------

EXAMPLES = [
    [
        "The Case for Four-Day Workweeks",
        "I've been thinking about the four-day workweek for months, and I want to lay out the case for it as clearly as I can. I'm going to cover the productivity research, the companies that have tried it, the objections I find compelling versus the ones I don't, and what I think it would actually take for this to become mainstream. This is a topic I have a real view on, and I want to share it.",
    ],
    [
        "Dr. Priya Nair on Adolescent Mental Health After the Pandemic",
        "Dr. Priya Nair is a child and adolescent psychiatrist at Stanford who has spent the past three years studying how the pandemic reshaped mental health outcomes for teenagers. In this conversation, she walks through what the data shows, what she's seeing in her clinical practice, and where she thinks the public conversation is getting it wrong. We also talk about what parents can actually do — and what is mostly noise.",
    ],
    [
        "The Aral Sea: A Disaster in Four Acts",
        "The Aral Sea was once the fourth largest lake in the world. By 2007, it had lost ninety percent of its volume. This episode tells the story in four parts: the Soviet irrigation decision that started it, the fishing industry that collapsed, the communities that tried to adapt, and the partial recovery that scientists didn't expect. It's a story about what happens when an ecosystem and an economy collapse at the same time.",
    ],
    [
        "Five Writers on What It Means to Write for the Internet Now",
        "Five writers who came up in the blog era sit down to talk about how the internet has changed what it means to publish writing. They don't agree on whether the changes are good. They do agree that the economics, the audience relationship, and the editorial incentives are all different from what they expected twenty years ago. A frank conversation about craft, attention, and money.",
    ],
]

LABEL_COLORS = {
    "interview": "#6366f1",   # indigo
    "solo":      "#8b5cf6",   # violet
    "panel":     "#a855f7",   # purple
    "narrative": "#d946ef",   # fuchsia
    "unknown":   "#94a3b8",   # slate
    None:        "#94a3b8",
}

LABEL_DESCRIPTIONS = {
    "interview": "One host + one guest. The guest's knowledge or experience drives the episode.",
    "solo":      "A single host speaking directly to the audience — opinion, reflection, or explainer.",
    "panel":     "Multiple guests (usually 3+) in structured discussion. No single voice dominates.",
    "narrative": "Reported or documentary storytelling. Events unfold across the episode.",
}


# ---------------------------------------------------------------------------
# Helper: format the classify output as HTML
# ---------------------------------------------------------------------------

def _label_badge(label: str) -> str:
    color = LABEL_COLORS.get(label, "#94a3b8")
    return (
        f'<span style="background:{color};color:white;padding:4px 14px;'
        f'border-radius:12px;font-weight:700;font-size:1.1em;letter-spacing:0.04em;">'
        f'{label or "unknown"}</span>'
    )


def _result_html(label: str, reasoning: str) -> str:
    desc = LABEL_DESCRIPTIONS.get(label, "Label not recognized.")
    badge = _label_badge(label)
    return f"""
<div style="font-family:sans-serif;padding:16px 0;">
  <div style="margin-bottom:12px;">{badge}</div>
  <p style="color:#6b7280;margin:0 0 12px 0;font-style:italic;">{desc}</p>
  <div style="background:#f8f7ff;border-left:4px solid #8b5cf6;padding:12px 16px;border-radius:0 8px 8px 0;">
    <strong style="color:#4c1d95;">Reasoning:</strong>
    <p style="margin:6px 0 0 0;color:#374151;">{reasoning}</p>
  </div>
</div>
"""


# ---------------------------------------------------------------------------
# Core UI callbacks
# ---------------------------------------------------------------------------

def classify_description(description: str) -> str:
    if not description.strip():
        return "<p style='color:#9ca3af;font-style:italic;'>Paste an episode description above and click Classify.</p>"

    labeled_examples = load_labeled_examples()

    if not labeled_examples:
        return (
            "<div style='background:#fef3c7;border-left:4px solid #f59e0b;padding:12px 16px;border-radius:0 8px 8px 0;'>"
            "<strong>⚠️ No labeled examples found.</strong><br>"
            "Open <code>data/my_labels.json</code> and add at least one label before classifying. "
            "See Milestone 1 in the lab instructions."
            "</div>"
        )

    result = classify_episode(description, labeled_examples)
    return _result_html(result["label"], result["reasoning"])


def fill_example(title: str, description: str) -> tuple[str, str]:
    return title, description


def run_eval() -> str:
    labeled_examples = load_labeled_examples()
    if not labeled_examples:
        return (
            "⚠️  No labeled examples found.\n\n"
            "Complete Milestone 1 first: open data/my_labels.json and add labels "
            "for the training episodes."
        )
    print("\n--- Running evaluation ---")
    eval_results = run_evaluation()
    report = format_evaluation_report(eval_results)
    print("--- Evaluation complete ---\n")
    return report


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

THEME = gr.themes.Soft(
    primary_hue="violet",
    secondary_hue="purple",
    neutral_hue="slate",
)

CSS = """
#classify-btn { background: #7c3aed; color: white; font-weight: 600; }
#classify-btn:hover { background: #6d28d9; }
#eval-btn { background: #4f46e5; color: white; font-weight: 600; }
#eval-btn:hover { background: #4338ca; }
.label-legend { font-size: 0.85em; color: #6b7280; }
"""

with gr.Blocks(title="Pod Classifier") as demo:

    gr.Markdown(
        """
# 🎙️ Pod Classifier
**AI201 Lab 3 — Few-Shot Podcast Episode Classifier**

Classify podcast episode descriptions into four categories: **interview**, **solo**, **panel**, or **narrative**.
Before the classifier works, you need to complete the milestones:
- **Milestone 1:** Label the training episodes in `data/my_labels.json`
- **Milestone 2:** Implement `build_few_shot_prompt()` and `classify_episode()` in `classifier.py`
- **Milestone 3:** Implement `compute_accuracy()` and `compute_per_class_accuracy()` in `evaluate.py`
        """
    )

    with gr.Tabs():

        # ── Tab 1: Classify ─────────────────────────────────────────────────
        with gr.Tab("🏷️ Classify"):
            gr.Markdown("### Try the classifier on any episode description")

            with gr.Row():
                with gr.Column(scale=2):
                    title_box = gr.Textbox(
                        label="Episode title (optional — for your reference)",
                        placeholder="e.g. Chef Marcus Lin on What Restaurant Culture Gets Wrong About Burnout",
                        lines=1,
                    )
                    description_box = gr.Textbox(
                        label="Episode description",
                        placeholder="Paste a podcast episode description here…",
                        lines=8,
                    )
                    classify_btn = gr.Button("Classify →", elem_id="classify-btn")

                with gr.Column(scale=2):
                    gr.Markdown("#### Result")
                    result_html = gr.HTML(
                        value="<p style='color:#9ca3af;font-style:italic;'>Result will appear here.</p>"
                    )

            gr.Markdown("---")
            gr.Markdown("#### Try an example")

            with gr.Row():
                for title, desc in EXAMPLES:
                    short = title[:42] + "…" if len(title) > 42 else title
                    btn = gr.Button(short, size="sm")
                    btn.click(
                        fn=fill_example,
                        inputs=[gr.State(title), gr.State(desc)],
                        outputs=[title_box, description_box],
                    )

            classify_btn.click(
                fn=classify_description,
                inputs=[description_box],
                outputs=[result_html],
            )

        # ── Tab 2: Evaluate ──────────────────────────────────────────────────
        with gr.Tab("📊 Evaluate"):
            gr.Markdown(
                """
### Run evaluation against the held-out test set

Click the button to run your classifier against all 20 pre-labeled test episodes
and see overall and per-class accuracy.

> **Note:** The evaluation calls the LLM once per test episode (20 calls total).
> Watch your terminal to see each classification as it happens.
                """
            )
            eval_btn = gr.Button("Run Evaluation", elem_id="eval-btn")
            eval_output = gr.Markdown(
                value="_Click **Run Evaluation** to see results._"
            )

            eval_btn.click(
                fn=run_eval,
                inputs=[],
                outputs=[eval_output],
            )

        # ── Tab 3: Label Guide ───────────────────────────────────────────────
        with gr.Tab("📖 Label Guide"):
            gr.Markdown(
                """
### Four-Label Taxonomy

Use this guide when labeling `data/my_labels.json` in Milestone 1.

---

#### 🎤 interview
One host, one guest. The guest's expertise, experience, or story is the main subject.
The host asks questions; the guest answers. The host may push back, but the guest drives content.

*Key signal:* Single named guest. Conversation structure.

---

#### 🎧 solo
One host speaking directly to the audience. No guests. May be opinion, reflection, analysis,
or personal essay. The host's voice and perspective are everything.

*Key signal:* First person throughout. No other voices.

---

#### 👥 panel
Multiple people (usually 3+) in structured discussion. Multiple perspectives on a shared topic.
No single voice dominates. May have a moderator, but the moderator does not drive content.

*Key signal:* "X experts discuss…" or a roundtable format.

---

#### 📻 narrative
Reported or documentary storytelling. Follows a story, character, or event across time.
Evidence is assembled from multiple sources. The episode has a story arc, not a conversation arc.

*Key signal:* Past tense, scenes, "This episode follows…", "Reported over X months…"

---

#### Edge cases

| Situation | Label |
|---|---|
| Interview with a strong storytelling frame | **interview** (guest still drives) |
| Solo episode where host uses "we" throughout | **solo** (one host's voice) |
| Two equal co-hosts, no guests | **panel** (multiple perspectives) |
| Narrative that weaves in interview clips | **narrative** (story arc dominates) |
| First-person personal story in past tense | **solo** if only the host's memory; **narrative** if built from external sources (documents, archives, others' interviews) |
                """
            )

    gr.Markdown(
        "<p style='text-align:center;color:#9ca3af;font-size:0.85em;margin-top:24px;'>"
        "AI201 · CodePath · Pod Classifier Lab</p>"
    )

if __name__ == "__main__":
    demo.launch(theme=THEME, css=CSS)
