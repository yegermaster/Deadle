import random

import pandas as pd

r = random.randint(0, 11339)

df = pd.read_csv("Nodes.csv", delimiter=';', error_bad_lines=False)
new_db = pd.DataFrame(columns=[
    'Id', 'Name', 'Link', 'birthcity', 'countryName', 'longitude',
    'latitude', 'continentName', 'birthyear', 'deathyear', 'agespan',
    'gender', 'occupation', 'industry', 'domain'])

new_db["Id"] = df["Id"]
new_db["Name"] = df["Name"]
new_db["Link"] = df["Link"]
new_db["birthcity"] = df["birthcity"]
new_db["countryName"] = df["countryName"]
new_db["longitude"] = df["longitude"]
new_db["latitude"] = df["latitude"]
new_db["continentName"] = df["continentName"]
new_db["birthyear"] = df["birthyear"]
new_db["deathyear"] = df["deathyear"]
new_db["agespan"] = df["agespan"]
new_db["gender"] = df["gender"]
new_db["occupation"] = df["occupation"]
new_db["industry"] = df["industry"]
new_db["domain"] = df["domain"]




if __name__ == "__main__":
    # new_db.to_excel('new.xlsx', sheet_name='new')
    # Adjust for case sensitivity and whitespace
    lebron_row = new_db.loc[new_db['Name'].str.strip().str.lower() == 'lebron james'.lower()]
    print(lebron_row)


