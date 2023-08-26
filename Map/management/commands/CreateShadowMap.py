from django.core.management.base import BaseCommand, CommandError
from PIL import Image
import random
import json

from Map.utils.map_json_utils import MapHandler, map_value

class Command(BaseCommand):
    help = 'Creates <number> reservoirs on <mapname> map'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mapname', type=str, default="map", help='Name of the map')
        parser.add_argument('-d', '--depth', action="store_true", default=False, help='Color of shadow is relational to height difference')

    def handle(self, *args, **options):
        map_name = options['mapname']
        use_depth = options['depth']
        print(f"Creating shadow map: map_name = {map_name}, depth_mode = {use_depth}")
        map_handler = MapHandler(map_name)
        map_handler.load_map_info()
        size = map_handler.get_map_field("size")
        shadow_map = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        shadow_color = (0, 0, 0, 30)

        for x in range(size):
            for y in range(size):
                h = map_handler.get_real_height(x, y)
                if h > 0:
                    h2 = map_handler.get_real_height(x+1, y-1)
                    if h < h2:
                        if use_depth:
                            shadow_color = (0, 0, 0, int(map_value(h2 - h, 0, .5, 10, 200)))
                        shadow_map.putpixel((x, y), shadow_color)
                    
        shadow_map.save(f"static/images/{map_name}_shadow.png")

        original_map = Image.open(f"static/images/{map_name}_geo.png").convert("RGBA")
        overlayed_map = Image.alpha_composite(original_map, shadow_map)
        overlayed_map.save(f"static/images/{map_name}_geo.png")

        original_map = Image.open(f"static/images/{map_name}_political.png").convert("RGBA")
        overlayed_map = Image.alpha_composite(original_map, shadow_map)
        overlayed_map.save(f"static/images/{map_name}_political.png")