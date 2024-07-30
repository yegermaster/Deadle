"""
This module handles the routes and core functionality for the Deadle web game.
It includes game initialization, user input processing, and feedback generation.
"""

import os
import random
import pandas as pd
from flask import render_template, request, redirect, url_for, session
from app import app, helper

app.secret_key = '123'
MAX_ATTEMPTS = 5

def load_data():
    """Load data from Excel file and return list of names and DataFrame."""
    df = pd.read_excel(r'data/dead_db.xlsx', dtype={'deathyear': 'Int64'}) # reading
    return df["Name"].tolist(), df

my_list, data_frame = load_data()


@app.route('/reset')
def reset():
    """Route to reset the game session and redirects to the index page"""
    clear_imgs()
    session.clear()
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    """Route for the main game page handling GET and POST requests."""
    if 'guess_attempts' not in session or 'target_info' not in session:
        initialize_game()

    feedback = ''  # Ensure feedback is always initialized to an empty string
    if request.method == 'POST':
        guess_name = request.form.get('guess')
        if guess_name:
            attempts = session.get('guess_attempts', 0)
            target = session.get('target_info', {})
            process_feedback = process_guess(guess_name)  # Capture the feedback from guessing
            if process_feedback:
                feedback = process_feedback  # Ensure we only assign non-None feedback
            if attempts >= MAX_ATTEMPTS - 1:
                session['reveal'] = True
                print("Reveal set to True")
                wiki_url = target.get('Link', '')
                image_filename = wiki_url.split('/')[-1] + '.jpg' if wiki_url else 'default.jpg'
                image_path = os.path.join(app.root_path, 'static', 'img', 'wiki_img', image_filename)
                if not os.path.exists(image_path) and wiki_url:
                    helper.download_image(wiki_url)
                session['image_filename'] = image_filename
                print("Image filename in session:", session['image_filename'])
                feedback += " The historical figure was: " + target.get('Name', 'Unknown')


    return render_template('index.html',
                           feedback=feedback,
                           my_list=my_list,
                           guess_history=session.get('guess_history', []),
                           image_filename=session.get('image_filename', ''),
                           MAX_ATTEMPTS=MAX_ATTEMPTS)


def initialize_game():
    """Initializes the game with random choice"""
    session['guess_attempts'] = 0
    session['guess_history'] = []
    r = random.randint(0, len(data_frame) - 1) # choosing random number from the list
    dict_data_frame = data_frame.iloc[r].to_dict()
    for k, v in dict_data_frame.items():
        if k=='countryName' or k=='continentName' or k=='occupation' :
            dict_data_frame.update({k:v.lower()})
    session['target_info'] = dict_data_frame

def process_guess(guess_name):
    """Processes a single guess and handling the attempts"""
    guessed_row = data_frame[data_frame['Name'].str.upper() == guess_name.upper()]
    if guessed_row.empty:
        return 'Name not in list. Try again'

    session['guess_attempts'] += 1
    guessed_row = guessed_row.iloc[0].to_dict()
    feedback = generate_feedback(guessed_row)
    session['guess_history'].append(feedback)
    session.modified = True

    if session['guess_attempts'] >= MAX_ATTEMPTS:
        return 'Max attempts. Reset to start again '

def get_death_feedback(guessed_row):
    """Gets the correct death year img output"""
    guessed_death = int(guessed_row['deathyear'])
    chosen_death = int(session['target_info']['deathyear'])
    diff = guessed_death - chosen_death
    if diff == 0:
        icon_image = None
        death_feedback = f"✅ Correct: {guessed_death}"
    elif abs(diff) <= 100:
        icon = 'green' if diff < 0 else 'red'
        icon_image = helper.icon_img_feedback(icon=f'still_alive_{icon}' if diff < 0 else f'already_dead_{icon}', directory='deaths')
        death_feedback = guessed_death
    elif abs(diff) <= 500:
        icon = 'yellow' if diff < 0 else 'red'
        icon_image = helper.icon_img_feedback(icon=f'still_alive_{icon}' if diff < 0 else f'already_dead_{icon}', directory='deaths')
        death_feedback = guessed_death
    else:
        icon = 'red'
        icon_image = helper.icon_img_feedback(icon=f'still_alive_{icon}' if diff < 0 else f'already_dead_{icon}', directory='deaths')
        death_feedback = guessed_death
    return death_feedback, icon_image


def get_country_img(guessed_row):
    """Gets the correct country img output"""
    guessed_country = guessed_row['countryName'].lower()
    chosen_country = session['target_info']['countryName']
    print(guessed_country, chosen_country)
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
        feedback[key] = get_feedback(guessed_row, attr, directory, *args) if key != 'country_feedback' else get_country_img(guessed_row)

    feedback.update({
        'name': guessed_row['Name'],
        'death_feedback': get_death_feedback(guessed_row)[0],
        'death_img': get_death_feedback(guessed_row)[1]
    })
    return feedback


def get_feedback(guessed_row, attribute, icon_dir, create_text=False):
    """Gets the feedback for a specific attribute."""
    # Check if the attribute value is a string before calling lower()
    print("getting feedback")
    guessed_value = guessed_row[attribute]
    if isinstance(guessed_value, str):
        guessed_value = guessed_value.lower()

    chosen_value = session['target_info'][attribute]
    if isinstance(chosen_value, str):
        chosen_value = chosen_value.lower()

    color = 'green' if guessed_value == chosen_value else 'red'
    icon = f'{guessed_value}_{color}' if isinstance(guessed_value, str) else f'{guessed_value}'
    icon_path = os.path.join('app', 'static', 'img', 'icons', icon_dir, f'{icon}.png')
    print(f"icon:, {icon} - icon_path:, {icon_path} - icon_dir:, {icon_dir} - os: {os.path.exists}")

    if create_text and not os.path.exists(icon_path):
        helper.create_text_image(str(guessed_value), color, directory=icon_path)
    return helper.icon_img_feedback(icon, directory=icon_dir)

def clear_imgs():
    """Clears images from directories."""
    helper.clear_dir("wiki_img")
    helper.clear_dir("icons/globe")
    helper.clear_dir("icons/occupations")
    helper.clear_dir("icons/continents")

if __name__ == "__main__":
    app.run(debug=True)