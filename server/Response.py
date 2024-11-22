class Success:
    def __init__(self, status='success', valid=False, solution=[[0 for _ in range(9)] for _ in range(9)], message=''):
        self.status = status
        self.valid = valid
        self.solution = solution
        self.message = message

    def to_dict(self):
        return {
            'status': self.status,
            'valid': self.valid,
            'solution': self.solution,
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
