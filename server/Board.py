from typing import Type, List, Set
from Status import Status
from Cell import Cell

class Board:
    def __init__(self, board):
        self.rows = len(board)
        self.cols = len(board[0])
        self.board = [[Cell(board[i][j], i, j) for j in range(self.cols)] for i in range(self.rows)]
        self.initialize_neighbours(self.board)

    def initialize_neighbours(self, board : List[List['Cell']]):
        for i in range(self.rows):
            for j in range(self.cols):
                for k in range(self.rows):
                    for l in range(self.cols):
                        if (i, j) != (k, l):
                            board[i][j].add_neighbour(board[k][l])
    
    # copied original_board into new_board
    def copy_board(self, original_board : List[List['Cell']]):
        new_board = [[Cell(original_board[i][j].value, i, j) for j in range(self.cols)] for i in range(self.rows)]
        self.initialize_neighbours(new_board)
        self.copy_possible(original_board, new_board)
        return new_board
    
    def copy_possible(self, original_board : List[List['Cell']], new_board : List[List['Cell']]):
        for i in range(self.rows):
            for j in range(self.cols):
                new_board[i][j].possible = set(original_board[i][j].possible)

    def solve(self):
        logic_functions = [
            self.get_status,
            self.logic_cycle_one,
            self.logic_cycle_two,
            self.guesser,
        ]

        status = Status.INCOMPLETE
        for logic_function in logic_functions:
            status = logic_function()
            if status != Status.INCOMPLETE:
                break

        return status
    
    def get_board_numbers(self):
        return [[self.board[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # An empty cell is a value if it cannot be any other value 
    def logic_cycle_one(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cur_cell = self.board[i][j]
                if cur_cell.value != 0:
                    self.remove_possibility_from_neighbours(cur_cell)
        
        return self.get_status()
    
    def remove_possibility_from_neighbours(self, cur_cell : Type['Cell']):
        neighbours_sets : List[Set['Cell']] = cur_cell.get_neighbours_sets()
        for neighbours_set in neighbours_sets:
            for cell in neighbours_set:
                cell.remove_possible(cur_cell.value)
                if cell.only_one_possible():
                    cell.value = cell.get_possible_value()
                    self.remove_possibility_from_neighbours(cell)


    # An empty cell is a value if no other neighbour of the same type is that value
    def logic_cycle_two(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cur_cell = self.board[i][j]
                if cur_cell.value == 0:
                    for possible in cur_cell.possible:
                        if not cur_cell.possible_exists_in_all_neighbour_types(possible):
                            cur_cell.value = possible
                            self.remove_possibility_from_neighbours(cur_cell)
                            break
        
        return self.get_status()

    # Makes a guess and backtracks
    def guesser(self):
        buckets = self.bucket_sort_empty_cells_by_possibilities()
        for bucket in buckets:
            for (i, j) in bucket:
                cur_cell : Cell = self.board[i][j]
                if cur_cell.value == 0:
                    old_board : List[List['Cell']] = self.copy_board(self.board)
                    possible_list = list(cur_cell.possible)
                    for possible in possible_list:
                        cur_cell.value = possible
                        old_board[i][j].remove_possible(possible) # Since we are going to guess it
                        status = self.solve()
                        if status == Status.MULTIPLE:
                            return status
                        if status == Status.COMPLETE: # First valid guess
                            return self.check_multiple_solutions(old_board)
                        self.board = self.copy_board(old_board)
                    
                    return Status.INVALID
                    
        return self.get_status()

    def bucket_sort_empty_cells_by_possibilities(self):
        buckets = [[] for _ in range(10)]
        for i in range(self.rows):
            for j in range(self.cols):
                cur_cell = self.board[i][j]
                if cur_cell.value == 0:
                    buckets[len(cur_cell.possible)].append((i, j))
        return buckets

    def check_multiple_solutions(self, old_board):
        possible_board = self.copy_board(self.board)
        self.board = self.copy_board(old_board)
        status = self.solve()
        if status == Status.INVALID:
            self.board = self.copy_board(possible_board)
            return Status.COMPLETE
        
        return Status.MULTIPLE

    def get_status(self):
        has_empty_cell = False
        for i in range(self.rows):
            for j in range(self.cols):
                cur_cell = self.board[i][j]
                if cur_cell.value == 0:
                    if len(cur_cell.possible) == 0:
                        return Status.INVALID
                    has_empty_cell = True
                    continue
                neighbours_sets : List[Set['Cell']] = cur_cell.get_neighbours_sets()
                for neighbours_set in neighbours_sets:
                    for cell in neighbours_set:
                        if cell.value == cur_cell.value:
                            return Status.INVALID
        
        return Status.INCOMPLETE if has_empty_cell else Status.COMPLETE
