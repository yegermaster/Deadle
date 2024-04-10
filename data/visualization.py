import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


df = pd.read_excel('dead_db.xlsx')


def plot_cross_section(occupation_industry=False, occupation_domain=False, industry_domain = False ):
    occupation_industry_cross = pd.crosstab(df['occupation'], df['industry'])
    occupation_domain_cross = pd.crosstab(df['occupation'], df['domain'])
    industry_domain_cross = pd.crosstab(df['domain'], df['industry'])
    plt.figure(figsize=(20, 15))

    if occupation_industry:
        sns.heatmap(occupation_industry_cross, annot=True, cmap="YlGnBu", fmt="d")
        plt.title('Occupation vs Industry Distribution')
        plt.ylabel('Occupation')
        plt.xlabel('Industry')
        plt.show()
    elif occupation_domain:
            sns.heatmap(occupation_domain_cross, annot=True, cmap="YlGnBu", fmt="d")
            plt.title('Occupation vs Domain Distribution')
            plt.ylabel('Occupation')
            plt.xlabel('Industry')
            plt.show()
    elif industry_domain:
        plt.figure(figsize=(20, 15))
        sns.heatmap(industry_domain_cross, annot=True, cmap="YlGnBu", fmt="d")
        plt.title('Domain vs Industry Distribution')
        plt.ylabel('Occupation')
        plt.xlabel('Industry')
        plt.show()

def plot_continent_count():
    continent_count = df['continentName'].value_counts()

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    continent_count.plot(kind='bar')
    plt.title('Count of Entries per Continent')
    plt.xlabel('Continent')
    plt.ylabel('Count')
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(np.arange(0, max(continent_count) + 1, 500), fontsize=15)
    plt.tight_layout()

    dir_path = '../../deadle/app/static/img/visualization'
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, 'continent_count_bar_chart.png')

    plt.savefig(file_path)
    plt.show()

def plot_country_count():
    country_count = df['countryName'].value_counts()
    country_count = country_count[country_count >= 30]

    plt.figure(figsize=(10, 6))
    country_count.plot(kind='bar')
    plt.title('Count of Entries per country with 30 + appearances')
    plt.xlabel('Country')
    plt.ylabel('Count')
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(np.arange(0, max(country_count) + 1, 50))
    plt.tight_layout()

    dir_path = '../../deadle/app/static/img/visualization'
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, 'country_count_bar_chart.png')


    plt.savefig(file_path)
    plt.show()

def plot_city_count():
    city_count = df['birthcity'].value_counts()
    city_count = city_count[city_count >= 10]

    plt.figure(figsize=(10, 6))
    city_count.plot(kind='bar')
    plt.title('Count of Entries per city')
    plt.xlabel('City')
    plt.ylabel('Count')
    plt.xticks(rotation=90, fontsize=6)
    plt.yticks(np.arange(0, max(city_count) + 1, 20))
    plt.tight_layout()

    dir_path = '../../deadle/app/static/img/visualization'
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, 'city_count_bar_chart.png')

    plt.savefig(file_path)
    plt.show()

def plot_domain_count():
    domain_count = df['domain'].value_counts()
    plt.figure(figsize=(10, 6))
    domain_count.plot(kind='bar')
    plt.title('Count of Entries per domain')
    plt.xlabel('Domain')
    plt.ylabel('Count')
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(np.arange(0, max(domain_count) + 1, 200))
    plt.tight_layout()

    dir_path = '../../deadle/app/static/img/visualization'
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, 'domain_count_bar_chart.png')


    plt.savefig(file_path)
    plt.show()

def plot_industry_count():
    industry_count = df['industry'].value_counts()
    plt.figure(figsize=(10, 6))
    industry_count.plot(kind='bar')
    plt.title('Count of Entries per industry')
    plt.xlabel('Industry')
    plt.ylabel('Count')
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(np.arange(0, max(industry_count) + 1, 200))
    plt.tight_layout()

    dir_path = '../../deadle/app/static/img/visualization'
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, 'industry_count_bar_chart.png')

    plt.savefig(file_path)
    plt.show()

def plot_occupation_count():
    occupation_count = df['occupation'].value_counts()
    occupation_count = occupation_count[occupation_count >= 20]


    plt.figure(figsize=(10, 6))
    occupation_count.plot(kind='bar')
    plt.title('Count of Entries per occupation')
    plt.xlabel('Occupation')
    plt.ylabel('Count')
    plt.xticks(rotation=90, fontsize=12)
    plt.yticks(np.arange(0, max(occupation_count) + 1, 200))
    plt.tight_layout()

    dir_path = '../../deadle/app/static/img/visualization'
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, 'occupation_count_bar_chart.png')

    plt.savefig(file_path)
    plt.show()

if __name__ == "__main__":

    plot_country_count()
    plot_continent_count()
    plot_domain_count()
    plot_industry_count()
    plot_occupation_count()
    plot_city_count()