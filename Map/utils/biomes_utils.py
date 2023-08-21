import random
from PIL import Image
import matplotlib.pyplot as plt

BIOME_RULES = [
    #[humidity, temperature]
    [0, 1],
    [0, 0.0],
    [0.0, 0.3],
    [0.4, 0.2],
    [0.5, 0.8],
    [1, 0.85],
    [0.4, -0.8],
    [0, -0.9]
]

BIOME_NAMES = [
    "Desert",
    "Grassland",
    "Grassland",
    "Forest",
    "Forest",
    "Tropical forest",
    "Boreal forest"
    "Tundra",
]

BIOME_COLORS = [
    "#FFFF66",
    "#CCFF99",
    "#CCFF99",
    "#009900",
    "#009900",
    "#33FF33",
    "#663300",
    "#CCFFFF",
]

def distance(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def get_closest_biome(coords, biome_coords):
    min_dist = 10
    biome_id = None
    for i, rule in enumerate(biome_coords):
        distance_to_biome = distance(coords[0], coords[1], rule[0], rule[1])
        if distance_to_biome < min_dist:
            min_dist = distance_to_biome
            biome_id = i
    return biome_id

if __name__ == "__main__":
    n = 50000

    points = []
    colors = []
    for i in range(n):
        h, t = random.random(), random.random()*2 - 1
        points.append((h, t))
        colors.append(BIOME_COLORS[get_closest_biome((h, t), BIOME_RULES)])


    # Unzip the points into separate x and y coordinates
    y_coords, x_coords = zip(*points)

    # Create a scatter plot
    plt.scatter(x_coords, y_coords, c=colors, s=15)

    # Add labels and title
    plt.xlabel('Temperature')
    plt.ylabel('Humidity')
    plt.title('Biomes chart')

    # Display the plot
    plt.show()