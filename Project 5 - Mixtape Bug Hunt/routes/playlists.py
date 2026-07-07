"""routes/playlists.py — Mixtape playlist routes"""

from flask import Blueprint, request, jsonify
from services.playlist_service import create_playlist, get_playlist_songs, get_playlist, get_user_playlists
from services.notification_service import add_to_playlist

playlists_bp = Blueprint("playlists", __name__)


@playlists_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    name = data.get("name")
    created_by = data.get("created_by")
    is_collaborative = data.get("is_collaborative", True)
    if not name or not created_by:
        return jsonify({"error": "name and created_by are required"}), 400
    try:
        playlist = create_playlist(name, created_by, is_collaborative)
        return jsonify(playlist.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@playlists_bp.route("/<playlist_id>")
def get_detail(playlist_id):
    try:
        playlist = get_playlist(playlist_id)
        return jsonify(playlist)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@playlists_bp.route("/<playlist_id>/songs")
def get_songs(playlist_id):
    try:
        songs = get_playlist_songs(playlist_id)
        return jsonify({"songs": songs, "count": len(songs)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@playlists_bp.route("/<playlist_id>/songs", methods=["POST"])
def add_song(playlist_id):
    data = request.get_json()
    song_id = data.get("song_id")
    added_by = data.get("added_by")
    if not song_id or not added_by:
        return jsonify({"error": "song_id and added_by are required"}), 400
    try:
        add_to_playlist(playlist_id, song_id, added_by)
        return jsonify({"message": "Song added to playlist"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
