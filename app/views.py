from flask import render_template, request, redirect, url_for
import pandas as pd
import random
from app import app

# Load the data
df = pd.read_excel('data/dead_db.xlsx')
my_list = df["Name"].tolist()

@app.route('/', methods=['GET', 'POST']) #organized
def index():
    target_word = random.choice(my_list)
    feedback = ""
    if request.method == 'POST':
        guess = request.form.get('guess').upper()
        if guess in my_list:
            # Implement feedback logic here as in your guesser() function
            feedback = "Correct! Or add more feedback here."
        else:
            feedback = "Try again."
    return render_template('index.html', feedback=feedback)

# Add more functions as needed, converting your logic from Tkinter to Flask views
