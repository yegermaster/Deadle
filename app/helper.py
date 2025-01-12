"""
This module contains functions for handling image downloads, processing geographical data,
and generating images for the Deadle web game.
"""
import os
import sys
import requests
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from flask import url_for
import cartopy.crs as ccrs
from urllib.parse import quote

# Set up base directory for handling paths
BASE_DIR = 'c:/Users/Owner/לימודים/למידה עצמית/תכנות/פייתון/deadle'
sys.path.append(BASE_DIR)

from app import app

def resize_img(path: str, size: tuple) -> None:
    """Resizes an image and saves it."""    
    img = Image.open(path)
    new_img = img.resize(size)
    new_img.save(path)

def download_image(wiki_url, local_filename):
    """
    FInds the Wikipedia page, finds an image, and downloads that image 
    and saves it.
    """
    # URL-encode to handle special characters in Wikipedia links
    wiki_url_encoded = quote(wiki_url, safe=':/')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...'}
    try:
        response = requests.get(wiki_url_encoded, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {wiki_url_encoded}: {e}")
        return  # Don’t attempt to parse if the page is unavailable

    soup = BeautifulSoup(response.text, 'html.parser') # Converts HTML in response.text into a BeautifulSoup object for easy HTML parsing.
    infobox = soup.find('table', class_='infobox')
    image_tag = infobox.find('img') if infobox else soup.find('img')
    if not image_tag or not image_tag.get('src'):
        print("No image found in the page.")
        return

    image_src = image_tag['src']
    # Handle cases like "//upload.wikimedia.org/..." or "/wiki/..."
    if image_src.startswith('//'):
        image_url = 'https:' + image_src
    elif image_src.startswith('/'):
        image_url = 'https://www.wikipedia.org' + image_src
    else:
        image_url = image_src

    load_wiki_image(image_url, local_filename)

def load_wiki_image(image_url, local_filename):
    """
    Actually download the image to your 'wiki_img' folder,
    using the 'local_filename' you already decided on in process_guess().
    """
    image_url_encoded = quote(image_url, safe=':/')
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; DeadleBot/1.0; +http://yourwebsite.com/bot)'}

    try:
        image_response = requests.get(image_url_encoded, headers=headers, stream=True, timeout=10)
        image_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to download the image from {image_url_encoded}: {e}")
        return

    base_dir = os.path.abspath('')
    save_dir = os.path.join(base_dir, 'app', 'static', 'img', 'wiki_img')
    os.makedirs(save_dir, exist_ok=True)

    final_path = os.path.join(save_dir, local_filename)
    with open(final_path, 'wb') as f:
        for chunk in image_response.iter_content(chunk_size=128):
            f.write(chunk)

    print(f"Image saved as {final_path}")

def get_cords(city):
    """Gets a given city's latitude and longitude."""
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}&limit=1"
    response = requests.get(url, timeout=10)
    data = response.json()
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lon, lat
    else:
        return None

def icon_img_feedback(icon: str, directory) -> str:
    """Returns HTML code for a given icon."""
    icon = str(icon)
    icon_filename = icon + '.png'
    icon_path = url_for('static', filename=f'img/icons/{directory}/{icon_filename}')
    icon_image = f"<img src='{icon_path}' alt='{icon}'>"
    return icon_image

def create_text_image(text: str, color: str, directory: str) -> None:
    """Creates an image with text and saves it."""
    if not text:
        text = "Unknown"

    img = Image.new('RGB', (150, 75), color='#262A34')
    d = ImageDraw.Draw(img)

    font_path = os.path.join(app.root_path, 'static', 'css', 'youmurdererbb_reg.ttf')
    font_size = 40

    while True:
        font = ImageFont.truetype(font_path, size=font_size)
        text_width, text_height = d.textbbox((0, 0), text, font=font)[2:]
        if text_width <= img.width - 15 and text_height <= img.height - 15:
            break
        font_size -= 1

    text_x = (img.width - text_width) / 2
    text_y = (img.height - text_height) / 2
    d.text((text_x - 1, text_y - 1), text, font=font, fill=(0, 0, 0))
    d.text((text_x - 2, text_y), text, font=font, fill=(250, 0, 0))

    thickness = 5
    d.rectangle((0, 0, img.width, img.height), outline=color, width=thickness)

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Add the filename with the .png extension
    file_path = os.path.join(directory, f"{text.lower()}_{color}.png")

    img.save(file_path)

def handle_globe_img(filename, color):
    """Handles the globe image by adding a border and resizing it."""
    img_path = os.path.join('app', 'static', 'img', 'icons', 'globe', f'{filename}.png')
    img = Image.open(img_path)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, img.width, img.height), outline=color, width=5)
    new_img = img.resize((100, 100))
    new_img.save(img_path)

def plot_location_on_globe(latitude, longitude, filename, color):
    """Plots the location on a globe and saves the image."""
    if not filename:
        filename = 'unknown'

    if np.isnan(latitude) or np.isnan(longitude):
        create_text_image('Unknown', color=color, directory=os.path.join(app.root_path, 'static', 'img', 'icons', 'globe'))
    else:
        fig = plt.figure(figsize=(5, 5), facecolor='#262A34')
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.Orthographic(longitude, latitude))
        ax.set_global()
        ax.stock_img()
        ax.plot(longitude, latitude, 'ro', markersize=10, transform=ccrs.Geodetic())
        ax.figure.patch.set_facecolor('#262A34')
        save_path = os.path.join("app", "static", "img", "icons", "globe", f"{filename}.png")
        directory = os.path.dirname(save_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        plt.savefig(save_path)
        plt.close(fig)  # Close the figure to free memory
        handle_globe_img(filename, color)
    print(f"Plotting location: lat={latitude}, lon={longitude}, filename={filename}, color={color}")

def clear_dir(dir_name):
    """Deletes all files inside the given directory within the static/img directory, without removing subdirectories."""
    base_dir = os.path.join('app', 'static', 'img')
    dir_path = os.path.join(base_dir, dir_name)

    if not os.path.exists(dir_path):
        print(f"The directory {dir_path} does not exist.")
        return

    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

if __name__ == '__main__':
    clear_dir("wiki_img")
    clear_dir("icons/globe")
    clear_dir("icons/occupations")
    clear_dir("icons/continents")
