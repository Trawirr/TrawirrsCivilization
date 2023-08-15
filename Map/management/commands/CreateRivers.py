from django.core.management.base import BaseCommand, CommandError
from PIL import Image
import random
import json
#from Map.utils.map_utils import get_tile_color, map_value, distance, get_height
from Map.utils.map_json_utils import get_map_height, get_map_field, get_lowest_adjacent

class Command(BaseCommand):
    help = 'Creates a new map with new Tiles, Areas and Civilizations'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mapname', type=str, default="map", help='Name of the map')
        parser.add_argument('-n', '--number', type=int, default=1, help='Number of rivers to generate')

    def handle(self, *args, **options):
        map_name = options['mapname']
        number_of_rivers = options['number']
        size = get_map_field(map_name, "size")
        river_map = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        river_color = (45, 200, 255, 256)

        for river in range(number_of_rivers):
            used_coords = []
            while True:
                x, y = random.randint(0, size-1), random.randint(0, size-1)
                if random.random() < get_map_height(map_name, x, y)/5000:
                    break
            print(f"\nRiver source: {x, y}")
            while get_map_height(map_name, x, y) > 0:
                print(f"--> {(x, y)} {get_map_height(map_name, x, y)}m")
                used_coords.append((x, y))
                x, y = get_lowest_adjacent(map_name, x, y, used_coords)
                river_map.putpixel((x, y), river_color)
            
            original_map = Image.open(f"static/images/{map_name}_geo.png").convert("RGBA")
            overlayed_map = Image.alpha_composite(original_map, river_map)
            overlayed_map.save(f"static/images/{map_name}_rivers.png")

