from PIL import Image
from coordinate_mapper import world_to_pixel
from config import MAP_CONFIG
import pandas as pd


def add_pixel_coordinates(df):
    frames = []

    for map_id in df["map_id"].unique():
        map_df = df[df["map_id"] == map_id].copy()

        img = Image.open(MAP_CONFIG[map_id]["image"])

        width, height = img.size

        pixels = map_df.apply(
            lambda row: world_to_pixel(
                row["x"],
                row["z"],
                row["map_id"],
                width,
                height
            ),
            axis=1
        )

        map_df["pixel_x"] = [p[0] for p in pixels]
        map_df["pixel_y"] = [p[1] for p in pixels]

        frames.append(map_df)

    return pd.concat(frames, ignore_index=True)