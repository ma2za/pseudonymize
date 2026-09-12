import io
import shutil
import urllib.request
import zipfile
from pathlib import Path

DATA_DIR = Path("data/gazetteer")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 1. Download US Census First Names (1990)
FIRST_NAMES_URL = "https://www2.census.gov/topics/genealogy/1990surnames/dist.female.first"
FIRST_NAMES_M_URL = "https://www2.census.gov/topics/genealogy/1990surnames/dist.male.first"
SURNAMES_URL = "https://www2.census.gov/topics/genealogy/1990surnames/dist.all.last"


def download_file(url, dest):
    if not dest.exists():
        print(f"Downloading {url}...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})  # noqa: S310
        with urllib.request.urlopen(req) as response, open(dest, "wb") as out_file:  # noqa: S310
            shutil.copyfileobj(response, out_file)


print("Fetching Census data...")
download_file(FIRST_NAMES_URL, DATA_DIR / "female_first.txt")
download_file(FIRST_NAMES_M_URL, DATA_DIR / "male_first.txt")
download_file(SURNAMES_URL, DATA_DIR / "surnames.txt")

names = set()
for file_name in ["female_first.txt", "male_first.txt", "surnames.txt"]:
    with open(DATA_DIR / file_name) as f:
        for line in f:
            parts = line.split()
            if parts:
                names.add(parts[0].capitalize())

print(f"Loaded {len(names)} unique names.")

# 2. Download World Cities (Geonames cities1000)
CITIES_URL = "https://download.geonames.org/export/dump/cities1000.zip"
print("Fetching Geonames cities data...")

req = urllib.request.Request(CITIES_URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as response, zipfile.ZipFile(io.BytesIO(response.read())) as z:  # noqa: S310
    z.extract("cities1000.txt", path=DATA_DIR)

locations = set()
with open(DATA_DIR / "cities1000.txt", encoding="utf-8") as f:
    for line in f:
        parts = line.split("\t")
        if len(parts) > 2:
            locations.add(parts[1])  # ascii name
            locations.add(parts[2])  # localized name

print(f"Loaded {len(locations)} unique locations.")

with open(DATA_DIR / "names.txt", "w", encoding="utf-8") as f:
    for n in sorted(names):
        f.write(n + "\n")

with open(DATA_DIR / "locations.txt", "w", encoding="utf-8") as f:
    for loc in sorted(locations):
        f.write(loc + "\n")
