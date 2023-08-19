from re import S
import jpype
import jpype.imports
from jpype import JClass
import model.ReadImage as r 
import os
import shutil

def solve(filename):
    read = r.myImageRead(filename)
    if len(read) == 1:
        return [False, 'Unreadable image']

    writeToFile(read, 'board.txt')
    result = javaSolve()
    if not result[0]:
        result.insert(1, read)
        result[2] += ' But here is the interpretation of the image! '
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
    return myRead('answer.txt')

def myRead(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file: 
            temp = []
            for word in line.split(' '):
                if validPhrase(word):
                    temp.append(word.strip())
            data.append(temp)

    status = getStatus()
    
    if status == 'invalid':
        return [False, 'Invalid puzzle!']

    return [True, data, getMessage(status)]

def getMessage(status):
    if status == 'complete':
        return 'Here is the solved puzzle:'
    
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

def setTargetPath():
    parent = os.path.join(os.getcwd(), 'model')
    target = os.path.join(parent, 'src')
    if not os.path.isdir(target):
        os.mkdir(target)
    
    else:
        shutil.rmtree(target)
        os.mkdir(target)
    
    return target