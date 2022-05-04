import random
import pygame
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import numpy as np
from Tiles import *
from Areas import *
import time
import string

SIZE_TILES = (100, 100)

HEIGHT_COLORS = [
    [-1.0, np.array([0,0,0])/255],
    [0, np.array([0,0,255])/255],
    [0, np.array([0,255,0])/255],
    [.3, np.array([255,255,0])/255],
    [.4, np.array([255,70,0])/255],
    [1.0, np.array([0,0,0])/255]
]

class MapGenerator:
    def __init__(self) -> None:
        pass

    # def Generate(self, x_dim: int, y_dim: int, mode: str):
    #     self.x_dim = x_dim
    #     self.y_dim = y_dim

    def __dist_from_edge(self, x, y, xSize, ySize, mode = ''):
        if mode == 'square':
            return min(1.0, (xSize+ySize)/60*min(xSize/2 - abs(x - xSize / 2), ySize/2 - abs(y - ySize / 2))/max(xSize/2, ySize/2))
        elif mode == 'circle':
            return min(1, (xSize+ySize)/6/((xSize/2 - x)**2 + (ySize/2 - y)**2 + 1/64)**.5)
        elif mode == 'real':
            return (xSize+ySize-abs(2*x-xSize)-abs(2*y-ySize))/2
        elif mode == 'borders':
            return 0<=x<xSize and 0<=y<ySize
        else:
            return 1.0

    def dist(self, x1, y1, x2, y2):
        #print(f"dist {x1, y1} {x2,y2} = {((x1-x2)**2 + (y1-y2)**2)**.5}")
        return ((x1-x2)**2 + (y1-y2)**2)**.5
        # print(f"{x}, {y} => {-((xSize/2 - x)**2 + (ySize/2 - y)**2)**.5} / {min(xSize/2 - abs(x - xSize / 2) + .01, ySize/2 - abs(y - ySize / 2) + .01)}")
        # return 1.0 - ((xSize/2 - x)**2 + (ySize/2 - y)**2)**.5/min(xSize/2 - abs(x - xSize / 2) + 1/32, ySize/2 - abs(y - ySize / 2) + 1/32)

    def __pick_color(self, h):
        if type(h) == list:
            return [self.__pick_color(h2) for h2 in h]
        else:
            h = h['height']
            for i, (height, color) in enumerate(HEIGHT_COLORS):
                if height >= h:
                    (h1, color1), (h2, color2) = HEIGHT_COLORS[i-1], HEIGHT_COLORS[i]
                    break
            return color1 + (color2 - color1) * (h - h1) / (h2 - h1)

    def generate_random_name(self):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(4,10)))

    def generate_map(self, x_dim, y_dim, mode = ''):
        self.seas = []
        self.lakes = []
        self.rivers = []
        self.continents = []
        self.islands = []

        self.x_dim, self.y_dim = x_dim, y_dim
        self.world_map = []
        self.color_map = []
        self.noises = [PerlinNoise(octaves=n) for n in [3, 6, 20]]

        for i in range(x_dim):
            row = []
            for j in range(y_dim):
                noise_val = 0
                for n, noise in enumerate(self.noises):
                    noise_val += noise([i/x_dim, j/y_dim]) * .5**n

                noise_val = (noise_val+1) * self.__dist_from_edge(i, j, x_dim, y_dim, mode) - 1
                if noise_val<0:
                    row.append(SeaTile(noise_val))
                else:
                    row.append(TerrainTile(noise_val))
            self.world_map.append(row)
            self.color_map.append(self.__pick_color(row))

        self.find_seas()
        self.find_lands()
        #self.show_map()
        self.create_rivers(self.create_sources())
        print('Map generating done')

    def find_seas(self):
        below_0 = [(x,y) for x in range(self.x_dim) for y in range(self.y_dim) if self.world_map[x][y]['height'] < 0]
        while len(below_0) > 0:
            to_visit = [below_0[random.randint(0, len(below_0)-1)]]
            sea_tiles = []
            while len(to_visit) > 0:
                point = to_visit.pop(0)
                if point in below_0:
                    below_0.remove(point)
                    sea_tiles.append(point)
                    for tile in self.get_adjacent(point[0], point[1]): to_visit.append(tile)
            type_of_water = len(sea_tiles) < 20 and 'Lake' or 'Sea'
            if type_of_water == 'Lake':
                self.lakes.append(Lake(sea_tiles, self.generate_random_name()))
            else:
                self.seas.append(Sea(sea_tiles, self.generate_random_name()))

            print(f"\nNew {type_of_water}: {sea_tiles=}")

    def find_lands(self):
        below_0 = [(x,y) for x in range(self.x_dim) for y in range(self.y_dim) if self.world_map[x][y]['height'] >= 0]
        while len(below_0) > 0:
            to_visit = [below_0[random.randint(0, len(below_0)-1)]]
            land_tiles = []
            while len(to_visit) > 0:
                point = to_visit.pop(0)
                if point in below_0:
                    below_0.remove(point)
                    land_tiles.append(point)
                    for tile in self.get_adjacent(point[0], point[1]): to_visit.append(tile)
            type_of_water = len(land_tiles) < 30 and 'Island' or 'Continent'
            print(f"\nNew {type_of_water}: {land_tiles=}")



    def show_map(self):
        plt.imshow(self.color_map)
        plt.show()
        # manager = plt.get_current_fig_manager()
        # manager.full_screen_toggle()
        # plt.pause(.1)
        # plt.close()

    def create_sources(self):
        num_sources = random.randint(round((self.x_dim * self.y_dim)**(1/3)/3), round((self.x_dim * self.y_dim)**(1/3)/2))
        #print(f"Random num of sources: {num_sources}")
        num_created = 0
        sources = []
        while num_created < num_sources:
            x_random, y_random = random.randint(0, self.x_dim-1), random.randint(0, self.y_dim-1)
            #print(num_created, x_random, y_random)
            if  random.random() < self.world_map[x_random][y_random]['height']-.1 and \
                list(filter(lambda xy: self.dist(x_random, y_random, xy[0], xy[1]) <= 2, sources)) == []:
                
                # self.world_map[x_random][y_random] = River(self.world_map[x_random][y_random]['height'])
                # self.color_map[x_random][y_random] = (0, 0, 255)
                
                sources.append((x_random, y_random))
                num_created += 1
        #print(f'Created {num_created} sources:\n{sources}')
        #print(round((self.x_dim * self.y_dim)**(1/3)))
        return sources

    def create_rivers(self, sources):
        self.rivers = []
        for source in sources:
            river_tiles = []
            x, y = source
            while True:
                river_tiles.append((x, y))
                # self.world_map[x][y] = River(self.world_map[x][y]['height'])
                # self.color_map[x][y] = (0, 0, 255)
                # self.show_map()
                lakeable, point = self.get_lowest_adjacent(x, y)
                if (x, y) == point:
                    if self.world_map[x][y]['height'] > 0 and lakeable:
                        x2, y2 = river_tiles[-2]
                        height = self.world_map[x][y]['height']+0.01
                        #print(f"Creating lake at {y}, {x}, height = {height}")
                        self.create_lake(x, y, height)
                    break
                x, y = point

            river_tiles = [(x,y) for x, y in river_tiles if type(self.world_map[x][y]) != LakeTile]
            self.rivers.append(River(river_tiles, self.generate_random_name))
            print(f"Created river from {source} to {river_tiles[-1]}")
            for x, y in [(x,y) for x, y in river_tiles if type(self.world_map[x][y]) != LakeTile]:
                self.world_map[x][y] = RiverTile(self.world_map[x][y]['height'])
                self.color_map[x][y] = (0, 0, 255) # (0, 0, 255)

    def create_lake(self, x, y, height):
        print(f"Creating lake at {y}, {x}")
        max_size = random.randint(4,15)
        visited = []
        to_visit = [(x, y)]
        lake_tiles = []
        #self.show_map()
        while len(to_visit) > 0:
            time.sleep(.25)
            # print(to_visit)
            # print(len(lake_tiles), len(set(lake_tiles)))
            # print(lake_tiles, '\n')
            point = to_visit.pop(0)
            x, y = point
            visited.append(point)

            if self.world_map[x][y]['height'] <= height and type(self.world_map[x][y]) not in (RiverTile, LakeTile, SeaTile):
                print(f"Added lake tile {point=}")
                lake_tiles.append(point)

                if len(lake_tiles) >= max_size:
                    print(f"Max size of lake achieved: {max_size}")
                    break

                # warunek niesasiadowania z morzem
                adjacent = self.get_adjacent(x, y, lambda point: len(list(filter(lambda p: type(self.world_map[p[0]][p[1]]) == SeaTile, self.get_adjacent(point[0], point[1]) ) ))==0)
                for tile in adjacent:
                    if tile not in visited and tile not in to_visit:
                        to_visit.append(tile)
                        
        print(f"Lake tiles: {lake_tiles}")
        for x, y in lake_tiles:
            self.world_map[x][y] = LakeTile(self.world_map[x][y]['height'])
            self.color_map[x][y] = (0, 50, 225) # (0, 120, 255)
        self.show_map()

    def get_adjacent(self, x, y, condition = None):
        # coords = [
        #     (x-1, y),
        #     (x+1, y),
        #     (x, y-1),
        #     (x, y+1)]
        if condition == None:
            condition = lambda point: self.__dist_from_edge(point[0], point[1], self.x_dim, self.y_dim, 'borders') > 0
        xx = yy = [-1,0,1]
        coords = [(x+dx, y+dy) for dy in yy for dx in xx]
        return list(filter(condition, coords))
        #return [(c1, c2) for c1, c2 in coords if self.__dist_from_edge(c1, c2, self.x_dim, self.y_dim, 'borders') > 0]

    def get_lowest_adjacent(self, x, y):
        coords = self.get_adjacent(x, y)
        h = self.world_map[x][y]['height']
        lowest_point = (x,y)
        for c1, c2 in coords:
            #print((c1, c2), type(self.world_map[c1][c2]) == River)
            if type(self.world_map[c1][c2]) == RiverTile or self.world_map[c1][c2]['height'] < 0:
                return False, (x, y)
            if self.world_map[c1][c2]['height'] <= h:
                lowest_point = (c1, c2)
                h = self.world_map[c1][c2]['height']
        return True, lowest_point

    def show_color_gradient(self):
        gradient = []
        for i in np.linspace(-1.0, 1.0):
            gradient.append(self.__pick_color(i))
        plt.imshow([gradient,gradient,gradient])
        plt.show()

my_generator = MapGenerator()
my_generator.generate_map(100, 100, 'circle')
print('     lakes:')
for r in my_generator.lakes:
    print(r.name)
print('     seas:')
for r in my_generator.seas:
    print(r.name)
print('     rivers:')
for r in my_generator.rivers:
    print(r.length, r.name)
my_generator.show_map()
