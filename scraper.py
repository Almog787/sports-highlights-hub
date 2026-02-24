import json
import yt_dlp
import re

def get_episode_number(title):
    # מחפש מספרים בכותרת כדי לנסות לסדר לפי פרקים
    match = re.search(r'פרק\s+(\d+)', title)
    return int(match.group(1)) if match else 999

def scrape_all():
    all_results = {}

    # --- חלק 1: איסוף המומינים (מסודר) ---
    print("🔍 Scraping The Moomins (Hebrew)...")
    moomin_query = "המומינים פרק מלא"
    moomin_episodes = []
    
    ydl_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # מחפש עד 50 תוצאות כדי לתפוס כמה שיותר פרקים
        info = ydl.extract_info(f"ytsearch50:{moomin_query}", download=False)
        for entry in info.get('entries', []):
            if entry and 'המומינים' in entry.get('title', ''):
                moomin_episodes.append({
                    "id": entry['id'],
                    "title": entry.get('title'),
                    "ep_num": get_episode_number(entry.get('title')),
                    "url": f"https://www.youtube.com/embed/{entry['id']}"
                })
    
    # מיון לפי מספר פרק
    moomin_episodes.sort(key=lambda x: x['ep_num'])
    all_results["moomins"] = moomin_episodes

    # --- חלק 2: איסוף שידורי מצויירים חיים (כפי שהיה) ---
    print("🔍 Scraping Live Cartoons...")
    live_queries = ["cartoon network live", "disney junior live", "nickelodeon live"]
    live_streams = []
    for q in live_queries:
        info = ydl.extract_info(f"ytsearch5:{q} live", download=False)
        for entry in info.get('entries', []):
            if entry:
                live_streams.append({
                    "id": entry['id'],
                    "title": entry.get('title'),
                    "url": f"https://www.youtube.com/embed/{entry['id']}"
                })
    all_results["cartoons"] = live_streams

    # שמירה ל-JSON
    with open('streams.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    print(f"✨ Done! Found {len(moomin_episodes)} Moomin episodes.")

if __name__ == "__main__":
    scrape_all()
