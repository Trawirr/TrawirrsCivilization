class Terrain:
    def __init__(self, tiles, name):
        self.tiles = tiles
        self.name = name

class River(Terrain):
    def __init__(self, tiles, name) -> None:
        super().__init__(tiles, name)
        self.length = len(tiles)

class Sea(Terrain):
    def __init__(self, tiles, name) -> None:
        super().__init__(tiles, name)

class Lake(Terrain):
    def __init__(self, tiles, name) -> None:
        super().__init__(tiles, name)

class Continent(Terrain):
    def __init__(self, tiles, name) -> None:
        super().__init__(tiles, name)

class Island(Terrain):
    def __init__(self, tiles, name) -> None:
        super().__init__(tiles, name)

class Mountain(Terrain):
    def __init__(self, tiles, name) -> None:
        super().__init__(tiles, name)