"""
routes/books.py — BookClub

Routes for browsing and adding books to the shared reading list.
"""

from flask import Blueprint, jsonify, request
from services import reading_service

books_bp = Blueprint("books", __name__)


@books_bp.route("/", methods=["GET"])
def list_books():
    """Return all books in the reading list."""
    books = reading_service.get_books()
    return jsonify([b.to_dict() for b in books])


@books_bp.route("/", methods=["POST"])
def add_book():
    """
    Add a new book to the reading list.

    Expected JSON body:
        title   (str, required)
        author  (str, required)
        pages   (int, required)
        genre   (str, optional)
        user_id (str, required) — the user adding the book
    """
    data = request.get_json()
    required = ["title", "author", "pages", "user_id"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    try:
        book = reading_service.add_book(
            title=data["title"],
            author=data["author"],
            pages=int(data["pages"]),
            genre=data.get("genre"),
            user_id=data["user_id"],
        )
        return jsonify(book.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
