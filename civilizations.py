from numpy import isin
from settings import *
from Tiles import *

class Civilization:
    names = NAMES['Tribe']
    all = []
    def __init__(self, tiles) -> None:
        self.__name = self.names.pop(0)
        self.__color = np.array(random.choices(range(256), k=3))
        self.__tiles = tiles
        for x, y in tiles:
            Tile.all[x][y].owner = self.__name
        Civilization.all.append(self)

        print(f"New {self.__class__.__name__}: name: {self.__name},  created")

    @property
    def tiles(self):
        return self.__tiles

    @property
    def color(self):
        return self.__color

    @classmethod
    def generate_tribes(cls):
        starting_tiles = []
        min_distance = 10
        while len(starting_tiles) < TRIBES_NUMBER:
            x_random, y_random = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            print(f"Random: {(x_random, y_random)}")
            print(f"{min_distance=}")
            if  isinstance(Tile.all[x_random][y_random], LandTile) and list(filter(lambda xy: Tile.distance(x_random, y_random, xy[0], xy[1]) <= min_distance, starting_tiles)) == []:
                starting_tiles.append((x_random, y_random))
                Civilization([(x_random, y_random)])
                min_distance = 10
            else:
                min_distance = max(2, min_distance-1)
            
        print(f"{starting_tiles=}")

    @classmethod
    def tiles_and_colors(cls):
        tiles_and_colors_list = [(civ.tiles, civ.color) for civ in Civilization.all]
        return tiles_and_colors_list

    

    