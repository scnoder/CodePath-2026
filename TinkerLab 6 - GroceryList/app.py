"""
app.py — GroceryList

Flask application factory and database setup.
"""

from flask import Flask
from extensions import db
import os


def create_app(config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///grocerylist.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    if config:
        app.config.update(config)

    db.init_app(app)

    from routes.lists import lists_bp

    app.register_blueprint(lists_bp, url_prefix="/lists")

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
