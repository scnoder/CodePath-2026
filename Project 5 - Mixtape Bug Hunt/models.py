"""
models.py — Mixtape

SQLAlchemy models for all database entities.
"""

import uuid
from datetime import datetime, timezone
from app import db


def generate_uuid():
    return str(uuid.uuid4())


# Association table for User friendships (many-to-many, symmetric)
friendships = db.Table(
    "friendships",
    db.Column("user_id", db.String(36), db.ForeignKey("user.id"), primary_key=True),
    db.Column("friend_id", db.String(36), db.ForeignKey("user.id"), primary_key=True),
)

# Association table for Song tags (many-to-many)
song_tags = db.Table(
    "song_tags",
    db.Column("song_id", db.String(36), db.ForeignKey("song.id"), primary_key=True),
    db.Column("tag_id", db.String(36), db.ForeignKey("tag.id"), primary_key=True),
)

# Association table for Playlist songs (many-to-many with ordering)
playlist_entries = db.Table(
    "playlist_entries",
    db.Column("playlist_id", db.String(36), db.ForeignKey("playlist.id"), primary_key=True),
    db.Column("song_id", db.String(36), db.ForeignKey("song.id"), primary_key=True),
    db.Column("position", db.Integer, nullable=False),
    db.Column("added_by", db.String(36), db.ForeignKey("user.id"), nullable=False),
    db.Column("added_at", db.DateTime, default=lambda: datetime.now(timezone.utc)),
)


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    listening_streak = db.Column(db.Integer, default=0)
    last_listened_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    shared_songs = db.relationship("Song", backref="shared_by_user", lazy=True)
    ratings = db.relationship("Rating", backref="rater", lazy=True)
    listening_events = db.relationship("ListeningEvent", backref="listener", lazy=True)
    notifications = db.relationship("Notification", backref="recipient", lazy=True)
    playlists = db.relationship("Playlist", backref="creator", lazy=True)
    friends = db.relationship(
        "User",
        secondary=friendships,
        primaryjoin=(friendships.c.user_id == id),
        secondaryjoin=(friendships.c.friend_id == id),
        lazy="dynamic",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "listening_streak": self.listening_streak,
            "last_listened_at": self.last_listened_at.isoformat() if self.last_listened_at else None,
        }


class Tag(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(64), unique=True, nullable=False)


class Song(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), nullable=False)
    album = db.Column(db.String(200), nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    shared_by = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    shared_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    share_note = db.Column(db.Text, nullable=True)

    # Relationships
    ratings = db.relationship("Rating", backref="song", lazy=True)
    listening_events = db.relationship("ListeningEvent", backref="song", lazy=True)
    tags = db.relationship("Tag", secondary=song_tags, lazy="subquery")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "genre": self.genre,
            "shared_by": self.shared_by,
            "shared_at": self.shared_at.isoformat(),
            "share_note": self.share_note,
            "tags": [tag.name for tag in self.tags],
        }


class ListeningEvent(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    song_id = db.Column(db.String(36), db.ForeignKey("song.id"), nullable=False)
    listened_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "song_id": self.song_id,
            "listened_at": self.listened_at.isoformat(),
        }


class Rating(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    song_id = db.Column(db.String(36), db.ForeignKey("song.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)  # 1–5
    rated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint("user_id", "song_id", name="unique_user_song_rating"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "song_id": self.song_id,
            "score": self.score,
            "rated_at": self.rated_at.isoformat(),
        }


class Playlist(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(200), nullable=False)
    created_by = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_collaborative = db.Column(db.Boolean, default=True)

    songs = db.relationship("Song", secondary=playlist_entries, lazy="subquery")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "is_collaborative": self.is_collaborative,
        }


class Notification(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    notification_type = db.Column(db.String(64), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    read = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.notification_type,
            "body": self.body,
            "created_at": self.created_at.isoformat(),
            "read": self.read,
        }
