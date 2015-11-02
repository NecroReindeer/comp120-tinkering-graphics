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


# Makes a copy of the image and randomly shuffles all of its pixels
def getShuffledImage(img):
    originalImg = img
    newImg = img
    originalPixels = originalImg.load()
    shuffledPixels = newImg.load()

    listOfPixels = addPixelsToList(img)
    random.shuffle(listOfPixels)

    for x in range(getWidth(img)):
        for y in range(getHeight(img)):
            pixelToMove = originalPixels[x,y]
            targetPixel = listOfPixels.pop()
            shuffledPixels[targetPixel[0], targetPixel[1]] = pixelToMove


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


# Changes colour of each pixel to the dominant colour
# component, above a given threshold
def changeToDominantColor(img, chosenColorIndex, minThreshold):
    pixels = img.load()
    targetColors = [RED, GREEN, BLUE]

    for x in range(getWidth(img)):
        for y in range(getHeight(img)):
            currentPixel = pixels[x,y]
            canChange = checkDominantColor(currentPixel, chosenColorIndex, minThreshold)

            if canChange:
                pixels[x,y] = targetColors[chosenColorIndex]


# Changes colour of any pixel in the image
# that isn't purely red, green or blue to black
def changeRestToBlack(img):
    pixels = img.load()
    for x in range(0, getWidth(img)):
        for y in range(0, getHeight(img)):
            currentPixel = pixels[x,y]
            if not (currentPixel == RED or
                    currentPixel == GREEN or
                    currentPixel == BLUE):
                pixels[x,y] = BLACK


# Changes pixels with a colour component above a given threshold to
# be purely the colour component with the highest value, then
# changes every other colour to black.
def emphasiseColors(minThreshold=50, file="jegermeister.jpg"):
    img = getImage(file)
    for i in range(NUMBER_OF_COLOR_COMPONENTS):
        changeToDominantColor(img, i, minThreshold)
    changeRestToBlack(img)
    img.show()
    newFileName = "emphasiseColors " + file
    img.save(newFileName)


# Randomly shuffles every single pixel in an image
def shufflePixels(file="sad.jpg"):
    img = getImage(file)
    getShuffledImage(img)
    img.show()
    newFileName = "shufflePixels " + file
    img.save(newFileName)


emphasiseColors()
shufflePixels()