"""
try_prs.py — GroceryList

Starts the app with BOTH proposed PR routes integrated so you can test
them with curl before writing your review.

Run INSTEAD of app.py:
    python try_prs.py

New endpoints (from the PRs):
    POST  /lists/<list_id>/purchase-all     PR #1
    GET   /lists/<list_id>/stats            PR #2

All existing endpoints still work.
"""

from datetime import datetime, timezone
from flask import jsonify, request
from app import create_app, db
from models import Item


# ---------------------------------------------------------------------------
# PR #1 service function — copied exactly from pr1_bulk_purchase.py
# ---------------------------------------------------------------------------

def purchase_all_items(list_id: str, user_id: str) -> int:
    """
    Mark all items in a list as purchased.

    Args:
        list_id: ID of the grocery list.
        user_id: ID of the user performing the bulk purchase.

    Returns:
        The number of items marked as purchased.
    """
    items = Item.query.filter_by(list_id=list_id).all()
    for item in items:
        item.is_purchased = True
        item.purchased_by = user_id
        item.purchased_at = datetime.now(timezone.utc)
    db.session.commit()
    return len(items)


# ---------------------------------------------------------------------------
# PR #2 service function — copied exactly from pr2_list_stats.py
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
# Create app and register the new PR routes alongside existing ones
# ---------------------------------------------------------------------------

app = create_app()


@app.route("/lists/<list_id>/purchase-all", methods=["POST"])
def purchase_all(list_id):
    """
    PR #1 — Mark all items in a list as purchased at once.

    Expected JSON body:
        user_id (str, required) — the user doing the shopping
    """
    data = request.get_json() or {}
    user_id = data.get("user_id")

    count = purchase_all_items(list_id, user_id)
    return jsonify({"purchased": count}), 200


@app.route("/lists/<list_id>/stats", methods=["GET"])
def list_stats(list_id):
    """PR #2 — Return summary statistics for a grocery list."""
    stats = get_list_stats(list_id)
    return jsonify(stats), 200


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("GroceryList — PR test mode")
    print("All existing endpoints active + two new PR endpoints:")
    print("  POST  /lists/<list_id>/purchase-all   (PR #1)")
    print("  GET   /lists/<list_id>/stats           (PR #2)")
    print("=" * 60)
    print()
    app.run(debug=False, port=5000)
