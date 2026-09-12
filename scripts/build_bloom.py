import urllib.request
from pathlib import Path

DATA_DIR = Path("data/gazetteer")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Fetch a standard list of 10,000 common English words
WORDS_URL = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"
dest = DATA_DIR / "common_words.txt"

if not dest.exists():
    print(f"Downloading {WORDS_URL}...")
    req = urllib.request.Request(WORDS_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response, open(dest, "wb") as f:  # noqa: S310
        f.write(response.read())

words = set()
with open(dest, encoding="utf-8") as f:
    for line in f:
        w = line.strip().lower()
        # Only keep words longer than 2 chars to avoid vetoing initials/short names
        if len(w) > 2 and w.isalpha():
            words.add(w)

print(f"Loaded {len(words)} common words for Bloom Filter Veto.")
