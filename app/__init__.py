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
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

# Configure the SQLAlchemy part of the app isntance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Initialize the database
db = SQLAlchemy(app)
# Initialize the login manager
login_manager = LoginManager(app)
# Define the login view for the login_required decorator
login_manager.login_view = 'login'
# Customize the flash message category for the login_required decorator
login_manager.login_message_category = 'info'

from app import views
from app import models

with app.app_context():
    db.create_all()