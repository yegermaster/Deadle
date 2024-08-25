"""
This module handles the routes and core functionality for the Deadle web game.
"""

from flask import render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from app import app, db
from app.auth import auth
import app.game as game
from app.models import User


app.register_blueprint(auth)
app.secret_key = '123'

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Redirect to the auth blueprint's login route."""
    return redirect(url_for('auth.login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Redirect to the auth blueprint's register route."""
    return redirect(url_for('auth.register'))

@app.route('/logout')
def logout():
    """Redirect to the auth blueprint's logout route."""
    return redirect(url_for('auth.logout'))

@app.route('/reset')
def reset():
    """Route to reset the game session and redirects to the index page."""
    game.clear_imgs()
    user_id = session.get('_user_id')
    session.clear()
    session['_user_id'] = user_id

    user = User.query.get(user_id)
    user.is_playing = False
    user.current_guess_count = 0
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Route for the main game page handling GET and POST requests."""
    if 'guess_attempts' not in session or 'target_info' not in session:
        game.initialize_game()

    user = current_user
    feedback = ''
    if request.method == 'POST':
        guess_name = request.form.get('guess')
        if guess_name:
            process_feedback = game.process_guess(guess_name)
            if process_feedback:
                feedback = process_feedback
    
    user_stats = {
        'username': user.username,
        'num_games': user.num_games,
        'num_guesses': user.num_guesses,
        'current_guess_count': user.current_guess_count,
        'num_wins': user.wins,
        'date_joined': user.date_joined.strftime('%Y-%m-%d')
    }
    return render_template('index.html', 
                           user=current_user, 
                           feedback=feedback,
                           my_list=game.my_list,
                           guess_history=session.get('guess_history', []),
                           image_filename=session.get('image_filename', ''),
                           MAX_ATTEMPTS=game.MAX_ATTEMPTS,
                           user_stats=user_stats)

if __name__ == "__main__":
    app.run(debug=True)
