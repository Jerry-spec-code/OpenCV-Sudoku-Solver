import os 
import cv2 as cv
import numpy as np 
from skimage.segmentation import clear_border
from PIL import Image

digits = [
    'One.png',
    'Two.png',
    'Three.png',
    'Four.png',
    'Five.png',
    'Six.png',
    'Seven.png',
    'Eight.png',
    'Nine.png'
]

# Predicts similarity between cell and other images based on mean squared error 
# Returns -1 if digit is not readable or if min error is the same across multiple digits
def predict(cell, debug=False):
    # Locates the uploaded image. 
    if debug:
        parent = os.getcwd()
    else:
        parent = os.path.join(os.getcwd(), 'model')
    target = os.path.join(parent, 'digits')
    # Initalize a list of errors 
    errors = []
    for filename in digits: 
        # Reads each digit 
        digit = cv.imread("/".join([target, filename]))
        #Convert digit from (64, 64, 3) to (64, 64)
        digit = adjustShape(digit)
        # apply automatic thresholding to the cell and then clear any
        # connected borders that touch the border of the cell
        thresh = cv.threshold(digit, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
        digit = clear_border(thresh)
        # Calculates mean squared error 
        err = np.sum((digit.astype("float") - cell.astype("float")) ** 2)
        err /= float(digit.shape[0] * digit.shape[1])
        # err = (whiteArea(digit) - whiteArea(cell)) ** 2
        errors.append(err)
    
    minErrorDigit = -1 # Default value 

    # Determines which digit has minimum mean squared error
    for i, err in enumerate(errors):
        if i == 0 or (minError > err and err >= 0):
            minErrorDigit = i + 1
            minError = err 
        elif err < 0:
            return -1 

 
    return minErrorDigit 

#Convert digit from (64, 64, 3) to (64, 64)
def adjustShape(digit):
    newDigit = []
    for firstArray in digit:
        temp = []
        for secondArray in firstArray: 
            temp += [elem for elem in secondArray]
        newDigit.append(temp)
    return np.array(newDigit)

def whiteArea(img):
    count = 0
    for i in range(0, len(img)):
        for j in range(0, len(img[i])):
            if img[i][j] > 0:
                count += 1
    
    return count 

def printDefaultArrays(debug=True):
    if debug:
        parent = os.getcwd()
    else:
        parent = os.path.join(os.getcwd(), 'model')
    target = os.path.join(parent, 'digits')
    # Initalize a list of errors 
    errors = []
    for filename in digits: 
        # Reads each digit
        print(filename) 
        digit = cv.imread("/".join([target, filename]))
        digit = adjustShape(digit)
        print(digit.shape)
        print(digit)
    
def display(msg, img):
    cv.imshow(msg, img)
    cv.waitKey(0)