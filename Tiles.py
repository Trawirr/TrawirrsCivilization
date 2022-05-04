class TerrainTile:
    def __init__(self, height) -> None:
        self.height = height

    def __getitem__(self, item):
        if item == 'height':
            return self.height

class SeaTile(TerrainTile):
    def __init__(self, height) -> None:
        super().__init__(height)

class RiverTile(TerrainTile):
    def __init__(self, height) -> None:
        super().__init__(height)
        # self.source = source
        # self.tiles = [source]

class LakeTile(TerrainTile):
    def __init__(self, height) -> None:
        super().__init__(height)