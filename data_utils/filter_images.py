import os
import json
import cv2
from tqdm import tqdm


def generate_crops(base_path, crops_destination_dir, full_legibile_path):
    with open(full_legibile_path, "r") as outfile:
        legible_results = json.load(outfile)

    all_legible = []
    for key in legible_results.keys():
        for entry in legible_results[key]:
            all_legible.append(os.path.join(base_path, entry))

    misses = 0
    for img_name in tqdm(all_legible, desc="Processing images"):
        base_name = os.path.basename(img_name)

        img = cv2.imread(img_name)
        if img is None:
            print(f"can't find {img_name}")
            misses += 1
            continue

        try:
            cv2.imwrite(os.path.join(crops_destination_dir, base_name), img)
        except Exception as e:
            print(f"Error saving {base_name}: {str(e)}")
            misses += 1

    print(f"Skipped {misses} out of {len(all_legible)}")


base_path = r"./jersey-number-pipeline-main"
crops_destination_dir = r"crops/imgs"
full_legible_path = r"legible.json"
generate_crops(base_path, crops_destination_dir, full_legible_path)
