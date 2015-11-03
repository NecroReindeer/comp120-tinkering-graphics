__author__ = 'Harriet'

import random
import math

from PIL import Image


# The number of colour components, in this case, 3 (red, green and blue)
NUMBER_OF_COLOR_COMPONENTS = 3

RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


def getImage(file):
    img = Image.open(file)
    return img


def getWidth(img):
    width = img.size[0]
    return width


def getHeight(img):
    height = img.size[1]
    return height


# Returns distance between 2 pixels as a float
def getDistance(firstPoint, secondPoint):
    xDistance = secondPoint[0]-firstPoint[0]
    yDistance = secondPoint[1] - firstPoint[1]
    distance = math.sqrt(xDistance**2.0 + yDistance**2.0)
    return distance


# Adds the coordinates of each pixel in an image to a list
def addPixelsToList(img):
    coordinates = []
    for x in range(0, getWidth(img)):
        for y in range(0, getHeight(img)):
            coordinates.append((x,y))
    return coordinates


# Returns a list of pixel coordinates contained in a square of
# specified size around a central point
def getSquare(img, centre, width, height):
    pixelSquare = []

    startX = centre[0] - width/2
    endX =  centre[0] + width/2

    startY = centre[1] - height/2
    endY = centre[1] + height/2

    for x in range(startX, endX):
        for y in range(startY, endY):
            if 0 < x < getWidth(img) and 0 < y < getHeight(img):
                pixelSquare.append((x,y))
    return pixelSquare



# returns a random length to be used for sides of square
def getRandomSquareSize(shuffleStep, randomness):
    squareSize = random.randrange(shuffleStep, shuffleStep * randomness)
    return squareSize


# Makes a copy of the image and randomly shuffles its pixels with
# nearby pixels
def getShuffledImage(img, shuffleStep, randomness):
    originalImg = img.copy()
    originalPixels = originalImg.load()
    shuffledPixels = img.load()
    width = getWidth(img)
    height = getHeight(img)

    for x in range(0, width, shuffleStep):
        for y in range(0, height, shuffleStep):
            currentCoordinates = [x,y]
            squareSize = getRandomSquareSize(shuffleStep, randomness)
            pixelSquare = getSquare(originalImg, currentCoordinates, squareSize, squareSize)
            shuffledPixelSquare = pixelSquare
            random.shuffle(shuffledPixelSquare)

            for pixel in pixelSquare:
                pixelToMove = originalPixels[pixel]
                pixelToBeReplaced = shuffledPixelSquare.pop()
                shuffledPixels[pixelToBeReplaced[0], pixelToBeReplaced[1]] = pixelToMove


# Randomly shuffles pixels in an image
def shufflePixels(shuffleStep=10, randomness=3, file="sad.jpg"):
    img = getImage(file)
    getShuffledImage(img, shuffleStep, randomness)
    img.show()



# Checks if the chosen colour component of a pixel is
# greater than the other two components and above
# the given minimum threshold
def checkDominantColor(pixel, targetComponentIndex, minThreshold):
    canChange = True
    for componentIndex in range(NUMBER_OF_COLOR_COMPONENTS):
        currentComponentValue = pixel[componentIndex]
        componentBeingChecked = pixel[targetComponentIndex]

        if componentIndex != targetComponentIndex:
            if (currentComponentValue >= componentBeingChecked * 0.9):
                canChange = False
        elif currentComponentValue <= minThreshold:
            canChange = False

    return canChange


# Changes colour of the dominant colour component of each pixel
# to a specified colour, above a given threshold
def changeDominantColor(img, chosenColorIndex, minThreshold, targetColors):
    pixels = img.load()
    for x in range(getWidth(img)):
        for y in range(getHeight(img)):
            currentPixel = pixels[x,y]
            canChange = checkDominantColor(currentPixel, chosenColorIndex, minThreshold)

            if canChange:
                pixels[x,y] = targetColors[chosenColorIndex]


# Changes colour of any pixel in the image
# that isn't one of the specified colours to black
def changeRestToBlack(img, targetColors):
    pixels = img.load()
    for x in range(getWidth(img)):
        for y in range(getHeight(img)):
            currentPixel = pixels[x,y]
            if currentPixel not in targetColors:
                pixels[x,y] = BLACK


# Changes pixels with a colour component above a given threshold to
# a specified colour, then changes every other colour to black.
def replaceDominantColors(minThreshold=50, file="jegermeister.jpg"):
    img = getImage(file)
    replacementForRed = (255, 0, 255)
    replacementForGreen = (0, 255, 255)
    replacementForBlue = (255, 255, 0)
    targetColors = [replacementForRed, replacementForBlue, replacementForGreen]

    for i in range(NUMBER_OF_COLOR_COMPONENTS):
        changeDominantColor(img, i, minThreshold, targetColors)

    changeRestToBlack(img, targetColors)
    img.show()







def drawCircles(file="glasses swap.jpg"):
    img = getImage(file)
    pixels = img.load()
    radius = 7
    gap = 7
    for x in range(0, getWidth(img), radius+gap):
        for y in range(0, getHeight(img), radius+gap):
            centre = [x, y]
            container = getSquare(img, centre, radius*2, radius*2)
            centreColor = pixels[x, y]

            for p in container:
                distanceFromCentre = getDistance(p, centre)
                if distanceFromCentre < radius:
                    pixels[p] = centreColor
                else:
                    pixels[p] = (0, 0, 0)
    img.show()


replaceDominantColors()
shufflePixels()
drawCircles()
