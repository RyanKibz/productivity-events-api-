
from sqlalchemy import select
from app import app
from extensions import db
from models import User, Event

with app.app_context():
    user = db.session.scalar(
        select(User).where(User.username == "demo")
    )

    if not user:
        user = User(username="demo")
        user.set_password("DemoPass123!")
        db.session.add(user)
        db.session.flush()

        for title, description in [
            ("Plan the week", "Set weekly priorities"),
            ("Study Flask", "Practice authentication"),
            ("Complete assignment", "Test the API")
        ]:
            db.session.add(Event(
                title=title,
                description=description,
                user_id=user.id
            ))

        db.session.commit()
        print("Demo account and events created.")
    else:
        print("Demo account already exists.")
