import numpy as np

SIZE_TILES = (100, 100)

HEIGHT_COLORS = [
    [-1.0, np.array([0,0,0])/255],
    [0, np.array([0,0,255])/255],
    [0, np.array([0,255,0])/255],
    [.3, np.array([255,255,0])/255],
    [.4, np.array([255,70,0])/255],
    [1.0, np.array([0,0,0])/255]
]

LAKE_MAX_SIZE = 40
ISLAND_MAX_SIZE = 100