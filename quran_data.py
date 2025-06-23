# quran_data.py
import json

def load_quran_verses(path="quran.json"):
    with open(path, "r", encoding="utf-8") as f:
        quran = json.load(f)

    all_verses = []
    for surah in quran:
        for verse in surah["verses"]:
            all_verses.append({
                "surah_id": surah["id"],
                "surah_name": surah["name"],
                "verse_id": verse["id"],
                "text": verse["text"],
                "translation": verse["translation"]
            })
    return all_verses
