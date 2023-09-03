from perlin_noise import PerlinNoise
from .map_utils import get_height, map_value, scale_value, lower_height
import json
import time
import os

LAND_TYPES = ['mountains', 'rivers', 'lakes', 'islands', 'continents']
WATER_TYPES = ['lakes', 'seas']

class MapHandler:
    def __init__(self, map_name) -> None:
        self.map_name = map_name

    def get_map_field(self, field_names):
        map_name = self.map_name[:self.map_name.rfind("_")] if self.map_name.rfind("_") != -1 else self.map_name
        with open(f"static/map_jsons/{map_name}.json") as f:
            data = json.load(f)
            tmp = None
            try:
                if isinstance(field_names, str): raise TypeError
            except:
                if field_names in data.keys():
                    tmp = data[field_names]
            else:
                tmp = []
                for field_name in field_names:
                    if field_name in data.keys():
                        tmp.append(data[field_name])
                    else:
                        tmp.append(None)
        return tmp
        
    def add_map_field(self, name, value):
        map_name = self.map_name[:self.map_name.rfind("_")] if self.map_name.rfind("_") != -1 else self.map_name
        with open(f"static/map_jsons/{self.map_name}.json", 'r') as file:
            map_info = json.load(file)
        if name not in map_info.keys():
            map_info[name] = [value]
        else:
            map_info[name].append(value)

        with open(f"static/map_jsons/{self.map_name}.json", 'w') as f:
            json.dump(map_info, f, indent=4)

    def load_map_info(self):
        self.octaves, self.size, self.seed, self.sea_level, self.border = self.get_map_field(["octaves", "size", "seed", "sea_level", "border"])

    def get_real_height(self, x, y):
        #print(x, y, f"{lower_height(get_height(x, y, self.octaves, self.seed, self.size, self.border))} - {self.sea_level} = {get_height(x, y, self.octaves, self.seed, self.size, self.border) - self.sea_level}")
        height = get_height(x, y, self.octaves, self.seed, self.size, self.border)
        if height > 0:
            height = lower_height(height)
        return height - self.sea_level
    
    def get_mapped_height(self, x, y):
        height = self.get_real_height(x, y)
    
        if height < 0:
            return map_value(height, -1, 0, -2000, -1)
        else:
            return map_value(height, 0, 1, 1, 5000)

    def get_area(self, x, y):
        map_name = self.map_name[:self.map_name.rfind("_")] if self.map_name.rfind("_") != -1 else self.map_name
        with open(f"static/map_jsons/{map_name}.json") as f:
            data = json.load(f)

        coords = (x, y)
        h = self.get_mapped_height(x, y)
        area_types = WATER_TYPES if h < 0 else LAND_TYPES

        for area_type in area_types:
            for area in data[area_type]:
                if find_binary(coords, area['tiles']):
                    return f"{area_type[0].upper() + area_type[1:-1]} {area['name']}"
        return None




def get_map_field(map_name, field_names):
    map_name = map_name[:map_name.rfind("_")] if map_name.rfind("_") != -1 else map_name
    with open(f"static/map_jsons/{map_name}.json") as f:
        data = json.load(f)
        tmp = None
        try:
            if isinstance(field_names, str): raise TypeError
        except:
            if field_names in data.keys():
                tmp = data[field_names]
        else:
            tmp = []
            for field_name in field_names:
                if field_name in data.keys():
                    tmp.append(data[field_name])
                else:
                    tmp.append(None)
        
        return tmp
    
def get_real_height(map_name, x, y):
    octaves = get_map_field(map_name, "octaves")
    size = get_map_field(map_name, "size")
    seed = get_map_field(map_name, "seed")
    sea_level = get_map_field(map_name, "sea_level")
    border = get_map_field(map_name, "border")

    #return scale_value(get_height(x, y, octaves, seed, size, border) - sea_level, lambda v: v**2*1.5, False)

    height = get_height(x, y, octaves, seed, size, border) - sea_level
    if height > 0: height = lower_height(height)
    #if height > 0: height = scale_value(get_height(x, y, octaves, seed, size, border) - sea_level, lambda v: v**2*1.5, False)
    return height

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
            return True
    return False

def get_map_names():
    directory_path = "static/images"
    file_names = []
    try:
        entries = os.listdir(directory_path)

        for entry in entries:
            entry_path = os.path.join(directory_path, entry)
            if os.path.isfile(entry_path):
                file_names.append(entry)

    except OSError as e:
        print(f"Error reading directory '{directory_path}': {e}")

    file_names = set([file_name[:file_name.find("_")] for file_name in file_names if "_" in file_name])
    return file_names