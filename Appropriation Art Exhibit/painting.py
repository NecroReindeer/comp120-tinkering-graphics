__author__ = 'Hat'

from PIL import Image

import color
import point

class Painting(object):
    """Store image data so that variables for the data do not
    need to be defined/passed in/to every function that uses them.
    """
    def __init__(self, img):
        """Can take arguments of type Painting, Image.Image or str"""
        self.img = img

    @property
    def img(self):
        return self.__img

    @img.setter
    def img(self, new_image):
        """Set the data relating to the image correctly
        when self.img is set
        """
        if isinstance(new_image, Painting):
            self.__img = new_image.__img
        elif isinstance(new_image, Image.Image):
            self.__img = new_image
        elif isinstance(new_image, str):
            self.__img = Image.open(new_image)
        else:
            raise TypeError("Argument must be Painting, Image.Image or str")

        self.__pixels = self.img.load()
        self.__size = self.img.size
        self.__width = self.size[0]
        self.__height = self.size[1]
        self.__mode = self.img.mode

    @property
    def pixels(self):
        return self.__pixels

    @property
    def size(self):
        return self.__size

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def mode(self):
        return self.__mode

    def show(self):
        """Show the image in default image viewer"""
        self.img.show()

    def copy(self):
        """Return a copy of the Painting instance"""
        return Painting(self.img.copy())

    def save(self, path):
        """Save the image in the location specified by path (path is a string)"""
        self.img.save(path)

    def paste(self, painting, top_left):
        """Paste image from a Painting into this instance of Painting"""
        self.img.paste(painting.img, top_left.coordinates)

    def resize(self, size):
        """Returns a copy of a Painting resized to a specified size"""
        return Painting(self.img.resize(size))

    def set_pixel_color(self, coordinates, color):
        """Set pixel at coordinates to a given color"""
        self.pixels[coordinates.coordinates] = color.color

    def get_pixel_color(self, coordinates):
        """Return the color of the pixel at coordinates"""
        return color.Color(*self.pixels[coordinates.coordinates])

    def clear_image(self, color):
        """Set image to a single color"""
        blank_img = Image.new(self.mode, (self.width, self.height), color.color)
        self.img = blank_img

    def is_in_image(self, point):
        """Checks if the supplied coordinate is within the image"""
        if 0 < point.x < self.width and 0 < point.y < self.height:
            return True
        else:
            return False

    def get_square(self, centre, width, height):
        """Return a list of pixel coordinates contained in a square
        of specified size around a central point

        Arguments
        centre -- the central point of the square
        width -- the width of the square
        height -- the height of the square
        """
        pixel_square = []

        start_x = centre.x - width/2
        end_x = centre.x + width/2

        start_y = centre.y - height/2
        end_y = centre.y + height/2

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                coord = point.Point(x, y)
                if self.is_in_image(coord):
                    pixel_square.append(coord)
        return pixel_square