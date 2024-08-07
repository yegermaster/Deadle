"""
This module handles the routes and core functionality for the Deadle web game.
It includes game initialization, user input processing, and feedback generation.
"""
import os
import random
import pandas as pd
import datetime as dt
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, helper, db, login_manager
from app.models import User

#TODO: Correct Guess scenerio
#TODO: Fix the stats modal
#TODO: Add timer for the app

app.secret_key = '123'
MAX_ATTEMPTS = 5

def load_data():
    """Load data from Excel file and return list of names and DataFrame."""
    df = pd.read_excel(r'data/dead_db.xlsx', dtype={'deathyear': 'Int64'}) # reading
    return df["Name"].tolist(), df

# Load data and store it in memory
my_list, data_frame = load_data()

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login logic"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration logic"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Handle user logout logic"""
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

@app.route('/check-auth')
def check_auth():
    return jsonify({'is_authenticated': current_user.is_authenticated})

@app.route('/reset')
def reset():
    """Route to reset the game session and redirects to the index page"""
    clear_imgs()
    user_id = session.get('_user_id')  # Preserve the user_id
    session.clear()
    session['_user_id'] = user_id  # Restore the user_id

    # Reset user stats
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
        initialize_game()

    feedback = ''
    if request.method == 'POST':
        guess_name = request.form.get('guess')
        if guess_name:
            attempts = session.get('guess_attempts', 0)
            target = session.get('target_info', {})
            guessed_row = data_frame[data_frame['Name'].str.upper() == guess_name.upper()]  # Fetch the guessed row
            if not guessed_row.empty:
                guessed_row = guessed_row.iloc[0].to_dict()  # Convert to dictionary if not empty
                process_feedback = process_guess(guess_name)  # Capture the feedback from guessing
            if process_feedback:
                feedback = process_feedback
            # Checks if reached max attempts
            if attempts >= MAX_ATTEMPTS - 1:
                session['reveal'] = True
                wiki_url = target.get('Link', '')
                image_filename = wiki_url.split('/')[-1] + '.jpg' if wiki_url else 'default.jpg'
                image_path = os.path.join(app.root_path, 'static', 'img', 'wiki_img', image_filename)
                if not os.path.exists(image_path) and wiki_url:
                    helper.download_image(wiki_url)
                session['image_filename'] = image_filename
                feedback += " The historical figure was: " + target.get('Name', 'Unknown')
            # Check if the guess is correct
            if guessed_row['Name'].upper() == session['target_info']['Name'].upper():
                feedback = 'Correct! You have guessed the right historical figure.'
                session['reveal'] = True
                user = current_user
                user.num_games += 1
                user.wins += 1  # Ensure 'wins' is part of your user model
                db.session.commit()
                flash('Congratulations! You guessed correctly.', 'success')
                return redirect(url_for('index'))  # Redirect to the main page or a success page

        
    # Fetch user stats
    user = current_user
    user_stats = {
        'username': user.username,
        'num_games': user.num_games,
        'num_guesses': user.num_guesses,
        'current_guess_count': user.current_guess_count,
        'num_wins': user.wins,
        'date_joined': user.date_joined.strftime('%Y-%m-%d')
    }
    
    return render_template('index.html',user=current_user, 
                           feedback=feedback,
                           my_list=my_list,
                           guess_history=session.get('guess_history', []),
                           image_filename=session.get('image_filename', ''),
                           MAX_ATTEMPTS=MAX_ATTEMPTS,
                           user_stats=user_stats)

def initialize_game():
    """Initializes the game with random choice"""
    today = dt.date.today()
    session['guess_attempts'] = 0
    session['guess_history'] = []
    r = random.randint(0, len(data_frame) - 1) # choosing random number from the list
    dict_data_frame = data_frame.iloc[r].to_dict()
    for k, v in dict_data_frame.items():
        if k=='countryName' or k=='continentName' or k=='occupation' :
            dict_data_frame.update({k:v.lower()})
    session['target_info'] = dict_data_frame

def process_guess(guess_name):
    """Processes a single guess and handles the attempts"""
    guessed_row = data_frame[data_frame['Name'].str.upper() == guess_name.upper()]
    if guessed_row.empty:
        return 'Name not in list. Try again'

    session['guess_attempts'] += 1
    guessed_row = guessed_row.iloc[0].to_dict()
    feedback = generate_feedback(guessed_row)

    # Append feedback to guess history if not already present
    if not any(guess['name'] == feedback['name'] for guess in session['guess_history']):
        session['guess_history'].append(feedback)
    
    session.modified = True

    user = current_user
    user.num_guesses += 1
    user.current_guess_count += 1
    db.session.commit()

    if guessed_row['Name'].upper() == session['target_info']['Name'].upper():
        user.num_games += 1
        user.current_guess_count = 0
        db.session.commit()

    if session['guess_attempts'] >= MAX_ATTEMPTS:
        session['reveal'] = True
        wiki_url = session['target_info'].get('Link', '')
        image_filename = wiki_url.split('/')[-1] + '.jpg' if wiki_url else 'default.jpg'
        image_path = os.path.join(app.root_path, 'static', 'img', 'wiki_img', image_filename)
        if not os.path.exists(image_path) and wiki_url:
            helper.download_image(wiki_url)
        session['image_filename'] = image_filename
        session.modified = True
        return 'Max attempts. Reset to start again '

    return None

def get_death_feedback(guessed_row):
    """Gets the correct death year img output"""
    guessed_death = int(guessed_row['deathyear'])
    chosen_death = int(session['target_info']['deathyear'])
    diff = guessed_death - chosen_death
    # Setting color thershold values
    g = 10
    y = 500
    if diff == 0:
        icon_image = None
        death_feedback = f"✅ Correct: {guessed_death}"
    elif diff > 0:
        # allready dead
        if diff < g:
            icon = 'green'
        elif g <= diff <= y:
            icon = 'yellow'
        else:
            icon = 'red'
        icon_image = helper.icon_img_feedback(icon=f'already_dead_{icon}', directory='deaths')
        death_feedback = guessed_death
    else:
        # still alive
        if abs(diff) < g:
            icon = 'green'
        elif g <= abs(diff) <= y:
            icon = 'yellow'
        else:
            icon = 'red'
        icon_image = helper.icon_img_feedback(icon=f'still_alive_{icon}', directory='deaths')
        death_feedback = guessed_death
    
    return death_feedback, icon_image

def get_country_img(guessed_row):
    """Gets the correct country img output"""
    guessed_country = guessed_row['countryName'].lower()
    chosen_country = session['target_info']['countryName']
    lat, lan = guessed_row['latitude'], guessed_row['longitude']
    color = 'red' if guessed_country != chosen_country else 'green'
    helper.plot_location_on_globe(lat, lan, guessed_country, color)
    country_img = helper.icon_img_feedback(guessed_country, 'globe')
    return country_img

def generate_feedback(guessed_row):
    """Generates feedback for the user's guess."""
    feedback_funcs = {
        'occupation_feedback': ('occupation', 'occupations', True),
        'continent_feedback': ('continentName', 'continents', True),
        'gender_feedback': ('gender', 'genders'),
        'country_feedback': ('countryName', 'globe')
    }
    feedback = {}
    for key, (attr, directory, *args) in feedback_funcs.items():
        if key != 'country_feedback':
            feedback[key] = get_feedback(guessed_row, attr, directory, *args)
        else:
            feedback[key] = get_country_img(guessed_row)

    feedback.update({
        'name': guessed_row['Name'],
        'death_feedback': get_death_feedback(guessed_row)[0],
        'death_img': get_death_feedback(guessed_row)[1]
    })
    return feedback

def get_feedback(guessed_row, attribute, icon_dir, create_text=False):
    """Gets the feedback for a specific attribute."""
    guessed_value = guessed_row[attribute]
    if isinstance(guessed_value, str):
        guessed_value = guessed_value.lower()

    chosen_value = session['target_info'][attribute]
    if isinstance(chosen_value, str):
        chosen_value = chosen_value.lower()

    color = 'green' if guessed_value == chosen_value else 'red'
    icon = f'{guessed_value}_{color}' if isinstance(guessed_value, str) else f'{guessed_value}'
    icon_path = os.path.join(app.root_path, 'static', 'img', 'icons', icon_dir, f'{icon}.png')
    icon_url = url_for('static', filename=f'img/icons/{icon_dir}/{icon}.png')
    icon_image = f"<img src='{icon_url}' alt='{icon}'>"

    if create_text and not os.path.exists(icon_path):
        helper.create_text_image(str(guessed_value), color, os.path.join(app.root_path, 'static', 'img', 'icons', icon_dir))

    return icon_image

def clear_imgs():
    """Clears images from directories."""
    helper.clear_dir("wiki_img")
    helper.clear_dir("icons/globe")
    helper.clear_dir("icons/occupations")
    helper.clear_dir("icons/continents")

if __name__ == "__main__":
    app.run(debug=True)