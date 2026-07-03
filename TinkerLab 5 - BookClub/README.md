# BookClub — AI201 Lab 5 Starter

A small reading list app where club members track books, log their progress, and see their reading stats.

## What the app does

- **Book list** — members add books to a shared reading list
- **Reading tracker** — mark books as started or finished
- **Stats** — reading streak, books finished this month, total pages read

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
# or: .venv\Scripts\activate   # Windows

pip install -r requirements.txt

python seed_data.py    # populate the database
python app.py          # start the server (runs at http://127.0.0.1:5000)
```

## API

| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| GET    | `/books/`                       | List all books                       |
| POST   | `/books/`                       | Add a book                           |
| POST   | `/reading/start`                | Mark a book as started               |
| POST   | `/reading/finish`               | Mark a book as finished              |
| GET    | `/reading/current/<user_id>`    | Books a user is currently reading    |
| GET    | `/reading/history/<user_id>`    | Books a user has finished            |
| GET    | `/stats/<user_id>`              | Reading streak, books this month, total pages |

## Codebase structure

```plaintext
app.py                  Flask application factory
models.py               SQLAlchemy models: User, Book, ReadingEvent
routes/
  books.py              Book list endpoints
  reading.py            Reading progress endpoints
  stats.py              Statistics endpoint
services/
  reading_service.py    Reading list business logic
  stats_service.py      Statistics calculations
seed_data.py            Database seed script
```

## Running example requests

After seeding, use `curl` or any HTTP client. The seed script prints all three user IDs — use them in the examples below:

```bash
# Get all books
curl http://127.0.0.1:5000/books/

# Get alex's stats (replace USER_ID with the ID printed by seed_data.py)
curl http://127.0.0.1:5000/stats/USER_ID

# Get alex's reading history
curl http://127.0.0.1:5000/reading/history/USER_ID
```
