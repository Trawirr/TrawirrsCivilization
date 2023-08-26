from perlin_noise import PerlinNoise
from .map_utils import get_height, map_value
import json
import time

LAND_TYPES = ['mountains', 'rivers', 'lakes', 'islands', 'continents']
WATER_TYPES = ['lakes', 'seas']

class MapHandler:
    def __init__(self, map_name) -> None:
        self.map_name = map_name

    def get_map_field(self, field_name):
        map_name = self.map_name[:self.map_name.rfind("_")]
        with open(f"static/map_jsons/{map_name}.json") as f:
            data = json.load(f)
            return data[field_name]
        
    def add_map_field(self, name, value):
        with open(f"static/map_jsons/{self.map_name}.json", 'r') as file:
            map_info = json.load(file)
        if name not in map_info.keys():
            map_info[name] = [value]
        else:
            map_info[name].append(value)

        with open(f"static/map_jsons/{self.map_name}.json", 'w') as f:
            json.dump(map_info, f, indent=4)

    def load_map_info(self):
        self.octaves = self.get_map_field("octaves")
        self.size = self.get_map_field("size")
        self.seed = self.get_map_field("seed")
        self.sea_level = self.get_map_field("sea_level")
        self.border = self.get_map_field("border")

    def get_real_height(self, x, y):
        return get_height(x, y, self.octaves, self.seed, self.size, self.border) - self.sea_level
    
    def get_mapped_height(self, x, y):
        height = self.get_real_height(x, y)
    
        if height < 0:
            return map_value(height, -1, 0, -2000, -1)
        else:
            return map_value(height, 0, 1, 1, 5000)


def get_map_field(map_name, field_name):
    map_name = map_name[:map_name.rfind("_")]
    with open(f"static/map_jsons/{map_name}.json") as f:
        data = json.load(f)
        return data[field_name]
    
def get_real_height(map_name, x, y):
    octaves = get_map_field(map_name, "octaves")
    size = get_map_field(map_name, "size")
    seed = get_map_field(map_name, "seed")
    sea_level = get_map_field(map_name, "sea_level")
    border = get_map_field(map_name, "border")

    return get_height(x, y, octaves, seed, size, border) - sea_level
    
def get_mapped_height(map_name, x, y):
    
    height = get_real_height(map_name, x, y)
    
    if height < 0:
        return map_value(height, -1, 0, -2000, -1)
    else:
        return map_value(height, 0, 1, 1, 5000)
    
def get_lowest_adjacent(map_name, x, y, used_coords=[]):
    adjacent_coords = [(x + xx, y + yy) for xx in [-1, 0, 1] for yy in [-1, 0, 1] if not (xx == 0 and yy == 0)]

    coords_min = adjacent_coords[0]
    h_min = get_mapped_height(map_name, coords_min[0], coords_min[1])

    for xx, yy in adjacent_coords[1:]:
        if (xx, yy) in used_coords:
            continue
        h = get_mapped_height(map_name, xx, yy)
        if h_min and h < h_min:
            h_min = h
            coords_min = (xx, yy)

    return coords_min

def is_coast(map_name, x, y):
    pass

def sort_tiles(all_tiles):
    return sorted(sorted(all_tiles, key = lambda xy: xy[1]), key = lambda xy: xy[0]) 

def find_binary(tile, all_tiles):
    x, y = tile
    left, right = 0, len(all_tiles) - 1
    index = len(all_tiles) // 2
    while left <= right:  # Changed the condition to <=
        index = (left + right) // 2  # Calculate index inside the loop
        #print(left, index, right)
        x_index, y_index = all_tiles[index]
        if x < x_index:
            right = index - 1  # Adjusted the right boundary
        elif x > x_index:
            left = index + 1  # Adjusted the left boundary
        elif y < y_index:
            right = index - 1  # Adjusted the right boundary
        elif y > y_index:
            left = index + 1  # Adjusted the left boundary
        else:
            print("binary: True")
            return True
    print("binary: False")
    return False

def get_area(map_name, x, y):
    map_name = map_name[:map_name.rfind("_")]
    with open(f"static/map_jsons/{map_name}.json") as f:
        data = json.load(f)

    coords = (x, y)
    h = get_mapped_height(map_name, x, y)
    area_types = WATER_TYPES if h < 0 else LAND_TYPES

    start = time.time()
    for area_type in area_types:
        print("\n", area_type)
        for area in data[area_type]:
            print(area_type, area['name'])
#            print(area_type, area['name'])
            if coords in area['tiles'] != find_binary(coords, area['tiles']):
                print(coords in area['tiles'], find_binary(coords, area['tiles']))
            if find_binary(coords, area['tiles']):
                print("-- Found --")
                return f"{area_type[0].upper() + area_type[1:-1]} {area['name']}"
    print(f"{time.time() - start}s")
    return None
