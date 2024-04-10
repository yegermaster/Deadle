import random
import pandas as pd
from app import helper

df = pd.read_csv("Nodes.csv", delimiter=';', on_bad_lines='skip')
df.drop_duplicates(subset=["Name"], inplace=True)
temp_db = pd.DataFrame(columns=[
    'Id', 'Name', 'Link', 'birthcity', 'countryName', 'longitude',
    'latitude', 'continentName', 'birthyear', 'deathyear', 'agespan',
    'gender', 'occupation', 'industry', 'domain'])

def fill_lat_lon(df):
    for index, row in df.iterrows():
        if pd.isna(row['latitude']) or pd.isna(row['longitude']) or row['latitude'] == "" or row['longitude'] == "":
            cords = helper.get_cords(row['birthcity'])
            if cords is not None:
                lat, lon = cords
                df.at[index, 'latitude'] = lat
                df.at[index, 'longitude'] = lon
            else:
                print(f"no coords found for {row['birthcity']}")

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
temp_db["longitude"] = df["longitude"]
temp_db["latitude"] = df["latitude"]

if __name__ == "__main__":
    alive_db = temp_db.loc[temp_db['deathyear'] == 2018]
    dead_db = temp_db[~temp_db.index.isin(alive_db.index)]
    df = dead_db



    dead_db.to_excel('dead_db.xlsx')

    unique_countries = df['countryName'].nunique()
    unique_continents = df['continentName'].nunique()
    unique_cities = df['birthcity'].nunique()

    unique_occupation = df['occupation'].nunique()
    unique_industry = df['industry'].nunique()
    unique_domain = df['domain'].nunique()

    oldest_birth_year = dead_db['birthyear'].min()
    newest_birth_year = dead_db['birthyear'].max()
    oldest_death_year = dead_db['deathyear'].min()
    newest_death_year = dead_db['deathyear'].max()

    oldest_birth_name = dead_db[dead_db['birthyear'] == oldest_birth_year]['Name'].iloc[0]
    newest_birth_name = dead_db[dead_db['birthyear'] == newest_birth_year]['Name'].iloc[0]
    oldest_death_name = dead_db[dead_db['deathyear'] == oldest_death_year]['Name'].iloc[0]
    newest_death_name = dead_db[dead_db['deathyear'] == newest_death_year]['Name'].iloc[0]

    print(
        f'Countries: {unique_countries}\nContinents: {unique_continents}\nCities: {unique_cities}\n'
        f'Occupation: {unique_occupation}\nIndustry: {unique_industry}\n Domain: {unique_domain},'
        f'Alive in 2018: {len(alive_db)}\nDead total: {len(dead_db)}\nOldest birth year: {oldest_birth_year}, Name: {oldest_birth_name}\n'
        f'Newest birth year: {newest_birth_year}, Name: {newest_birth_name}\nOldest death year: {oldest_death_year}, Name: {oldest_death_name}\n'
        f'Newest death year: {newest_death_year}, Name: {newest_death_name}\n All occupations: {df["occupation"].unique()}\n'
        f'All ndustries: {df["industry"].unique()}\nAll Domains: {df["domain"].unique()}')


