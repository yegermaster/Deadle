"""
This module creates a class for the user to keep track his login data and game statisitcs.
"""

from datetime import datetime
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """ The User class represents a registered player in the Deadle game.
    Inherits from:
      - db.Model (SQLAlchemy) for ORM functionality
      - UserMixin (Flask-Login) for built-in authentication helpers (e.g., is_authenticated, get_id).

    Attributes:
        id (int): Primary key; unique identifier for each user record.
        username (str): Unique name chosen by the user (limited to 150 chars).
        password (str): User's password (storing as hashed & salted for production security).
        num_games (int): Tracks how many games the user has played.
        num_guesses (int): Total guesses made across all games; useful for long-term stats or leaderboards.
        is_playing (bool): Flag indicating if the user is currently in an active game session.
        current_guess_count (int): Number of guesses the user has made in the current game.
        wins (int): Number of successful games (win count).
        date_joined (DateTime): Timestamp of when the account was created; defaults to UTC now.
    """
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
        """ Define how the User object is represented as a string."""
        return f"<User {self.username}>"
