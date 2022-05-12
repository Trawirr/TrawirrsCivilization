import random

class NameGenerator:
    def __init__(self) -> None:
        self.names = {}
        for area_type in ['lakes', 'seas', 'rivers', 'continents', 'islands', 'mountains', 'towns']:
            with open(f"names/{area_type}.txt") as f:
                self.names[area_type] = [name.strip() for name in f.readlines()]

    def generate_name(self, area_type):
        picked_index = random.randint(0, len(self.names[area_type])-1)
        return self.names[area_type].pop(picked_index)

