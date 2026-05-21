import os, json

img_dir = 'data/images/val2017'
all_imgs = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Use only first 100
imgs = all_imgs[:100]

tasks = [{'data': {'image': f'http://localhost:8081/data/images/val2017/{img}'}} for img in imgs]

with open('data/import_tasks.json', 'w') as f:
    json.dump(tasks, f)

print(f'Created import file with {len(tasks)} images')
