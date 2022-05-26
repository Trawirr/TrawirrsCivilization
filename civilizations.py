from settings import *

class Civilization:
    names = NAMES['Tribe']
    all = []
    def __init__(self) -> None:
        self.__name = self.names.pop(0)
        Civilization.all.append(self)

    