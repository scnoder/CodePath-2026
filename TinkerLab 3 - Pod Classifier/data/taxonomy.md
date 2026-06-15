# Podcast Format Taxonomy

Use these four labels when annotating `train_episodes.json`. Each label captures the structural format of the episode — not the topic, production quality, or tone.

---

## Labels

### `interview`
A host speaks with one or more guests. The episode is structured around questions and responses. The guest has expertise, experience, or a story that the host is drawing out.

**Key signal:** There is a clear host-guest dynamic. The host is asking; the guest is answering.

**Examples:** Expert interviews, author Q&As, celebrity profiles, "founder story" conversations.

---

### `solo`
One host speaks alone, without guests. Could be a personal essay, opinion piece, tutorial, weekly reflection, or instructional walkthrough.

**Key signal:** One voice, no guest. The host is sharing their own thoughts, analysis, or experience.

**Examples:** Personal reflections, commentary episodes, "what I learned this week," opinion essays.

---

### `panel`
Three or more speakers discuss a topic together without a clear host-guest dynamic. All participants contribute as rough equals; no one is being interviewed.

**Key signal:** Multiple voices, roughly equal standing. Nobody is the clear subject of the conversation.

**Examples:** Expert roundtables, debate episodes, multi-host shows discussing a shared topic.

---

### `narrative`
A story is told over the course of the episode, usually with reporting, production, or multiple sources woven together. The episode has a story arc — characters, events, and a thread that pulls through.

**Key signal:** Structured as a story, not a conversation. Often uses audio clips, interview excerpts assembled for narrative effect, or documentary-style production.

**Examples:** Investigative journalism, true crime, documentary essays, reported features, audio portraits.

---

## How to Handle Ambiguous Cases

Some descriptions genuinely fit more than one label. That's intentional — it mirrors the real challenge of building labeled training data. Here's how to resolve common edge cases:

**Interview that tells a story:** If the episode is structured as Q&A (even if the guest tells long stories), label it `interview`. The structural format matters more than the content.

**Solo host who references "we" or other voices:** If one person is clearly driving the episode and others are minor supporting voices, label it `solo`.

**Two hosts talking to each other:** If there's no guest and both hosts speak roughly equally, label it `panel`. If one clearly leads and one is more of a sounding board, consider `solo`.

**Narrative built from interviews:** If the episode is structured as a story (with a narrative arc) but uses interview excerpts as raw material, label it `narrative`. The assembly is what matters, not the source material.

**First-person personal story:** This is the trickiest boundary. A solo host can tell a deeply personal story in past tense with a clear arc — and it's still `solo`, not `narrative`. The difference is the *source*. Ask: is the host the only source, speaking from memory and reflection? That's `solo`. Or does the episode draw on external material — documents, archives, other people's interviews, recordings — to reconstruct events? That's `narrative`. A host saying "here's what that year was like for me" is solo. A host saying "I built this episode from letters my grandmother left behind and interviews with my aunts" is narrative, because the story is assembled from sources beyond the host's own voice.

**When you're genuinely unsure:** Pick the label that fits the *structure* you'd expect if you were listening, not the label that fits the description's marketing language. Description writers are trying to make the episode sound interesting — they're not trying to be structurally accurate.

---

## Valid Labels (for reference)

```
interview
solo
panel
narrative
```

These are the only four valid labels. Use exactly these strings in `my_labels.json`.
