"""
agent.py

The FitFindr planning loop. Orchestrates the three tools in response to a
natural language user query, passing state between them via a session dict.

Complete tools.py and test each tool in isolation before implementing this file.

Usage (once implemented):
    from agent import run_agent
    from utils.data_loader import get_example_wardrobe

    result = run_agent(
        query="vintage graphic tee under $30, size M",
        wardrobe=get_example_wardrobe(),
    )
    print(result["fit_card"])
    print(result["error"])   # None on success
"""

from tools import search_listings, suggest_outfit, create_fit_card
import json # for parsing

# ── Groq client ───────────────────────────────────────────────────────────────
from groq import Groq
import os
def _get_groq_client():
    """Initialize and return a Groq client using GROQ_API_KEY from .env."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to a .env file in the project root."
        )
    return Groq(api_key=api_key)
SYSTEM_PROMPT = "You are FitFindr, a fashion styling assistant that helps users find thrifted clothing and build outfits."
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_listings",
            "description": "Search the mock listings dataset for items matching the description, optional size, and optional price ceiling. Returns a list of matching listing dicts sorted by relevance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Keywords describing what the user is looking for (e.g., 'vintage graphic tee')"
                    },
                    "size": {
                        "type": "string",
                        "description": "Size string to filter by, or null to skip size filtering. Matching is case-insensitive (e.g., 'M' matches 'S/M')"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price (inclusive), or null to skip price filtering"
                    }
                },
                "required": ["description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_outfit",
            "description": "Given a thrifted item and the user's wardrobe, suggest 1-2 complete outfits. If wardrobe is empty, offers general styling advice.",
            "parameters": {
                "type": "object",
                "properties": {
                    "new_item": {
                        "type": "object",
                        "description": "The listing dict for the thrifted item the user is considering buying"
                    },
                    "wardrobe": {
                        "type": "object",
                        "description": "The user's wardrobe dict with an 'items' key containing a list of wardrobe item dicts"
                    }
                },
                "required": ["new_item", "wardrobe"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_fit_card",
            "description": "Generate a short 2-4 sentence shareable outfit caption usable as an Instagram/TikTok caption for a thrifted find.",
            "parameters": {
                "type": "object",
                "properties": {
                    "outfit": {
                        "type": "string",
                        "description": "The outfit suggestion string from suggest_outfit"
                    },
                    "new_item": {
                        "type": "object",
                        "description": "The listing dict for the thrifted item"
                    }
                },
                "required": ["outfit", "new_item"]
            }
        }
    }
]

# ── session state ─────────────────────────────────────────────────────────────

def _new_session(query: str, wardrobe: dict) -> dict:
    """
    Initialize and return a fresh session dict for one user interaction.

    The session dict is the single source of truth for everything that happens
    during a run — it stores the original query, parsed parameters, tool results,
    and any error that caused early termination.

    You may add fields to this dict as needed for your implementation.
    """
    return {
        "query": query,              # original user query
        "parsed": {},                # extracted description / size / max_price
        "search_results": [],        # list of matching listing dicts
        "selected_item": None,       # top result, passed into suggest_outfit
        "wardrobe": wardrobe,        # user's wardrobe dict
        "outfit_suggestion": None,   # string returned by suggest_outfit
        "fit_card": None,            # string returned by create_fit_card
        "error": None,               # set if the interaction ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Main agent entry point. Runs the FitFindr planning loop for a single
    user interaction and returns the completed session dict.

    Args:
        query:    Natural language user request
                  (e.g., "vintage graphic tee under $30, size M")
        wardrobe: User's wardrobe dict — use get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py

    Returns:
        The session dict after the interaction completes. Check session["error"]
        first — if it is not None, the interaction ended early and the other
        output fields (outfit_suggestion, fit_card) will be None.

    TODO — implement this function using the planning loop you designed in planning.md:

        Step 1: Initialize the session with _new_session().

        Step 2: Parse the user's query to extract a description, size, and
                max_price. You can use regex, string splitting, or ask the LLM
                to parse it — document your choice in planning.md.
                Store the result in session["parsed"].

        Step 3: Call search_listings() with the parsed parameters.
                Store results in session["search_results"].
                If no results: set session["error"] to a helpful message and
                return the session early. Do NOT proceed to suggest_outfit
                with empty input.

        Step 4: Select the item to use (e.g., the top result).
                Store it in session["selected_item"].

        Step 5: Call suggest_outfit() with the selected item and wardrobe.
                Store the result in session["outfit_suggestion"].

        Step 6: Call create_fit_card() with the outfit suggestion and selected item.
                Store the result in session["fit_card"].

        Step 7: Return the session.

    Before writing code, complete the Planning Loop and State Management sections
    of planning.md — your implementation should match what you described there.
    """
    # TODO: implement the planning loop
    session = _new_session(query, wardrobe)
    count = 0
    MAX_RUNNING = 10


    #### Parsing ####
    response = _get_groq_client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": """Extract size, price, and description from the user's input.
            Return ONLY a JSON object with no extra text in this exact format:
            {"description": "...", "size": "..." or null, "price": float or null}"""},
            {"role": "user", "content": query}
        ]
    )

    parsed = json.loads(
        response.choices[0].message.content.strip()
    )

    session["parsed"] = parsed

    #### Calling search_listings() ####
    listings = search_listings(session["parsed"]["description"], 
                               session["parsed"]["size"], 
                               float(session["parsed"]["price"]) if parsed["price"] is not None else None
                               )

    #### Select item to use ####
    if not listings:
        session["error"] = "Apologies, there as been a small bump. Please try again with a different item!"
        return session
    
    session["search_results"] = listings
    session["selected_item"] = listings[0]

    #### Creating the loop ####
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]

    while count < MAX_RUNNING:
        response = _get_groq_client().chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto"

        )
        assistant_message = response.choices[0].message
        messages.append(assistant_message)

        if not assistant_message.tool_calls:
            break
        
        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if tool_name == "suggest_outfit":
                #### Calling suggest_outfit() ####
                result = suggest_outfit(session["selected_item"], wardrobe)
                session["outfit_suggestion"] = result
            
            elif tool_name == "create_fit_card":
                #### Calling create_fit_card() ####
                if not session.get("outfit_suggestion"):
                    result = "No outfit generated yet"
                else:
                    result = create_fit_card(session["outfit_suggestion"], listings[0])
                    session["fit_card"] = result
            
            else:
                result = {"error": f"Unknown tool: {tool_name}"}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result if isinstance(result, (dict, list)) else result)
            })

    return session
# ── CLI test ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe, get_empty_wardrobe

    print("=== Happy path: graphic tee ===\n")
    session = run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    )
    if session["error"]:
        print(f"Error: {session['error']}")
    else:
        print(f"Found: {session['selected_item']['title']}")
        print(f"\nOutfit: {session['outfit_suggestion']}")
        print(f"\nFit card: {session['fit_card']}")

    print("\n\n=== No-results path ===\n")
    session2 = run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    )
    print(f"Error message: {session2['error']}")
