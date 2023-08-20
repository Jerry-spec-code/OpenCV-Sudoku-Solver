from re import S
import jpype
import jpype.imports
from jpype import JClass
import model.ReadImage as r 
import os
import shutil

class Solution():
    def __init__(self, valid=False, solution=[[0] * 9 for _ in range(9)], message=''):
        self.valid = valid
        self.solution = solution
        self.message = message


def imageSolve(filename):
    read = r.readImage(filename)
    if len(read) == 1:
        return Solution(message = 'Unreadable image')

    writeToFile(read, 'board.txt')
    result = javaSolve()
    if not result.valid:
        result.solution = read.tolist()
        result.message += ' But here is the interpretation of the image! Edit the board as you see fit'
        result.valid = True
    return result

def gridSolve(inputList): 
    writeToFile(inputList, 'board.txt')
    return javaSolve()

def writeToFile(inputList, filename):
    with open(filename, 'w') as f:
        for row in inputList:
            for elem in row:
                f.write(str(elem) + " ")
            f.write("\n")
        
    f.close()

# Calls the java code 
def javaSolve():
    if not jpype.isJVMStarted():
        jpype.startJVM(convertStrings=False)
    solver = JClass('App')
    solver.main(['arg'])
    return readFromFile('answer.txt')

def readFromFile(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file: 
            temp = []
            for word in line.split(' '):
                if validPhrase(word):
                    temp.append(word.strip())
            data.append(temp)

    status = getStatus()
    
    return Solution(message = getMessage(status)) if status == 'invalid' else Solution(valid = True, solution = data, message = getMessage(status))

def getMessage(status):
    if status == 'complete':
        return 'Here is the solved puzzle:'

    elif status == 'invalid':
        return 'Invalid puzzle!'
    
    return 'This puzzle has multiple solutions. Here is one solution:'

def getStatus():
    with open('status.txt', 'r') as file:
        for line in file: 
            for word in line.split(' '):
                return word 

def validPhrase(word):
    for letter in word:
        if letter != ' ' and letter != '\n':
            return True
    
    return False

def getTargetPath():
    parent = os.path.join(os.getcwd(), 'model')
    target = os.path.join(parent, 'src')
    if not os.path.isdir(target):
        os.mkdir(target)
    
    else:
        shutil.rmtree(target)
        os.mkdir(target)
    
    return target