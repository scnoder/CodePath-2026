"""
services/collection_service.py — CineLog

Business logic for managing a user's film collection (films they've already watched).
All functions follow the project's verb_to_noun naming convention.
"""

from app import db
from models import Film, CollectionEntry


class FilmNotFoundError(Exception):
    """Raised when a film_id does not exist in the database."""
    pass


class AlreadyInCollectionError(Exception):
    """Raised when a film is already in the user's collection."""
    pass


class NotInCollectionError(Exception):
    """Raised when trying to remove a film that isn't in the collection."""
    pass


def add_to_collection(user_id, film_id, rating=None):
    """
    Add a film to a user's collection (i.e., mark it as watched).

    Args:
        user_id (str): UUID of the user.
        film_id (str): UUID of the film.
        rating (int, optional): Rating from 1–5. May be added later.

    Returns:
        CollectionEntry: The newly created entry.

    Raises:
        FilmNotFoundError: If film_id does not exist.
        AlreadyInCollectionError: If the film is already in the user's collection.
    """
    film = Film.query.get(film_id)
    if film is None:
        raise FilmNotFoundError(f"No film found with id '{film_id}'")

    existing = CollectionEntry.query.filter_by(
        user_id=user_id, film_id=film_id
    ).first()
    if existing:
        raise AlreadyInCollectionError(
            f"Film '{film_id}' is already in this user's collection"
        )

    entry = CollectionEntry(user_id=user_id, film_id=film_id, rating=rating)
    db.session.add(entry)
    db.session.commit()
    return entry


def remove_from_collection(user_id, film_id):
    """
    Remove a film from a user's collection.

    Args:
        user_id (str): UUID of the user.
        film_id (str): UUID of the film.

    Returns:
        bool: True if the entry was removed.

    Raises:
        NotInCollectionError: If the film is not in the user's collection.
    """
    entry = CollectionEntry.query.filter_by(
        user_id=user_id, film_id=film_id
    ).first()
    if entry is None:
        raise NotInCollectionError(
            f"Film '{film_id}' is not in this user's collection"
        )

    db.session.delete(entry)
    db.session.commit()
    return True


def get_collection(user_id):
    """
    Return all films in a user's collection, sorted by date added (newest first).

    Args:
        user_id (str): UUID of the user.

    Returns:
        list[dict]: List of film dicts (not CollectionEntry objects) with
                    the date_added and rating from the entry attached.
    """
    entries = (
        CollectionEntry.query
        .filter_by(user_id=user_id)
        .order_by(CollectionEntry.date_added.desc())
        .all()
    )

    result = []
    for entry in entries:
        film_dict = entry.film.to_dict()
        film_dict["date_added"] = entry.date_added.isoformat()
        film_dict["rating"] = entry.rating
        result.append(film_dict)

    return result
