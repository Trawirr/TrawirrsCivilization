from django.core.management.base import BaseCommand, CommandError
from PIL import Image
import random
import json
import time
from Map.utils.map_json_utils import get_map_field, get_mapped_height, sort_tiles, MapHandler
from Map.utils.map_utils import generate_random_string

class Command(BaseCommand):
    help = 'Creates land and water areas on <mapname> map'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mapname', type=str, default="map", help='Name of the map')
        parser.add_argument('-mt', '--mountain', type=int, default=3000, help='Mountain height treshold')

    def handle(self, *args, **options):
        map_name = options['mapname']
        mountain = options['mountain']
        print(f"Creating reservoirs: map_name = {map_name}, mountain treshold = {mountain}")
        map_handler = MapHandler(map_name)
        map_handler.load_map_info()
        # split tiles
        water_tiles = []
        land_tiles = []
        mountain_tiles = []
        size = map_handler.get_map_field("size")

        for x in range(size):
            for y in range(size):
                h = map_handler.get_mapped_height(x, y)
                if h < 0:
                    water_tiles.append((x, y))
                else:
                    land_tiles.append((x, y))
                    if h > mountain:
                        mountain_tiles.append((x, y))

        for reservoir in split_areas(water_tiles):
            area_type = "seas" if len(reservoir) > 400 else "lakes"
            map_handler.add_map_field(area_type, {"name": generate_random_string(), "tiles": sort_tiles(reservoir)})

        for land in split_areas(land_tiles):
            area_type = "continents" if len(land) > 500 else "islands"
            map_handler.add_map_field(area_type, {"name": generate_random_string(), "tiles": sort_tiles(land)})

        for mountain in split_areas(mountain_tiles):
            map_handler.add_map_field("mountains", {"name": generate_random_string(), "tiles": sort_tiles(mountain)})

def get_adjacent_tiles(coords, adjacency_type="normal"):
    x, y = coords
    if adjacency_type == "normal":
        adjacent_coords = [(x + xx, y + yy) for xx in [-1, 0, 1] for yy in [-1, 0, 1] if not (xx == 0 and yy == 0)]
    elif adjacency_type == "cardinal":
        adjacent_coords = [(x + xx, y + yy) for xx in [-1, 0, 1] for yy in [-1, 0, 1] if not (xx == 0 and yy == 0) and (xx == 0 or yy == 0)]
    return adjacent_coords

def split_areas(all_tiles):
    areas = []
    while all_tiles:
        to_visit = [all_tiles[0]]
        area_tiles = []
        while to_visit:
            tile = to_visit.pop(0)
            if tile in all_tiles:
                all_tiles.remove(tile)
                area_tiles.append(tile)
                adjacent_tiles = get_adjacent_tiles(tile)
                for tile in adjacent_tiles:
                    to_visit.append(tile)
        areas.append(area_tiles)
    return areas
