from django.core.management.base import BaseCommand, CommandError
from perlin_noise import PerlinNoise
from PIL import Image

from Map.utils.map_utils import get_tile_color, map_value, distance
import random

class Command(BaseCommand):
    help = 'Creates a new map with new Tiles, Areas and Civilizations'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--size', type=int, default=128, help='Size of a map')
        parser.add_argument('-o', '--octaves', type=str, default="3 6 12 24", help='List of octaves')
        parser.add_argument('-sl', '--sealevel', type=float, default=0.7, help='Sea level/procentage')
        parser.add_argument('-b', '--border', type=int, default=5, help='Border width')
        parser.add_argument('-n', '--name', type=str, default="map", help='Map file name')

    def handle(self, *args, **options):
        size = options['size']
        octaves = options['octaves']
        sea_level_arg = options['sealevel']
        border = options['border']
        name = options['name']
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
        image_political = Image.new("RGB", (size, size))
        height_min, height_max = 1, 0
        for x in range(size):
            for y in range(size):
                height = 0
                for i, noise in enumerate(noises):
                    height += noise([x/100, y/100]) * .5**i

                distance_from_edge = distance(x, y, size//2, size//2) - size//2 + border
                if distance_from_edge > 0:
                    height -= map_value(distance_from_edge, 0, border, 0, limit)
                    #print(distance_from_edge, distance_from_edge/distance(0, 0, size//2, size//2))
                    #height -= distance_from_edge/(distance(0, 0, size//2, size//2) - border)
            
                height_fixed = int((height + 1) * 127.5)
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

        image_rgb.save(f"static/images/{name}_geo.png")
        image_political.save(f"static/images/{name}_political.png")
                