import random
from PIL import Image
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import json
import time

from Map.utils.map_json_utils import MapHandler

BIOME_RULES = [
    #[humidity, temperature]
    [0, 0.8],
    [0.2, 0.0],
    [0.2, 0.4],
    [0.4, -0.2],
    [0.6, 0.6],
    [1, 0.85],
    [0.5, -0.7],
    [0, -0.9]
]

BIOME_NAMES = [
    "Desert",
    "Grassland",
    "Grassland",
    "Forest",
    "Forest",
    "Tropical forest",
    "Boreal forest",
    "Tundra",
]

BIOME_COLORS = [
    (255, 255, 102),
    (204, 255, 153),
    (204, 255, 153),
    (0, 153, 0),
    (0, 153, 0),
    (51, 255, 51),
    (102, 51, 0),
    (204, 255, 255),
]

BIOME_COLORS_STR = [
    "#FFFF66",
    "#CCFF99",
    "#CCFF99",
    "#009900",
    "#009900",
    "#33FF33",
    "#663300",
    "#CCFFFF",
]

class BiomeHandler(MapHandler):
    def __init__(self, map_name) -> None:
        self.map_name = map_name
        self.points = []

    def get_closest_biome(self, coords, biome_coords=BIOME_RULES):
        min_dist = 100
        biome_id = None
        for i, rule in enumerate(biome_coords):
            distance_to_biome = distance(coords[0], coords[1], rule[0], rule[1])
            if distance_to_biome < min_dist:
                min_dist = distance_to_biome
                biome_id = i
        return biome_id
    
    def get_biome_color(self, biome_id):
        return BIOME_COLORS[biome_id]
    
    def plot_points(self):
        x, y = zip(*self.points)

        plt.scatter(x, y, s=2)

        plt.xlabel('Temperature')
        plt.ylabel('Humidity')
        plt.title('Biomes chart')

        plt.show()

    def count_nearby_water_tiles(self, x, y, r=2):
        water_counter = 0
        lakes = [lake_coords for lake_coords in self.get_map_field('lakes')]
        rivers = [river_coords for river_coords in self.get_map_field('rivers')]

        for xx in range(x-r, x+r+1):
            for yy in range(y-r, y+r+1):
                if xx < 0 or yy < 0 or xx >= self.size or yy >= self.size:
                    continue
                if self.get_real_height(xx, yy) < 0:
                    water_counter += 1
                else:
                    if (xx, yy) in lakes:
                        water_counter += 1
                    elif (xx, yy) in rivers:
                        water_counter += 1
        return water_counter

    def get_humidity(self, x, y, r=4):
        return self.noise_humidity([x/100, y/50]) + self.count_nearby_water_tiles(x, y, r)/(r+1)**2/5

    def get_temperature(self, x, y):
        return (self.noise_temperature([x/100, y/50]) - self.get_real_height(x, y)) * 1.5 + (1 - distance_to_equator(x, self.size))

    def get_biome(self, x, y, plot=False):
        humidity = self.get_humidity(x, y)
        temperature = self.get_temperature(x, y)
        if plot: self.points.append((temperature, humidity))

        return self.get_closest_biome((humidity, temperature), BIOME_RULES)
        
    def set_map_field(self, name, value):
        with open(f"static/map_jsons/{self.map_name}.json", 'r') as file:
            map_info = json.load(file)

        map_info[name] = value

        with open(f"static/map_jsons/{self.map_name}.json", 'w') as f:
            json.dump(map_info, f, indent=4)

    def load_biome_info(self):
        self.seed_humidity, self.seed_temperature = self.get_map_field(["seed_humidity", "seed_temperature"])
        if not self.seed_humidity:
            self.seed_humidity = random.randint(1, 10000)
            self.set_map_field("seed_humidity", self.seed_humidity)
            
        if not self.seed_temperature:
            self.seed_temperature = random.randint(1, 10000)
            self.set_map_field("seed_temperature", self.seed_temperature)

        self.noise_humidity = PerlinNoise(octaves=2, seed=self.seed_humidity)
        self.noise_temperature = PerlinNoise(octaves=2, seed=self.seed_temperature)

    def get_temp_hum(self, x, y):
        return f"T {self.get_temperature(x, y):.2f}, H {self.get_humidity(x, y):.2f}"

def distance(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def distance_to_equator(y, size):
    return abs(y - size/2)/(size/2)

if __name__ == "__main__":
    n = 50000

    points = []
    colors = []
    labels = []
    biome_handler = BiomeHandler("")
    for i in range(n):
        h, t = random.random(), random.random()*2 - 1
        biome_id = biome_handler.get_closest_biome((h, t), BIOME_RULES)
        points.append((h, t))
        colors.append(BIOME_COLORS_STR[biome_id])
        labels.append(BIOME_NAMES[biome_id])


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