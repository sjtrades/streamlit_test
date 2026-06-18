import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
from PIL import Image

from coordinate_mapper import world_to_pixel

DATA_FOLDER = "player_data"

frames = []

print("Loading files...")

for day_folder in os.listdir(DATA_FOLDER):
    day_path = os.path.join(DATA_FOLDER, day_folder)

    if not os.path.isdir(day_path):
        continue

    print(f"Loading {day_folder}")

    for file_name in os.listdir(day_path):
        file_path = os.path.join(day_path, file_name)

        try:
            table = pq.read_table(file_path)
            df = table.to_pandas()

            df["event"] = df["event"].apply(lambda x: x.decode("utf-8") if isinstance(x, bytes) else x)

            frames.append(df)

        except Exception as e:
            print(f"Failed: {file_name}")
            print(e)

df = pd.concat(frames, ignore_index=True)

print("\nDataset Shape:")
print(df.shape)

print("\nMap Distribution:")
print(df["map_id"].value_counts())

print("\nEvent Distribution:")
print(df["event"].value_counts())

MAP_NAME = "AmbroseValley"
IMAGE_PATH = "minimaps/AmbroseValley_Minimap.png"
# MAP_NAME = "GrandRift"
# IMAGE_PATH = "minimaps/GrandRift_Minimap.png"
# MAP_NAME = "Lockdown"
# IMAGE_PATH = "minimaps/Lockdown_Minimap.jpg"

df = df[df["map_id"] == MAP_NAME]

df = df[df["event"].isin(["Position", "BotPosition"])]

print(f"\nFiltered Rows: {len(df)}")

img = Image.open(IMAGE_PATH)

img_width, img_height = img.size

print(f"\nImage Size: {img_width} x {img_height}")
print(f"\nImage Mode: {img.mode}")


# pixels = df.apply(
#     lambda row: world_to_pixel(
#         row["x"], row["z"], row["map_id"], img_width, img_height
#     ),
#     axis=1,
# )

# df["pixel_x"] = [p[0] for p in pixels]
# df["pixel_y"] = [p[1] for p in pixels]

# print("\nWorld Coordinate Range")
# print("X:", df["x"].min(), df["x"].max())
# print("Z:", df["z"].min(), df["z"].max())
# print("\nPixel Coordinate Range")
# print("Pixel X:", df["pixel_x"].min(), df["pixel_x"].max())
# print("Pixel Y:", df["pixel_y"].min(), df["pixel_y"].max())

# if len(df) > 10000:
#     df = df.sample(10000, random_state=42)

# plt.figure(figsize=(12, 12))

# plt.imshow(img)

# plt.scatter(df["pixel_x"], df["pixel_y"], s=2, alpha=0.25)

# plt.title(f"{MAP_NAME} Coordinate Validation")

# plt.tight_layout()

# plt.show()


def check_image_data():

    for path in [
        "minimaps/AmbroseValley_Minimap.png",
        "minimaps/GrandRift_Minimap.png",
        "minimaps/Lockdown_Minimap.jpg"
    ]:
        img = Image.open(path)
        print(f"\nChecking {path}")
        print(img.size)
        print(img.mode)

# if __name__ == "__main__":
#     check_image_data()