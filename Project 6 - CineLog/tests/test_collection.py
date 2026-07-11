"""
tests/test_collection.py — CineLog

Tests for the collection service.
These tests demonstrate the patterns used across the codebase — read them
before writing your own tests for the watchlist feature (see Comment 4).
"""

import pytest
from app import create_app, db
from models import User, Film, CollectionEntry
from services.collection_service import (
    add_to_collection,
    remove_from_collection,
    get_collection,
    FilmNotFoundError,
    AlreadyInCollectionError,
    NotInCollectionError,
)


@pytest.fixture
def app():
    """Create an isolated test app with an in-memory database."""
    app = create_app(config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_user(app):
    """A user to use in tests."""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def sample_film(app):
    """A film to use in tests."""
    with app.app_context():
        film = Film(title="Paddington 2", year=2017, genre="Comedy")
        db.session.add(film)
        db.session.commit()
        return film.id


# ── Basic add ───────────────────────────────────────────────────────────────

def test_add_to_collection_creates_entry(app, sample_user, sample_film):
    """
    Adding a valid film should create a CollectionEntry in the database.
    """
    with app.app_context():
        entry = add_to_collection(user_id=sample_user, film_id=sample_film)

        assert entry is not None
        assert entry.user_id == sample_user
        assert entry.film_id == sample_film

        # Verify it persisted
        in_db = CollectionEntry.query.filter_by(
            user_id=sample_user, film_id=sample_film
        ).first()
        assert in_db is not None


# ── Deduplication ────────────────────────────────────────────────────────────

def test_add_to_collection_duplicate_raises(app, sample_user, sample_film):
    """
    Adding the same film twice should raise AlreadyInCollectionError,
    not silently create a duplicate entry.
    """
    with app.app_context():
        add_to_collection(user_id=sample_user, film_id=sample_film)

        with pytest.raises(AlreadyInCollectionError):
            add_to_collection(user_id=sample_user, film_id=sample_film)

        # Confirm only one entry exists
        count = CollectionEntry.query.filter_by(
            user_id=sample_user, film_id=sample_film
        ).count()
        assert count == 1


# ── Nonexistent film ─────────────────────────────────────────────────────────

def test_add_to_collection_nonexistent_film_raises(app, sample_user):
    """
    Adding a film_id that doesn't exist in the database should raise
    FilmNotFoundError, not a database integrity error.
    """
    with app.app_context():
        fake_film_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(FilmNotFoundError):
            add_to_collection(user_id=sample_user, film_id=fake_film_id)


# ── get_collection sort order ────────────────────────────────────────────────

def test_get_collection_returns_newest_first(app, sample_user):
    """
    get_collection() should return films sorted by date_added descending
    (most recently added first).
    """
    with app.app_context():
        from datetime import datetime, timezone, timedelta
        from models import Film, CollectionEntry

        film_a = Film(title="Alien", year=1979, genre="Horror")
        film_b = Film(title="Blade Runner", year=1982, genre="Sci-Fi")
        db.session.add_all([film_a, film_b])
        db.session.commit()

        earlier = datetime.now(timezone.utc) - timedelta(days=5)
        later = datetime.now(timezone.utc)

        entry_a = CollectionEntry(user_id=sample_user, film_id=film_a.id, date_added=earlier)
        entry_b = CollectionEntry(user_id=sample_user, film_id=film_b.id, date_added=later)
        db.session.add_all([entry_a, entry_b])
        db.session.commit()

        collection = get_collection(sample_user)
        titles = [f["title"] for f in collection]

        # Blade Runner was added later, so it should come first
        assert titles[0] == "Blade Runner"
        assert titles[1] == "Alien"
