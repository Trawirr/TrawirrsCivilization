from django.core.management.base import BaseCommand, CommandError
from PIL import Image
import random
import json
import time
from Map.utils.map_json_utils import get_map_field, get_mapped_height, MapHandler
from Map.utils.map_utils import generate_random_string

class Command(BaseCommand):
    help = 'Creates land and water areas on <mapname> map'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mapname', type=str, default="map", help='Name of the map')
        parser.add_argument('-s', '--s', type=int, default=3000, help='Biomes sides')

    def handle(self, *args, **options):
        pass