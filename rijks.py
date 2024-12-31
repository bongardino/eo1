import json
import os
import random
import urllib.request
from utils import random_classification, has_proper_dimensions, replace_url_in_html_file, append_to_history

API_KEY = os.environ.get("RIJKS_API_KEY")
BASE_URL = "https://www.rijksmuseum.nl/api/en/collection"
CLASSES = ['painting', 'print', 'drawing']


def fetch_artwork_image(api_key):
    classification = random_classification(CLASSES)
    print(classification)

    def make_request_and_filter():
        params = {
            "key": api_key,
            "format": "json",
            "type": classification,
            "imgonly": True,
            "p": random.randint(1, 1000),
            "ps": 100
        }
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        request_url = f"{BASE_URL}?{query_string}"

        try:
            with urllib.request.urlopen(request_url) as response:
                if response.getcode() != 200:
                    return []

                response_json = json.loads(response.read().decode())
                portrait_images = []
                for art in response_json.get("artObjects", []):
                    image_url = art.get("webImage", {}).get("url")
                    width = art.get("webImage", {}).get("width")
                    height = art.get("webImage", {}).get("height")
                    if has_proper_dimensions(width, height):
                        portrait_images.append(image_url)

                return portrait_images
        except urllib.error.URLError as e:
            print(f"Error making request: {e}")
            return []

    for attempt in range(50):
        images = make_request_and_filter()
        if images:
            return random.choice(images)

    return None

if __name__ == "__main__":
    artwork = fetch_artwork_image(API_KEY)
    print(artwork)
    if artwork:
        replace_url_in_html_file(artwork)
        append_to_history(artwork)
    else:
        print("No artwork found that meets the requirements.")
