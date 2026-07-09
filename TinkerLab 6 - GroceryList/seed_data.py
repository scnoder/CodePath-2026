"""
seed_data.py — GroceryList

Populates the database with realistic test data.
Run with: python seed_data.py

This script creates:
- 2 users: maya and leo
- 2 grocery lists (one private, one shared)
- 12 items across the two lists, with a mix of purchased and unpurchased
"""

from datetime import datetime, timedelta, timezone
from app import create_app, db
from models import User, GroceryList, Item


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        now = datetime.now(timezone.utc)

        # ------------------------------------------------------------------
        # Users
        # ------------------------------------------------------------------
        maya = User(username="maya", email="maya@grocerylist.app")
        leo = User(username="leo", email="leo@grocerylist.app")
        db.session.add_all([maya, leo])
        db.session.flush()

        # ------------------------------------------------------------------
        # Lists
        # ------------------------------------------------------------------
        weekly_shop = GroceryList(
            name="Weekly Shop",
            created_by=maya.id,
            is_shared=False,
        )
        party_supplies = GroceryList(
            name="Party Supplies",
            created_by=leo.id,
            is_shared=True,
        )
        db.session.add_all([weekly_shop, party_supplies])
        db.session.flush()

        # ------------------------------------------------------------------
        # Items — Weekly Shop (maya's private list)
        # 8 items: 5 unpurchased, 3 purchased
        # Two "produce" items — one purchased, one not — to expose the
        # by_category counting ambiguity in PR 2.
        # ------------------------------------------------------------------
        weekly_items = [
            # Unpurchased
            Item(list_id=weekly_shop.id, name="Bananas",       quantity=1.0, unit="bunch",  category="produce",  added_by=maya.id, added_at=now - timedelta(hours=5)),
            Item(list_id=weekly_shop.id, name="Greek Yogurt",  quantity=2.0, unit="cups",   category="dairy",    added_by=maya.id, added_at=now - timedelta(hours=5)),
            Item(list_id=weekly_shop.id, name="Sourdough",     quantity=1.0, unit="loaf",   category="bakery",   added_by=maya.id, added_at=now - timedelta(hours=4)),
            Item(list_id=weekly_shop.id, name="Chicken Thighs",quantity=2.0, unit="lbs",    category="meat",     added_by=maya.id, added_at=now - timedelta(hours=4)),
            Item(list_id=weekly_shop.id, name="Pasta",         quantity=1.0, unit="box",    category="pantry",   added_by=maya.id, added_at=now - timedelta(hours=3)),
            # Purchased
            Item(list_id=weekly_shop.id, name="Apples",        quantity=6.0, unit="count",  category="produce",  added_by=maya.id, added_at=now - timedelta(hours=5),
                 is_purchased=True, purchased_by=maya.id, purchased_at=now - timedelta(hours=1)),
            Item(list_id=weekly_shop.id, name="Milk",          quantity=1.0, unit="gallon", category="dairy",    added_by=maya.id, added_at=now - timedelta(hours=5),
                 is_purchased=True, purchased_by=maya.id, purchased_at=now - timedelta(hours=1)),
            Item(list_id=weekly_shop.id, name="Olive Oil",     quantity=1.0, unit="bottle", category="pantry",   added_by=leo.id,  added_at=now - timedelta(hours=3),
                 is_purchased=True, purchased_by=leo.id,  purchased_at=now - timedelta(minutes=30)),
        ]

        # ------------------------------------------------------------------
        # Items — Party Supplies (leo's shared list)
        # 4 items: 2 unpurchased, 2 purchased
        # ------------------------------------------------------------------
        party_items = [
            # Unpurchased
            Item(list_id=party_supplies.id, name="Paper Plates", quantity=50.0, unit="count",  category="supplies", added_by=leo.id,  added_at=now - timedelta(days=2)),
            Item(list_id=party_supplies.id, name="Sparkling Water", quantity=6.0, unit="cans", category="beverages",added_by=leo.id,  added_at=now - timedelta(days=2)),
            # Purchased
            Item(list_id=party_supplies.id, name="Chips",        quantity=3.0,  unit="bags",   category="snacks",   added_by=maya.id, added_at=now - timedelta(days=2),
                 is_purchased=True, purchased_by=maya.id, purchased_at=now - timedelta(hours=3)),
            Item(list_id=party_supplies.id, name="Salsa",        quantity=2.0,  unit="jars",   category="snacks",   added_by=maya.id, added_at=now - timedelta(days=2),
                 is_purchased=True, purchased_by=maya.id, purchased_at=now - timedelta(hours=3)),
        ]

        db.session.add_all(weekly_items + party_items)
        db.session.commit()

        print("Seed data created successfully.")
        print(f"  Users: 2 (maya, leo)")
        print(f"  Lists: 2 (Weekly Shop, Party Supplies)")
        print(f"  Items: {len(weekly_items) + len(party_items)} "
              f"({sum(1 for i in weekly_items + party_items if not i.is_purchased)} unpurchased, "
              f"{sum(1 for i in weekly_items + party_items if i.is_purchased)} purchased)")
        print()
        print("User IDs (use these to test the API):")
        print(f"  maya: {maya.id}")
        print(f"  leo:  {leo.id}")
        print()
        print("List IDs:")
        print(f"  Weekly Shop (maya's, private): {weekly_shop.id}")
        print(f"  Party Supplies (leo's, shared): {party_supplies.id}")


if __name__ == "__main__":
    seed()
