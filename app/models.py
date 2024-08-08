"""
This module creates a class for the user to keep track his login data and game statisitcs.
"""

from datetime import datetime
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """Class to create the User data base to keep track of user stats"""
    id = db.Column(db.Integer, primary_key=True)  # Primary key column for unique identification of each user; data type is Integer.
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    num_games = db.Column(db.Integer, default=0)
    num_guesses = db.Column(db.Integer, default=0)
    is_playing = db.Column(db.Boolean, default=False)
    current_guess_count = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"
