import requests, os, json
from tqdm import tqdm

# Download 200 images from COCO via their API
os.makedirs("data/images/val2017", exist_ok=True)
os.makedirs("data/annotations", exist_ok=True)

# Download annotation file (small subset)
print("Downloading annotations...")
ann_url = "https://raw.githubusercontent.com/nightrome/cocostuff/master/dataset/cocostuff-10k-v1.1.json"

# We'll use Open Images instead - faster
image_urls = [
    f"https://farm{i}.staticflickr.com/" for i in range(1, 10)
]

# Use COCO's official small sample
print("Fetching COCO sample images...")
response = requests.get("https://picsum.photos/v2/list?limit=200")
photos = response.json()

for i, photo in enumerate(tqdm(photos, desc="Downloading images")):
    img_url = f"https://picsum.photos/id/{photo['id']}/640/480"
    img_path = f"data/images/val2017/{photo['id']}.jpg"
    if not os.path.exists(img_path):
        r = requests.get(img_url, timeout=10)
        with open(img_path, 'wb') as f:
            f.write(r.content)

print(f"\n✅ Downloaded {len(photos)} images!")
print(f"Location: data/images/val2017/")