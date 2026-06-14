# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
This tool will go through all of the listing.json and finds the item that the user requested.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `description` (str): It is the keywords of the item that the user is looking for.
- `size` (str): It is the size of the item that the user is looking for.
- `max_price` (float): It is the maximum price that they will go for that item.

**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->
It returns a dictionary of all the items that the user wanted most likely.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->
If it fails or returns nothing it should return that the model cannot find anything and should reccommend other items that are similar and avaliable.

---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
This tool looks at the given item and the user's wardrobe and checks to see if there are any items in the listings that can help the user with their style.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): It is a dictionary of the user's thrifted item.
- `wardrobe` (dict): The wardrobe is what they currently have.
 
**What it returns:**
<!-- Describe the return value -->
The return statement should be a string of other items that matches their style.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->
It would return a general statment for other items.

---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->
The tool takes in an outfit and details about the outfit and returns a string for a good caption for social media.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `outfit` (...): It is the name describing what the outfit is.

**What it returns:**
<!-- Describe the return value -->
It returns a string describing the outfit for a proper Instagram or Tiktok caption.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->
The code will return "Sorry, I could not generate a caption due to there being no outfit. Please try again."

---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- Describe the logic your planning loop uses. What does it look at? What conditions change its behavior? How does it know when it's done? -->
An agent decides which tools to call based on the description of the tool itself. It checks for keywords and if there are any changes to those keywords or if it needs anything, then it uses other tools. The agent knows that it is done once it hits a maximum amount of iterations or credits or it goes to a single string with no tools needed to evaluate it.

---

## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->


---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | |
| suggest_outfit | Wardrobe is empty | |
| create_fit_card | Outfit input is missing or incomplete | |

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     ASCII art, a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html), or an embedded
     sketch are all fine. You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->

---

## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->

**Milestone 3 — Individual tool implementations:**

**Milestone 4 — Planning loop and state management:**

---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**
<!-- What does the agent do first? Which tool is called? With what input? -->

**Step 2:**
<!-- What happens next? What was returned from step 1? What tool is called now? -->

**Step 3:**
<!-- Continue until the full interaction is complete -->

**Final output to user:**
<!-- What does the user actually see at the end? -->
