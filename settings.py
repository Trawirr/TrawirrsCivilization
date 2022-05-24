import numpy as np
import os

GRID_SIZE = 100
OCTAVES = [3, 6, 18, 24]

HEIGHT_COLORS = [
    [-1.0, np.array([0,0,0])/255],
    [0, np.array([0,0,255])/255],
    [0, np.array([0,255,0])/255],
    [.3, np.array([255,255,0])/255],
    [.4, np.array([255,70,0])/255],
    [1.0, np.array([0,0,0])/255]
]

WATER_COLORS = [
    [-1.0, np.array([0,0,0])],
    [0, np.array([0,0,255])],
    [1.0, np.array([0,150,255])]
]

LAND_COLORS = [
    [0, np.array([0,255,0])],
    [.3, np.array([255,255,0])],
    [.4, np.array([255,70,0])],
    [1.0, np.array([0,0,0])]
]
LAKE_MAX_NUMBER = 12

LAKE_COLOR = np.array([0,100,255])/255
RIVER_COLOR = np.array([0,0,255])/255

LAKE_MAX_SIZE = 40
ISLAND_MAX_SIZE = 100
RIVER_LAKE_SIZES = (4, 15)

NAMES = {}
for filename in os.listdir('names'):
    filepath = os.path.join('names', filename)
    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            key = filename.split('.')[0]
            NAMES[key] = [name.strip() for name in f.readlines()]

WIDTH = 1080
HEIGHT = 720

TILE_SIZE = 5