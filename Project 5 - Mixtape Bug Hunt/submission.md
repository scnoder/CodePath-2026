# Submission — Mixtape Bug Hunt

## AI Usage

I used Claude throughout both environment setup and bug investigation.

**Environment/setup help:** Claude explained why `python app.py` caused a SQLAlchemy double-import error (the app factory gets imported twice — once as `__main__`, once as `app` — when something else imports `app` as a module), and walked me through running the app correctly with `flask run` on PowerShell (`$env:FLASK_APP` / `$env:FLASK_DEBUG` instead of the bash-style `VAR=value command` syntax, which doesn't work in PowerShell).

**Bug investigation:** For each bug, I read the relevant function myself and formed a hypothesis about the root cause before asking Claude to confirm or correct it.
- **Streak bug:** I identified the suspicious line (`today.weekday() != 6`) myself. Claude confirmed the hypothesis and explained *why* it only manifests on Sundays (Python's `weekday()` returns 6 for Sunday), which I then verified against the exact sequence in the bug report (Sat → Sun reset → Mon resumes).
- **Feed bug:** I suspected `get_activity_feed()`; Claude corrected this — that function is explicitly documented as unfiltered by recency, so it isn't the source. Claude traced the actual bug to `get_friends_listening_now()`, where `RECENT_THRESHOLD = timedelta(hours=24)` implements a rolling 24-hour window rather than a "since midnight today" filter. I verified this against the reporter's exact timestamps (11pm listen, still visible at 9am).
- **Search duplication bug:** I suspected something in a loop. Claude identified the actual cause as a SQL-level join fan-out (`outerjoin` on `song_tags` produces one row per tag, not per song), and confirmed it explained the exact 3x duplication on a 3-tag song from the bug report.

**Where I verified/overrode Claude:** I did not accept any fix without checking it against the actual seed data and model definitions I had already read (e.g., confirming `Crown Heights Anthem` really does have 3 tags in `seed_data.py`, and confirming `User.friends` and `ListeningEvent` fields in `models.py` matched what the feed functions assumed). I also asked Claude to explain the mechanism behind each bug (not just hand me a fix) so I could confirm the reasoning matched the bug report's actual symptoms before treating the diagnosis as correct.

---

## Codebase Map

### Main files and their responsibilities

- **`app.py`** — Flask application factory (`create_app()`). Builds the Flask app, configures SQLAlchemy (`SQLALCHEMY_DATABASE_URI`, defaulting to a local SQLite file), calls `db.init_app(app)`, registers all four blueprints under their URL prefixes (`/songs`, `/playlists`, `/users`, `/feed`), and calls `db.create_all()` inside an app context. `db = SQLAlchemy()` is instantiated here and imported by every other module that needs database access.

- **`models.py`** — Defines all 6 SQLAlchemy models and 3 association tables:
  - `User` — has `listening_streak` and `last_listened_at` columns used by the streak feature, plus relationships to songs, ratings, listening events, notifications, and playlists. `friends` is a self-referential many-to-many relationship through the `friendships` table.
  - `Tag`, `Song` — `Song` has a many-to-many relationship to `Tag` via the `song_tags` association table.
  - `ListeningEvent` — one row per listen (`user_id`, `song_id`, `listened_at`). This is the table both the streak feature and the feed feature read from, but for different purposes.
  - `Rating` — one row per (user, song) pair, enforced by a unique constraint. There is no separate "review" concept — a rating is just a 1–5 `score`.
  - `Playlist` — many-to-many to `Song` via `playlist_entries`, which (unlike `song_tags`) carries extra columns: `position`, `added_by`, and `added_at`. This is the pattern called out in the assignment prompt — playlist order is explicit, not insertion order.
  - `Notification` — flat table (`user_id`, `notification_type`, `body`, `read`), created generically by `notification_service.create_notification()` and reused for multiple notification types (currently just `song_added_to_playlist`, but the type string suggests more are expected, e.g. `song_rated`).

- **`routes/`** — One blueprint per resource (`songs.py`, `playlists.py`, `users.py`, `feed.py`). Every route function parses the request (query params or JSON body), calls exactly one service function, and formats the response as JSON with an appropriate status code. Routes contain no business logic themselves — errors from services are caught as `ValueError` and turned into 400/404 responses.

- **`services/`** — All business logic lives here, one file per feature area:
  - `search_service.py` — `search_songs()`, `get_song()`.
  - `streak_service.py` — `update_listening_streak()`, plus (referenced by routes but not yet reviewed in full) `get_streak()` and `record_listening_event()`.
  - `feed_service.py` — `get_friends_listening_now()`, `get_activity_feed()`.
  - `notification_service.py` — `create_notification()`, `add_to_playlist()`, `rate_song()`, `get_notifications()`, `mark_as_read()`. Notably, this file owns both notification creation *and* the two actions that trigger notifications (adding to a playlist, rating a song) — it isn't purely a "notification CRUD" file.
  - `playlist_service.py` — `create_playlist()`, `get_playlist()`, `get_playlist_songs()`, `get_user_playlists()`.

- **`seed_data.py`** — Populates a fresh database with 5 users (with friendships), 25 songs (with 0/1/3+ tags to specifically exercise the search-duplication bug), 3 playlists, and a mix of recent/old listening events designed to exercise the "listening now" recency bug. This is clearly written as a bug-hunt fixture, not generic sample data — the tag counts and event timestamps map directly onto the two bugs above.

### Data flow: adding a song to a playlist → notification

1. Client sends `POST /playlists/<playlist_id>/songs` with `{"song_id": ..., "added_by": ...}`.
2. `routes/playlists.py::add_song()` parses the body and calls `notification_service.add_to_playlist(playlist_id, song_id, added_by)`. The route does no validation beyond checking the two fields are present.
3. `add_to_playlist()` (in `services/notification_service.py`) does the actual work:
   - Loads `Song`, `User` (the adder), and `Playlist` by ID, raising `ValueError` for any that don't exist (caught by the route as a 400).
   - Appends the song to `playlist.songs` (the ORM-managed `playlist_entries` relationship) and commits — this is the actual "add to playlist" side effect.
   - If the adder is *not* the song's original sharer (`song.shared_by != added_by_user_id`), it calls `create_notification()` with `notification_type="song_added_to_playlist"` and a body string naming the adder, song, and playlist.
4. `create_notification()` builds a `Notification` row and commits it. There's no separate "notification builder" per type — the message body is just an f-string assembled by the caller (`add_to_playlist`), so each trigger point (playlist adds, ratings, etc.) is responsible for writing its own notification text.
5. The recipient later retrieves it via `GET /users/<user_id>/notifications`, which calls `get_notifications()`.

Two things worth noting about this flow: there's no notification if you add your *own* shared song to a playlist (intentional, per the `!=` check), and the entire flow is synchronous — the notification is created in the same request/transaction as the playlist update, not queued separately.

### Patterns noticed

- **Strict routes → services separation.** Every route file does request parsing and JSON formatting only; every actual query or mutation happens in `services/`. This matches the pattern described in the assignment prompt exactly.
- **No separate "action" tables where a flag will do.** Ratings live directly on a `Rating` row tied to `Song` (not embedded on `Song` itself, correcting my earlier assumption) but the model is otherwise minimal — a `Rating` is nothing but `(user_id, song_id, score)`.
- **Many-to-many tables are used for two different purposes**: pure tagging (`song_tags`, no extra columns) versus ordered/attributed membership (`playlist_entries`, carrying `position`/`added_by`/`added_at`). Code that joins against these tables needs to be aware of which kind it's dealing with — the search-duplication bug happened specifically because a query joined against `song_tags` without accounting for its one-to-many fan-out.
- **Timestamps are stored per-event, and multiple features derive different things from the same table** (`ListeningEvent`). The streak bug and the feed bug are unrelated in cause, but both stem from ambiguity around what "recent" or "today" should mean relative to a stored UTC timestamp.

### Two additional issues noticed but not in the original bug reports (flagging for verification, not yet root-caused)

- `services/playlist_service.py::get_playlist_songs()` returns `songs[:-1]` instead of `songs` — this drops the last song in every playlist's song list regardless of playlist size. Worth confirming whether this is an intended "preview" truncation or an unintended slice bug.
- `services/notification_service.py::add_to_playlist()` appends directly to `playlist.songs` (the ORM secondary relationship), but `playlist_entries` has `position` and `added_by` as `nullable=False` columns with no default. Appending via the plain secondary relationship may not populate those columns, which could raise an `IntegrityError` at runtime — worth testing directly rather than assuming it works.

---

## Root Cause Analysis

### Bug 1 — Listening streak resets to 1 every Sunday

**Symptom:** A user with a 12-day streak who listened on both Saturday and Sunday saw their streak drop to 1 on Sunday, then correctly increment to 2 on Monday.

**Root cause:** In `streak_service.py::update_listening_streak()`, the streak-increment branch was:
```python
elif days_since_last == 1 and today.weekday() != 6:
    user.listening_streak += 1
else:
    user.listening_streak = 1
```
`date.weekday()` returns `6` for Sunday. So even when a user listened on consecutive days (`days_since_last == 1`), if the current day happened to be a Sunday, the added `and today.weekday() != 6` condition evaluated `False`, sending execution to the `else` branch and resetting the streak to 1. The documented streak rules (in the function's own docstring) make no mention of weekdays at all — this condition doesn't correspond to any specified business rule.

**Fix:** Removed the weekday condition entirely, leaving the increment based solely on `days_since_last`:
```python
elif days_since_last == 1:
    user.listening_streak += 1
else:
    user.listening_streak = 1
```

---

### Bug 2 — "Friends Listening Now" shows yesterday evening's activity the next morning

**Symptom:** A friend's listen from 11pm the previous night still appeared under "listening now" at 9am the next day, despite the friend not having opened the app since.

**Root cause:** In `feed_service.py::get_friends_listening_now()`, the recency filter used a rolling window rather than a calendar-day boundary:
```python
RECENT_THRESHOLD = timedelta(hours=24)
cutoff = datetime.now(timezone.utc) - RECENT_THRESHOLD
```
This keeps any event visible for exactly 24 hours after it occurred, regardless of what calendar day it is. An 11pm event checked at 9am the next morning is only ~10 hours old, well inside the 24-hour window, so it stays visible until 11pm the *next* day — a full day later than a user would expect from a feature called "listening now."

**Fix:** Replaced the rolling window with a cutoff pinned to the start of the current calendar day (UTC):
```python
now = datetime.now(timezone.utc)
cutoff = now.replace(hour=0, minute=0, second=0, microsecond=0)
```
This makes the filter "has this user listened today," matching the feature's intent. Note: this assumes UTC is an acceptable proxy for "today" for all users; per-user timezone handling would be a separate follow-up if the app needs to support users across timezones precisely.

---

### Bug 3 — Songs with multiple tags appear multiple times in search results

**Symptom:** Searching "Anthem" returned "Crown Heights Anthem" three times, identical in every field. Songs with fewer tags did not duplicate.

**Root cause:** In `search_service.py::search_songs()`, the query joined `Song` to the `song_tags` association table:
```python
db.session.query(Song)
    .outerjoin(song_tags, Song.id == song_tags.c.song_id)
    .filter(...)
    .all()
```
A SQL join produces one row per matching pair across the joined tables, not one row per `Song`. A song with 3 tags matches 3 rows in `song_tags`, so the join returns that song 3 times — exactly matching the reported 3x duplication on a song with 3 tags in the seed data (`rap`, `hip-hop`, `boom bap`). The join's output was never actually used (no tag columns were selected or aggregated), so it served no purpose other than causing the fan-out.

**Fix:** Removed the unnecessary join entirely, since `Song.tags` is already available via the ORM relationship and is used separately inside `to_dict()`:
```python
db.session.query(Song)
    .filter(
        db.or_(
            Song.title.ilike(f"%{query}%"),
            Song.artist.ilike(f"%{query}%"),
        )
    )
    .all()
```