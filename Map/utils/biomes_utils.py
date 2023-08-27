import random
from PIL import Image
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import json

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

    def get_humidity(self, x, y):
        return self.noise_humidity([x/100, y/50]) + 0.5

    def get_temperature(self, x, y):
        return (self.noise_temperature([x/100, y/50]) - self.get_real_height(x, y)/2) * 1.5 + (1 - distance_to_equator(x, self.size))

    def get_biome(self, x, y, plot=False):
        humidity = self.noise_humidity([x/100, y/50]) + 0.5
        temperature = (self.noise_temperature([x/100, y/50]) - self.get_real_height(x, y)/2) * 1.5 + (1 - distance_to_equator(x, self.size))
        if plot: self.points.append((temperature, humidity))

        return self.get_closest_biome((humidity, temperature), BIOME_RULES)

    def get_map_field(self, field_name):
        map_name = self.map_name[:self.map_name.rfind("_")] if self.map_name.rfind("_") != -1 else self.map_name
        with open(f"static/map_jsons/{map_name}.json") as f:
            data = json.load(f)
            if field_name in data.keys():
                return data[field_name]
            return None
        
    def set_map_field(self, name, value):
        with open(f"static/map_jsons/{self.map_name}.json", 'r') as file:
            map_info = json.load(file)

        map_info[name] = value

        with open(f"static/map_jsons/{self.map_name}.json", 'w') as f:
            json.dump(map_info, f, indent=4)

    def load_biome_info(self):
        if self.get_map_field("seed_humidity"):
            self.seed_himidity = self.get_map_field("seed_humidity")
        else:
            self.seed_himidity = random.randint(1, 10000)
            self.set_map_field("seed_humidity", self.seed_himidity)
            
        if self.get_map_field("seed_temperature"):
            self.seed_temperature = self.get_map_field("seed_temperature")
        else:
            self.seed_temperature = random.randint(1, 10000)
            self.set_map_field("seed_temperature", self.seed_temperature)

        self.noise_humidity = PerlinNoise(octaves=2, seed=self.seed_himidity)
        self.noise_temperature = PerlinNoise(octaves=2, seed=self.seed_temperature)

def get_temp_hum(map_name, x, y):
    biome_handler = BiomeHandler(map_name)
    biome_handler.load_biome_info()
    biome_handler.load_map_info()
    return f"T {biome_handler.get_temperature(x, y):.2f}, H {biome_handler.get_humidity(x, y):.2f}"

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