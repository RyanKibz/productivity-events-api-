
from flask import Blueprint, request, jsonify, session
from sqlalchemy import select
from extensions import db
from models import Event
from auth_routes import login_required

event_bp = Blueprint("events", __name__)


def owned_event(event_id):
    return db.session.scalar(
        select(Event).where(
            Event.id == event_id,
            Event.user_id == session["user_id"]
        )
    )
@event_bp.get("/events")
@login_required
def list_events():
    try:
        page = int(request.args.get("page", "1"))
        per_page = int(request.args.get("per_page", "10"))
    except ValueError:
        return jsonify(error="Invalid pagination values"), 400

    if page < 1 or not 1 <= per_page <= 100:
        return jsonify(error="Invalid pagination values"), 400

    query = db.select(Event).where(
        Event.user_id == session["user_id"]
    ).order_by(Event.id)

    result = db.paginate(query, page=page, per_page=per_page, error_out=False)

    return jsonify(
        events=[event.to_dict() for event in result.items],
        pagination={
            "page": page,
            "per_page": per_page,
            "total": result.total,
            "pages": result.pages
        }
    )
@event_bp.post("/events")
@login_required
def create_event():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON body required"), 400

    title = data.get("title")
    description = data.get("description", "")
    if not isinstance(title, str) or not title.strip():
        return jsonify(error="Title is required"), 400
    if not isinstance(description, str):
        return jsonify(error="Description must be text"), 400

    event = Event(
        title=title.strip(),
        description=description,
        user_id=session["user_id"]
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201

@event_bp.get("/events/<int:event_id>")
@login_required
def get_event(event_id):
    event = owned_event(event_id)
    if not event:
        return jsonify(error="Event not found"), 404
    return jsonify(event.to_dict())

@event_bp.patch("/events/<int:event_id>")
@login_required
def update_event(event_id):
    event = owned_event(event_id)
    if not event:
        return jsonify(error="Event not found"), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON body required"), 400

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return jsonify(error="Invalid title"), 400
        event.title = data["title"].strip()

    if "description" in data:
        if not isinstance(data["description"], str):
            return jsonify(error="Invalid description"), 400
        event.description = data["description"]

    db.session.commit()
    return jsonify(event.to_dict())

@event_bp.delete("/events/<int:event_id>")
@login_required
def delete_event(event_id):
    event = owned_event(event_id)
    if not event:
        return jsonify(error="Event not found"), 404

    db.session.delete(event)
    db.session.commit()
    return "", 204
