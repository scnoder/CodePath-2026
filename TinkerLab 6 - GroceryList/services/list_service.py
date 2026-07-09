"""
services/list_service.py — GroceryList

Business logic for grocery lists and their items.
"""

from datetime import datetime, timezone
from extensions import db
from models import User, GroceryList, Item


# ---------------------------------------------------------------------------
# List operations
# ---------------------------------------------------------------------------

def get_all_lists() -> list[GroceryList]:
    """Return all grocery lists, most recently created first."""
    return GroceryList.query.order_by(GroceryList.created_at.desc()).all()


def get_list(list_id: str) -> GroceryList | None:
    """Return a single grocery list by ID, or None if not found."""
    return db.session.get(GroceryList, list_id)


def create_list(name: str, created_by: str, is_shared: bool = False) -> GroceryList:
    """
    Create a new grocery list.

    Args:
        name:       Display name for the list.
        created_by: ID of the user creating the list.
        is_shared:  Whether other users can view and add to this list.

    Returns:
        The newly created GroceryList.

    Raises:
        ValueError: If the user does not exist.
    """
    user = db.session.get(User, created_by)
    if not user:
        raise ValueError(f"User {created_by!r} not found")

    grocery_list = GroceryList(name=name, created_by=created_by, is_shared=is_shared)
    db.session.add(grocery_list)
    db.session.commit()
    return grocery_list


# ---------------------------------------------------------------------------
# Item operations
# ---------------------------------------------------------------------------

def get_items(list_id: str) -> list[Item]:
    """
    Return all items for a list, unpurchased items first, then purchased.

    Args:
        list_id: ID of the grocery list.

    Returns:
        List of Items ordered by is_purchased ascending (False before True),
        then by added_at ascending.

    Raises:
        ValueError: If the list does not exist.
    """
    grocery_list = db.session.get(GroceryList, list_id)
    if not grocery_list:
        raise ValueError(f"List {list_id!r} not found")

    return (
        Item.query.filter_by(list_id=list_id)
        .order_by(Item.is_purchased.asc(), Item.added_at.asc())
        .all()
    )


def add_item(
    list_id: str,
    name: str,
    added_by: str,
    quantity: float | None = None,
    unit: str | None = None,
    category: str | None = None,
) -> Item:
    """
    Add a new item to a grocery list.

    Args:
        list_id:   ID of the grocery list.
        name:      Item name.
        added_by:  ID of the user adding the item.
        quantity:  Optional numeric quantity.
        unit:      Optional unit of measure (e.g. "lbs", "oz", "count").
        category:  Optional category (e.g. "produce", "dairy").

    Returns:
        The newly created Item.

    Raises:
        ValueError: If the list or user does not exist.
    """
    grocery_list = db.session.get(GroceryList, list_id)
    if not grocery_list:
        raise ValueError(f"List {list_id!r} not found")

    user = db.session.get(User, added_by)
    if not user:
        raise ValueError(f"User {added_by!r} not found")

    item = Item(
        list_id=list_id,
        name=name,
        quantity=quantity,
        unit=unit,
        category=category,
        added_by=added_by,
    )
    db.session.add(item)
    db.session.commit()
    return item


def mark_purchased(list_id: str, item_id: str, user_id: str) -> Item:
    """
    Mark an item as purchased.

    Args:
        list_id:  ID of the grocery list (used to verify the item belongs to it).
        item_id:  ID of the item to mark as purchased.
        user_id:  ID of the user marking it purchased.

    Returns:
        The updated Item.

    Raises:
        ValueError: If the item does not exist in the given list, or if the
                    item is already purchased.
    """
    item = Item.query.filter_by(id=item_id, list_id=list_id).first()
    if not item:
        raise ValueError(f"Item {item_id!r} not found in list {list_id!r}")
    if item.is_purchased:
        raise ValueError(f"Item {item_id!r} is already marked as purchased")

    item.is_purchased = True
    item.purchased_by = user_id
    item.purchased_at = datetime.now(timezone.utc)
    db.session.commit()
    return item
