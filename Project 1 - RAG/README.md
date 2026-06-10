# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
This bot reviews speeches by Abraham Lincoln. THey are generally hard to read and understand as it was a complex topic and time period in US history. 

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Lincoln Library|Website |https://www.abrahamlincolnonline.org/lincoln/speeches/ |


---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
My chunk sizes was 500 characters because it has a lot of small and important details within sentences.
**Overlap:**
I kept my overlap at 50 because i ddint want any information getting lost due to the intricate wordings and details.
**Why these choices fit your documents:**
These choices fit my document because ther eis a lot of wording and details that are provided in his speeches.
**Final chunk count:**
There are 1166 chunks.
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
The embedding model used was all-MiniLM-L6-v2
**Production tradeoff reflection:**
There is a loss in semeantic nurance and it has a low memory usage.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |When was the Gettysburg Address spoke? |The Gettysburg Address was delivered on November 19, 1863 |November 19, 1863. |eh could be better |100% |
| 2 |What did Lincoln say about slavery in the Cooper Union Address? |Lincoln argued that the federal government had the right to control slavery in the territories, and that the founders who framed the Constitution understood this. He challenged Southern claims that Republicans were radical agitators. |He also mentioned that the supporters of slavery are dissatisfied with what the opponents of slavery say about slavery. Additionally, Lincoln noted that the founders have left no record of their understanding on the direct question of federal control of slavery in the federal territories. |much better this time  |100% |
| 3 |What was Lincoln's warning about mobs and lawlessness in the Lyceum Address? |Lincoln warned that mob rule and disregard for laws posed a serious threat to American democracy.  |I don't have enough information on that. |it didnt provide a response so thats not good |0% |
| 4 |How did Lincoln describe the cause of the Civil War? |The cause of the Civil War:
Lincoln stated that slavery was the cause of the war. |Lincoln described the cause of the Civil War as being related to the interest of colored slaves, "All knew that this interest was, somehow, the cause of the war." He specifically stated that the object for which the insurgents would rend the Union was "to strengthen, perpetuate, and extend this interest". |Really good response |90% |
| 5 |What arguments did Lincoln make in the House Divided speech? |
Lincoln argued that the government could not endure permanently half slave and half free |I don't have enough information on that. The provided excerpts from "Housedivided" do not contain the full speech or the main arguments made by Lincoln. They only provide some background information and quotes related to the Nebraska bill and the issue of slavery. |it was worse this time |5% |

**Retrieval quality:** 3 / 1 / 1  
**Response accuracy:** 3 / 1 / 1

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
