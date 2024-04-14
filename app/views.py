from flask import render_template, request, redirect, url_for, session
import pandas as pd
import random
from app import app, helper
import os

app.secret_key = '123'

df = pd.read_excel('data/dead_db.xlsx', dtype={'deathyear': 'Int64'}) # reading
my_list = df["Name"].tolist() # getting the Names for the player the cose from

@app.route('/reset')
def reset():
    """Route to reset the game session and redirects to the index page"""
    #TODO: mabye delete all images
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
        if attempts < 4: #TODO: hardcode this 4
            feedback = process_guess(guess_name)
        if attempts == 4:
            session['reveal'] = True
            print("Reveal set to True")
            # deal with image
            wiki_url = target['Link']
            image_filename =  wiki_url.split('/')[-1] + '.jpg'
            image_path = os.path.join('app', 'static', 'img','wiki_img', image_filename)
            if not os.path.exists(image_path):
                helper.download_image(wiki_url)
            session['image_filename'] = image_filename
            print("Image filename in session:", session['image_filename'])
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

#TODO: get rid of double code (there is ALOT(!) of similar functions in this code
def get_occupation_feedback(guessed_row):
    """Gets the correct occupation img output"""
    guessed_occupation = guessed_row['occupation'].lower()
    chosen_occupation = session['target_info']['occupation'].lower()
    color = 'green' if guessed_occupation == chosen_occupation else 'red'
    icon = f'{guessed_occupation}_{color}'
    icon_path = os.path.join('app', 'static', 'img','icons', 'occupations', icon)
    if not os.path.exists(icon_path):
        helper.create_text_image(guessed_occupation.lower(), color, directory='app/static/img/icons/occupations/')
    return helper.icon_img_feedback(icon, directory='occupations')

def get_continent_feedback(guessed_row):
    """Gets the correct continent img output"""
    guessed_con = guessed_row['continentName'].lower()
    chosen_con = session['target_info']['continentName'].lower()
    color = 'green' if guessed_con == chosen_con else 'red'
    icon = f'{guessed_con}_{color}'
    icon_path = os.path.join('app', 'static', 'img','icons', 'occupations', icon)
    if not os.path.exists(icon_path):
        helper.create_text_image(guessed_con.lower(), color, directory='app/static/img/icons/continents/')
    return helper.icon_img_feedback(icon, directory='continents')

def get_gender_feedback(guessed_row):
    """Gets the correct gender img output"""
    guessed_gender = guessed_row['gender']
    chosen_gender = session['target_info']['gender']
    color = 'green' if guessed_gender == chosen_gender else 'red'
    icon = f'{guessed_gender.lower()}_{color}'
    return helper.icon_img_feedback(icon, directory='genders')

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
    """Generate feedback from the database compared to the guess"""
    guess_name = guessed_row['Name']
    city_name = guessed_row['birthcity']
    direction_image = get_direction_feedback(guessed_row)
    gender_feedback = get_gender_feedback(guessed_row)
    continent_feedback =get_continent_feedback(guessed_row)
    occupation_feedback = get_occupation_feedback(guessed_row)
    death_feedback, death_img = get_death_feedback(guessed_row)
    country_feedback = get_country_img(guessed_row)

    feedback = {
        'name': guess_name,
        'gender_feedback': gender_feedback,
        'city_name': city_name.lower(),
        'direction_image': direction_image,
        'country_feedback': country_feedback.lower(),
        'continent_feedback': continent_feedback.lower(),
        'occupation_feedback': occupation_feedback,
        'death_feedback': death_feedback,
        'death_img' : death_img
         }
    return feedback


if __name__ == "__main__":
    app.run(debug=True)
