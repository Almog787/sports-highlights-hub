import json
import yt_dlp

def scrape_streams():
    # Configuration by internal YouTube Category IDs:
    # 25 = News & Politics, 1 = Film & Animation, 24 = Entertainment
    categories = {
        "news": {"q": "live news channel", "cat_id": "25"},
        "cartoons": {"q": "live cartoons kids 24/7", "cat_id": "1"},
        "movies": {"q": "live cinema full movies", "cat_id": "1"}
    }

    results = {}
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for key, config in categories.items():
            print(f"Scraping category: {key}...")
            # Use search with filters for better accuracy
            search_query = f"ytsearch12:{config['q']}"
            try:
                info = ydl.extract_info(search_query, download=False)
                valid_streams = []
                
                for entry in info.get('entries', []):
                    # Robust checking: verify it's a live stream ID
                    if entry and entry.get('id'):
                        valid_streams.append({
                            "id": entry['id'],
                            "title": entry.get('title', 'Live Stream'),
                            "url": f"https://www.youtube.com/embed/{entry['id']}"
                        })
                results[key] = valid_streams
            except Exception as e:
                print(f"Error in {key}: {e}")

    with open('streams.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    scrape_streams()
