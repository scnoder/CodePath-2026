"""routes/feed.py — Mixtape feed routes"""

from flask import Blueprint, jsonify
from services.feed_service import get_friends_listening_now, get_activity_feed

feed_bp = Blueprint("feed", __name__)


@feed_bp.route("/<user_id>/listening-now")
def listening_now(user_id):
    try:
        feed = get_friends_listening_now(user_id)
        return jsonify({"feed": feed, "count": len(feed)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@feed_bp.route("/<user_id>/activity")
def activity(user_id):
    try:
        feed = get_activity_feed(user_id)
        return jsonify({"feed": feed, "count": len(feed)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
