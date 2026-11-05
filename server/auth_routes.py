
from functools import wraps
from flask import Blueprint, request, jsonify, session
from sqlalchemy import select
from extensions import db
from models import User
from flask_wtf.csrf import generate_csrf

auth_bp = Blueprint("auth", __name__)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify(error="Authentication required"), 401
        return func(*args, **kwargs)
    return wrapper

@auth_bp.post("/signup")
def signup():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON body required"), 400
    username = data.get("username")
    password = data.get("password")
    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify(error="Username and password required"), 400
    username = username.strip().lower()
    if not username or not 8 <= len(password.encode("utf-8")) <= 72:
        return jsonify(error="Invalid username or password length"), 400
    if db.session.scalar(select(User).where(User.username == username)):
        return jsonify(error="Username already exists"), 409
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    session.clear()
    session["user_id"] = user.id
    return jsonify(user.to_dict()), 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON body required"), 400
    username = data.get("username")
    password = data.get("password")
    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify(error="Invalid credentials"), 401
    user = db.session.scalar(
        select(User).where(User.username == username.strip().lower())
    )
    if not user or not user.check_password(password):
        return jsonify(error="Invalid credentials"), 401
    session.clear()
    session["user_id"] = user.id
    return jsonify(user.to_dict()), 200

@auth_bp.post("/logout")
def logout():
    session.clear()
    return "", 204
    
@auth_bp.get("/check_session")
@auth_bp.get("/me")
@login_required
def check_session():
    user = db.session.get(User, session["user_id"])
    if not user:
        session.clear()
        return jsonify(error="Authentication required"), 401
    return jsonify(user.to_dict()), 200


@auth_bp.get("/csrf-token")
def csrf_token():
    return jsonify(csrf_token=generate_csrf())
