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


# Returns distance between 2 coordinates as a float
def getDistance(firstPoint, secondPoint):
    xDistance = secondPoint[0] - firstPoint[0]
    yDistance = secondPoint[1] - firstPoint[1]
    distance = math.sqrt(xDistance**2.0 + yDistance**2.0)
    return distance

def showGallery():

    hugPainting = Painting("hug.png")
    dotEffect = DotEffect( 10, 5, BLACK)
    dotEffect.convertToDots(hugPainting)
    hugPainting.show()

    sadPainting = Painting("sad.jpg")
    shuffleEffect = ShuffleEffect(10, 3)
    shuffleEffect.shuffleImage(sadPainting)
    sadPainting.show()

    newColors = [(255, 0, 255),
                 (255, 255, 0),
                 (0, 255, 255)]

    jegermeisterPainting = Painting("jegermeister.jpg")
    colorChangeEffect = ThreeColorEffect(50, newColors)
    colorChangeEffect.replaceDominantColors(jegermeisterPainting)
    jegermeisterPainting.show()


class Painting():
    def __init__(self, img):
        if isinstance(img, str):
            self.img = Image.open(img)
        else:
            self.img = img
        self.pixels = self.img.load()
        self.width, self.height = self.img.size
        self.mode = self.img.mode

    @property
    def img(self):
        return self.img

    @img.setter
    def img(self, newImg):
        self.img = newImg
        self.pixels = self.img.load
        self.width, self.height = self.img.size
        self.mode = self.img.mode

    def show(self):
        self.img.show()

    def copy(self):
        copy = self.img.copy()
        return copy

    def setPixel(self, coordinates, color):
        self.pixels[coordinates] = color

    def getPixel(self, coordinates):
        return self.pixels[coordinates]

    def clearImage(self, color):
        newImage = Image.new(self.mode, (self.width, self.height), color)
        self.img = newImage

    # Returns a list of pixel coordinates contained in a square of
    # specified size around a central point
    def getSquare(self, centre, width, height):
        pixelSquare = []

        startX = centre[0] - width/2
        endX = centre[0] + width/2

        startY = centre[1] - height/2
        endY = centre[1] + height/2

        for x in range(startX, endX):
            for y in range(startY, endY):
                if 0 < x < self.width and 0 < y < self.height:
                    pixelSquare.append((x,y))
        return pixelSquare


class DotEffect():
    def __init__(self, radius, gap, background):
        self.radius = radius
        self.diameter = self.radius * 2
        self.gap = gap
        self.background = background

    # Converts an image to be made up of circles of a given radius with
    # the colour of the pixel at the centre of the circle
    def convertToDots(self, painting):
        if (self.diameter + self.gap) % 2 != 0:                             #To account for rounding errors with ints
            squareSize = self.diameter + self.gap + 1
        else:
            squareSize = self.diameter + self.gap
        firstCircleCentre = squareSize / 2                                  # So circles on top edge are fully visible

        canvas = Image.new(painting.mode, (painting.width, painting.height), self.background)
        canvas = Painting(canvas)

        for x in range(firstCircleCentre, painting.width, squareSize):
            for y in range(firstCircleCentre, painting.height, squareSize):
                centre = x, y
                box = painting.getSquare(centre, squareSize, squareSize)
                centreColor = painting.getPixel(centre)

                for pixel in box:
                    distanceFromCentre = getDistance(pixel, centre)
                    if distanceFromCentre < self.radius:                    # Because every point on circumference
                        canvas.setPixel(pixel, centreColor)                 # of circle is equal distance from the
        painting.img = canvas.img                                           # centre


class ShuffleEffect():
    def __init__(self, shuffleStep, randomness):
        self.shuffleStep = shuffleStep
        self.randomness = randomness

    # Returns a random length to be used for sides of square.
    # Squares are random size so that the picture looks less
    # uniform and grid-like
    def getRandomSquareSize(self):
        squareSize = random.randrange(self.shuffleStep,
                                      self.shuffleStep * self.randomness)
        return squareSize

    # Makes a copy of the image and randomly shuffles its pixels with
    # nearby pixels
    def shuffleImage(self, painting):
        originalPainting = Painting(painting.copy())
        for x in range(0, painting.width, self.shuffleStep):
            for y in range(0, painting.height, self.shuffleStep):
                currentCoordinates = (x,y)
                squareSize = self.getRandomSquareSize()
                pixelSquare = originalPainting.getSquare(currentCoordinates,
                                                         squareSize, squareSize)
                shuffledPixelSquare = pixelSquare
                random.shuffle(shuffledPixelSquare)

                for pixel in pixelSquare:
                    pixelToMove = originalPainting.getPixel(pixel)
                    pixelToBeReplaced = shuffledPixelSquare.pop()
                    painting.setPixel(pixelToBeReplaced, pixelToMove)


class ThreeColorEffect():
    def __init__(self, threshold, replacementColors):
        self.threshold = threshold
        self.replacementColors = replacementColors

    # Changes pixels with a colour component above a given threshold to
    # a specified colour, then changes every other colour to black.
    def replaceDominantColors(self, painting):

        for i in range(NUMBER_OF_COLOR_COMPONENTS):
            self.changeDominantColor(i, painting)
        self.changeRestToBlack(painting)

    # Checks if the chosen colour component of a pixel is
    # greater than the other two components and above
    # the given minimum threshold
    def checkDominantColor(self, pixel, targetComponentIndex, minThreshold):
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
    def changeDominantColor(self, chosenColorIndex, painting):

        for x in range(painting.width):
            for y in range(painting.height):
                currentCoordinate = x, y
                currentPixel = painting.getPixel(currentCoordinate)
                canChange = self.checkDominantColor(currentPixel,
                                                    chosenColorIndex, self.threshold)

                if canChange:
                    painting.setPixel(currentCoordinate, self.replacementColors[chosenColorIndex])

    # Changes colour of any pixel in the image
    # that isn't one of the specified colours to black
    def changeRestToBlack(self, painting):
        for x in range(painting.width):
            for y in range(painting.height):
                currentCoordinate = x, y
                currentPixel = painting.getPixel(currentCoordinate)
                if currentPixel not in self.replacementColors:
                    painting.setPixel(currentCoordinate, BLACK)


showGallery()