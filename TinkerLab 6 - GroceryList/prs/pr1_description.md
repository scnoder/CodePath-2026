# PR #1 — feat: add bulk purchase endpoint

**Author:** Leo Chen
**Branch:** `feat/bulk-purchase`
**Touches:** `routes/lists.py`, `services/list_service.py`

---

## What this does

Adds `POST /lists/<list_id>/purchase-all` — marks every item in a list as purchased
in one request. Useful when you finish shopping and want to clear the whole list
without tapping each item individually.

I used Claude to generate the initial implementation, then wired it into the existing
blueprint. Tested manually with curl on the happy path — works great.

## Files changed

See `pr1_bulk_purchase.py` for the full proposed code.

## Testing done

```bash
# Seed the DB, then start the PR test server:
python seed_data.py
python try_prs.py

# Mark everything in a list as purchased
curl -X POST http://127.0.0.1:5000/lists/LIST_ID/purchase-all \
  -H "Content-Type: application/json" \
  -d '{"user_id": "USER_ID"}'
# → {"purchased": 5}  ✓
```

## Expected behavior

- All unpurchased items in the list become `is_purchased: true`
- Each item's `purchased_by` is set to the requesting user
- Each item's `purchased_at` is set to now
- Response returns the count of items that were purchased
