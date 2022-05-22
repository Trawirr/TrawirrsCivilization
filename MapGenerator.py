import random
from time import time
from tokenize import Name
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import numpy as np
from Tiles import *
from Areas import *
from settings import *
from NameGenerator import NameGenerator


class MapGenerator:
    def __init__(self) -> None:
        self.name_generator = NameGenerator()

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
        return ((x1-x2)**2 + (y1-y2)**2)**.5
        
    def __pick_color(self, h):
        if type(h) == list:
            return [self.__pick_color(h2) for h2 in h]
        else: 
            h = h['height']
            for i, (height, _) in enumerate(HEIGHT_COLORS):
                if height >= h:
                    (h1, color1), (h2, color2) = HEIGHT_COLORS[i-1], HEIGHT_COLORS[i]
                    break
            return color1 + (color2 - color1) * (h - h1) / (h2 - h1)

    def generate_map(self, x_dim, y_dim, mode = ''):
        self.areas = {area_type: [] for area_type in ['lakes', 'seas', 'rivers', 'continents', 'islands', 'mountains']}

        self.x_dim, self.y_dim = x_dim, y_dim
        self.world_map = []
        self.color_map = []
        self.political_map = []
        self.noises = [PerlinNoise(octaves=n) for n in OCTAVES]

        for i in range(x_dim):
            row = []
            for j in range(y_dim):
                noise_val = 0
                for n, noise in enumerate(self.noises):
                    noise_val += noise([i/x_dim, j/y_dim]) * .5**n

                noise_val = (noise_val+1) * self.__dist_from_edge(i, j, x_dim, y_dim, mode) - 1
                if noise_val<0:
                    row.append(WaterTile(noise_val))
                else:
                    row.append(LandTile(noise_val))
            self.world_map.append(row)

        print(f"Generating areas...")
        start = time()
        self.__generate_areas()
        print(time() - start, 's')
        print(f"Generating color map...")
        start = time()
        self.__generate_color_map()
        print(time() - start, 's')
        print(f"Generating political map...")
        start = time()
        self.__generate_political_map()
        print(time() - start, 's')
        print('Map generating done')

    def __add_area(self, area, area_type, class_name):
        for x, y in area:
            if area_type in ['lake', 'river']:
                self.world_map[x][y] = WaterTile(self.world_map[x][y]['height'])
            self.world_map[x][y].set_attribute('type', area_type)
        area_type_key = area_type + 's'
        self.areas[area_type_key].append((class_name(area, self.name_generator.generate_name(area_type_key))))  

    def __generate_areas(self):
        water = self.__find_areas(lambda x: x < 0)
        lands = self.__find_areas(lambda x: x >= 0)
        mountains = self.__find_areas(lambda x: x > 0.35)
        rivers, lakes = self.__create_rivers(self.__create_sources())

        for area in rivers: self.__add_area(area, 'river', River)

        for area in lakes: self.__add_area(area, 'lake', Lake)

        for area in water:
            if len(area) <= LAKE_MAX_SIZE: self.__add_area(area, 'lake', Lake)
            else: self.__add_area(area, 'sea', Sea)

        for area in lands:
            if len(area) <= ISLAND_MAX_SIZE: self.__add_area(area, 'island', Island)
            else: self.__add_area(area, 'continent', Continent)

        for area in mountains: self.__add_area(area, 'mountain', Mountain)

    def __find_areas(self, condition):
        all_tiles = [(x,y) for x in range(self.x_dim) for y in range(self.y_dim) if condition(self.world_map[x][y]['height'])]
        areas = []
        while len(all_tiles) > 0:
            to_visit = [all_tiles[0]]
            area_tiles = []
            while (len(to_visit)) > 0:
                point = to_visit.pop(0)
                if point in all_tiles:
                    all_tiles.remove(point)
                    area_tiles.append(point)
                    for tile in self.get_adjacent(point[0], point[1]): to_visit.append(tile)
            areas.append(area_tiles)
        return areas

    def __generate_color_map(self):
        self.color_map = [[self.world_map[x][y].pick_color() for y in range(self.y_dim)] for x in range(self.x_dim)]

    def __generate_political_map(self):
        # self.political_map = [[(1,1,1) if self.world_map[x][y]['height'] >= 0 else self.world_map[x][y].pick_color()
        #     for y in range(self.y_dim)] 
        #     for x in range(self.x_dim)]
        self.political_map = [[(1,1,1) if type(self.world_map[x][y]) != WaterTile else self.color_map[x][y]
                                for y in range(self.y_dim)]
                                for x in range(self.x_dim)]

    def show_map(self):
        plt.imshow(self.color_map)
        plt.show()
        plt.imshow(self.political_map)
        plt.show()

    def __create_sources(self):
        num_sources = random.randint(round((self.x_dim * self.y_dim)**(1/3)/3), round((self.x_dim * self.y_dim)**(1/3)/2))
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

    def __create_rivers(self, sources):
        rivers, lakes = [], []
        for source in sources:
            river_tiles = []
            x, y = source
            while True:
                river_tiles.append((x, y))
                # self.world_map[x][y] = River(self.world_map[x][y]['height'])
                # self.color_map[x][y] = (0, 0, 255)
                # self.show_map()
                lakeable, point = self.get_lowest_adjacent(x, y)
                # if (x, y) == point it means the river flows into a sea or a lake at this point 
                if (x, y) == point:
                    lake_tiles = []
                    if self.world_map[x][y]['height'] > 0 and lakeable:
                        # x2, y2 = river_tiles[-2]
                        height = self.world_map[x][y]['height']+0.01
                        #print(f"Creating lake at {y}, {x}, height = {height}")
                        lake_tiles = self.__create_lake(x, y, height)
                        lakes.append(lake_tiles)
                    river_tiles = [tile for tile in river_tiles if tile not in lake_tiles]
                    if len(river_tiles) > 0: rivers.append(river_tiles)
                    break
                x, y = point
        return rivers, lakes
            # rivers.append(river_tiles)

            # river_tiles = [(x,y) for x, y in river_tiles if type(self.world_map[x][y]) != LakeTile]
            # self.areas['rivers'].append(River(river_tiles, self.name_generator.generate_name('rivers')))
            
            # for x, y in [(x,y) for x, y in river_tiles if type(self.world_map[x][y]) != LakeTile]:
            #     self.world_map[x][y] = RiverTile(self.world_map[x][y]['height'])
            #     self.color_map[x][y] = (0, .25, 1)

    def __create_lake(self, x, y, height):
        max_size = random.randint(RIVER_LAKE_SIZES[0], RIVER_LAKE_SIZES[1])
        visited = []
        to_visit = [(x, y)]
        lake_tiles = []
        #self.show_map()
        while len(to_visit) > 0:
            # print(to_visit)
            # print(len(lake_tiles), len(set(lake_tiles)))
            # print(lake_tiles, '\n')
            point = to_visit.pop(0)
            x, y = point
            visited.append(point)

            if self.world_map[x][y]['height'] <= height:
                #print(f"Added lake tile {point=}")
                lake_tiles.append(point)

                if len(lake_tiles) >= max_size:
                    #print(f"Max size of lake achieved: {max_size}")
                    break

                # warunek niesasiadowania z morzem
                adjacent = self.get_adjacent(x, y, lambda point: len(list(filter(lambda p: type(self.world_map[p[0]][p[1]]) == WaterTile, self.get_adjacent(point[0], point[1]) ) ))==0)
                for tile in adjacent:
                    if tile not in visited and tile not in to_visit:
                        to_visit.append(tile)
        return lake_tiles
                        
        # print(f"Lake tiles: {lake_tiles}")
        # for x, y in lake_tiles:
        #     self.world_map[x][y] = LakeTile(self.world_map[x][y]['height'])
        #     self.color_map[x][y] = (0, .75, 1)

    def get_adjacent(self, x, y, condition = None, mode = 'full'):
        if condition == None:
            condition = lambda point: self.__dist_from_edge(point[0], point[1], self.x_dim, self.y_dim, 'borders') > 0
        if mode == 'full':
            xx = yy = [-1,0,1]
            coords = [(x+dx, y+dy) for dy in yy for dx in xx]
        else:
            coords = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        return list(filter(condition, coords))

    def get_lowest_adjacent(self, x, y):
        coords = self.get_adjacent(x, y, mode='full')
        h = self.world_map[x][y]['height']
        lowest_point = (x,y)
        for c1, c2 in coords:
            #print((c1, c2), type(self.world_map[c1][c2]) == River)
            if type(self.world_map[c1][c2]) == WaterTile or self.world_map[c1][c2]['height'] < 0:
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

    def print_areas(self):
        self.generate_map(100, 100, 'circle')
        for key in self.areas.keys():
            print(key)
            for area in self.areas[key]:
                print(f"    {area.name} {area.tiles[:10]}")

def generate_color_map(world_map):
        self.color_map = [[self.world_map[x][y].pick_color() for y in range(self.y_dim)] for x in range(self.x_dim)]

def generate_political_map():
    # self.political_map = [[(1,1,1) if self.world_map[x][y]['height'] >= 0 else self.world_map[x][y].pick_color()
    #     for y in range(self.y_dim)] 
    #     for x in range(self.x_dim)]
    self.political_map = [[(1,1,1) if type(self.world_map[x][y]) != WaterTile else self.color_map[x][y]
                            for y in range(self.y_dim)]
                            for x in range(self.x_dim)]

if __name__ == '__main__':
    my_generator = MapGenerator()
    my_generator.generate_map(100, 100, 'circle')

    my_generator.show_map()
