from django.core.management.base import BaseCommand, CommandError
from perlin_noise import PerlinNoise
from PIL import Image

from Map.utils.map_utils import get_tile_color, map_value
import random

class Command(BaseCommand):
    help = 'Creates a new map with new Tiles, Areas and Civilizations'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--size', type=int, help='Size of a map')
        parser.add_argument('-o', '--octaves', type=str, default="3 6 12 24", help='List of octaves')
        parser.add_argument('-sl', '--sealevel', type=float, default=0.7, help='Sea level/procentage')

    def handle(self, *args, **options):
        size = options['size']
        octaves = options['octaves']
        sea_level_arg = options['sealevel']
        print("Creating a map...", size, octaves)

        octaves = [int(o) for o in octaves.split()]
        noises = [PerlinNoise(octaves=o) for o in octaves]
        limit = 0.5 * (1 - 0.5**len(octaves)) / 0.5
        sea_level = map_value(sea_level_arg, 0, 1, -limit, limit)
        heights_max = [0 for o in octaves]
        heights_min = [0 for o in octaves]
        print(f"octaves: {octaves}")
        image = Image.new("L", (size, size))
        image_rgb = Image.new("RGB", (size, size))
        height_min, height_max = 1, 0
        for x in range(size):
            for y in range(size):
                height = 0
                for i, noise in enumerate(noises):
                    height += noise([x/100, y/100]) * .5**i
                #     heights_min[i] = min(heights_min[i], noise([x/100, y/100]))
                #     heights_max[i] = max(heights_max[i], noise([x/100, y/100]))
                # height_min = min(height_min, height)
                # height_max = max(height_max, height)
                height_fixed = int((height + 1) * 127.5)

                tile_type = "water" if height <= sea_level else "land"
                image.putpixel((x, y), height_fixed)
                image_rgb.putpixel((x, y), get_tile_color(height, -limit, limit, tile_type))
        print(height_min, height_max)
        print("-->", heights_min, heights_max)

        image.save("static/images/map.png")
        image_rgb.save("static/images/map_rgb.png")
                