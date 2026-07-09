# PR #2 — feat: add list stats endpoint

**Author:** Maya Okafor
**Branch:** `feat/list-stats`
**Touches:** `routes/lists.py`, `services/list_service.py`

---

## Background

The frontend team asked for a stats endpoint to power the active shopping view.
Their exact request:

> "We need to show users how many items are still on their list and break down
> what's remaining by category — so someone shopping at a grocery store can see
> 'I still need 2 things in produce, 1 in dairy' and navigate by section."

## What this does

Adds `GET /lists/<list_id>/stats` — returns total items, purchased count,
remaining count, and a per-category breakdown.

Prompt I used to generate the initial implementation:

> "Write a Flask route that returns grocery list statistics including total item
> count, purchased count, remaining count, and a breakdown of item counts by
> category. Use SQLAlchemy to query the database."

Tested on both seeded lists and the numbers add up.

## Files changed

See `pr2_list_stats.py` for the full proposed code.

## Testing done

```bash
python seed_data.py
python try_prs.py

curl http://127.0.0.1:5000/lists/LIST_ID/stats
# → {
#     "list_id": "...",
#     "total_items": 8,
#     "purchased": 3,
#     "remaining": 5,
#     "by_category": {
#       "produce": 2, "dairy": 2, "bakery": 1, "meat": 1, "pantry": 2
#     }
#   }
```
