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
    (45, 175, 255),
    (45, 190, 255)
]

HEIGHTS_LAND = [
    0.15,
    0.3,
    0.5,
    0.65,
    0.8,
    1.0
]

COLORS_LAND = [
    (114, 193, 134),
    (162, 215, 164),
    (225, 227, 158),

    (241, 151, 82),
    (221, 100, 80),
    (130, 40, 23)
]

def generate_random_string(length=10):
    characters = string.ascii_letters
    random_chars = [random.choice(characters) for _ in range(length)]
    filename = "".join(random_chars)
    return filename

def get_name(filename, n=1):
    with open(f"static/names/{filename}.txt") as f:
        names = [n.strip() for n in f.readlines()]
    return random.sample(names, n)

def map_value(value, min1, max1, min2, max2):
    value = max(min(value, max1), min1)
    span1 = max1 - min1
    span2 = max2 - min2

    value_scaled = float(value - min1) / float(span1)

    return min2 + (value_scaled * span2)

def scale_value(value, scale, normalize=True):
    if normalize: return map_value(value, scale(0), scale(1), 0, 1)
    return scale(value)

def lower_height(height):
    return height**(map_value(height, 0, 0.3, 3, 1))

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