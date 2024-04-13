import requests
from bs4 import BeautifulSoup
import os
import requests
from flask import url_for
from PIL import Image, ImageDraw, ImageFont


def download_image(wiki_url):
    """Downloads the main image from wikipedia url"""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': wiki_url
    }
    try:
        response = requests.get(wiki_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error", errh)
        return
    except requests.exceptions.ConnectionError as errc:
        print("Connection Error", errc)
        return
    except requests.exceptions.Timeout as errt:
        print("Timeout Error", errt)
        return
    except requests.exceptions.RequestException as err:
        print("Oops: unknown error", err)
        return

    if response.status_code != 200:
        print("Failed to fetch the webpage")
        return

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        infobox = soup.find('table', class_='infobox')
        image_tag = infobox.find('img') if infobox else soup.find('img') # searching for the imag in the html of the wiki link
        if not image_tag or not image_tag.get('src'):
            print("No image found")
            return

        image_src = image_tag['src']
        image_url = "https:" + image_src if image_src.startswith("//") else image_src
        if image_url.startswith("/"):
            domain = "https://www.wikipedia.org"
            image_url = domain + image_url

        load_wiki_image(image_url, wiki_url, headers) # downloading the image
    except Exception as e:
        print(f"An error occurred while processing the image: {e}")

def load_wiki_image(image_url, wiki_url, headers):
    try:
        image_response = requests.get(image_url, headers=headers, stream=True)
        image_response.raise_for_status()

        base_dir = os.path.abspath('')
        image_path = os.path.join(base_dir, 'app', 'static', 'img', 'wiki_img')
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        image_name = os.path.join(image_path, wiki_url.split('/')[-1]+ '.jpg') # saving the image with its own name

        with open(image_name, 'wb') as f:
            for chunk in image_response.iter_content(chunk_size=128):
                f.write(chunk)
        print(f"Image successfully downloaded: {image_name}")
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as erre:
        print("Oops: Something Else ", erre)

def get_direction(from_coord, to_coord):
    lat1, lon1 = from_coord
    lat2, lon2 = to_coord

    lat_diff = lat2 - lat1
    lon_diff = lon2 - lon1

    if lat_diff > 0 and abs(lon_diff) < abs(lat_diff) / 2:
        return 'N'
    elif lat_diff < 0 and abs(lon_diff) < abs(abs(lat_diff) / 2):
        return 'S'
    elif lon_diff > 0 and abs(lat_diff) < abs(lon_diff) / 2:
        return 'E'
    elif lon_diff < 0 and abs(lat_diff) < abs(lon_diff) / 2:
        return 'W'
    elif lat_diff > 0 and lon_diff > 0:
        return 'NE'
    elif lat_diff < 0 < lon_diff:
        return 'SE'
    elif lat_diff < 0 and lon_diff < 0:
        return 'SW'
    elif lat_diff > 0 > lon_diff:
        return 'NW'
    return 'Unknown'

def get_cords(city):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}&limit=1"
    response = requests.get(url)
    data = response.json()
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lon, lat
    else:
        return None

def icon_img_feedback(icon, dir):
    icon_filename = icon + '.png'
    icon_path = url_for('static', filename=f'img/icons/{dir}/{icon_filename}')
    icon_image = f"<img src='{icon_path}' alt='{icon}'>"
    return icon_image

def create_text_image(text, color, dir):
    img  = Image.new('RGB', (150, 75), color = '#262A34')
    d = ImageDraw.Draw(img)

    font_path = r'C:\Users\Owner\לימודים\deadle\app\static\css\youmurdererbb_reg.ttf'
    font = ImageFont.truetype(font_path,size=40)

    text_width, text_height = d.textsize(text, font=font)
    text_x = (img.width - text_width) / 2
    text_y = (img.height - text_height) / 2
    d.text((text_x - 1, text_y - 1), text, font=font, fill=(0, 0, 0))
    d.text((text_x-2, text_y), text, font=font, fill=(250,0,0))

    thickness = 5
    d.rectangle([0, 0, img.width, img.height], outline=color, width= thickness)

    img.save(f'{dir}{text}_{color}.png')

if __name__ == '__main__':
    create_text_image('shoe maker', 'red', 'occupations')