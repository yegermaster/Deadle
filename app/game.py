import os
import random
import datetime as dt
import pandas as pd
from flask import session, flash, redirect, url_for
from app import app, helper, db  # Import the Flask app instance
from app.models import User

MAX_ATTEMPTS = 5

def load_data():
    """Load data from Excel file and return list of names and DataFrame."""
    df = pd.read_excel(r'data/dead_db.xlsx', dtype={'deathyear': 'Int64'})
    return df["Name"].tolist(), df

# Load data and store it in memory
my_list, data_frame = load_data()

def initialize_game():
    """Initializes the game with a random choice."""
    session['guess_attempts'] = 0
    session['guess_history'] = []
    r = random.randint(0, len(data_frame) - 1)
    dict_data_frame = data_frame.iloc[r].to_dict()
    for k, v in dict_data_frame.items():
        if k in ['countryName', 'continentName', 'occupation']:
            dict_data_frame[k] = v.lower()
    session['target_info'] = dict_data_frame

def process_guess(guess_name):
    """Processes a single guess and handles the attempts."""
    guessed_row = data_frame[data_frame['Name'].str.upper() == guess_name.upper()]
    if guessed_row.empty:
        return 'Name not in list. Try again'

    session['guess_attempts'] += 1
    guessed_row = guessed_row.iloc[0].to_dict()
    feedback = generate_feedback(guessed_row)

    if not any(guess['name'] == feedback['name'] for guess in session['guess_history']):
        session['guess_history'].append(feedback)

    session.modified = True
    user = User.query.get(session['_user_id'])
    user.num_guesses += 1
    user.current_guess_count += 1

    if guessed_row['Name'].upper() == session['target_info']['Name'].upper():
        user.num_games += 1
        user.current_guess_count = 0
        db.session.commit()
        flash('Congratulations! You guessed correctly.', 'success')
        return redirect(url_for('index'))

    if session['guess_attempts'] >= MAX_ATTEMPTS:
        session['reveal'] = True
        wiki_url = session['target_info'].get('Link', '')
        image_filename = wiki_url.split('/')[-1] + '.jpg' if wiki_url else 'default.jpg'
        image_path = os.path.join(app.root_path, 'static', 'img', 'wiki_img', image_filename)
        if not os.path.exists(image_path) and wiki_url:
            helper.download_image(wiki_url)
        session['image_filename'] = image_filename
        user.num_games += 1  # Update the game count here as well
        db.session.commit()  # Ensure changes are committed to the database
        return 'Max attempts. Reset to start again'

    db.session.commit()  # Make sure to commit the changes after every modification
    return None

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

def get_death_feedback(guessed_row):
    """Gets the correct death year img output."""
    guessed_death = int(guessed_row['deathyear'])
    chosen_death = int(session['target_info']['deathyear'])
    diff = guessed_death - chosen_death
    g = 10
    y = 500
    if diff == 0:
        icon_image = None
        death_feedback = f"✅ Correct: {guessed_death}"
    elif diff > 0:
        icon = 'green' if diff < g else 'yellow' if g <= diff <= y else 'red'
        icon_image = helper.icon_img_feedback(icon=f'already_dead_{icon}', directory='deaths')
        death_feedback = guessed_death
    else:
        icon = 'green' if abs(diff) < g else 'yellow' if g <= abs(diff) <= y else 'red'
        icon_image = helper.icon_img_feedback(icon=f'still_alive_{icon}', directory='deaths')
        death_feedback = guessed_death

    return death_feedback, icon_image

def get_country_img(guessed_row):
    """Gets the correct country img output."""
    guessed_country = guessed_row['countryName'].lower()
    chosen_country = session['target_info']['countryName']
    lat, lan = guessed_row['latitude'], guessed_row['longitude']
    color = 'red' if guessed_country != chosen_country else 'green'
    helper.plot_location_on_globe(lat, lan, guessed_country, color)
    country_img = helper.icon_img_feedback(guessed_country, 'globe')
    return country_img

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
