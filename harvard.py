import json
import os
import time
import urllib.request
from utils import random_classification, has_proper_dimensions, replace_url_in_html_file


base_dir = os.path.dirname(__file__)
API_KEY = os.environ.get("HARVARD_API_KEY")
BASE_URL = "https://api.harvardartmuseums.org/object"
CLASSES = ['paintings', 'prints', 'drawings', 'photographs']
PAGE_PATH = os.path.join(base_dir, 'frame.html')

def fetch_artworks(page):
    classification = random_classification(CLASSES)

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

def find_artwork_with_proper_dimensions():
    page = 1
    while True:
        data = fetch_artworks(page)

        for artwork in data["records"]:
            if artwork.get("images"):
                image_data = artwork["images"][0]
                width = image_data["width"]
                height = image_data["height"]
                if has_proper_dimensions(width, height):
                    return artwork

        # Check if there are more pages to fetch
        if data["info"]["page"] < data["info"]["pages"]:
            time.sleep(0.1)
            print("Page:", page)
            page += 1
        else:
            # No more pages to fetch
            return None

if __name__ == "__main__":
    artwork = find_artwork_with_proper_dimensions()
    if artwork:
        image_data = artwork.get("images", [{}])[0]
        artist = artwork.get("people", [{}])[0]
        print("Title:", artwork.get("title"))
        print("Artist:", artist.get("displayname"))
        print("Image URL:", image_data.get("baseimageurl"))
        print("Width:", image_data.get("width"))
        print("Height:", image_data.get("height"))

        replace_url_in_html_file(PAGE_PATH, image_data.get("baseimageurl"))
    else:
        print("No artwork found that meets the requirements.")
