__author__ = 'Harriet'

import Image


def getImage(file):
    img = Image.open(file)
    return img


# Changes colour of each pixel to the dominant colour
# component, above a given threshold
def changeToColor(img, colourIndex, minThreshold=50):
    pixels = img.load()
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            currentPixel = pixels[x,y]
            canChange = True

            for component in range(0,3):
                if component != colourIndex:
                    if currentPixel[component] >= currentPixel[colourIndex] * 0.9:
                        canChange = False
                elif currentPixel[colourIndex] <= minThreshold:
                    canChange = False

            if canChange:
                newColor = [0, 0, 0]
                newColor[colourIndex] = 255
                currentPixel = (newColor[0], newColor[1], newColor[2])
                pixels[x,y] = currentPixel


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
    img.save("changeHighColors " + file)


changeHighColors()