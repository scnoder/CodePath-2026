"""
routes/collection.py — CineLog

Endpoints for a user's film collection (films they've logged as watched).
"""

from flask import Blueprint, jsonify, request
from services.collection_service import (
    add_to_collection,
    remove_from_collection,
    get_collection,
    FilmNotFoundError,
    AlreadyInCollectionError,
    NotInCollectionError,
)

collection_bp = Blueprint("collection", __name__)


@collection_bp.route("/<user_id>", methods=["GET"])
def view_collection(user_id):
    """
    GET /collection/<user_id>

    Returns all films in a user's collection, sorted newest-first.
    """
    films = get_collection(user_id)
    return jsonify(films)


@collection_bp.route("/<user_id>/add", methods=["POST"])
def add_film(user_id):
    """
    POST /collection/<user_id>/add

    Body: { "film_id": "<uuid>", "rating": 4 }  (rating optional)
    """
    data = request.get_json()
    if not data or "film_id" not in data:
        return jsonify({"error": "film_id is required"}), 400

    try:
        entry = add_to_collection(
            user_id=user_id,
            film_id=data["film_id"],
            rating=data.get("rating"),
        )
        return jsonify(entry.to_dict()), 201
    except FilmNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except AlreadyInCollectionError as e:
        return jsonify({"error": str(e)}), 409


@collection_bp.route("/<user_id>/remove", methods=["DELETE"])
def remove_film(user_id):
    """
    DELETE /collection/<user_id>/remove

    Body: { "film_id": "<uuid>" }
    """
    data = request.get_json()
    if not data or "film_id" not in data:
        return jsonify({"error": "film_id is required"}), 400

    try:
        remove_from_collection(user_id=user_id, film_id=data["film_id"])
        return jsonify({"message": "Removed from collection"}), 200
    except NotInCollectionError as e:
        return jsonify({"error": str(e)}), 404
