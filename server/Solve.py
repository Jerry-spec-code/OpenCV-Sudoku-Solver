import model.ReadImage as r 
import os
import shutil

from Board import Board
from Status import Status
from Response import Success

def image_solve(filename):
    board = r.readImage(filename).tolist()
    if len(board) == 1:
        return Success(message='Unreadable image')

    result = grid_solve(board)
    if not result.valid:
        result.solution = board
        result.message += ' But here is the interpretation of the image! Edit the board as you see fit'
        result.valid = True
    return result

def grid_solve(board):
    board_obj = Board(board)
    status = board_obj.solve()
    message = get_message(status)
    valid = Status != Status.INVALID
    solution = board_obj.get_board_numbers()
    result = Success(valid=valid, solution=solution, message=message)
    return result

def get_message(status):
    message_dict = {
        Status.COMPLETE: 'Here is the solved puzzle:',
        Status.INVALID: 'Invalid puzzle!',
        Status.MULTIPLE: 'This puzzle has multiple solutions. Here is one solution:'
    }
    return message_dict[status] if status in message_dict else 'Unknown Error During Solve'

def get_target_path():
    parent = os.path.join(os.getcwd(), 'model')
    target = os.path.join(parent, 'src')
    if not os.path.isdir(target):
        os.mkdir(target)
    
    else:
        shutil.rmtree(target)
        os.mkdir(target)
    
    return target
