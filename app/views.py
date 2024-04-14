from flask import render_template, request, redirect, url_for, session
import pandas as pd
import random
from app import app, helper
import os

app.secret_key = '123'
MAX_ATTEMPTS = 4

def load_data():

    df = pd.read_excel('data/dead_db.xlsx', dtype={'deathyear': 'Int64'}) # reading
    return df["Name"].tolist(), df

my_list, df = load_data()
@app.route('/reset')
def reset():
    """Route to reset the game session and redirects to the index page"""
    #TODO: maybe delete all images
    session.clear()
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
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
                image_path = os.path.join('app', 'static', 'img', 'wiki_img', image_filename)
                if not os.path.exists(image_path) and wiki_url:
                    helper.download_image(wiki_url)
                session['image_filename'] = image_filename
                print("Image filename in session:", session['image_filename'])
                feedback += " The historical figure was: " + target.get('Name', 'Unknown')

    return render_template('index.html',
                           feedback=feedback,
                           my_list=my_list,
                           guess_history=session.get('guess_history', []),
                           image_filename=session.get('image_filename', ''))


def initialize_game():
    """Initializes the game with random choice"""
    session['guess_attempts'] = 0
    session['guess_history'] = []
    r = random.randint(0, len(df) - 1) # choosing random number from the list
    dict_df = df.iloc[r].to_dict()
    for k, v in dict_df.items():
        if k=='birthcity' or k=='countryName' or k=='continentName' or k=='occupation' :
            dict_df.update({k:v.lower()})
    session['target_info'] = dict_df


def process_guess(guess_name):
    """Processes a single guess and handling the attempts"""
    guessed_row = df[df['Name'].str.upper() == guess_name.upper()]
    if guessed_row.empty:
        return 'Name not in list. Try again'

    session['guess_attempts'] += 1
    guessed_row = guessed_row.iloc[0].to_dict()
    feedback = generate_feedback(guessed_row)
    session['guess_history'].append(feedback)
    session.modified = True

    if session['guess_attempts'] >= 5:
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


def get_direction_feedback(guessed_row):
    """Gets the correct direction year img output"""
    to_coord= (float(guessed_row['latitude']), float(guessed_row['longitude']))
    from_coord = (float(session['target_info']['latitude']), float( session['target_info']['longitude']))
    direction = helper.get_direction(from_coord, to_coord)
    direction_image = helper.icon_img_feedback(direction, 'directions')
    return direction_image

def get_country_img(guessed_row):
    """Gets the correct country img output"""
    guessed_country = guessed_row['countryName']
    chosen_country = session['target_info']['countryName']
    lat, lan = guessed_row['latitude'], guessed_row['longitude']
    color = 'green' if guessed_country == chosen_country else 'red'
    helper.plot_location_on_globe(lat, lan, guessed_country, color)
    country_img = helper.icon_img_feedback(guessed_country, 'globe')
    return country_img

def generate_feedback(guessed_row):
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
        'city_name': guessed_row['birthcity'].lower(),
        'direction_image': get_direction_feedback(guessed_row),
        'death_feedback': get_death_feedback(guessed_row)[0],
        'death_img': get_death_feedback(guessed_row)[1]
    })
    return feedback


def get_feedback(guessed_row, attribute, icon_dir, create_text=False):
    # Check if the attribute value is a string before calling lower()
    guessed_value = guessed_row[attribute]
    if isinstance(guessed_value, str):
        guessed_value = guessed_value.lower()

    chosen_value = session['target_info'][attribute]
    if isinstance(chosen_value, str):
        chosen_value = chosen_value.lower()

    color = 'green' if guessed_value == chosen_value else 'red'
    icon = f'{guessed_value}_{color}' if isinstance(guessed_value, str) else f'{guessed_value}'
    icon_path = os.path.join('app', 'static', 'img', 'icons', icon_dir, icon)

    if create_text and not os.path.exists(icon_path):
        helper.create_text_image(str(guessed_value), color, directory=f'app/static/img/icons/{icon_dir}/')
    return helper.icon_img_feedback(icon, directory=icon_dir)


if __name__ == "__main__":
    app.run(debug=True)
