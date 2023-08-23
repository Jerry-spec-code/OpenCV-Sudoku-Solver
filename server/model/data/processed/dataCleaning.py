import os

def main():
    # clear()
    movePending()
    renameData()

def movePending():
    file = 'input.txt'
    nums = readLines(file)
    nums = list(map(strip, nums))
    emptyPendingFolder(nums)

def renameData():
    hashmap = {}
    digits = [
        'One',
        'Two',
        'Three',
        'Four',
        'Five',
        'Six',
        'Seven',
        'Eight',
        'Nine'
    ]
    for i in range(1, 10):
        hashmap[i] = digits[i - 1]
        target = os.path.join(os.getcwd(), str(i))
        sortedFiles = sorted(os.listdir(target))
        indexToStart = 0
        for file in sortedFiles:
            if digits[i - 1] in file:
                indexToStart += 1
        for file in sortedFiles:
            if digits[i - 1] in file:
                continue
            os.system('mv ' + str(i) + '/' + file + ' ' + str(i) + '/' + digits[i - 1] + str(indexToStart) + '.png')
            indexToStart += 1

def clear():
    empty1To9()

def readLines(file):
    with open(file, 'r') as f:
        return f.readlines()

def strip(num):
    return num.strip()

def emptyPendingFolder(nums):
    target = os.path.join(os.getcwd(), 'pending')
    numIndex = 0
    sortedFiles = sorted(os.listdir(target))
    for file in sortedFiles:
        cmd = 'cp pending/' + file + ' ' + nums[numIndex]
        os.system(cmd)
        numIndex += 1
    os.system('rm pending/*')

def empty1To9():
    for i in range(1, 10):
        os.system('rm -r ' + str(i) + ' && mkdir ' + str(i))

if __name__ == '__main__':
    main()