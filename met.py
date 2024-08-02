import random
import urllib.request
import json
import os
import time
import re
from utils import replace_url_in_html_file

base_dir = os.path.dirname(__file__)
BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
CLASSIFICATIONS = [
  "Books",
  "Bronzes"
  "Ceramics",
  "Drawings",
  "Paintings",
  "Periodicals",
  "Prints",
  "Sculpture",
  "Stone",
  "Swords",
]
PAGE_PATH = os.path.join(base_dir, 'frame.html')

def fetch_met_object_ids():
    with urllib.request.urlopen(f"{BASE_URL}") as url:
        data = json.loads(url.read().decode())
        return data["objectIDs"]

def fetch_artwork_info(object_id):
    with urllib.request.urlopen(f"{BASE_URL}/{object_id}") as url:
        return json.loads(url.read().decode())

def is_desired_type(art):
    """ Check if the artwork matches the desired type """
    return art.get("classification") in CLASSIFICATIONS

def has_proper_dimensions(art):
    try:
        # Check if 'measurements' is not None and is a list with at least one item
        if art.get("measurements") and isinstance(art["measurements"], list) and len(art["measurements"]) > 0:
            width = art["measurements"][0]["elementMeasurements"].get("Width", 0)
            height = art["measurements"][0]["elementMeasurements"].get("Height", 0)
            aspect_ratio = width / height
            return 0.5 <= aspect_ratio <= 0.6
        else:
            return False
    except (IndexError, KeyError, ZeroDivisionError):
        return False

def fetch_artwork_image():
    object_ids = fetch_met_object_ids()
    for attempt in range(1000):
        time.sleep(0.5)
        object_id = random.choice(object_ids)
        # object_id = 392068
        print(object_id)
        art = fetch_artwork_info(object_id)
        # breakpoint()
        if art.get("isPublicDomain") and has_proper_dimensions(art) and is_desired_type(art):
            return art.get("primaryImage", None)
    return None

if __name__ == "__main__":
    artwork_url = fetch_artwork_image()
    print(artwork_url)
    if artwork_url:
        replace_url_in_html_file(PAGE_PATH, artwork_url)
    else:
        print("No artwork found that meets the requirements.")
