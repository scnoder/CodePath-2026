"""
routes/lists.py — GroceryList

All routes for grocery lists and their items.
"""

from flask import Blueprint, jsonify, request
from services import list_service

lists_bp = Blueprint("lists", __name__)


# ---------------------------------------------------------------------------
# List routes
# ---------------------------------------------------------------------------

@lists_bp.route("/", methods=["GET"])
def get_lists():
    """Return all grocery lists."""
    lists = list_service.get_all_lists()
    return jsonify([l.to_dict() for l in lists])


@lists_bp.route("/", methods=["POST"])
def create_list():
    """
    Create a new grocery list.

    Expected JSON body:
        name       (str, required)
        created_by (str, required) — user ID
        is_shared  (bool, optional, default false)
    """
    data = request.get_json() or {}
    missing = [f for f in ["name", "created_by"] if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    try:
        grocery_list = list_service.create_list(
            name=data["name"],
            created_by=data["created_by"],
            is_shared=data.get("is_shared", False),
        )
        return jsonify(grocery_list.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# ---------------------------------------------------------------------------
# Item routes (nested under a list)
# ---------------------------------------------------------------------------

@lists_bp.route("/<list_id>/items", methods=["GET"])
def get_items(list_id):
    """
    Return all items for a grocery list.

    Items are ordered unpurchased-first, then by the order they were added.
    """
    try:
        items = list_service.get_items(list_id)
        return jsonify([item.to_dict() for item in items])
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@lists_bp.route("/<list_id>/items", methods=["POST"])
def add_item(list_id):
    """
    Add a new item to a grocery list.

    Expected JSON body:
        name      (str, required)
        added_by  (str, required) — user ID
        quantity  (float, optional)
        unit      (str, optional)
        category  (str, optional)
    """
    data = request.get_json() or {}
    missing = [f for f in ["name", "added_by"] if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    try:
        item = list_service.add_item(
            list_id=list_id,
            name=data["name"],
            added_by=data["added_by"],
            quantity=data.get("quantity"),
            unit=data.get("unit"),
            category=data.get("category"),
        )
        return jsonify(item.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@lists_bp.route("/<list_id>/items/<item_id>", methods=["PATCH"])
def mark_purchased(list_id, item_id):
    """
    Mark an item as purchased.

    Expected JSON body:
        user_id (str, required) — the user marking the item purchased
    """
    data = request.get_json() or {}
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing required field: user_id"}), 400

    try:
        item = list_service.mark_purchased(
            list_id=list_id,
            item_id=item_id,
            user_id=user_id,
        )
        return jsonify(item.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
