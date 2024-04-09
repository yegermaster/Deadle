import random

import pandas as pd

r = random.randint(0, 11339)

df = pd.read_csv("Nodes.csv", delimiter=';', on_bad_lines='skip')
temp_db = pd.DataFrame(columns=[
    'Id', 'Name', 'Link', 'birthcity', 'countryName', 'longitude',
    'latitude', 'continentName', 'birthyear', 'deathyear', 'agespan',
    'gender', 'occupation', 'industry', 'domain'])

temp_db["Id"] = df["Id"]
temp_db["Name"] = df["Name"]
temp_db["Link"] = df["Link"]
temp_db["birthcity"] = df["birthcity"]
temp_db["countryName"] = df["countryName"]
temp_db["longitude"] = df["longitude"]
temp_db["latitude"] = df["latitude"]
temp_db["continentName"] = df["continentName"]
temp_db["birthyear"] = df["birthyear"]
temp_db["deathyear"] = df["deathyear"]
temp_db["agespan"] = df["agespan"]
temp_db["gender"] = df["gender"]
temp_db["occupation"] = df["occupation"]
temp_db["industry"] = df["industry"]
temp_db["domain"] = df["domain"]



if __name__ == "__main__":
    alive_db = temp_db.loc[temp_db['deathyear'] == 2018]
    #dead_db = temp_db[~temp_db.index.isin(alive_db.index)]
    #dead_db.to_excel('dead_db.xlsx')