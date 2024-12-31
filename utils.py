import random
import re
from datetime import date

FRAME_PATH = os.path.join(base_dir, 'frame.html')
LOG_PATH = os.path.join(base_dir, 'history.log')

cache = {}

def random_classification(CLASSES):
    if 'classification' not in cache:
        classification = random.choice(CLASSES)
        cache['classification'] = classification
    return cache['classification']

# Ensure the image will look good in portrait mode
def has_proper_dimensions(width, height):
    aspect_ratio = width / height
    return 0.5 <= aspect_ratio <= 0.6

def replace_url_in_html_file(new_url, file_path = FRAME_PATH):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        url_pattern = r'(https?://[^"\'>]+)'
        updated_content = re.sub(url_pattern, new_url, file_content)

        with open(file_path, 'w') as file:
            file.write(updated_content)

        print(f"URL replaced successfully in '{file_path}'.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def append_to_history(content, file_path = LOG_PATH):
    entry = f"{date.today()} - {content}"
    open(file_path, 'a').write(entry + '\n')
