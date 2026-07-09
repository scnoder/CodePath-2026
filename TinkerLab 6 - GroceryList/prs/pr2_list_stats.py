"""
PR #2 — List Stats Feature
============================
Proposed additions for the list statistics endpoint.

Use case (from the frontend team's request):
    "We need a stats endpoint for the active shopping view — show users
    how many items are still on their list and break down what's left
    by category so they can navigate the store by section."

To test this code without modifying the main app, run:
    python try_prs.py
then use the curl examples in pr2_description.md.

To integrate permanently (not required for the review):
  1. Copy get_list_stats() into services/list_service.py
  2. Copy the list_stats() route into routes/lists.py
"""

# ---------------------------------------------------------------------------
# Addition to services/list_service.py
# ---------------------------------------------------------------------------

def get_list_stats(list_id: str) -> dict:
    """
    Compute summary statistics for a grocery list.

    Returns a dict with:
        list_id      — the list ID
        total_items  — total number of items on the list
        purchased    — number of items marked as purchased
        remaining    — number of items not yet purchased
        by_category  — item counts grouped by category
    """
    items = Item.query.filter_by(list_id=list_id).all()

    total = len(items)
    purchased = sum(1 for item in items if item.is_purchased)
    remaining = total - purchased

    by_category = {}
    for item in items:
        cat = item.category or "uncategorized"
        by_category[cat] = by_category.get(cat, 0) + 1

    return {
        "list_id": list_id,
        "total_items": total,
        "purchased": purchased,
        "remaining": remaining,
        "by_category": by_category,
    }


# ---------------------------------------------------------------------------
# Addition to routes/lists.py
# ---------------------------------------------------------------------------

@lists_bp.route("/<list_id>/stats", methods=["GET"])
def list_stats(list_id):
    """Return summary statistics for a grocery list."""
    stats = list_service.get_list_stats(list_id)
    return jsonify(stats), 200
