# AI201 Lab 3 — Pod Classifier

A few-shot podcast episode classifier. Given an episode description, classifies it
as `interview`, `solo`, `panel`, or `narrative` using labeled examples and an LLM.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

## Run

```bash
python app.py
```

## Lab milestones

| Milestone | Task | File |
|---|---|---|
| 1 | Label 20 training episodes | `data/my_labels.json` |
| 2 | Implement the few-shot classifier | `classifier.py` |
| 3 | Implement evaluation metrics | `evaluate.py` |

See the lab instructions for full details.

## Project structure

```
ai201-lab3-podclassifier-starter/
├── app.py              # Gradio UI
├── classifier.py       # Few-shot classification logic
├── evaluate.py         # Evaluation metrics
├── config.py           # Settings and constants
├── requirements.txt
├── .env.example
├── data/
│   ├── train_episodes.json   # 20 episodes to label (Milestone 1)
│   ├── test_episodes.json    # 20 pre-labeled episodes (held-out test set)
│   ├── my_labels.json        # Your labels — edit this in Milestone 1
│   └── taxonomy.md           # Label definitions and edge cases
└── specs/
    ├── system-design.md      # Architecture overview
    ├── classifier-spec.md    # Spec for Milestone 2 (fill in before coding)
    └── evaluation-spec.md    # Spec for Milestone 3 (fill in before coding)
```
