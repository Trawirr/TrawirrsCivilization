from perlin_noise import PerlinNoise
from .map_utils import get_height, map_value
import json

def get_map_field(map_name, field_name):
    map_name = map_name.replace("_geo", "").replace("_political", "").replace(".png", "")
    with open(f"static/map_jsons/{map_name}.json") as f:
        data = json.load(f)
        return data[field_name]
    
def get_map_height(map_name, x, y):
    octaves = get_map_field(map_name, "octaves")
    size = get_map_field(map_name, "size")
    seed = get_map_field(map_name, "seed")
    sea_level = get_map_field(map_name, "sea_level")
    border = get_map_field(map_name, "border")
    
    height = get_height(x, y, octaves, seed, size, border) - sea_level
    
    if height < 0:
        return map_value(height, -1, 0, -2000, -1)
    else:
        return map_value(height, 0, 1, 1, 5000)
    
def get_lowest_adjacent(map_name, x, y, used_coords=[]):
    adjacent_coords = [(x + xx, y + yy) for xx in [-1, 0, 1] for yy in [-1, 0, 1] if not (xx == 0 and yy == 0)]

    coords_min = adjacent_coords[0]
    h_min = get_map_height(map_name, coords_min[0], coords_min[1])

    for xx, yy in adjacent_coords[1:]:
        if (xx, yy) in used_coords:
            continue
        h = get_map_height(map_name, xx, yy)
        if h_min and h < h_min:
            h_min = h
            coords_min = (xx, yy)

    return coords_min
