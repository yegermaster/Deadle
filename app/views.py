from flask import render_template, request, redirect, url_for, session
import pandas as pd
import random
from app import app


app.secret_key = '123'

df = pd.read_excel('data/dead_db.xlsx')
my_list = df["Name"].tolist()


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'guess_attempts' not in session:
        session['guess_attempts'] = 0
        session['guess_history'] = []
        r = random.randint(0, len(df) - 1)
        session['target_info'] = df.iloc[r].to_dict()

    feedback = ''
    if request.method == 'POST' and session['guess_attempts'] < 5:
        guess_name = request.form.get('guess')
        guessed_row = df[df['Name'].str.upper() == guess_name.upper()]

        if not guessed_row.empty:
            guessed_row = guessed_row.iloc[0].to_dict()
            gender_feedback = "✅" if guessed_row['gender'] == session['target_info']['gender'] else "❌"
            city_feedback = "✅" if guessed_row['birthcity'] == session['target_info']['birthcity'] else "❌"
            country_feedback = "✅" if guessed_row['countryName'] == session['target_info']['countryName'] else "❌"
            continent_feedback = "✅" if guessed_row['continentName'] == session['target_info']['continentName'] else "❌"
            domain_feedback = "✅" if guessed_row['domain'] == session['target_info']['domain'] else "❌"
            death_feedback = "✅" if guessed_row['deathyear'] == session['target_info']['deathyear'] else "❌"
            birth_feedback = "✅" if guessed_row['birthyear'] == session['target_info']['birthyear'] else "❌"



            session['guess_history'].append(
                {'name': guess_name,
                 'gender_feedback': gender_feedback,
                 'city_feedback': city_feedback,
                 'country_feedback': country_feedback,
                 'continent_feedback': continent_feedback,
                 'domain_feedback': domain_feedback,
                 'death_feedback': death_feedback,
                 'birth_feedback': birth_feedback
                 })

            session['guess_attempts'] +=1
            # more categories here
        else:
            feedback = "Game over"

        if session['guess_attempts'] >= 5:
            feedback = 'reset'

        session.modified = True

    return render_template('index.html', feedback=feedback, my_list=my_list, guess_history=session['guess_history'])

@app.route('/reset', methods=['GET'])
def reset():
    # Reset game state
    session.pop('guess_attempts', None)
    session.pop('guess_history', None)
    session.pop('target_info', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)