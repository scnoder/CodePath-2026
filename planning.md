# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |https://www.abrahamlincolnonline.org/lincoln/speeches/speech.htm |List of Lincoln Speeches |https://www.abrahamlincolnonline.org/lincoln/speeches/lyceum.htm |
| 2 |https://www.abrahamlincolnonline.org/lincoln/speeches/speech.htm |List of Lincoln Speeches |https://www.abrahamlincolnonline.org/lincoln/speeches/temperance.htm |
| 3 |https://www.abrahamlincolnonline.org/lincoln/speeches/speech.htm |List of Lincoln Speeches |https://www.abrahamlincolnonline.org/lincoln/speeches/clay.htm |
| 4 |https://www.abrahamlincolnonline.org/lincoln/speeches/speech.htm |List of Lincoln Speeches |https://www.abrahamlincolnonline.org/lincoln/speeches/house.htm |
| 5 |https://www.abrahamlincolnonline.org/lincoln/speeches/speech.htm |List of Lincoln Speeches |https://www.abrahamlincolnonline.org/lincoln/speeches/cooper.htm |
| 6 |https://www.abrahamlincolnonline.org/lincoln/speeches/speech.htm |List of Lincoln Speeches |https://www.abrahamlincolnonline.org/lincoln/speeches/farewell.htm |
| 7 |https://www.abrahamlincolnonline.org/lincoln/speeches/speech.htm |List of Lincoln Speeches |https://www.abrahamlincolnonline.org/lincoln/speeches/1inaug.htm |
| 8 |https://www.abrahamlincolnonline.org/lincoln/speeches/speech.htm |List of Lincoln Speeches |https://www.abrahamlincolnonline.org/lincoln/speeches/gettysburg.htm |
| 9 |https://www.abrahamlincolnonline.org/lincoln/speeches/speech.htm |List of Lincoln Speeches |https://www.abrahamlincolnonline.org/lincoln/speeches/inaug2.htm |
| 10 |https://www.abrahamlincolnonline.org/lincoln/speeches/speech.htm |List of Lincoln Speeches |https://www.abrahamlincolnonline.org/lincoln/speeches/last.htm |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
100 charactesr
**Overlap:**
0
**Reasoning:**
This will allow for proper chunking since 100 characters will be the average size and no overlap means there will be no missing information
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2
**Top-k:**
5
**Production tradeoff reflection:**
The tradeoff is that too much information might get contained.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |How did Lincoln's view of preserving the Union change between the First Inaugural Address and the Second Inaugural Address? |In the First Inaugural Address (1861), Lincoln focused on preserving the Union and avoiding civil war, arguing that secession was legally invalid and appealing for national unity. By the Second Inaugural Address (1865), after four years of war, Lincoln reflected on slavery as a fundamental cause of the conflict and emphasized reconciliation, charity, and healing rather than assigning blame. |
| 2 |Which speech contains the phrase "government of the people, by the people, for the people," and what was the occasion? |The phrase appears in the Gettysburg Address (1863). Lincoln delivered the speech at the dedication of the Soldiers' National Cemetery in Gettysburg, Pennsylvania, following the Battle of Gettysburg. |
| 3 |What concern about threats to American democracy did Lincoln express in the Lyceum Address? |In the Lyceum Address (1838), Lincoln argued that the greatest threat to American democracy would not come from foreign invasion but from internal lawlessness, mob violence, and citizens' failure to respect the rule of law and constitutional institutions. |
| 4 |How did Lincoln describe slavery in both the Cooper Union Address and the Second Inaugural Address? |In the Cooper Union Address (1860), Lincoln argued that the Founding Fathers intended the federal government to have authority to restrict the expansion of slavery into federal territories. In the Second Inaugural Address (1865), he described slavery as the root cause of the Civil War and suggested that the nation's suffering was a form of divine judgment for the offense of slavery. |
| 5 |What was Lincoln's message in his Farewell Address to Springfield, and how does it compare with the tone of his Last Public Address? |In the Farewell Address to Springfield (1861), Lincoln expressed humility, uncertainty, gratitude toward his hometown, and reliance on divine guidance as he departed for Washington. In the Last Public Address (1865), delivered near the end of the Civil War, he focused on reconstruction, restoring the Union, and extending limited voting rights to African Americans. The farewell speech is personal and reflective, while the last public address is forward-looking and political. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. The wrong information could be retrieved form the formatting of the doucments.

2. The sentences are too long or short and that causes retreival issues.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
