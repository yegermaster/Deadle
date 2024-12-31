"""
This module handles the game logic of the Deadle web game.
"""

import os
import random
import pandas as pd
from flask import session, flash, redirect, url_for
from app import app, helper, db
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
    guessed_dict = guessed_row.iloc[0].to_dict()
    feedback = generate_feedback(guessed_dict)

    if not any(guess['name'] == feedback['name'] for guess in session['guess_history']):
        session['guess_history'].append(feedback)

    session.modified = True
    user = User.query.get(session['_user_id'])
    user.num_guesses += 1
    user.current_guess_count += 1

    # Check if user guessed correctly
    if guessed_dict['Name'].upper() == session['target_info']['Name'].upper():
        user.num_games += 1
        user.current_guess_count = 0
        db.session.commit()
        flash('Congratulations! You guessed correctly.', 'success')

    wiki_url = session['target_info'].get('Link', '')
    if wiki_url:
        raw_name = wiki_url.split('/')[-1]
        if not raw_name:
            raw_name = 'default'
        base, ext = os.path.splitext(raw_name)
        if not ext:
            ext = '.jpg'
        final_filename = base + ext
        session['image_filename'] = final_filename

        helper.download_image(wiki_url, final_filename)  # calls load_wiki_image()
    else:
        session['image_filename'] = 'default.jpg'

    # If max attempts reached or guessed correctly, reveal the figure
    if (
        session['guess_attempts'] >= MAX_ATTEMPTS
        or guessed_dict['Name'].upper() == session['target_info']['Name'].upper()
    ):
        session['reveal'] = True
        user.num_games += 1
        db.session.commit()
        return None

    db.session.commit()
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
    guessed_value = guessed_row.get(attribute)
    if not guessed_value or (isinstance(guessed_value, float) and np.isnan(guessed_value)):
        guessed_value = 'unknown'

    guessed_value = str(guessed_value).lower()

    chosen_value = session['target_info'].get(attribute, '').lower()

    color = 'green' if guessed_value == chosen_value else 'red'
    icon = f'{guessed_value}_{color}'
    icon_path = os.path.join(app.root_path, 'static', 'img', 'icons', icon_dir, f'{icon}.png')
    icon_url = url_for('static', filename=f'img/icons/{icon_dir}/{icon}.png')
    icon_image = f"<img src='{icon_url}' alt='{icon}'>"

    if create_text and not os.path.exists(icon_path):
        helper.create_text_image(guessed_value, color, os.path.join(app.root_path, 'static', 'img', 'icons', icon_dir))

    print(f"guessed_value: {guessed_value}, attribute: {attribute}, icon: {icon}")
    return icon_image

def clear_imgs():
    """Clears images from directories."""
    helper.clear_dir("wiki_img")
    helper.clear_dir("icons/globe")
    helper.clear_dir("icons/occupations")
    helper.clear_dir("icons/continents")
