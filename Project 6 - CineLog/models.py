"""
models.py — CineLog

SQLAlchemy models. Film IDs use UUIDs throughout.
(This is the post-refactor state on main — integer IDs were migrated to UUIDs.)
"""

import uuid
from datetime import datetime, timezone
from app import db


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    collection_entries = db.relationship("CollectionEntry", backref="user", lazy=True)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}


class Film(db.Model):
    # Film IDs are UUIDs — refactored from integer in commit:
    # "refactor: migrate film IDs from integer to UUID"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    director = db.Column(db.String(200), nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    poster_url = db.Column(db.String(500), nullable=True)
    average_rating = db.Column(db.Float, default=0.0)

    collection_entries = db.relationship("CollectionEntry", backref="film", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "director": self.director,
            "genre": self.genre,
            "poster_url": self.poster_url,
            "average_rating": self.average_rating,
        }


class CollectionEntry(db.Model):
    """Represents a film a user has already watched and logged."""
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    film_id = db.Column(db.String(36), db.ForeignKey("film.id"), nullable=False)
    date_added = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    rating = db.Column(db.Integer, nullable=True)  # 1–5, optional

    __table_args__ = (
        db.UniqueConstraint("user_id", "film_id", name="unique_user_film_collection"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "film_id": self.film_id,
            "date_added": self.date_added.isoformat(),
            "rating": self.rating,
        }
