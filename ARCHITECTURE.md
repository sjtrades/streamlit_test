# LILA BLACK - Architecture Overview

## What is this?

This document describes the architecture and implementation decisions behind the LILA BLACK Player Journey Visualization Tool.

---

## Technology Choices

|------------|--------------------------------------------------|
| Technology | Reason                                           |
|------------|--------------------------------------------------|
| Python     | Data processing and analysis                     |
| Streamlit  | Rapid development of interactive dashboards      |
| Pandas     | Filtering and manipulation of data               |
| Plotly     | Interactive journey and heatmap visualizations   |
| PyArrow    | Efficient reading of parquet files               |
| Pillow     | Loading minimap images                           |
|------------|--------------------------------------------------|

---

## Data Flow

The application follows the pipeline below.

Parquet Files
    │
load_all_data()
    │
Decode Events
    │
Combine into DataFrame
    │
Coordinate Mapping
    │
Map / Date / Match Filtering
    │
Journey / Playback / Heatmaps
    │
Plotly Rendering

At startup, parquet files are loaded and combined into a single Pandas DataFrame.
Event values stored as bytes are decoded into readable strings.
User selections progressively filter the dataset before rendering journeys, events or heatmaps.

---

## Coordinate Mapping

The coordinate transformation parameters are maintained in `MAP_CONFIG`. These values were taken directly from the dataset README and used for world-to-minimap coordinate conversion.
The dataset provides 3d world positions, for minimap visualization (2d), only `x` and `z` coordinates are required. The `y` coordinate represents elevation and is ignored.

### Step 1 : Convert world coordinates into UV space

u = (x - origin_x) / scale
v = (z - origin_z) / scale

### Step 2 : Convert UV coordinates into image pixels

pixel_x = u _ image_width
pixel_y = (1 - v) _ image_height

The Y-axis is flipped because image coordinates use a top-left origin.

### Data Validation

Before implementing the visualization layer, a validation utility was created to overlay all movement events on top of the minimap. This was used to verify that player traffic aligned with roads, buildings, and traversable areas, confirming the correctness of the world-to-minimap coordinate conversion.

---

## Assumptions

### Minimap Assets

The provided minimap assets are not fully consistent in file format as well as resolution.
The README specified minimaps as 1024×1024, while the supplied assets were exported at a higher resolution.

To make the coordinate mapping robust against future asset re-exports and differing image formats, the implementation converts world coordinates to normalized UV coordinates and then scales them using the actual image dimensions loaded at runtime rather than relying on a hardcoded resolution.

### Timestamps

The dataset documentation specifies that timestamps represent milliseconds elapsed within a match.

While loading parquet files, pandas automatically converts these values into `datetime64[ns]`. For playback implementation, the original millisecond values are reconstructed to preserve the ordering of events.

### Heatmaps

Heatmaps are generated at the map level by aggregating telemetry data from all matches played on the selected map.
This provides designers with a broader understanding of:

- High traffic routes
- Frequent engagement locations
- Common player death zones

Heatmap visualization parameters such as marker size, color and opacity are maintained in `HEATMAP_CONFIG`.
These settings are configurable on a per-map basis to improve visibility across minimaps with different visual characteristics.

### Storm Events

The supplied dataset contains only a small number of storm-related events, so they may not appear for every selected match.

---

## Tradeoffs

|-----------------------|-----------------------------------------------------------------------|
| Consideration         | Decision                                                              |
|-----------------------|-----------------------------------------------------------------------|
| Visualization         | Plotly selected over Matplotlib for interactivity                     |
| UI Framework          | Streamlit selected for rapid prototyping                              |
| Heatmaps              | Generated per map instead of per match                                |
| Playback              | Slider-based playback selected over animation                         |
| Coordinate Mapping    | Dynamic image dimensions selected over fixed 1024×1024 images         |
| Data Loading          | Preload all parquet files due to manageable dataset size (~89k rows)  |
|-----------------------|-----------------------------------------------------------------------|