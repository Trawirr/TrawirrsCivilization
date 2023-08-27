from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from PIL import Image
import random
import json
from Map.utils.map_utils import get_tile_color, map_value, distance, get_height, scale_value

class Command(BaseCommand):
    help = 'Creates a new map with new Tiles, Areas and Civilizations'

    def add_arguments(self, parser):
        # map parameters
        parser.add_argument('-s', '--size', type=int, default=128, help='Size of a map')
        parser.add_argument('-o', '--octaves', type=str, default="3 6 12 24", help='List of octaves')
        parser.add_argument('-sl', '--sealevel', type=float, default=0.5, help='Sea level/procentage')
        parser.add_argument('-b', '--border', type=int, default=20, help='Border width')
        parser.add_argument('-sd', '--seed', type=int, default=random.randint(1, 100000), help='Map seed')
        parser.add_argument('-n', '--name', type=str, default="map", help='Map file name')

        # reservoirs parameters
        parser.add_argument('-rn', '--riversnumber', type=int, default=5, help='Number of rivers to generate')
        
        # biomes parameters
        # ...

        # shadow parameters
        parser.add_argument('-d', '--depth', action="store_true", default=False, help='Color of shadow is relational to height difference')

        # areas parameters
        parser.add_argument('-mt', '--mountain', type=int, default=3000, help='Mountain height treshold')

    def handle(self, *args, **options):
        size = options['size']
        octaves = options['octaves']
        sea_level_arg = options['sealevel']
        border = options['border']
        seed = options['seed']
        name = options['name']
        riversnumber = options['riversnumber']
        depth = options['depth']
        mountain = options['mountain']
        options_names = ["size", "octaves", "sealevel", "border", "seed", "name", "riversnumber", "depth", "mountain"]
        options_str = [f'{op} = {options[op]}' for op in options_names]
        print(f"Creating a map: {', '.join(options_str)}")
        print("Creating height map")

        octaves = [int(o) for o in octaves.split()]
        limit = 0.5 * (1 - 0.5**len(octaves)) / 0.5
        sea_level = map_value(sea_level_arg, 0, 1, -limit, limit)
        image = Image.new("L", (size, size))
        image_rgb = Image.new("RGB", (size, size))
        image_political = Image.new("RGB", (size, size))
        height_max, height_max2 = 0, 0
        for x in range(size):
            for y in range(size):
                height = get_height(x, y, octaves, seed, size, border)
                #if height > 0: height = scale_value(height, lambda v: v**2*1.5, False)
                # if height > 0: height = scale_value(height, lambda v: (v*2)**3/2, False)
            
                height_fixed = int((height + 1) * 127.5)
                height_max = max(height_fixed, height_max)
                height_max2 = max(height, height_max2)
                image.putpixel((x, y), height_fixed)

                if height <= sea_level:
                    tile_type = "water"
                    bottom = -limit
                    top = sea_level
                    political_color = (45, 185, 255)
                else:
                    tile_type = "land"
                    bottom = sea_level
                    top = limit
                    political_color = (255, 255, 255)

                image_rgb.putpixel((x, y), get_tile_color(height, bottom, top, tile_type))
                image_political.putpixel((x, y), political_color)

        image.save(f"static/images/{name}_gray.png")
        image_rgb.save(f"static/images/{name}_geo.png")
        image_political.save(f"static/images/{name}_political.png")

        map_info = {
            "size": size,
            "octaves": octaves,
            "sea_level": sea_level,
            "border": border,
            "seed": seed,
            "height_limit": limit,
            "seas": [],
            "lakes": [],
            "rivers": [],
            "continents": [],
            "islands": [],
            "mountains": [],
        }

        with open(f"static/map_jsons/{name}.json", 'w') as f:
            json.dump(map_info, f, indent=4)
                
        call_command("CreateBiomes")
        call_command("CreateReservoirs", number=riversnumber)
        call_command("CreateShadowMap", depth=depth)
        call_command("CreateAreas", mountain=mountain)