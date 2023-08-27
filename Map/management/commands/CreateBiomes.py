from django.core.management.base import BaseCommand, CommandError
from PIL import Image
import random
import json
import time
from Map.utils.map_json_utils import get_map_field, get_mapped_height, MapHandler
from Map.utils.map_utils import generate_random_string
from Map.utils.biomes_utils import BiomeHandler

class Command(BaseCommand):
    help = 'Creates land and water areas on <mapname> map'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mapname', type=str, default="map", help='Name of the map')
        #parser.add_argument('-s', '--s', type=int, default=3000, help='Biomes sides')

    def handle(self, *args, **options):
        map_name = options['mapname']
        biome_handler = BiomeHandler(map_name)
        biome_handler.load_map_info()
        biome_handler.load_biome_info()
        size = biome_handler.get_map_field("size")
        biome_map = Image.new("RGBA", (size, size), (0, 0, 0, 0))

        for x in range(size):
            for y in range(size):
                if biome_handler.get_real_height(x, y) > 0:
                    biome_map.putpixel((x, y), biome_handler.get_biome_color(biome_handler.get_biome(x, y)))

        original_map = Image.open(f"static/images/{map_name}_geo.png").convert("RGBA")
        overlayed_map = Image.alpha_composite(original_map, biome_map)
        overlayed_map.save(f"static/images/{map_name}_biomes.png")