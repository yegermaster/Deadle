"""
This module initializes the Flask application and sets up the SQLAlchemy database connection.

The application is configured to connect to a PostgreSQL database. SQLAlchemy is used as the
Object-Relational Mapper (ORM) for database interactions.

Configuration:
- SQLALCHEMY_DATABASE_URI: The URI for connecting to the PostgreSQL database.

Usage:
    from app import app, db
"""
from flask import Flask

app = Flask(__name__)
app.secret_key = '123'

from app import views