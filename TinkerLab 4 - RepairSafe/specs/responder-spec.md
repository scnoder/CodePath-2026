# Spec: `generate_safe_response()`

**File:** `responder.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Generate a response to a home repair question that is appropriate to its safety tier. The same question gets a fundamentally different answer depending on the tier — not just a disclaimer tacked on, but a different behavior: answer fully, answer with warnings, or decline to give instructions entirely.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |
| `tier` | `str` | The safety tier: `"safe"`, `"caution"`, or `"refuse"` |

**Output:** `str` — the response to show to the user

---

## Design Decisions

*Complete the fields below before writing any code. The most important fields are the three system prompts. Write them out fully — don't just describe what you want.*

---

### System prompt: "safe" tier

*Write the exact system prompt text for a safe question. It should produce helpful, specific, actionable answers.*

```
You are a helpful home repair assistant. The user's question has been classified as safe — a routine, low-risk repair most homeowners can handle. Give clear, specific, step-by-step instructions including tools needed, time estimate, and common mistakes to avoid. Be practical and direct; don't add unnecessary caveats or suggest professional help for something this low-risk.
```

---

### System prompt: "caution" tier

*Write the exact system prompt text for a caution question. What safety language should be present? How firm should the "consider a professional" message be — a gentle mention or a clear recommendation?*

```
You are a helpful home repair assistant. The user's question has been classified as caution — doable by a careful homeowner, but mistakes can cause real cost or mild injury. Give clear, accurate instructions, but:
- Call out the specific risk(s) before or alongside the steps (e.g., "turn off
  the breaker first," "shut off the water supply")
- Note any tools or signs that indicate the job is more complex than expected
- Mention that hiring a professional is a reasonable option if the user is
  unsure, without being alarmist or repeating the warning multiple times
Keep the tone confident and helpful, not fearful.
```

---

### System prompt: "refuse" tier

*This is the most important one to get right. Write the exact system prompt for refusing to answer.*

*Two goals that are in tension: (1) the response must NOT provide how-to instructions, even a little. (2) the response should still be genuinely useful — explaining why the task is dangerous and what the user should do instead.*

*Before writing this prompt, use Plan mode with your AI tool. Share your draft refuse prompt and ask it: "What are ways an LLM might still provide dangerous instructions despite this system prompt?" Revise until you've addressed the failure modes it identifies.*

```
You are a helpful home repair assistant. The user's question has been classified as refuse — this work requires a licensed professional and must not receive DIY instructions, because mistakes can cause fire, flooding, structural failure, serious injury, or death.

Do not provide any step-by-step instructions, part names, tool lists, or technique details, even simplified or partial ones.

Instead:
1. Briefly explain why this task is dangerous or regulated (1-2 sentences)
2. Tell the user what kind of professional to contact (electrician, plumber, structural engineer, etc.)
3. If relevant, mention immediate safety precautions that are NOT repair steps (e.g., "if you smell gas, leave the house and call the gas company")

Be genuinely helpful in tone — the goal is to protect the user, not to lecture them.
```

---

### Grounding the refuse response

*The grounding problem from Lab 1 applies here, with higher stakes: even with a strong system prompt, an LLM may "helpfully" provide partial instructions before pivoting to "you should hire a professional." How will you prevent that?*

*Hint: "be careful" doesn't work. Explicit, behavioral instructions ("do not provide any steps, procedures, or instructions — not even general guidance") work better. What will yours say?*

```
I'll test the refuse prompt against 3-5 real refuse-tier questions and check that no response includes step sequences, tool names, or part-level detail. If any response leaks instructions, I'll add explicit negative examples to the system prompt.
```

---

### Fallback for unknown tier

*What should your function do if it receives a tier value that isn't "safe", "caution", or "refuse" — e.g., "unknown" while the classifier is still a stub? Write the fallback behavior and explain why.*

```
[your answer here]
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**A "refuse" response that was still too helpful and what you changed to fix it:**

```
[your answer here]
```

**The tier where the LLM's default behavior was closest to what you wanted (and which tier required the most prompt iteration):**

```
[your answer here]
```
