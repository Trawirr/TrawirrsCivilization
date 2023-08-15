import string
import random
from perlin_noise import PerlinNoise

HEIGHTS_WATER = [
    0.05,
    0.2,
    0.7,
    0.95,
    1.0
]

COLORS_WATER = [
    (0, 0, 50),
    (25, 100, 140),
    (35, 145, 200),
    (45, 185, 255),
    (45, 200, 255)
]

HEIGHTS_LAND = [
    0.1,
    0.25,
    0.5,
    0.7,
    0.8,
    1.0
]

COLORS_LAND = [
    (114, 193, 134),
    (162, 215, 164),
    (225, 227, 158),

    (241, 121, 82),
    (221, 85, 80),
    (130, 23, 45)
]

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    random_chars = [random.choice(characters) for _ in range(length)]
    filename = "".join(random_chars)
    return filename

def map_value(value, min1, max1, min2, max2):
    value = min(value, max1)
    span1 = max1 - min1
    span2 = max2 - min2

    value_scaled = float(value - min1) / float(span1)

    return min2 + (value_scaled * span2)

def distance(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def get_height(x, y, octaves, seed, size, border):
    limit = 0.5 * (1 - 0.5**len(octaves)) / 0.5
    noises = [PerlinNoise(octaves=o, seed=seed) for o in octaves]
    height = 0
    for i, noise in enumerate(noises):
        height += noise([x/100, y/100]) * .5**i

    if border > 0:
        distance_from_edge = distance(x, y, size//2, size//2) - size//2 + border
        if distance_from_edge > 0:
            height -= map_value(distance_from_edge, 0, border, 0, limit)
    return height

def get_color(height, tile_type="land"):
    if tile_type == "land":
        heights, colors = HEIGHTS_LAND, COLORS_LAND
    elif tile_type == "water":
        heights, colors = HEIGHTS_WATER, COLORS_WATER

    for i, h in enumerate(heights):
        if h >= height:
            return colors[i]
        
def get_color_from_range(height_ratio, color1, color2, height_min=0.0, height_max=1.0):
    return tuple(int(map_value(color1[i] + (color2[i] - color1[i]) * height_ratio, height_min, height_max, 0, 1)) for i in range(3))

def get_tile_color(height, height_min, height_max, tile_type="land"):
    return get_color(map_value(height, height_min, height_max, 0, 1), tile_type)