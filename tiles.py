from time import time
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from settings import *
import numpy as np
#from areas2 import Area

class Tile:
    all = [[None for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]
    x, y = 0, 0
    colors = None

    def __init__(self, height: float) -> None:
        # Assign values to self object
        self.__height = height
        self.__area_type = ""
        self.__area_name = ""
        self.__attributes = {}

        # Add tile to the Tile.all list
        self.__get_next_all_position()
        Tile.all[self.x][self.y] = self
        #print(f"Added new {self.__class__.__name__}, {self.height=} to all{(self.x, self.y)}")

    @property
    def height(self):
        return self.__height

    @property
    def meters(self):
        return self.__height*1e4

    def add_attribute(self, key, value):
        if key in self.__attributes.keys():
            self.__attributes[key].append(value)
        else:
            self.__attributes[key] = [value]

    def assign_area(self, area_type, area_name):
        self.__area_type = area_type
        self.__area_name = area_name

    def pick_color(self):
        for i, (h, _) in enumerate(self.colors):
            if h >= self.height:
                (h1, color1), (h2, color2) = self.colors[i-1], self.colors[i]
                break
        return color1 + (color2 - color1) * (self.height - h1) / (h2 - h1)

    def __get_next_all_position(self):
        self.x, self.y = Tile.x, Tile.y
        Tile.x = Tile.x + (Tile.y + 1) // GRID_SIZE
        Tile.y = (Tile.y + 1) % GRID_SIZE

    def get_adjacent_tiles(self, condition = None, mode = 'full'):
        x, y = self.x, self.y
        if condition == None:
            condition = lambda point: Tile.dist_from_edge(point[0], point[1], 'borders') > 0
        if mode == 'full':
            xx = yy = [-1,0,1]
            coords = [(x+dx, y+dy) for dy in yy for dx in xx]
        else:
            coords = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        return list(filter(condition, coords))

    def get_lowest_adjacent_tile(self):
        coords = self.get_adjacent_tiles()
        h = Tile.all[self.x][self.y].height
        lowest_point = (self.x, self.y)
        print(f"start {lowest_point} {Tile.all[lowest_point[0]][lowest_point[1]].height}")
        for c1, c2 in coords:
            if Tile.all[c1][c2] is WaterTile or Tile.all[c1][c2].height < 0:
                return False, (self.x, self.y)
            if Tile.all[c1][c2].height <= h:
                print(f"{Tile.all[c1][c2].height} <= {h}")
                lowest_point = (c1, c2)
                h = Tile.all[lowest_point[0]][lowest_point[1]].height
        print(f"koniec {lowest_point} {Tile.all[lowest_point[0]][lowest_point[1]].height}\n")
        return True, lowest_point

    @classmethod
    def generate_map(cls, mode='circle') -> None:
        noises = [PerlinNoise(octaves=n) for n in OCTAVES]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                noise_val = 0
                for n, noise in enumerate(noises):
                    noise_val += noise([i/GRID_SIZE, j/GRID_SIZE]) * .5**n

                noise_val = (noise_val+1) * Tile.dist_from_edge(i, j, mode) - 1
                # noise_val = (noise_val+1) - 1
                if noise_val<0:
                    WaterTile(noise_val)
                else:
                    LandTile(noise_val)
        print(f"Generating done...\n\n")

    @classmethod
    def fix_tile(cls, x, y):
        tmp = (Tile.x, Tile.y)
        Tile.x, Tile.y = x, y
        Tile.all[x][y] = cls(Tile.all[x][y].height)
        Tile.x, Tile.y = tmp

    @staticmethod
    def get_tiles_by_height(height_condition):
        correct_tiles = [(x,y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if height_condition(Tile.all[x][y].height)]
        return correct_tiles

    @staticmethod
    def generate_color_map():
        start = time()
        color_map = [list(map(lambda tile: tile.pick_color(), row)) for row in Tile.all]
        color_map = np.array(color_map)
        print(f"Generated color map in {time()-start}s")
        return color_map

    @staticmethod
    def distance(x1, y1, x2, y2):
        return ((x1-x2)**2 + (y1-y2)**2)**.5

    @staticmethod
    def dist_from_edge(x, y, mode = ''):
        if mode == 'square':
            return min(1.0, (GRID_SIZE+GRID_SIZE)/60*min(GRID_SIZE/2 - abs(x - GRID_SIZE / 2), GRID_SIZE/2 - abs(y - GRID_SIZE / 2))/max(GRID_SIZE/2, GRID_SIZE/2))
        elif mode == 'circle':
            return min(1, (GRID_SIZE+GRID_SIZE)/6/((GRID_SIZE/2 - x)**2 + (GRID_SIZE/2 - y)**2 + 1/64)**.5)
        elif mode == 'real':
            return (GRID_SIZE+GRID_SIZE-abs(2*x-GRID_SIZE)-abs(2*y-GRID_SIZE))/2
        elif mode == 'borders':
            return 0<=x<GRID_SIZE and 0<=y<GRID_SIZE
        else:
            return 1.0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}, {self.height=}"

class LandTile(Tile):
    colors = LAND_COLORS
    def __init__(self, height: float) -> None:
        super().__init__(height)

class WaterTile(Tile):
    colors = WATER_COLORS
    def __init__(self, height: float) -> None:
        super().__init__(height)

if __name__ == '__main__':
    Tile.generate_map()
    color_map = Tile.generate_color_map()
    plt.imshow(color_map)
    plt.show()
