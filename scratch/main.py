import random
import pandas as pd


def handle_age(target_row, guess_row):
    target_birth_year = target_row['birthyear'].iloc[0]
    target_death_year = target_row['deathyear'].iloc[0]
    guess_birth_year = guess_row['birthyear'].iloc[0]
    guess_death_year = guess_row['deathyear'].iloc[0]
    if target_birth_year - guess_birth_year < 0:
        print('younger')
    else:
        print('older')
    if target_death_year - guess_death_year < 0:
        print('died before')
    else:
        print('died after')

def handle_place(target_row, guess_row):
    target_city = target_row['birthcity'].iloc[0]
    target_continent = target_row['continentName'].iloc[0]
    target_country = target_row['countryName'].iloc[0]
    guess_city = guess_row['birthcity'].iloc[0]
    guess_continent = guess_row['continentName'].iloc[0]
    guess_country = guess_row['countryName'].iloc[0]

    if guess_continent == target_continent:
        print('correct continent')
    if guess_country == target_country:
        print('correct country')
    if guess_city == target_city:
        print('correct city')

def handle_person(target_row, guess_row):
    target_gender = target_row["gender"].iloc[0]
    target_domain = target_row["domain"].iloc[0]
    guess_gender = guess_row["gender"].iloc[0]
    guess_domain = guess_row["domain"].iloc[0]

    if target_gender == guess_gender:
        print(target_gender)
    if target_domain == guess_domain:
        print("domain")


def handle_guess(target_row, guess_row):
    handle_age(target_row, guess_row)
    handle_place(target_row, guess_row)
    handle_person(target_row, guess_row)

def guesser():
    db = pd.read_excel('dead_db.xlsx')
    r = random.randint(0, len(db) - 1)
    print(db["Name"][r], r)
    target_name = db.loc[r, "Name"]
    target_row = db.loc[db["Name"] == target_name]

    tries = 5
    while tries > 0:
        guess = input("guess here: ")

        if target_name == guess:
            print("done")
            break
        else:
            guess_row = db.loc[db["Name"] == guess]
            handle_guess(target_row, guess_row)
        tries -=1



if __name__ == "__main__":
    guesser()