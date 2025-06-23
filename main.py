import whisper
import openai
import json

# 1. Load Whisper model
model = whisper.load_model("base")  # Use "tiny" or "small" if you want it faster

# 2. Transcribe Arabic audio
result = model.transcribe("music.wav", language="ar")
transcribed_text = result["text"]
print(f"\n🎧 Transcribed Arabic: {transcribed_text}\n")

# 3. Load your OpenAI API Key
openai.api_key = "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"

# 4. Load Quran verses (or subset for now to stay within token limits)
with open("quran_subset.json", "r", encoding="utf-8") as f:
    quran_data = json.load(f)

# Flatten verses to simple list
verses = []
for surah in quran_data:
    for verse in surah["verses"]:
        verses.append({
            "text": verse["text"],
            "translation": verse["translation"],
            "surah": surah["name"],
            "ayah_id": verse["id"]
        })

# 5. Prepare the prompt
def build_prompt(transcribed_text, verses):
    sample_verses = verses[:25]  # keep short for token budget
    verses_str = "\n".join([
        f"{v['surah']} [{v['ayah_id']}]: {v['text']} ({v['translation']})"
        for v in sample_verses
    ])
    
    return f"""
You are a Quran verse matching assistant.

Your job is to match the following Arabic line to the most similar Quran verse from the list below. Respond only with the best matched verse and its translation and surah.

Transcribed Arabic line:
\"{transcribed_text}\"

Quran verses to match from:
{verses_str}

Return only the most relevant match like this:
Surah: <surah name> [ayah number]
Arabic: <verse text>
Translation: <verse translation>
"""

# 6. Get response from OpenAI
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # or gpt-4
    messages=[
        {"role": "system", "content": "You are a Quran matching assistant."},
        {"role": "user", "content": build_prompt(transcribed_text, verses)}
    ],
    temperature=0.3,
)

# 7. Print result
match = response.choices[0].message["content"]
print("\n📖 Matched Ayah:\n", match)
