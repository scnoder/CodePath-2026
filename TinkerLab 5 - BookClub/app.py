"""
app.py — BookClub

Flask application factory and database setup.
"""

from flask import Flask
from extensions import db
import os


def create_app(config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///bookclub.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    if config:
        app.config.update(config)

    db.init_app(app)

    # Register blueprints
    from routes.books import books_bp
    from routes.reading import reading_bp
    from routes.stats import stats_bp

    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(reading_bp, url_prefix="/reading")
    app.register_blueprint(stats_bp, url_prefix="/stats")

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
