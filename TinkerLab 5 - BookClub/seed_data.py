"""
seed_data.py — BookClub

Populates the database with realistic test data.
Run with: python seed_data.py

This script creates:
- 3 users with established reading histories
- 10 books across different genres and page counts
- Reading events spanning the past 3 months
"""

from datetime import datetime, timedelta, timezone
from app import create_app, db
from models import User, Book, ReadingEvent


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        now = datetime.now(timezone.utc)

        # ------------------------------------------------------------------
        # Users
        # ------------------------------------------------------------------
        alex = User(
            username="alex",
            email="alex@bookclub.app",
            reading_streak=0,
        )
        priya = User(
            username="priya",
            email="priya@bookclub.app",
            reading_streak=0,
        )
        marcus = User(
            username="marcus",
            email="marcus@bookclub.app",
            reading_streak=0,
        )
        db.session.add_all([alex, priya, marcus])
        db.session.flush()

        # ------------------------------------------------------------------
        # Books (10 total — varied genres and page counts)
        # ------------------------------------------------------------------
        books = [
            Book(title="The Left Hand of Darkness",  author="Ursula K. Le Guin",    pages=286,  genre="sci-fi",           added_by=alex.id,   added_at=now - timedelta(days=90)),
            Book(title="Parable of the Sower",        author="Octavia E. Butler",    pages=352,  genre="sci-fi",           added_by=alex.id,   added_at=now - timedelta(days=85)),
            Book(title="Giovanni's Room",              author="James Baldwin",         pages=176,  genre="literary fiction", added_by=alex.id,   added_at=now - timedelta(days=80)),
            Book(title="Crying in H Mart",             author="Michelle Zauner",       pages=256,  genre="memoir",           added_by=priya.id,  added_at=now - timedelta(days=75)),
            Book(title="The House on Mango Street",    author="Sandra Cisneros",       pages=110,  genre="literary fiction", added_by=priya.id,  added_at=now - timedelta(days=70)),
            Book(title="Piranesi",                     author="Susanna Clarke",        pages=272,  genre="fantasy",          added_by=priya.id,  added_at=now - timedelta(days=60)),
            Book(title="Interior Chinatown",           author="Charles Yu",            pages=288,  genre="literary fiction", added_by=marcus.id, added_at=now - timedelta(days=50)),
            Book(title="Bewilderment",                 author="Richard Powers",        pages=278,  genre="sci-fi",           added_by=marcus.id, added_at=now - timedelta(days=40)),
            Book(title="Tomorrow, and Tomorrow",       author="Gabrielle Zevin",       pages=416,  genre="literary fiction", added_by=marcus.id, added_at=now - timedelta(days=30)),
            Book(title="Demon Copperhead",             author="Barbara Kingsolver",    pages=560,  genre="literary fiction", added_by=alex.id,   added_at=now - timedelta(days=20)),
        ]
        db.session.add_all(books)
        db.session.flush()

        # ------------------------------------------------------------------
        # Reading events for alex
        # ------------------------------------------------------------------

        # Three books alex has finished over the past several days.
        # Note: started_at order ≠ finished_at order (book[0] was started first
        # but finished last — alex reads multiple books at once).
        alex_finished = [
            ReadingEvent(
                user_id=alex.id,
                book_id=books[0].id,
                started_at=now - timedelta(days=85),
                finished_at=now - timedelta(hours=3),
            ),
            ReadingEvent(
                user_id=alex.id,
                book_id=books[1].id,
                started_at=now - timedelta(days=78),
                finished_at=now - timedelta(days=1),
            ),
            ReadingEvent(
                user_id=alex.id,
                book_id=books[2].id,
                started_at=now - timedelta(days=70),
                finished_at=now - timedelta(days=2),
            ),
        ]

        # Two books alex has started but not yet finished
        alex_in_progress = [
            ReadingEvent(
                user_id=alex.id,
                book_id=books[5].id,
                started_at=now - timedelta(days=65),
                finished_at=None,
            ),
            ReadingEvent(
                user_id=alex.id,
                book_id=books[9].id,
                started_at=now - timedelta(days=15),
                finished_at=None,
            ),
        ]

        alex.last_finished_at = alex_finished[0].finished_at

        # ------------------------------------------------------------------
        # Reading events for priya
        # ------------------------------------------------------------------

        priya_finished = [
            ReadingEvent(
                user_id=priya.id,
                book_id=books[3].id,
                started_at=now - timedelta(days=30),
                finished_at=now - timedelta(days=8),
            ),
            ReadingEvent(
                user_id=priya.id,
                book_id=books[4].id,
                started_at=now - timedelta(days=25),
                finished_at=now - timedelta(days=7),
            ),
        ]
        priya.last_finished_at = priya_finished[-1].finished_at

        # ------------------------------------------------------------------
        # Reading events for marcus
        # ------------------------------------------------------------------

        marcus_in_progress = [
            ReadingEvent(
                user_id=marcus.id,
                book_id=books[6].id,
                started_at=now - timedelta(days=5),
                finished_at=None,
            )
        ]

        db.session.add_all(
            alex_finished + alex_in_progress + priya_finished + marcus_in_progress
        )
        db.session.commit()

        print("Seed data created successfully.")
        print(f"  Users:  3 (alex, priya, marcus)")
        print(f"  Books:  {len(books)}")
        print(f"  Events: {len(alex_finished) + len(alex_in_progress) + len(priya_finished) + len(marcus_in_progress)}")
        print()
        print("User IDs (use these to test the API):")
        print(f"  alex:   {alex.id}")
        print(f"  priya:  {priya.id}")
        print(f"  marcus: {marcus.id}")


if __name__ == "__main__":
    seed()
