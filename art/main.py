import json
import random
import re
import subprocess
import time
import urllib.request
import os

API_KEY = ""
BASE_URL = "https://api.harvardartmuseums.org/object"
CLASSES = ['paintings', 'prints', 'drawings', 'photographs']
PAGE_PATH = os.path.join(dir, 'frame.html')
cache = {}
dir = os.path.dirname(__file__)

def random_classification():
    if 'classification' not in cache:
        classification = random.choice(CLASSES)
        cache['classification'] = classification
    return cache['classification']

def fetch_artworks(page):
    classification = random_classification()

    params = {
        "apikey": API_KEY,
        "hasimage": True,
        "size": 15, # Smaller page size seems to encourage better randomimity
        "sort": "random", # Sort of random.
        "height>width": "",
        "q": "classification:%s" % classification,
        "page": page
    }

    url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return data

# Ensure the image will look good in portrait mode
def has_proper_dimensions(image_data):
    width = image_data["width"]
    height = image_data["height"]
    aspect_ratio = width / height
    return 0.5 <= aspect_ratio <= 0.6

def find_artwork_with_proper_dimensions():
    page = 1
    while True:
        data = fetch_artworks(page)

        for artwork in data["records"]:
            if artwork.get("images"):
                image_data = artwork["images"][0]
                if has_proper_dimensions(image_data):
                    return artwork

        # Check if there are more pages to fetch
        if data["info"]["page"] < data["info"]["pages"]:
            time.sleep(0.1)
            print("Page:", page)
            page += 1
        else:
            # No more pages to fetch
            return None

def replace_url_in_html_file(file_path, new_url):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        # find the URL
        url_pattern = r'(https?://[^"\'>]+)'
        updated_content = re.sub(url_pattern, new_url, file_content)

        with open(file_path, 'w') as file:
            file.write(updated_content)

        print(f"URL replaced successfully in '{file_path}'.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    artwork = find_artwork_with_proper_dimensions()
    if artwork:
        try:
            # Execute the command and capture the output
            output = subprocess.check_output('pkill -o chromium', shell=True)
            print(output)
        except subprocess.CalledProcessError as e:
            print("Error executing the command:", e)

        print("Title:", artwork.get("title"))
        artist = artwork.get("people", [{}])[0]
        print("Artist:", artist.get("displayname"))
        image_data = artwork.get("images", [{}])[0]
        print("Image URL:", image_data.get("baseimageurl"))
        print("Width:", image_data.get("width"))
        print("Height:", image_data.get("height"))

        replace_url_in_html_file(PAGE_PATH, image_data.get("baseimageurl"))
        try:
            output = subprocess.check_output(f'chromium-browser {PAGE_PATH} --start-fullscreen', shell=True)
            print(output)
        except subprocess.CalledProcessError as e:
            print("Error executing the command:", e)
    else:
        print("No artwork found that meets the requirements.")
