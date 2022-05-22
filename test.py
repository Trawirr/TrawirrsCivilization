from Tiles import *
import random

class Testy:
    tiles = []

    def __init__(self) -> None:
        self.id = len(Testy.tiles)
        Testy.tiles.append(self)

    def add_tile(self, another_class):
        self.tiles.append(another_class(random.random()))

    @property
    def attr(self):
        return self._attr

    @attr.setter
    def attr(self, value):
        self._attr = value

    def __repr__(self) -> str:
        return f"Test({self.id})"

def find_name(**kwargs):
    print(kwargs['name'])

# testy = Testy()
# for i in range(5):
#     testy.add_tile(LandTile)

# for tile in Testy.tiles:
#     print(tile['height'], type(tile))

# find_name(name='Kwarg Name')

# Testy.attr = 1
# attr_val = Testy.attr
# print(f"{attr_val=}")
for i in range(5):
    Testy()
print(Testy.tiles)