from django.core.management.base import BaseCommand, CommandError
from PIL import Image
import random
import json
#from Map.utils.map_utils import get_tile_color, map_value, distance, get_height
from Map.utils.map_json_utils import get_mapped_height, get_map_field, get_lowest_adjacent, sort_tiles, MapHandler
from Map.utils.map_utils import COLORS_WATER, generate_random_string

class Command(BaseCommand):
    help = 'Creates <number> reservoirs on <mapname> map'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mapname', type=str, default="map", help='Name of the map')
        parser.add_argument('-n', '--number', type=int, default=1, help='Number of rivers to generate')

    def handle(self, *args, **options):
        map_name = options['mapname']
        map_handler = MapHandler(map_name)
        number_of_rivers = options['number']
        print(f"Creating reservoirs: map_name = {map_name}, number of rivers = {number_of_rivers}")
        size = map_handler.get_map_field("size")
        river_map = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        river_color = COLORS_WATER[-1]
        lake_color = COLORS_WATER[-2]

        # Creating n rivers
        rivers = []
        all_river_coords = []
        for river in range(number_of_rivers):
            river_coords = []

            # Searching for source coords
            while True:
                x, y = random.randint(0, size-1), random.randint(0, size-1)
                if random.random() < get_mapped_height(map_name, x, y)/5000:
                    break
                
            # Generating river
            while get_mapped_height(map_name, x, y) > 0 and not check_rivers((x, y), rivers):
                river_coords.append((x, y))
                x, y = get_lowest_adjacent(map_name, x, y, river_coords)
                river_map.putpixel((x, y), river_color)

            rivers.append(river_coords)
            for coords in river_coords:
                all_river_coords.append(coords)

        all_river_coords_copy = all_river_coords.copy()
        lakes = []
        lake_coords = []
        while all_river_coords_copy:
            coords = all_river_coords_copy.pop()
            adjacent_water_coords = get_adjacent_water(coords, all_river_coords)
            number_of_adjacent_water_coords = len(adjacent_water_coords)

            if number_of_adjacent_water_coords == 8:
                lake_coords.append(coords)
                if random.random() < 0.8:
                    river_map.putpixel(coords, lake_color)

            elif number_of_adjacent_water_coords > 2:
                lake_coords.append(coords)

            elif number_of_adjacent_water_coords == 2 and get_adjacent_water(adjacent_water_coords[0], lake_coords) and get_adjacent_water(adjacent_water_coords[1], lake_coords):
                lake_coords.append(coords)

            elif lake_coords:
                lakes.append(lake_coords)
                lake_coords = []

        for lake in lakes:
            for lake_coords in lake:
                for river in rivers:
                    if lake_coords in river:
                        river.remove(lake_coords)


        original_map = Image.open(f"static/images/{map_name}_geo.png").convert("RGBA")
        overlayed_map = Image.alpha_composite(original_map, river_map)
        overlayed_map.save(f"static/images/{map_name}_geo.png")

        original_map = Image.open(f"static/images/{map_name}_political.png").convert("RGBA")
        overlayed_map = Image.alpha_composite(original_map, river_map)
        overlayed_map.save(f"static/images/{map_name}_political.png")

        original_map = Image.open(f"static/images/{map_name}_biomes.png").convert("RGBA")
        overlayed_map = Image.alpha_composite(original_map, river_map)
        overlayed_map.save(f"static/images/{map_name}_biomes.png")

        for river in rivers:
            map_handler.add_map_field("rivers", {"name": generate_random_string(), "tiles": sort_tiles(river)})

        for lake in lakes:
            map_handler.add_map_field("lakes", {"name": generate_random_string(), "tiles": sort_tiles(lake)})

def check_rivers(coords, rivers):
    for river in rivers:
        if coords in river:
            return True
    return False

def get_adjacent_water(coords, all_coords):
    x, y = coords
    adjacent_coords = [(x + xx, y + yy) for xx in [-1, 0, 1] for yy in [-1, 0, 1] if not (xx == 0 and yy == 0) and (x + xx, y + yy) in all_coords]
    return adjacent_coords

def are_adjacent(coords1, coords2):
    return abs(coords1[0] - coords2[0]) <= 1 and abs(coords1[1] - coords2[1]) <= 1

def get_common_elements(list1, list2):
    return list(set(list1).intersection(list2))