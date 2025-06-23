# quran_matcher.py
from sentence_transformers import SentenceTransformer, util
from quran_data import load_quran_verses

# Load Quran
quran_verses = load_quran_verses()

# Prepare verse translations
verse_texts = [v["translation"] for v in quran_verses]

# Load sentence transformer
print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")  

# Encode all verse translations
print("Encoding verses...")
verse_embeddings = model.encode(verse_texts, convert_to_tensor=True)

def menu():
    while True:
        print("\nMenu:")
        print("1. Find closest Quran verse")
        print("2. Exit")
        choice = input("Enter your choice (1/2): ").strip()
        if choice == '1':
            print("\nType a phrase to find the closest Quran verse:")
            query = input("Your phrase: ")
            # Encode the query
            query_embedding = model.encode(query, convert_to_tensor=True)
            # Compute cosine similarity
            cos_scores = util.cos_sim(query_embedding, verse_embeddings)[0]
            # Get top 5 matches
            top_results = cos_scores.topk(5)
            print("\nTop matching Quran verses:\n")
            for score, idx in zip(top_results[0], top_results[1]):
                verse = quran_verses[int(idx)]
                print(f"[{verse['surah_name']} - {verse['verse_id']}]")
                print(f"Ayat: {verse['text']}")
                print(f"Translation: {verse['translation']}")
                print(f"Score: {score:.4f}")
                print("-" * 60)
        elif choice == '2':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    menu()
