from database import db
from datetime import datetime

class ChatHistory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_message = db.Column(
        db.Text,
        nullable=False
    )

    bot_response = db.Column(
        db.Text,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )