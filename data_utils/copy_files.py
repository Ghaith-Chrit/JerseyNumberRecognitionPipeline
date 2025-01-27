import os
import shutil
import json

with open(r"out\SoccerNetResults\diff.json", "r") as diff_file:
    differences = json.load(diff_file)

crops_source_dir = r"out\SoccerNetResults\crops\imgs"
model_output_source_dir = r"data\SoccerNet\test\images"
destination_base_dir = r"out\SoccerNetResults\diff"


def copy_images(difference):
    path = difference["path"]

    crop_dest_dir = os.path.join(destination_base_dir, path, "crops")
    model_output_dest_dir = os.path.join(destination_base_dir, path, "model_output")
    os.makedirs(crop_dest_dir, exist_ok=True)
    os.makedirs(model_output_dest_dir, exist_ok=True)

    crop_source_path = crops_source_dir
    model_output_source_path = os.path.join(model_output_source_dir, path)

    if os.path.exists(crop_source_path):
        crop_images = [
            p for p in os.listdir(crop_source_path) if p.startswith(f"{path}_")
        ]

        for image in crop_images:
            source_image_path = os.path.join(crop_source_path, image)
            dest_image_path = os.path.join(crop_dest_dir, image)

            if not os.path.exists(dest_image_path):
                shutil.copy(source_image_path, dest_image_path)

    if os.path.exists(model_output_source_path):
        model_output_images = [
            p for p in os.listdir(model_output_source_path) if p.startswith(f"{path}_")
        ]

        for image in model_output_images:
            source_image_path = os.path.join(model_output_source_path, image)
            dest_image_path = os.path.join(model_output_dest_dir, image)

            if not os.path.exists(dest_image_path):
                shutil.copy(source_image_path, dest_image_path)


for difference in differences:
    copy_images(difference)

print("Files have been copied successfully.")
