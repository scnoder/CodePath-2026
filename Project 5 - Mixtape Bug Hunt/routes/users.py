"""routes/users.py — Mixtape user routes"""

from flask import Blueprint, request, jsonify
from app import db
from models import User
from services.streak_service import get_streak
from services.notification_service import get_notifications, mark_as_read

users_bp = Blueprint("users", __name__)


@users_bp.route("/<user_id>")
def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())


@users_bp.route("/<user_id>/streak")
def streak(user_id):
    try:
        current_streak = get_streak(user_id)
        return jsonify({"user_id": user_id, "streak": current_streak})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@users_bp.route("/<user_id>/notifications")
def notifications(user_id):
    unread_only = request.args.get("unread_only", "false").lower() == "true"
    try:
        notifs = get_notifications(user_id, unread_only=unread_only)
        return jsonify({"notifications": notifs, "count": len(notifs)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@users_bp.route("/notifications/<notification_id>/read", methods=["POST"])
def read_notification(notification_id):
    try:
        mark_as_read(notification_id)
        return jsonify({"message": "Notification marked as read"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
