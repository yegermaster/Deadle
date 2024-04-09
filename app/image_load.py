import requests
from bs4 import BeautifulSoup
import os

def download_image(wiki_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': wiki_url
    }
    response = requests.get(wiki_url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch the webpage")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    infobox = soup.find('table', class_='infobox')
    image_tag = infobox.find('img') if infobox else soup.find('img')
    if not image_tag or not image_tag.get('src'):
        print("No image found")
        return

    image_src = image_tag['src']
    image_url = "https:" + image_src if image_src.startswith("//") else image_src
    if image_url.startswith("/"):
        domain = "https://www.wikipedia.org"
        image_url = domain + image_url

    image_response = requests.get(image_url, headers=headers, stream=True)
    if image_response.status_code == 200:
        base_dir = os.path.abspath('')
        image_path = os.path.join(base_dir, 'app', 'static', 'img')
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        image_name = os.path.join(image_path, wiki_url.split('/')[-1]+ '.jpg')

        with open(image_name, 'wb') as f:
            for chunk in image_response.iter_content(chunk_size=128):
                f.write(chunk)
        print(f"Image successfully downloaded: {image_name}")
    else:
        print("Failed to download the image")

if __name__ == '__main__':
    download_image("https://en.wikipedia.org/wiki/Rudolf_II,_Holy_Roman_Emperor")
    download_image("https://en.wikipedia.org/wiki/Winston_Churchill")
