# Plant Advisor — AI201 Lab 2 Starter

A conversational agent that helps users care for their houseplants. Ask it anything about a plant in its database and it will look up the care requirements, check the current seasonal context, and give you specific, grounded advice.

The app is built and running. The agent isn't functional yet — that's the lab.

---

## Setup

**1. Fork and clone this repo.**

**2. Create and activate a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
# or: .venv\Scripts\activate   # Windows
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

**4. Add your Groq API key.** Copy `.env.example` to `.env` and paste in your key from [console.groq.com](https://console.groq.com).

**5. Run the app:**

```bash
python app.py
```

Plant Advisor will open in your browser. The chat interface works, but the agent returns a placeholder message until you complete Milestone 2.

---

## Project Structure

```
ai201-lab2-plantadvisor-starter/
├── app.py              ← Gradio UI (complete — do not modify)
├── config.py           ← API keys and settings (complete)
├── agent.py            ← Tool definitions + run_agent() to implement
├── tools.py            ← lookup_plant() and get_seasonal_conditions() to implement
├── data/
│   ├── plants.json     ← 15-plant database (complete)
│   └── seasons.json    ← Seasonal care data (complete)
├── specs/
│   ├── system-design.md        ← Start here
│   ├── tool-functions-spec.md  ← Complete before Milestone 1
│   └── agent-loop-spec.md      ← Complete before Milestone 2
└── requirements.txt
```

## Where to Start

Open `specs/system-design.md`. Read the whole thing before opening any code file.
