__author__ = 'Harriet'

from PIL import Image

# The number of colour components, in this case, 3 - red, green and blue
NUMBER_OF_COLOR_COMPONENTS = 3

def getImage(file):
    img = Image.open(file)
    return img


def createColor(red, green, blue):
    newColor = [red, green, blue]
    return newColor


def assignColor(color):
    color = (color[0], color[1], color[2])
    return color


# Changes colour of each pixel to the dominant colour
# component, above a given threshold
def changeToDominantColor(img, chosenColorIndex, minThreshold=50):
    pixels = img.load()

    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            currentPixel = pixels[x,y]
            canChange = True

            for componentIndex in range(NUMBER_OF_COLOR_COMPONENTS):

                currentComponentValue = currentPixel[componentIndex]
                componentBeingChecked = currentPixel[chosenColorIndex]

                if componentIndex != chosenColorIndex:
                    if (currentComponentValue >= componentBeingChecked * 0.9):
                        canChange = False
                elif currentComponentValue <= minThreshold:
                    canChange = False

            if canChange:
                newColor = createColor(0,0,0)
                newColor[chosenColorIndex] = 255
                pixels[x,y] = assignColor(newColor)


# Changes colour of any pixel in the image
# that isn't purely red, green or blue to black
def changeRestToBlack(img):
    pixels = img.load()
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            currentPixel = pixels[x,y]
            if not (currentPixel == (255,0,0) or
                    currentPixel == (0,255,0) or
                    currentPixel == (0,0,255)):
                pixels[x,y] = (0,0,0)


# Changes pixels with a colour component above a given threshold to
# be purely the colour component with the highest value, then
# changes every other colour to black.
def changeHighColors(file="jegermeister.jpg"):
    img = getImage(file)
    for i in range(NUMBER_OF_COLOR_COMPONENTS):
        changeToDominantColor(img,i)
    changeRestToBlack(img)

    newFileName = "changeHighColours " + file
    img.show()
    img.save(newFileName)


changeHighColors()