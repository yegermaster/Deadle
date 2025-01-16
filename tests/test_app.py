import requests
import os

def fetch_countries_data() -> list:
    url = "https://restcountries.com/v3.1/all?fields=name,flags"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []

def find_country_flag_url(countries: list, country_name: str) -> str:
    for country in countries:
        if country.get("name", {}).get("common", "").lower() == country_name.lower():
            return country.get("flags", {}).get("png", "")
    return ""

def download_flag(flag_url: str, country_name: str) -> str:
    if not flag_url:
        return "Flag URL not found."
    try:
        response = requests.get(flag_url, timeout=30)
        response.raise_for_status()  # Ensure the download is successful
        os.makedirs("flags", exist_ok=True)
        flag_filepath = f"flags/{country_name.replace(' ', '_')}.png"
        with open(flag_filepath, "wb") as file:
            file.write(response.content)
        return f"Flag saved at: {flag_filepath}"
    except requests.exceptions.RequestException as e:
        return f"Error downloading flag: {e}"

def get_country_flag(country_name: str) -> str:
    countries = fetch_countries_data()
    if not countries:
        return "Failed to fetch country data."
    flag_url = find_country_flag_url(countries, country_name)
    if not flag_url:
        return f"Country '{country_name}' not found."
    return download_flag(flag_url, country_name)

# Example usage
result = get_country_flag("FRANCE")
print(result)
