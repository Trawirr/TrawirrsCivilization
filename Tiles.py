from settings import *

class TerrainTile:
    def __init__(self, height) -> None:
        self.height = height
        self.attributes = {}
        

    def __getitem__(self, item):
        if item == 'height':
            return self.height

    def set_attribute(self, key, value):
        self.attributes[key] = value

    def add_attribute(self, key, value):
        if self.attributes[key]:
            self.attributes[key].append(value)
        else:
            self.attributes[key] = [value]

class WaterTile(TerrainTile):
    def __init__(self, height) -> None:
        super().__init__(height)
        self.owner = None
        self.food = 0
        self.production = 0

    def pick_color(self):
        for i, (h, _) in enumerate(WATER_COLORS):
                if h >= self.height:
                    (h1, color1), (h2, color2) = WATER_COLORS[i-1], WATER_COLORS[i]
                    break
        return color1 + (color2 - color1) * (self.height - h1) / (h2 - h1)

class LandTile(TerrainTile):
    def __init__(self, height) -> None:
        super().__init__(height)

    def pick_color(self):
        for i, (h, _) in enumerate(LAND_COLORS):
                if h >= self.height:
                    (h1, color1), (h2, color2) = LAND_COLORS[i-1], LAND_COLORS[i]
                    break
        return color1 + (color2 - color1) * (self.height - h1) / (h2 - h1)