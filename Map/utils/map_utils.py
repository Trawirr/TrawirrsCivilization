HEIGHTS_WATER = [
    -1.0,
    -0.5,
    0.0,
    1.0
]

COLORS_WATER = [
    (0, 0, 0),
    (0, 0, 255),
    (0, 100, 255),
    (0, 255, 255)
]

HEIGHTS_LAND = [
    -1.0,
    0.0,
    0.3,
    0.6,
    0.9,
    1.0
]

COLORS_LAND = [
    (50, 200, 50),
    (0, 153, 0),
    (153, 255, 51),
    (180, 180, 0),
    (110, 20, 0),
    (50, 0, 0)
]

def map_value(value, min1, max1, min2, max2):
    span1 = max1 - min1
    span2 = max2 - min2

    value_scaled = float(value - min1) / float(span1)

    return min2 + (value_scaled * span2)

def get_color_rules(height, tile_type="land"):
    if tile_type == "land":
        heights, colors = HEIGHTS_LAND, COLORS_LAND
    elif tile_type == "water":
        heights, colors = HEIGHTS_WATER, COLORS_WATER

    for i, h in enumerate(heights):
        if h > height:
            height_ratio = (height - heights[i-1]) / (heights[i] - heights[i-1])
            return height_ratio, colors[i-1], colors[i]
        
def get_color_from_range(height_ratio, color1, color2, height_min=0.0, height_max=1.0):
    return tuple(int(map_value(color1[i] + (color2[i] - color1[i]) * height_ratio, height_min, height_max, 0, 1)) for i in range(3))

def get_tile_color(height, height_min, height_max, tile_type="land"):
    height_ratio, color1, color2 = get_color_rules(height, tile_type)
    return get_color_from_range(height_ratio, color1, color2, height_min, height_max)