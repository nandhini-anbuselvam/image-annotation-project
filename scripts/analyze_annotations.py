import json
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Load annotations
with open('data/annotations/annotations.json', 'r') as f:
    data = json.load(f)

print(f"Total tasks: {len(data)}")

# Parse annotations
label_counts = defaultdict(int)
box_sizes = []
annotated_images = []
empty_images = []
all_boxes = []

for task in data:
    image_url = task['data']['image']
    image_name = image_url.split('/')[-1]
    annotations = task.get('annotations', [])

    if not annotations or not annotations[0]['result']:
        empty_images.append(image_name)
        continue

    annotated_images.append(image_name)
    boxes_in_image = []

    for ann in annotations:
        for result in ann['result']:
            if result['type'] == 'rectanglelabels':
                label = result['value']['rectanglelabels'][0]
                label_counts[label] += 1
                w = result['value']['width']
                h = result['value']['height']
                x = result['value']['x']
                y = result['value']['y']
                box_sizes.append(w * h)
                boxes_in_image.append({'label': label, 'x': x, 'y': y, 'w': w, 'h': h})
                all_boxes.append({'image': image_name, 'label': label, 'x': x, 'y': y, 'w': w, 'h': h})

print(f"\n✅ Annotated images: {len(annotated_images)}")
print(f"⚠️  Unannotated images: {len(empty_images)}")
print(f"📦 Total bounding boxes: {len(all_boxes)}")
print(f"\n📊 Label Distribution:")
for label, count in sorted(label_counts.items(), key=lambda x: -x[1]):
    print(f"   {label}: {count}")

# ── Plot 1: Label Distribution Bar Chart ──
os.makedirs('output', exist_ok=True)
plt.figure(figsize=(10, 5))
labels = list(label_counts.keys())
counts = list(label_counts.values())
colors = ['#FF0000','#0000FF','#00AA00','#FFA500','#800080','#00AAAA','#808080']
bars = plt.bar(labels, counts, color=colors[:len(labels)], edgecolor='black')
for bar, count in zip(bars, counts):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             str(count), ha='center', fontweight='bold')
plt.title('Annotation Label Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Label')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('output/label_distribution.png', dpi=150)
plt.close()
print("\n✅ Saved: output/label_distribution.png")

# ── Plot 2: Box Size Distribution ──
plt.figure(figsize=(10, 5))
plt.hist(box_sizes, bins=20, color='steelblue', edgecolor='black')
plt.title('Bounding Box Size Distribution (%area)', fontsize=14, fontweight='bold')
plt.xlabel('Box Area (% of image)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('output/box_size_distribution.png', dpi=150)
plt.close()
print("✅ Saved: output/box_size_distribution.png")

# ── Plot 3: Annotated vs Unannotated Pie Chart ──
plt.figure(figsize=(6, 6))
plt.pie([len(annotated_images), len(empty_images)],
        labels=['Annotated', 'Unannotated'],
        colors=['#00AA00', '#FF4444'],
        autopct='%1.1f%%', startangle=90)
plt.title('Annotation Coverage', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('output/annotation_coverage.png', dpi=150)
plt.close()
print("✅ Saved: output/annotation_coverage.png")

# ── QC Check: Flag tiny boxes (likely errors) ──
tiny_boxes = [b for b in all_boxes if b['w'] * b['h'] < 1.0]
print(f"\n🔍 QC Check - Tiny boxes (possible errors): {len(tiny_boxes)}")
for b in tiny_boxes:
    print(f"   Image: {b['image']} | Label: {b['label']} | Size: {b['w']:.1f}x{b['h']:.1f}%")

# ── QC Check: Images with too many boxes ──
from collections import Counter
img_box_counts = Counter(b['image'] for b in all_boxes)
crowded = {img: cnt for img, cnt in img_box_counts.items() if cnt > 8}
print(f"\n🔍 QC Check - Crowded images (>8 boxes): {len(crowded)}")
for img, cnt in crowded.items():
    print(f"   {img}: {cnt} boxes")

print("\n✅ Analysis complete! Check the output/ folder.")