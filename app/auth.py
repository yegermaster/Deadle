"""
This module handles the authentication logic of the Deadle web game.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db, login_manager


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login logic"""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Attempt to find the user by username in the database.
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            # Use flash to provide user feedback on an unsuccessful login attempt.
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration logic"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Generate a hashed password with a recommended method (e.g. pbkdf2, bcrypt, or argon2).
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        # Construct a new user object with default stats from the User model.
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to login', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    """Handle user logout logic"""
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

@auth.route('/check-auth')
def check_auth():
    """Check if user is authnticated"""
    return jsonify({'is_authenticated': current_user.is_authenticated})
