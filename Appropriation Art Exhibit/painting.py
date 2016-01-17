"""Contain a class for storing image data and manipulating images.

This module contains a class that can be used to store and
manipulate images.

Classes:
Painting -- class for storing and manipulating images
"""


# External libraries
from PIL import Image

# Own modules
import color
import point


class Painting(object):
    """Store properties and methods relating to storing and manipulating images.

    This class stores image data so that variables for the data do not
    need to be defined/passed in to every function that uses them.
    It also contains methods for the basic manipulation of images such as
    clearing an image resizing.

    Public methods:
    show -- shows the painting in default image viewer
    save -- save the painting in specified location
    copy -- make a copy of the painting
    paste -- insert painting into another painting
    resize - copy and resize the painting-
    set_pixel_color -- sets the colour of a given pixel
    get_pixel_color -- returns the colour of a given pixel
    clear image -- clears the painting to one colour
    is_in_image -- check if a point is inside the painting
    get_square -- return a square of pixels from the painting
    """

    def __init__(self, img):
        """Initialise the properties.

        The intialiser can take arguments of type Painting,
        Image.Image or a string of the path to an image file

        Arguments:
        img -- image as a Painting, Image.Image or file path string
        """

        self.img = img

    @property
    def img(self):
        return self.__img

    @img.setter
    def img(self, new_image):
        """Set the data relating to the image correctly"""

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
        """Show the image in default windows image viewer"""

        self.img.show()

    def copy(self):
        """Return a copy of the Painting instance"""

        return Painting(self.img.copy())

    def save(self, path):
        """Save the image in the location specified by the path string

        Arguements:
        path -- string containing location that the image should be saved"""

        self.img.save(path)

    def paste(self, painting, top_left):
        """Paste the image from a Painting into this instance of Painting

        This method pastes the image from another Painting instance into
        this instance. The position of the pasted image is specified by
        where the top left should be positioned.

        Arguments:
        painting -- image that should be pasted as a Painting
        top_left -- position that the top left of basted image should be as point.Point
        """

        self.img.paste(painting.img, top_left.coordinates)

    def resize(self, size):
        """Return a copy of a Painting resized to the specified size

        Arguments:
        size -- desired size as a tuple
        """

        return Painting(self.img.resize(size))

    def set_pixel_color(self, coordinates, color):
        """Set pixel at the given coordinates to a given color.

        Arguments:
        coordinates -- coordinates of the pixel as a point.Point
        color -- colour of pixel as a color.Color
        """

        self.pixels[coordinates.coordinates] = color.color

    def get_pixel_color(self, coordinates):
        """Return the color.Color of the pixel at the given coordinates

        Arguments:
        coordinates -- coordinates of the pixel as a point.Point
        """

        return color.Color(*self.pixels[coordinates.coordinates])

    def clear_image(self, color):
        """Set the image to a single color.

        This method clears the image and sets it to a
        single specified colour.

        Arguments:
        color -- colour to clear the image to as a color.Color
        """

        blank_img = Image.new(self.mode, (self.width, self.height), color.color)
        self.img = blank_img

    def is_in_image(self, point):
        """Check if the supplied point is within the image.

        Arguments:
        point -- coordinates of point to check as a point.Point
        """

        # Needs to be between 0 and its size
        if 0 < point.x < self.width and 0 < point.y < self.height:
            return True
        else:
            return False

    def get_square(self, centre, width, height):
        """Return a list of pixel coordinates representing a square.

        This method returns a list of pixel coordinates contained in a
        square of the specified size around a central point.

        Arguments
        centre -- the central point of the square
        width -- the width of the square
        height -- the height of the square
        """

        pixel_square = []

        # Start and end is half of the size from the center
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