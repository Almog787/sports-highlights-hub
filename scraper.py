import json
import yt_dlp

def scrape_cartoons():
    # מילות חיפוש ממוקדות לערוצי ילדים ומצויירים בשידור חי
    queries = [
        "live cartoons for kids 24/7",
        "official cartoon channel live",
        "nursery rhymes live stream",
        "animated movies live",
        "kids tv show live stream"
    ]

    all_streams = []
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for q in queries:
            print(f"Searching for: {q}...")
            # מחפש את 10 התוצאות הראשונות לכל מילת חיפוש
            search_query = f"ytsearch10:{q} live" 
            try:
                info = ydl.extract_info(search_query, download=False)
                for entry in info.get('entries', []):
                    if entry and entry.get('id'):
                        # מוודא שאין כפילויות
                        if not any(s['id'] == entry['id'] for s in all_streams):
                            all_streams.append({
                                "id": entry['id'],
                                "title": entry.get('title', 'Kids Live Show'),
                                "url": f"https://www.youtube.com/embed/{entry['id']}"
                            })
            except Exception as e:
                print(f"Error searching {q}: {e}")

    # שמירת כל השידורים תחת קטגוריית cartoons
    results = {"cartoons": all_streams}

    with open('streams.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"Successfully found {len(all_streams)} cartoon streams.")

if __name__ == "__main__":
    scrape_cartoons()
