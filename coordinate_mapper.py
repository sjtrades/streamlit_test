from config import MAP_CONFIG

def world_to_pixel(x, z, map_id, image_width, image_height):
    cfg = MAP_CONFIG[map_id]

    u = (x - cfg["origin_x"]) / cfg["scale"]
    v = (z - cfg["origin_z"]) / cfg["scale"]

    pixel_x = u * image_width
    pixel_y = (1 - v) * image_height

    return pixel_x, pixel_y