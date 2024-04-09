from flask import render_template, request, redirect, url_for, session
import pandas as pd
import random
from app import app


app.secret_key = '123'

df = pd.read_excel('data/dead_db.xlsx', dtype={'deathyear': 'Int64'})
my_list = df["Name"].tolist()

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'guess_attempts' not in session or 'target_info' not in session:
        initialize_game()

    feedback = ''
    game_over = False
    if request.method == 'POST':
        guess_name = request.form.get('guess')
        if session['guess_attempts'] < 5:
            feedback = process_guess(guess_name)
        if session['guess_attempts'] == 5 or game_over:
            # When it's the last guess or the game is over, reveal the answer
            session['reveal'] = True
            feedback += " The historical figure was: " + session['target_info']['Name']
        elif session['guess_attempts'] > 5:
            # Should not happen, but just in case
            feedback = "Max attempts reached. Please reset to start again."

    return render_template('index.html', feedback=feedback, my_list=my_list, guess_history=session.get('guess_history', []))

def initialize_game():
    session['guess_attempts'] = 0
    session['guess_history'] = []
    r = random.randint(0, len(df) - 1)
    session['target_info'] = df.iloc[r].to_dict()


def process_guess(guess_name):
    if session['guess_attempts'] >=5:
        reveal_info = {
            'reveal': True,
            'target_name': session['target_info']['Name'],
            'target_gender': session['target_info']['gender'],
            'target_city': session['target_info']['birthcity'],
            'target_country': session['target_info']['countryName'],
            'target_continent': session['target_info']['continentName'],
            'target_death': int(session['target_info']['deathyear']),
            'target_domain': session['target_info']['domain']
        }
        session['reveal_info'] = reveal_info
        return 'Game over. please reset to start a new game'

    guessed_row = df[df['Name'].str.upper() == guess_name.upper()]
    if guessed_row.empty:
        return 'Name not in list. Try again'


    guessed_row = guessed_row.iloc[0].to_dict()
    session['guess_attempts'] += 1
    feedback = generate_feedback(guessed_row)
    session['guess_history'].append(feedback)
    session.modified = True

    if session['guess_attempts'] >= 5:
        return 'Max attempts reached. Reset to start again/'

def death_feedback(guessed_row):
    guessed_death = int(guessed_row['deathyear'])
    chosen_death = int(session['target_info']['deathyear'])

    if guessed_death == chosen_death:
        death_feedback = f"✅ Correct: {guessed_death}"
    elif guessed_death < chosen_death:
        death_feedback = f"⬆️ Earlier: {guessed_death}"
    else:
        death_feedback = f"⬇️ Later: {guessed_death}"

    return death_feedback


def generate_feedback(guessed_row):
    guess_name = guessed_row['Name']

    gender_feedback = f"✅ {guessed_row['gender']}" if guessed_row['gender'] == session['target_info']['gender'] else f"❌ {guessed_row['gender']}"


    city_feedback = f"✅ {guessed_row['birthcity']}" if guessed_row['birthcity'] == session['target_info']['birthcity'] else f"❌ {guessed_row['birthcity']}"
    country_feedback = f"✅ {guessed_row['countryName']}" if guessed_row['countryName'] == session['target_info']['countryName'] else f"❌{guessed_row['countryName']}"
    continent_feedback = f"✅{guessed_row['continentName']}" if guessed_row['continentName'] == session['target_info']['continentName'] else f"❌{guessed_row['continentName']}"

    domain_feedback = f"✅ {guessed_row['domain']}" if guessed_row['domain'] == session['target_info']['domain'] else f"❌{ guessed_row['domain']}"

    death_feedback_result = death_feedback(guessed_row)

    feedback =         {'name': guess_name,
         'gender_feedback': gender_feedback,
         'city_feedback': city_feedback,
         'country_feedback': country_feedback,
         'continent_feedback': continent_feedback,
         'domain_feedback': domain_feedback,
         'death_feedback': death_feedback_result,
         }

    return feedback


if __name__ == "__main__":
    app.run(debug=True)