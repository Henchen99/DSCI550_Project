import os
import pandas as pd
import torch
from diffusers import FluxPipeline
from PIL import Image
from tqdm import tqdm
import xlsxwriter

# === Load image generation pipeline ===
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16
)
pipe.to("cpu")

# === Paths ===
csv_path = "DSCI550_Project/data/processed/hp_with_date_and_witness_count.csv"
output_img_dir = "DSCI550_Project/data/text_to_images"
output_excel_path = csv_path.replace(".csv", "_FULL_with_images.xlsx")

# Ensure image output directory exists
os.makedirs(output_img_dir, exist_ok=True)

# === Load full dataset ===
df = pd.read_csv(csv_path)

# Track generated image paths
image_paths = []

# === Generate images ===
for idx, row in tqdm(df.iterrows(), total=len(df)):
    prompt = str(row['description'])

    try:
        image = pipe(
            prompt,
            height=256,
            width=256,
            guidance_scale=3.5,
            num_inference_steps=10,
            max_sequence_length=512,
            generator=torch.Generator("cuda").manual_seed(0)
        ).images[0]

        img_path = os.path.join(output_img_dir, f"image_{idx}.png")
        image.save(img_path)
        image_paths.append(img_path)

    except Exception as e:
        print(f"Error on row {idx}: {e}")
        image_paths.append("")

# === Add image paths to DataFrame ===
df['image_path'] = image_paths

# === Write to Excel with images ===
workbook = xlsxwriter.Workbook(output_excel_path)
worksheet = workbook.add_worksheet()

# Write headers
for col_idx, col_name in enumerate(df.columns):
    worksheet.write(0, col_idx, col_name)

# Write data and insert images
for row_idx, row in tqdm(df.iterrows(), total=len(df)):
    for col_idx, col_name in enumerate(df.columns):
        if col_name == 'image_path':
            img_file = row[col_name]
            if os.path.exists(img_file):
                worksheet.insert_image(row_idx + 1, col_idx, img_file, {
                    'x_scale': 0.25,
                    'y_scale': 0.25,
                    'x_offset': 5,
                    'y_offset': 5
                })
            else:
                worksheet.write(row_idx + 1, col_idx, "Image not found")
        else:
            worksheet.write(row_idx + 1, col_idx, str(row[col_name]))

workbook.close()
print(f"✅ Excel file with embedded images saved to: {output_excel_path}")
