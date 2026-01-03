class Success:
    def __init__(self, status='success', valid=False, original=[[0 for _ in range(9)] for _ in range(9)], 
                 solution=[[0 for _ in range(9)] for _ in range(9)], updates=[], message=''):
        self.status = status
        self.valid = valid
        self.original = original
        self.solution = solution
        self.updates = updates
        self.message = message

    def to_dict(self):
        return {
            'status': self.status,
            'valid': self.valid,
            'original': self.original,
            'solution': self.solution,
            'updates': self.updates,
            'message': self.message
        }

class Error:
    def __init__(self, status='fail', error=''):
        self.status = status
        self.error = error

    def to_dict(self):
        return {
            'status': self.status,
            'error': self.error,
        }
