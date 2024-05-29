"""
Module for processing and analyzing data from a CSV file containing historical figures.
Loads data, processes it, and exports results to an Excel file.
"""


import os
import sys
import pandas as pd
from application import helper


# Set up base directory for handling paths
BASE_DIR = 'c:/Users/Owner/לימודים/למידה עצמית/תכנות/פייתון/deadle'
sys.path.append(BASE_DIR)


# Paths to files
nodes_csv_path = os.path.join(BASE_DIR, 'data', 'Nodes.csv')
dead_db_path = os.path.join(BASE_DIR, 'data', 'dead_db.xlsx')

# Load and process CSV file
df = pd.read_csv(nodes_csv_path, delimiter=';', on_bad_lines='skip')
df.drop_duplicates(subset=["Name"], inplace=True)

# DataFrame setup
temp_db = df[['Name', 'Link', 'birthcity', 'countryName', 'longitude',
              'latitude', 'continentName', 'birthyear', 'deathyear', 'agespan',
              'gender', 'occupation', 'industry', 'domain']].copy()


def fill_lat_lon(data_frame):
    """Fill missing latitude and longitude using helper function."""
    for index, row in data_frame.iterrows():
        if pd.isna(row['latitude']) or pd.isna(row['longitude']) or row['latitude'] == "" or row['longitude'] == "":
            cords = helper.get_cords(row['birthcity'])
            if cords is not None:
                lat, lon = cords
                data_frame.at[index, 'latitude'] = lat
                data_frame.at[index, 'longitude'] = lon
            else:
                print(f"no cords found for {row['birthcity']}")


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
    data_frame = dead_db

    dead_db.reset_index(drop=True, inplace=True)

    dead_db.to_excel('data/dead_db.xlsx', index=False)

    unique_countries = data_frame['countryName'].nunique()
    unique_continents = data_frame['continentName'].nunique()
    unique_cities = data_frame['birthcity'].nunique()

    unique_occupation = data_frame['occupation'].nunique()
    unique_industry = data_frame['industry'].nunique()
    unique_domain = data_frame['domain'].nunique()

    oldest_birth_year = dead_db['birthyear'].min()
    newest_birth_year = dead_db['birthyear'].max()
    oldest_death_year = dead_db['deathyear'].min()
    newest_death_year = dead_db['deathyear'].max()

    oldest_birth_name = dead_db[dead_db['birthyear']
                                == oldest_birth_year]['Name'].iloc[0]
    newest_birth_name = dead_db[dead_db['birthyear']
                                == newest_birth_year]['Name'].iloc[0]
    oldest_death_name = dead_db[dead_db['deathyear']
                                == oldest_death_year]['Name'].iloc[0]
    newest_death_name = dead_db[dead_db['deathyear']
                                == newest_death_year]['Name'].iloc[0]

    # Count the number of missing values in the 'birthcity' column
    missing_city_names = dead_db['birthcity'].isna().sum()

    print(f"Number of entries with no birthcity: {missing_city_names}")

    names_with_missing_city = dead_db[dead_db['birthcity'].isna()]['Name']

    print("Names with missing birthcity:")
    print(names_with_missing_city)
    print(
        f'Countries: {unique_countries}\nContinents: {unique_continents}\nCities: {unique_cities}\n'
        f'Occupation: {unique_occupation}\nIndustry: {unique_industry}\n Domain: {unique_domain},'
        f'\nAlive in 2018: {len(alive_db)}\nDead total: {len(dead_db)}\nOldest birth year: {oldest_birth_year}, '
        f'Name: {oldest_birth_name}\nNewest birth year: {newest_birth_year}, Name: {newest_birth_name}\n'
        f'Oldest death year: {oldest_death_year}, Name: {oldest_death_name}\nNewest death year: {newest_death_year}, '
        f'Name: {newest_death_name}\nAll occupations: {data_frame["occupation"].unique()}\n'
        f'All industries: {data_frame["industry"].unique()}\nAll Domains: {data_frame["domain"].unique()}')
