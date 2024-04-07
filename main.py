import random

import pandas as pd

import constants as c


def handle_age(guess, target):
    if guess - target < 0:
        pirnt("older")
    else:
        print("younger")

def handle_guess(target_name, guess):
    guess_row = db.loc[db['Name'].str.strip().str.lower() == guess]
    hanlde_age(float(guess_row['birthyear'].iloc[0]), target_birth_year)
    handle_occupation()
    handle_continent()
    handle_gender()
    handle_countery()

def guesser():
    db = pd.read_excel('new.xlsx')
    r = random.randint(0, len(db) - 1)
    print(db["Name"][r], r)
    target_name = db.loc[r, "Name"].strip().lower()
    target_birth_year = float(db.loc[r, "birthyear"])
    target_birth_year = float(db.loc[r, "birthyear"])
    target_birth_year = float(db.loc[r, "birthyear"])
    target_birth_year = float(db.loc[r, "birthyear"])
    target_birth_year = float(db.loc[r, "birthyear"])


    print(f'Target: {target_name}, {r}, {target_birth_year}')

    tries = 5
    while tries > 0:
        guess = input("guess here: ").strip().lower()

        if target_name == guess:
            print("done")
            break

        else:
            guess_row = db.loc[db['Name'].str.strip().str.lower() == guess]
            if not guess_row.empty:
                handle_guess(target_name, guess)
                hanlde_age(float(guess_row['birthyear'].iloc[0]), target_birth_year)
            else:
                print('no found')
        tries -=1



if __name__ == "__main__":
    guesser()