# Classifier Spec — Pod Classifier

Complete this spec **before** writing any code for Milestone 2.

Use Plan or Ask mode to think through each blank field. When you're done,
your answers here become the blueprint for `build_few_shot_prompt()` and
`classify_episode()` in `classifier.py`.

---

## build_few_shot_prompt(labeled_examples, description)

### What it does
Constructs a prompt string for the LLM that includes the task instructions,
all labeled training examples, and the new episode description to classify.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `labeled_examples` | `list[dict]` | Each dict has `"title"`, `"description"`, `"label"` (and others). These are the examples you labeled in Milestone 1. |
| `description` | `str` | The episode description to classify. |

### Output

| Return value | Type | Description |
|---|---|---|
| prompt | `str` | A complete prompt string ready to send to the LLM. |

---

### Spec fields — fill these in before writing code

**Task instruction (what should the LLM know about the task?):**

```
You are classifying podcast episodes by their format. Classify the episode
into exactly one of these four labels:

- interview: a conversation between a host and one or more guests
- solo: a single host speaking from memory, experience, or opinion — no guests,
  no assembled external sources
- panel: multiple guests with roughly equal speaking time, often debating or
  discussing a topic together
- narrative: a story assembled from external sources — interviews, archival
  audio, reporting — with a clear narrative arc

Return only the label and your reasoning. Do not explain the taxonomy.
```

---

**How should labeled examples be formatted in the prompt?**

```
Each example should include the episode title, a brief excerpt or the full
description, and the correct label. Separate examples with a blank line or
a delimiter like "---". Include all fields that help the model see why the
label was applied — title and description are both useful; other fields
(like episode ID) are not needed.
```

---

**Example block sketch (write one concrete example):**

```
Title: Can Technology Fix Loneliness?
Description: Social isolation has become one of the defining public health challenges of the moment. This week, we put together a panel that's probably too interdisciplinary to agree on anything: a sociologist who studies loneliness, a technologist who builds social products, a therapist who sees clients dealing with it, and a philosopher who thinks the framing is wrong. We don't pretend to resolve the question. But we think the disagreement itself is clarifying.
Label: panel
```

---

**How should the new episode (to be classified) be presented?**

```
Present it in the same format as the labeled examples, but omit the Label
line and replace it with an instruction to classify. For example:

Title: {title}
Description: {description}
Label: ?

Then add a line like: "Classify the episode above. Return your answer in
the format below:" followed by the output format you chose.
```

---

**What output format should you request from the LLM?**

```
A clear string format or a JSON file will make the parsing reliable. A label on it's own line is most ideal because it will be easier to detect and find. A structed format is best like "Label: X / Reasoning: Y" because it is more easier to read by the LLM. The tradeoffs compared to JSON files is that a string would be easier to mess up and have minor sytax errors that can be major in the long run.
```

---

**Edge cases to handle in the prompt:**

```
If labeled_examples is empty, there should be a graceful error message and the program should stop. This will prevent error messages from the model. If the description is very short, then it should compare the given descriptions with the description of the examples in order to get a proper analysis.
```

---

## classify_episode(description, labeled_examples)

### What it does
Classifies a single podcast episode description using the few-shot LLM classifier.
Returns a dict with a label and reasoning.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `description` | `str` | The episode description to classify. |
| `labeled_examples` | `list[dict]` | Labeled training examples from `load_labeled_examples()`. |

### Output

| Return value | Type | Description |
|---|---|---|
| result | `dict` | Must have keys `"label"` and `"reasoning"`. `"label"` must be one of `VALID_LABELS` or `"unknown"`. |

---

### Spec fields — fill these in before writing code

**Step 1 — Build the prompt:**

```
Call build_few_shot_prompt(labeled_examples, description) and store the
returned string in a variable (e.g., prompt). Pass through both arguments
exactly as received — no modification needed before calling.
```

---

**Step 2 — Send to the LLM:**

```
Call _client.chat.completions.create() with:
  - model: the model name from config (LLM_MODEL)
  - messages: a list with one dict — {"role": "user", "content": prompt}
    (system-design.md shows an optional system message too — either shape works)
  - max_tokens: a reasonable limit (e.g., 200–300) to keep responses concise

Extract the response text from:
  response.choices[0].message.content
```

---

**Step 3 — Parse the response:**

```
I will extract the label by stripping all of the whitespaces and unnecessary characters and then making everything in lowercase. Then I will loop through the labels and check if one of those labels are in the text input. Finally, I will return or store the information.
```

---

**Step 4 — Validate the label:**

```
If the LLM returns a label that isn't in VALID_LABELS then the label should be set to "unknown" temporarily and then ran again.
```

---

**Step 5 — Handle errors gracefully:**

```
If there is an unparseable response, the function should return an error message that will be a string and end the running of the program.
```

---

### Return value structure

```python
{
    "label": str,      # one of VALID_LABELS, or "unknown" if invalid/error
    "reasoning": str,  # brief explanation from the LLM
}
```

---

## Notes on label quality

The classifier is only as good as your labels. If your training examples have
inconsistent or ambiguous labels, the LLM will learn the wrong pattern.

Before implementing the classifier, re-read `data/taxonomy.md` and double-check
any labels you're unsure about. Annotation quality is part of the lab.

---

## Implementation Notes

*Fill this in after implementing and testing both functions.*

**Test: what does the raw LLM response look like for one episode?**

```
Episode tested: [title]
Raw response text: [paste it here]
```

**How did you parse the label out of the response?**

```
[describe the string operations — strip, split, lower, etc.]
```

**Did any episodes return `"unknown"`? If so, why?**

```
[yes / no — if yes, what did the raw response look like?]
```

**One thing about the output format that surprised you:**

```
[your answer here]
```
