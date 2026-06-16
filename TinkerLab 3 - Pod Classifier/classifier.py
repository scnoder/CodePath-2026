import json
import os
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_LABELS, DATA_PATH, TRAIN_FILE, LABELS_FILE

_client = Groq(api_key=GROQ_API_KEY)


def load_labeled_examples() -> list[dict]:
    """
    Load the training episodes and merge them with the student's labels.

    Returns a list of dicts, each with:
      - "id"          : episode ID
      - "title"       : episode title
      - "podcast"     : podcast name
      - "description" : episode description
      - "label"       : the label from my_labels.json (may be None if not yet annotated)

    Only returns episodes where the label is a valid, non-null string.
    Episodes with null labels are silently skipped.
    """
    train_path = os.path.join(DATA_PATH, TRAIN_FILE)
    labels_path = os.path.join(DATA_PATH, LABELS_FILE)

    with open(train_path, encoding="utf-8") as f:
        episodes = {ep["id"]: ep for ep in json.load(f)}

    with open(labels_path, encoding="utf-8") as f:
        labels = {entry["id"]: entry["label"] for entry in json.load(f)}

    labeled = []
    for ep_id, ep in episodes.items():
        label = labels.get(ep_id)
        if label in VALID_LABELS:
            labeled.append({**ep, "label": label})

    return labeled


def build_few_shot_prompt(labeled_examples: list[dict], description: str) -> str:
    """
    Build a few-shot classification prompt using the student's labeled training examples.

    TODO — Milestone 2:

    Your prompt needs to:
      1. Describe the task and the four valid labels
      2. Show the labeled training examples so the LLM can learn the pattern
      3. Present the new description and ask for a classification

    The LLM should return a single label from VALID_LABELS (exactly as written)
    plus a brief explanation of its reasoning. Think carefully about the output
    format you request — you'll need to parse it in classify_episode().

    Before writing code, complete specs/classifier-spec.md.
    """


    examples_text = ""

    for i in labeled_examples:
        examples_text += f"Title: {i['title']}\n"
        examples_text += f"Description: {i['description']}\n"
        examples_text += f"Label: {i['label']}\n"
        examples_text += "---\n"
    
    prompt = f"""You are classifying podcast eposodes based on if they are an interview, panel, narrative, or a solo.
            You are classifying podcast episodes by their format. Classify the episode into exactly one of these four labels:

            - interview: a conversation between a host and one or more guests
            - solo: a single host speaking from memory, experience, or opinion — no guests, no assembled external sources
            - panel: multiple guests with roughly equal speaking time, often debating or discussing a topic together
            - narrative: a story assembled from external sources — interviews, archival audio, reporting — with a clear narrative arc

            Return only the label and your reasoning. Do not explain the taxonomy.

            Here is a list of all of the labels:
            {examples_text}

            Now, classify this episode:
            Description: {description}
            Label: ?

            Classify the episode above. Return your answer in this format:
            Label = <label>
            Reasoning: <brief explanation>
    """


    return prompt


def classify_episode(description: str, labeled_examples: list[dict]) -> dict:
    """
    Classify a single podcast episode description using the few-shot LLM classifier.

    TODO — Milestone 2 (complete after build_few_shot_prompt):

    Steps:
      1. Call build_few_shot_prompt() to construct the prompt
      2. Send it to the LLM via _client.chat.completions.create()
      3. Parse the response to extract a label and reasoning
      4. Validate the label — if it's not in VALID_LABELS, set it to "unknown"
      5. Return a dict with "label" and "reasoning" keys

    Handle the case where the LLM returns something unparseable gracefully —
    don't let a bad response crash the whole evaluation.

    Before writing code, complete specs/classifier-spec.md.
    """
    prompt = build_few_shot_prompt(load_labeled_examples(), description)

    format = """Each example should include the episode title, a brief excerpt or the full description, and the correct label. Separate examples with a blank line or a delimiter like "---". Include all fields that help the model see why the label was applied — title and description are both useful; other fields (like episode ID) are not needed.

                Here is an example:
                Title: Can Technology Fix Loneliness?
                Description: Social isolation has become one of the defining public health challenges of the moment. This week, we put together a panel that's probably too interdisciplinary to agree on anything: a sociologist who studies loneliness, a technologist who builds social products, a therapist who sees clients dealing with it, and a philosopher who thinks the framing is wrong. We don't pretend to resolve the question. But we think the disagreement itself is clarifying.
                Label: panel

                Here is the format:
                Title: {title}
                Description: {description}
                Label: ?

        """
    response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": format},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )

    reply = response.choices[0].message.content
    
    listings = load_labeled_examples()

    label = "unknown"
    for listing in listings:
        if listing["label"] == list(reply.split())[1]:
            label = listing

    return {
        "label": label,
        "reasoning": reply[24:]
    }