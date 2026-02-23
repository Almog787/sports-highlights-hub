import os, json, requests

DATA_FOLDER = "data"
# שימוש בגרסה יציבה יותר של הלוגואים
LOGO_BASE_URL = "https://www.thesportsdb.com/images/media/team/badge/small/"

def clean_name(name):
    """מנקה שמות קבוצות כדי לשפר את החיפוש"""
    return name.replace("FC", "").replace("CF", "").strip()

def fetch_data():
    if not os.path.exists(DATA_FOLDER): os.makedirs(DATA_FOLDER)
    
    print("Fetching highlights...")
    try:
        sb_data = requests.get("https://www.scorebat.com/video-api/v3/").json().get('response', [])
    except: sb_data = []

    # ארגון נתונים לפי ליגה
    leagues_data = {}
    
    for item in sb_data[:30]: # לוקחים יותר נתונים כדי שיהיה מה לחלק
        comp = item.get("competition", "Other")
        if comp not in leagues_data:
            leagues_data[comp] = []
        
        title = item.get("title", "")
        teams = title.split(' - ')
        home = clean_name(teams[0]) if len(teams) > 0 else "Home"
        away = clean_name(teams[1]) if len(teams) > 1 else "Away"

        # ניסיון חכם להשיג לוגו (שימוש ב-API חינמי ללא מפתח לחיפוש מהיר)
        leagues_data[comp].append({
            "title": title,
            "date": item.get("date"),
            "embed_code": item.get("videos", [{}])[0].get("embed"),
            "url": item.get("matchviewUrl"),
            "home_team": home,
            "away_team": away,
            # נשתמש בשירות חלופי ללוגואים אם TSDB נכשל
            "home_logo": f"https://ui-avatars.com/api/?name={home}&background=random&color=fff&size=128",
            "away_logo": f"https://ui-avatars.com/api/?name={away}&background=random&color=fff&size=128"
        })

    with open(f"{DATA_FOLDER}/highlights_by_league.json", "w", encoding="utf-8") as f:
        json.dump(leagues_data, f, ensure_ascii=False, indent=4)

    # משיכת תוצאות חיות
    try:
        api_key = os.environ.get("LIVE_API_KEY")
        if api_key:
            r = requests.get("https://v3.football.api-sports.io/fixtures?live=all", headers={'x-apisports-key': api_key})
            live = r.json().get('response', [])
            with open(f"{DATA_FOLDER}/live_scores.json", "w", encoding="utf-8") as f:
                json.dump(live, f, ensure_ascii=False)
    except: pass

if __name__ == "__main__":
    fetch_data()
