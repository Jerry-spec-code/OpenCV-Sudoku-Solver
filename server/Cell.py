from typing import Type, List, Set

class Cell:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.possible = set([i for i in range(1, 10)]) if value == 0 else set()
        self.row_neighbours = set()
        self.col_neighbours = set()
        self.box_neighbours = set()
    
    def add_possible(self, value):
        self.possible.add(value)
    
    def remove_possible(self, value):
        if value in self.possible:
            self.possible.remove(value)

    def add_neighbour(self, other : Type['Cell']):
        if self.x == other.x:
            self.row_neighbours.add(other)
        if self.y == other.y:
            self.col_neighbours.add(other)
        if self.get_box_number() == other.get_box_number():
            self.box_neighbours.add(other)
    
    def get_box_number(self):
        return (self.x // 3) * 3 + (self.y // 3)
    
    def get_neighbours_sets(self):
        return [self.row_neighbours, self.col_neighbours, self.box_neighbours]
    
    def only_one_possible(self):
        return len(self.possible) == 1

    def get_possible_value(self):
        return self.possible.pop()
    
    def possible_exists_in_all_neighbour_types(self, possible):
        neighbours_sets : List[Set['Cell']] = self.get_neighbours_sets()
        for neighbours_set in neighbours_sets:
            has_possible = False
            for cell in neighbours_set:
                if possible in cell.possible:
                    has_possible = True
                    break
            if not has_possible:
                return False
        return True