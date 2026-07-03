"""
services/reading_service.py — BookClub

Handles all reading list operations: adding books, starting and finishing
books, and retrieving a user's reading history.
"""

from datetime import datetime, timezone
from extensions import db
from models import User, Book, ReadingEvent


def get_books() -> list[Book]:
    """Return all books in the shared reading list, most recently added first."""
    return Book.query.order_by(Book.added_at.desc()).all()


def add_book(title: str, author: str, pages: int, genre: str, user_id: str) -> Book:
    """
    Add a new book to the shared reading list.

    Args:
        title:   Book title.
        author:  Book author.
        pages:   Total page count.
        genre:   Genre string (optional).
        user_id: ID of the user adding the book.

    Returns:
        The newly created Book.
    """
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")

    book = Book(title=title, author=author, pages=pages, genre=genre, added_by=user_id)
    db.session.add(book)
    db.session.commit()
    return book


def start_reading(user_id: str, book_id: str) -> ReadingEvent:
    """
    Record that a user has started reading a book.

    Creates a ReadingEvent with started_at set to now and finished_at as None.
    Raises ValueError if the user is already reading this book.

    Args:
        user_id: ID of the user.
        book_id: ID of the book.

    Returns:
        The created ReadingEvent.
    """
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")

    book = db.session.get(Book, book_id)
    if not book:
        raise ValueError(f"Book {book_id} not found")

    existing = ReadingEvent.query.filter_by(user_id=user_id, book_id=book_id).first()
    if existing:
        raise ValueError(f"User {user_id} is already reading book {book_id}")

    event = ReadingEvent(
        user_id=user_id,
        book_id=book_id,
        started_at=datetime.now(timezone.utc),
    )
    db.session.add(event)
    db.session.commit()
    return event


def mark_as_finished(user_id: str, book_id: str) -> ReadingEvent:
    """
    Mark a book as finished for a user.

    Sets finished_at to now and updates the user's last_finished_at timestamp.
    Raises ValueError if the user has not started this book.

    Args:
        user_id: ID of the user.
        book_id: ID of the book.

    Returns:
        The updated ReadingEvent.
    """
    event = ReadingEvent.query.filter_by(user_id=user_id, book_id=book_id).first()
    if not event:
        raise ValueError(f"No reading record found for user {user_id} and book {book_id}")
    if event.finished_at is not None:
        raise ValueError(f"User {user_id} has already finished book {book_id}")

    now = datetime.now(timezone.utc)
    event.finished_at = now

    user = db.session.get(User, user_id)
    user.last_finished_at = now

    db.session.commit()
    return event


def get_reading_history(user_id: str) -> list[ReadingEvent]:
    """
    Return all books a user has finished, most recently finished first.

    Only includes events where finished_at is set (i.e., books that have been
    completed — not books currently in progress).

    Args:
        user_id: ID of the user.

    Returns:
        List of ReadingEvent objects ordered by finished_at descending.
    """
    return (
        ReadingEvent.query.filter_by(user_id=user_id)
        .filter(ReadingEvent.finished_at.isnot(None))
        .order_by(ReadingEvent.started_at.desc())
        .all()
    )


def get_currently_reading(user_id: str) -> list[ReadingEvent]:
    """
    Return books a user has started but not yet finished.

    Args:
        user_id: ID of the user.

    Returns:
        List of ReadingEvent objects where finished_at is None, ordered by
        started_at descending.
    """
    return (
        ReadingEvent.query.filter_by(user_id=user_id)
        .filter(ReadingEvent.finished_at.is_(None))
        .order_by(ReadingEvent.started_at.desc())
        .all()
    )
