import urllib.request
import json
import random

def fetch_all_object_ids():
    url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        return data["objectIDs"]

def fetch_object_info(object_id):
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())

def main():
    print("Fetching object IDs...")
    object_ids = fetch_all_object_ids()
    
    print("Randomly selecting 1000 object IDs...")
    selected_ids = random.sample(object_ids, 1000)

    unique_classifications = set()
    print("Fetching data for selected objects...")
    for object_id in selected_ids:
        info = fetch_object_info(object_id)
        classification = info.get("classification", "Unknown")
        unique_classifications.add(classification)

    print(f"Unique classifications found ({len(unique_classifications)}):")
    for classification in sorted(unique_classifications):
        print(classification)

if __name__ == "__main__":
    main()
