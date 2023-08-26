from django.test import TestCase
from Map.utils.map_json_utils import find_binary
from Map.management.commands.CreateAreas import sort_tiles
import random
import time
# Create your tests here.

n = 10000
size = 10000

all_tiles = sort_tiles([(x, y) for x in range(random.randint(1, size)) for y in range(random.randint(1, size))])
times = []
times_in = []

for i in range(n):
    tile = (random.randint(1, size), random.randint(1, size))
    #print(f"{tile} in {all_tiles}")
    start = time.time()
    ans = find_binary(tile, all_tiles)
    end = time.time() - start
    times.append(end)

    start = time.time()
    ans_in = tile in all_tiles
    end = time.time() - start
    times_in.append(end)

    if ans != ans_in:
        print(i, ans_in, "error!")

print(f"binary: {sum(times)/n:.6f}\nin: {sum(times_in)/n}")