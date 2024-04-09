import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

r = random.randint(0, 11339)

df = pd.read_csv("Nodes.csv", delimiter=';', on_bad_lines='skip')
df.drop_duplicates(subset=["Name"], inplace=True)
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
temp_db["longitude"] = df["longitude"]
temp_db["latitude"] = df["latitude"]



if __name__ == "__main__":
    alive_db = temp_db.loc[temp_db['deathyear'] == 2018]
    dead_db = temp_db[~temp_db.index.isin(alive_db.index)]
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

    print(f'Unique countries: {unique_countries}')
    print(f'Unique continents: {unique_continents}')
    print(f'Unique cities: {unique_cities}')
    print(f'Unique occupation: {unique_occupation}')
    print(f'Unique industry: {unique_industry}')
    print(f'Unique domain: {unique_domain}')
    print(f'Alive in 2018: {len(alive_db)}')
    print(f'Dead (all other years): {len(dead_db)}')
    print(f'Oldest birth year: {oldest_birth_year}, Name: {oldest_birth_name}')
    print(f'Newest birth year: {newest_birth_year}, Name: {newest_birth_name}')
    print(f'Oldest death year: {oldest_death_year}, Name: {oldest_death_name}')
    print(f'Newest death year: {newest_death_year}, Name: {newest_death_name}')
    print("Unique Occupations:", df['occupation'].unique())
    print("Unique Industries:", df['industry'].unique())
    print("Unique Domains:", df['domain'].unique())


    occupation_industry_crosstab = pd.crosstab(df['occupation'], df['industry'])
    occupation_domain_crosstab = pd.crosstab(df['occupation'], df['domain'])
    indusrt_domain_crosstab = pd.crosstab(df['domain'], df['industry'])

    plt.figure(figsize=(20, 15))
    sns.heatmap(occupation_industry_crosstab, annot=True, cmap="YlGnBu", fmt="d")
    plt.title('Occupation vs Industry Distribution')
    plt.ylabel('Occupation')
    plt.xlabel('Industry')
    plt.show()

    plt.figure(figsize=(20, 15))
    sns.heatmap(occupation_domain_crosstab, annot=True, cmap="YlGnBu", fmt="d")
    plt.title('Occupation vs Domain Distribution')
    plt.ylabel('Occupation')
    plt.xlabel('Industry')
    plt.show()

    plt.figure(figsize=(20, 15))
    sns.heatmap(indusrt_domain_crosstab, annot=True, cmap="YlGnBu", fmt="d")
    plt.title('Domain vs Industry Distribution')
    plt.ylabel('Occupation')
    plt.xlabel('Industry')
    plt.show()

