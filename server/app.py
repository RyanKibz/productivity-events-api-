
import os
from flask import Flask
from extensions import db, migrate, bcrypt, csrf

app = Flask(__name__)


secret = os.environ.get("SECRET_KEY")
if not secret and os.environ.get("FLASK_ENV") == "production":
    raise RuntimeError("SECRET_KEY must be set in production")

app.config.update(
    SECRET_KEY=secret or "development-only-change-me",
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        "DATABASE_URL", "sqlite:///productivity.db"
    ),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get(
        "COOKIE_SECURE", "false"
    ).lower() == "true",
)

db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
csrf.init_app(app)

from models import User, Event
from auth_routes import auth_bp
from event_routes import event_bp
from flask_wtf.csrf import CSRFError
from flask import jsonify

app.register_blueprint(auth_bp)
app.register_blueprint(event_bp)


@app.errorhandler(CSRFError)
def handle_csrf_error(error):
    return jsonify(error=error.description), 400


