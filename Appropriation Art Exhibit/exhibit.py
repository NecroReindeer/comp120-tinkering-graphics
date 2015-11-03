__author__ = 'Harriet'

import random

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


# Adds the coordinates of each pixel in an image to a list
def addPixelsToList(img):
    coordinates = []
    for x in range(0, getWidth(img)):
        for y in range(0, getHeight(img)):
            coordinates.append((x,y))
    return coordinates



# returns a random length to be used for sides of square
def getRandomSquareSize(shuffleStep, randomness):
    squareSize = random.randrange(shuffleStep, shuffleStep * randomness)
    return squareSize


# returns a list of pixel coordinates contained in a square of random size
# surrounding a given central pixel
def getSquare(width, height, pixelCoordinates, shuffleStep, randomness):
    pixelSquare = []
    squareSize = getRandomSquareSize(shuffleStep, randomness)

    startX = pixelCoordinates[0] - squareSize/2
    endX =  pixelCoordinates[0] + squareSize/2

    startY = pixelCoordinates[1] - squareSize/2
    endY =  pixelCoordinates[1] + squareSize/2

    for x in range(startX, endX):
        for y in range(startY, endY):
            if 0 < x < width and 0 < y < height:
                pixelSquare.append((x,y))
    return pixelSquare


# Makes a copy of the image and randomly shuffles its pixels with
# nearby pixels
def getShuffledImage(img, shuffleStep, randomness):
    originalImg = img
    newImg = img
    originalPixels = originalImg.load()
    shuffledPixels = newImg.load()
    width = getWidth(img)
    height = getHeight(img)

    for x in range(0, width, shuffleStep):
        for y in range(0, height, shuffleStep):
            currentCoordinates = [x,y]
            pixelSquare = getSquare(width, height, currentCoordinates, shuffleStep, randomness)
            shuffledPixelSquare = pixelSquare
            random.shuffle(shuffledPixelSquare)

            for pixel in pixelSquare:
                pixelToMove = originalPixels[pixel]
                targetPixel = shuffledPixelSquare.pop()
                shuffledPixels[targetPixel[0], targetPixel[1]] = pixelToMove


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



replaceDominantColors()
shufflePixels()
