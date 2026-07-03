"""
routes/reading.py — BookClub

Routes for tracking reading progress: starting a book, finishing a book,
and viewing what a user is currently reading.
"""

from flask import Blueprint, jsonify, request
from services import reading_service

reading_bp = Blueprint("reading", __name__)


@reading_bp.route("/start", methods=["POST"])
def start_reading():
    """
    Mark that a user has started reading a book.

    Expected JSON body:
        user_id (str, required)
        book_id (str, required)
    """
    data = request.get_json()
    required = ["user_id", "book_id"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    try:
        event = reading_service.start_reading(
            user_id=data["user_id"],
            book_id=data["book_id"],
        )
        return jsonify(event.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@reading_bp.route("/finish", methods=["POST"])
def finish_reading():
    """
    Mark that a user has finished reading a book.

    Expected JSON body:
        user_id (str, required)
        book_id (str, required)
    """
    data = request.get_json()
    required = ["user_id", "book_id"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    try:
        event = reading_service.mark_as_finished(
            user_id=data["user_id"],
            book_id=data["book_id"],
        )
        return jsonify(event.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@reading_bp.route("/current/<user_id>", methods=["GET"])
def currently_reading(user_id):
    """Return the books a user is currently reading (started but not finished)."""
    events = reading_service.get_currently_reading(user_id)
    result = []
    for e in events:
        entry = e.to_dict()
        entry["book"] = e.book.to_dict()
        result.append(entry)
    return jsonify(result)


@reading_bp.route("/history/<user_id>", methods=["GET"])
def reading_history(user_id):
    """Return the books a user has finished, most recently finished first."""
    events = reading_service.get_reading_history(user_id)
    result = []
    for e in events:
        entry = e.to_dict()
        entry["book"] = e.book.to_dict()
        result.append(entry)
    return jsonify(result)
