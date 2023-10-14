from datetime import datetime
from schoolAI import db
from uuid import uuid4


def get_uuid():
    return uuid4().hex


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.String(34), primary_key=True, unique=True, nullable=False, default=get_uuid
    )

    email = db.Column(db.String(345), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    topics = db.relationship("ExplainedTopics", backref="user", lazy="dynamic")
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f" email({self.email}), date_created({self.date_created}))"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "email": self.email,
            "date_created": self.date_created,
        }


class ExplainedTopics(db.Model):
    __tablename__ = "explained_topics"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(34), db.ForeignKey("users.id"), nullable=False)
    topic = db.Column(db.String(120), nullable=False)
    explanation = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, user_id, topic, explanation):
        self.user_id = user_id
        self.topic = topic
        self.explanation = explanation

    def __repr__(self):
        return f"user_name({self.user.email}), topic({self.topic}), explanation({self.explanation}))"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "user_id": self.user.email,
            "topic": self.topic,
            "explanation": self.explanation,
            "date_created": self.date_created,
        }
