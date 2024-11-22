import os 
import cv2 as cv
import numpy as np 
import imutils
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import model.Model as model 

debug = False  

def readImage(filename):
    try:
        # Locates the uploaded image. 
        parent = os.path.join(os.getcwd(), 'model')
        target = os.path.join(parent, 'src')
        img = cv.imread("/".join([target, filename]))
        return findBoard(img)
    
    except Exception as e:
        print(e)
        return [False]

def findBoard(img):
    # Convert to grayscale mode 
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Removes noise in the image 
    bfilter = cv.bilateralFilter(gray, 13, 20, 20)
    #Detect edges in the image.
    edged = cv.Canny(bfilter, 13, 180)
    #Detect all the continuous points within the edges 
    keypoints = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(imutils.grab_contours(keypoints), key=cv.contourArea, reverse=True)
    # initialize a contour that corresponds to the puzzle outline
    location = None 
    # Finds rectangular contour
    for contour in contours:
        # approximate the contour
        approx = cv.approxPolyDP(contour, 0.02 * cv.arcLength(contour, True), True)
        # if our approximated contour has four points, then we can
		# assume we have found the outline of the puzzle
        if len(approx) == 4:
            location = approx
            break
    
    if location is None:
        return [False]
    
    # apply a four point perspective transform to both the original
	# image and grayscale image to obtain a top-down bird's eye view
	# of the puzzle
    warped = four_point_transform(gray, location.reshape(4, 2))

    if debug:
        display('Warped', warped)

    return localize(warped)

def localize(img):
    board = np.zeros([9, 9], dtype="int")
    # divide the warped image into a 9x9 grid
    stepX = img.shape[1] // 9
    stepY = img.shape[0] // 9

    # Get the photo for each cell to train the model
    cells = []
    for y in range(0, 9):
        row = []
        for x in range(0, 9):
            # compute the starting and ending (x, y)-coordinates of the current cell
            startX = x * stepX
            startY = y * stepY
            endX = (x + 1) * stepX
            endY = (y + 1) * stepY
            cell = cv.resize(img[startY:endY, startX:endX], (192, 64))
            # apply automatic thresholding to the cell and then clear any
	        # connected borders that touch the border of the cell
            thresh = cv.threshold(cell, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
            thresh = clear_border(thresh)
            row.append(thresh) 
        cells.append(row)
    
    if debug:
        for i in range(0, 9): 
            for j in range(0, 9):
                display('Cell: ' + str(existsDigit(cells[i][j])), cells[i][j])

    for i in range(0, 9):
        for j in range(0, 9):
            #Checks if the image contains a digit 
            isDigit = existsDigit(cells[i][j])
            if isDigit: 
                # Predicts the value of the digit 
                # saveDigitAsImage(cells[i][j], i, j)
                board[i][j] = model.predict(cells[i][j], debug=debug)
                if board[i][j] == -1: #Unreadable digit 
                    return [False]

    if debug:
        print(board)
        
    return board.astype(int)

def existsDigit(cell): 
    # find contours in the thresholded cell
    cnts = cv.findContours(cell.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Returns true if there is a digit, false otherwise. 
    return not len(cnts) == 0 

def saveDigitAsImage(cell, i, j):
    parent = os.path.join(os.getcwd(), 'model')
    target = os.path.join(parent, 'data', 'processed', 'pending')
    filename = str(i) + str(j) + '.png'
    cv.imwrite("/".join([target, filename]), cell)


def display(msg, img):
    cv.imshow(msg, img)
    cv.waitKey(0)
