import os
from PIL import Image
from tqdm import tqdm

input_dir = "./data/crops/imgs"
output_dir = "./data/bicubic/crops/imgs"
target_width = 140
target_height = 176

os.makedirs(output_dir, exist_ok=True)

try:
    from PIL.Image import Resampling

    BICUBIC = Resampling.BICUBIC
except ImportError:
    BICUBIC = Image.BICUBIC

valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")
valid_files = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_extensions)]
success_count = 0

for filename in tqdm(valid_files, desc="Processing images", unit="file"):
    img_path = os.path.join(input_dir, filename)
    try:
        with Image.open(img_path) as img:
            resized_img = img.resize((target_width, target_height), resample=BICUBIC)
            output_path = os.path.join(output_dir, filename)
            resized_img.save(output_path, quality=95)
            success_count += 1
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")

print(f"\nSuccessfully resized {success_count}/{len(valid_files)} images.")
