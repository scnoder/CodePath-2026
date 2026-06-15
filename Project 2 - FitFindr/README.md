# FitFindr — Starter Kit

This starter kit contains everything you need to begin Project 2.

## What's Included

```
ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── planning.md                # Your planning template — fill this out first
└── requirements.txt           # Python dependencies
```

## Setup

```bash
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (get a free key at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_key_here
```

## The Mock Listings Dataset

`data/listings.json` contains 40 mock secondhand listings across categories (tops, bottoms, outerwear, shoes, accessories) and styles (vintage, y2k, grunge, cottagecore, streetwear, and more).

Each listing has: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.

Load it with:
```python
from utils.data_loader import load_listings
listings = load_listings()
```

## The Wardrobe Schema

`data/wardrobe_schema.json` defines the format your agent uses to represent a user's existing wardrobe. It includes:

- `schema`: field definitions for a wardrobe item
- `example_wardrobe`: a sample wardrobe with 10 items you can use for testing
- `empty_wardrobe`: a starting template for a new user

Load an example wardrobe with:
```python
from utils.data_loader import get_example_wardrobe
wardrobe = get_example_wardrobe()
```

## Tool Inventory
-  `search_listings()`
    - Parameters: `description: str`, `size: str | None = None`, `max_price: float | None = None`
    - Return Type: `list[dict]`
    - Description: searches listings by keywords, filters by size and price
- `suggest_outfit()`
    - Parameters: `new_item: dict`, `wardrobe: dict`
    - Return Type: `str`
    - Description: suggests outfits using the selected item and wardrobe
- `create_fit_card()`
    - Parameters: `outfit: str`, `new_item: dict`
    Return Type: `str`
    Description: generates an Instagram/TikTok caption

## Planning Loop
If `search_listings()` returns empty, set `session["error"]` and return early without calling the other two tools. If `results` exist, select `listings[0]` as the selected item, then call `suggest_outfit()`, then pass that result to `create_fit_card()`.

## State Management
- `session["parsed"]`: stored after LLM parses the query
- `session["search_results"]`: stored after `search_listings()`
- `session["selected_item"]`: stored as `listings[0]`
- `session["outfit_suggestion"]`: stored after `suggest_outfit()`
- `session["fit_card"]`: stored after `create_fit_card()`

## Error Handling
If `search_listings()` returns an empty list for 'designer ballgown size XXS under $5', `session["error"]` is set and the function returns early before calling `suggest_outfit()`.

## Spec Reflection
The spec helped me to plan out what I was going to do and ways to do it. I diverged from it by using the model for a lot of the `run_agent()` function where I used the LLM to parse, separate, and evaluate the data provided instead of using Python methods.

## AI Usage
I used AI to combine the steps and implementations of the functions in `run_agent()` with the planning loop. I used the flowchart that I had created to give it an outline on what to do.

I also used Claude to debug logic errors. For example, my `TOOLS_DEFINITION` did not look for null values which caused errors for when one of the parameters was empty. This caused issues for the LLM since it didn't get something it was expecting.