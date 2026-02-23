import os
import json
import requests
from datetime import datetime

# --- Configuration ---
# ScoreBat Free Video API
API_URL = "https://www.scorebat.com/video-api/v3/"
DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "sports_highlights.json")

def ensure_environment():
    """
    Fail-safe: Ensures the data directory and database file exist.
    """
    try:
        if not os.path.exists(DATA_FOLDER):
            print(f"Creating directory: {DATA_FOLDER}")
            os.makedirs(DATA_FOLDER)
        
        if not os.path.exists(DATA_FILE):
            print(f"Creating initial database file: {DATA_FILE}")
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
    except Exception as e:
        print(f"Critical error during environment setup: {e}")
        exit(1)

def fetch_sports_data():
    """
    Fetches the latest football highlights from ScoreBat API.
    """
    print(f"Fetching data from {API_URL}...")
    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Check if 'response' key exists in ScoreBat API
        return data.get('response', [])
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with API: {e}")
        return None

def process_and_save(raw_data):
    """
    Processes the raw API data and saves it to a clean JSON file.
    """
    if not raw_data:
        print("No data to process.")
        return

    processed_list = []
    for item in raw_data:
        # Extracting relevant fields for the frontend
        clean_item = {
            "title": item.get("title"),
            "competition": item.get("competition"),
            "thumbnail": item.get("thumbnail"),
            "url": item.get("matchviewUrl"),
            "embed_code": item.get("videos", [{}])[0].get("embed"), # Get the first video embed
            "date": item.get("date"),
            "last_updated": datetime.now().isoformat()
        }
        processed_list.append(clean_item)

    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(processed_list, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved {len(processed_list)} items to {DATA_FILE}.")
    except Exception as e:
        print(f"Error saving data to file: {e}")

def main():
    print("--- Sports News Aggregator Started ---")
    ensure_environment()
    
    highlights = fetch_sports_data()
    if highlights:
        process_and_save(highlights)
    
    print("--- Process Completed ---")

if __name__ == "__main__":
    main()
