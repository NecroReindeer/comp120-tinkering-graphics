__author__ = 'Harriet'

from PIL import Image


def getImage(file):
    img = Image.open(file)
    return img


def createColor(red, green, blue):
    newColor = [red, green, blue]
    return newColor


def assignColor(pixel, color):
    pixel = (color[0], color[1], color[2])
    return pixel



# Changes colour of each pixel to the dominant colour
# component, above a given threshold
def changeToColor(img, chosenColorIndex, minThreshold=50):

    NUMBER_OF_COMPONENTS = 3
    pixels = img.load()

    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            currentPixel = pixels[x,y]
            canChange = True

            for componentIndex in range(NUMBER_OF_COMPONENTS):

                currentComponentValue = currentPixel[componentIndex]
                chosenComponentValue = currentPixel[chosenColorIndex]

                if componentIndex != chosenColorIndex:
                    if (currentComponentValue >=
                            chosenComponentValue * 0.9):
                        canChange = False
                elif currentComponentValue <= minThreshold:
                    canChange = False

            if canChange:
                newColor = createColor(0,0,0)
                newColor[chosenColorIndex] = 255
                newPixel = assignColor(currentPixel, newColor)
                pixels[x,y] = newPixel


# Changes colour of any pixel in the image
# that isn't purely red, green or blue to black
def changeRestToBlack(img):
    pixels = img.load()
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            if not (pixels[x,y] == (255, 0, 0) or
                    pixels[x,y] == (0, 255, 0) or
                    pixels[x,y] == (0, 0, 255)):
                pixels[x,y] = (0, 0, 0)


# Changes pixels with a colour component above a given threshold to
# be purely the colour component with the highest value, then
# changes every other colour to black.
def changeHighColors(file="jegermeister.jpg"):
    img = getImage(file)
    numberOfColorComponents = 3
    for i in range(0,numberOfColorComponents):
        changeToColor(img,i)
    changeRestToBlack(img)

    newFileName = "changeHighColours " + file
    img.show()
    img.save(newFileName)

changeHighColors()