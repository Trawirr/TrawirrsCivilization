import random
from Tiles import *

class Area:
    names = NAMES['Area']
    all = []
    def __init__(self, tiles: list) -> None:
        self.__tiles = tiles
        self.__name = self.names.pop(0)
        print(f"Created: {self.__class__.__name__} {self.name} of size {len(self.tiles)} tiles")
        Area.all.append(self)
        for x, y in self.__tiles:
            Tile.all[x][y].add_attribute('area', f'{self.__class__.__name__}: {self.name}')

    @property
    def name(self):
        return self.__name
        
    @property
    def tiles(self):
        return self.__tiles

    def find_peaks(self):
        pass

    @classmethod
    def generate_areas(cls): # <-------------------
        print("Generating areas...")
        water = Area.separate_areas(lambda x: x < 0)
        lands = Area.separate_areas(lambda x: x >= 0)
        mountains = Area.separate_areas(lambda x: x > 0.35)
        lakes = Area.create_lakes()
        rivers = Area.create_rivers(Area.create_sources())

        for area in water:
            if len(area) <= LAKE_MAX_SIZE:
                Lake(area)
            else:
                Sea(area)

        for area in lands:
            if len(area) <= ISLAND_MAX_SIZE:
                Island(area)
            else:
                Continent(area)

        for area in mountains:
            Mountain(area)

        for area in rivers:
            River(area)

        for area in lakes:
            Lake(area)

    @classmethod
    def separate_areas(cls, condition):
        all_tiles = Tile.get_tiles_by_height(condition)
        areas = []
        while len(all_tiles) > 0:
            to_visit = [all_tiles[0]]
            area_tiles = []
            while (len(to_visit)) > 0:
                point = to_visit.pop(0)
                if point in all_tiles:
                    all_tiles.remove(point)
                    area_tiles.append(point)
                    for tile in Tile.all[point[0]][point[1]].get_adjacent_tiles(): 
                        to_visit.append(tile)
            areas.append(area_tiles)
        return areas

    @classmethod
    def create_sources(cls):
        sources = []
        while len(sources) < RIVER_MAX_NUMBER:
            x_random, y_random = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            if  random.random() < Tile.all[x_random][y_random].height - .1 and \
                list(filter(lambda xy: Tile.distance(x_random, y_random, xy[0], xy[1]) <= 5, sources)) == []:
                sources.append((x_random, y_random))
        return sources

    @classmethod
    def create_rivers(cls, sources):
        rivers = []
        for source in sources:
            river_tiles = []
            x, y = source
            while True:
                print(x,y)
                if isinstance(Tile.all[x][y], WaterTile):
                    break
                river_tiles.append((x, y))
                sorted_adjacent_tiles = Tile.all[x][y].get_lowest_adjacent_tile()
                for tile in sorted_adjacent_tiles:
                    if tile not in river_tiles:
                        point = tile
                        break
                if point == (x, y):
                    break
                x, y = point
            for x, y in river_tiles:
                WaterTile.fix_tile(x, y)
            rivers.append(river_tiles)
        return rivers

    @classmethod
    def create_lakes(cls):
        lakes = []
        visited = []
        while len(lakes) < LAKE_MAX_NUMBER:
            lake_tiles = []
            lake_size = random.randint(3, LAKE_MAX_SIZE)
            x, y = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            height_max = Tile.all[x][y].height
            if random.random() > 1 - height_max:
                continue
            to_visit = [(x, y)]
            while len(lake_tiles) < lake_size and to_visit:
                x, y = to_visit.pop(0)
                
                if isinstance(Tile.all[x][y], WaterTile) or Tile.all[x][y].is_adjacent_to(WaterTile):
                    break

                if (x, y) not in visited and Tile.all[x][y].height <= height_max:
                    lake_tiles.append((x, y))
                    visited.append((x, y))

                    adjacent_tiles = Tile.all[x][y].get_adjacent_tiles()
                    for tile in adjacent_tiles:
                        to_visit.append(tile)
                    
            if lake_tiles:
                lake_height = min([Tile.all[x][y].height for x, y in lake_tiles])
                for x, y in lake_tiles:
                    WaterTile.fix_tile(x, y, lake_height*2)
                lakes.append(lake_tiles)
        return lakes
                

        # condition = lambda p: Tile.all[p[0]][p[1]] is WaterTile
        # max_size = random.randint(1, LAKE_MAX_SIZE)
        # visited = []
        # to_visit = [(x, y)]
        # lake_tiles = []

        # while len(to_visit) > 0:
        #     point = to_visit.pop(0)
        #     x, y = point
        #     visited.append(point)
        #     if Tile.all[x][y].height <= height:
        #         lake_tiles.append(point)
        #         if len(lake_tiles) >= max_size:
        #             break

        #         adjacent = Tile.all[x][y].get_adjacent_tiles(lambda point: len(list(filter(condition, Tile.all[x][y].get_adjacent_tiles())))==0)
        #         for tile in adjacent:
        #             if tile not in visited and tile not in to_visit:
        #                 to_visit.append(tile)
        # return lake_tiles


    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.name}, {len(self.tiles)} tiles)"


# Source, ending?
class River(Area):
    names = NAMES['River']
    def __init__(self, tiles) -> None:
        super().__init__(tiles)
        self.length = len(tiles)

class Sea(Area):
    names = NAMES['Sea']
    def __init__(self, tiles) -> None:
        super().__init__(tiles)

class Lake(Area):
    names = NAMES['Lake']
    def __init__(self, tiles) -> None:
        super().__init__(tiles)

class Continent(Area):
    names = NAMES['Continent']
    def __init__(self, tiles) -> None:
        super().__init__(tiles)

class Island(Area):
    names = NAMES['Island']
    def __init__(self, tiles) -> None:
        super().__init__(tiles)

# Peaks?
class Mountain(Area):
    names = NAMES['Mountain']
    def __init__(self, tiles) -> None:
        super().__init__(tiles)