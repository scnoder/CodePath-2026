"""
PR #1 — Bulk Purchase Feature
================================
Proposed additions for the bulk purchase endpoint.

To test this code without modifying the main app, run:
    python try_prs.py
then use the curl examples in pr1_description.md.

To integrate permanently (not required for the review):
  1. Copy purchase_all_items() into services/list_service.py
  2. Copy the purchase_all() route into routes/lists.py
"""

# ---------------------------------------------------------------------------
# Addition to services/list_service.py
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
# Addition to routes/lists.py
# ---------------------------------------------------------------------------

@lists_bp.route("/<list_id>/purchase-all", methods=["POST"])
def purchase_all(list_id):
    """
    Mark all items in a list as purchased at once.

    Expected JSON body:
        user_id (str, required) — the user doing the shopping
    """
    data = request.get_json() or {}
    user_id = data.get("user_id")

    count = list_service.purchase_all_items(list_id, user_id)
    return jsonify({"purchased": count}), 200
