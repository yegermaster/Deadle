from flask import render_template, request, redirect, url_for, session
import pandas as pd
import random
from app import app

#app = Flask(__name__)
#app.secret_key = 'http://127.0.0.1:5000'

# Load the data
df = pd.read_excel('data/dead_db.xlsx')
my_list = df["Name"].tolist()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'target_word' not in session:
        session['target_word'] = random.choice(my_list)
    target_word = session['target_word']

    feedback = None
    if request.method == 'POST':
        guess = request.form.get('guess')
        if guess in my_list:
            feedback = "Correct! Or add more feedback here."
            session.pop('target_word', None)
    return render_template('index.html', feedback=feedback)

def process_guess(guess, target_word):
    if guess.upper() == target_word.upper():
        return "Correct!"
    else:
        return "Try again"

if __name__ == "__main__":
    app.run(debug=True)