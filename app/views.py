from flask import render_template, request, redirect, url_for, session
import pandas as pd
import random
from app import app, helper
import os

app.secret_key = '123'

df = pd.read_excel('data/dead_db.xlsx', dtype={'deathyear': 'Int64'})
my_list = df["Name"].tolist()

@app.route('/reset')
def reset():
    """Route to reset the game session and redirects to the index page"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route.
    Initializes the game and Sends feedback and renders the page.
    """
    if 'guess_attempts' not in session or 'target_info' not in session:
        initialize_game()

    feedback = ''
    if request.method == 'POST': # when the player makes a guess
        guess_name = request.form.get('guess')
        attempts = session.get('guess_attempts', 0)
        target = session.get('target_info', {})
        if attempts < 5:
            feedback = process_guess(guess_name)
        if attempts == 5:
            session['reveal'] = True
            # deal with image
            wiki_url = target['Link']
            image_filename =  wiki_url.split('/')[-1] + '.jpg'
            image_path = os.path.join('app', 'static', 'img', image_filename)
            if not os.path.exists(image_path):
                helper.download_image(wiki_url)
            session['image_filename'] = image_filename
            feedback += " The historical figure was: " + target['Name']
    # sends the information to the html file (frontend)
    return render_template('index.html',
                           feedback=feedback,
                           my_list=my_list,
                           guess_history=session.get('guess_history', []),
                           image_filename = session.get('image_filename', '')
                           )

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

def death_feedback(guessed_row):
    """Generates feedback for death year and the correct image"""
    guessed_death = int(guessed_row['deathyear'])
    chosen_death = int(session['target_info']['deathyear'])


    if guessed_death == chosen_death: # correct
        death_feedback = f"✅ Correct: {guessed_death}"
        icon_image = None
    elif chosen_death > guessed_death >= chosen_death - 100: # guess is under by 100-
        icon_image = death_img_feedback(icon='still_alive_green')
        death_feedback = guessed_death
    elif chosen_death > guessed_death >= chosen_death - 500: # guess is under by 100-500
        icon_image = death_img_feedback(icon='still_alive_yellow')
        death_feedback = guessed_death
    elif chosen_death > guessed_death < chosen_death -500: # guess is under by 500+
        icon_image = death_img_feedback(icon='still_alive_red')
        death_feedback = guessed_death
    elif chosen_death < guessed_death <= chosen_death + 100: # guess is over by 100-
        icon_image = death_img_feedback(icon='already_dead_green')
        death_feedback = guessed_death
    elif chosen_death < guessed_death <= chosen_death + 500: # guess is over by 100-500
        icon_image = death_img_feedback(icon='already_dead_yellow')
        death_feedback = guessed_death
    elif chosen_death < guessed_death >= chosen_death + 500: # guess is over by 500+
        icon_image = death_img_feedback(icon='already_dead_red')
        death_feedback = guessed_death
    else:
        death_feedback = 'no death feedback'
        icon_image = None

    return death_feedback, icon_image


def direction_feedback(guessed_row):
    to_coord= (float(guessed_row['longitude']), float(guessed_row['latitude']))
    from_coord = (float(session['target_info']['longitude']), float( session['target_info']['latitude']))
    direction = helper.get_direction(from_coord, to_coord)
    icon_filename = direction + '.png'
    icon_path = url_for('static', filename=f'img/icons/{icon_filename}')
    direction_image = f"<img src='{icon_path}' alt='{direction}'>"
    return direction_image

def death_img_feedback(icon):
    icon_filename = icon + '.png'
    icon_path = url_for('static', filename=f'img/icons/{icon_filename}')
    icon_image = f"<img src='{icon_path}' alt='{icon}'>"
    return icon_image


def generate_feedback(guessed_row):
    """Generate feedback from the database compared to the guess"""
    guess_name = guessed_row['Name']
    city_name = guessed_row['birthcity']
    direction_image = direction_feedback(guessed_row)
    gender_feedback = f"✅ {guessed_row['gender']}" if guessed_row['gender'] == session['target_info']['gender'] else f"❌ {guessed_row['gender']}"
    country_feedback = f"✅ {guessed_row['countryName']}" if guessed_row['countryName'] == session['target_info']['countryName'] else f"❌{guessed_row['countryName']}"
    continent_feedback = f"✅{guessed_row['continentName']}" if guessed_row['continentName'] == session['target_info']['continentName'] else f"❌{guessed_row['continentName']}"
    occupation_feedback = f"✅ {guessed_row['occupation']}" if guessed_row['occupation'] == session['target_info']['occupation'] else f"❌{ guessed_row['occupation']}"

    death_feedback_result, death_img = death_feedback(guessed_row)

    feedback = {
        'name': guess_name,
        'gender_feedback': gender_feedback,
        'city_name': city_name.lower(),
        'direction_image': direction_image,
        'country_feedback': country_feedback.lower(),
        'continent_feedback': continent_feedback.lower(),
        'occupation_feedback': occupation_feedback.lower(),
        'death_feedback': death_feedback_result,
        'death_img' : death_img
         }

    return feedback


if __name__ == "__main__":
    app.run(debug=True)
