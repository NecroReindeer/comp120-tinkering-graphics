"""Contain a class for storing and manipulating colours.

This module contains a class that can be used to store and
manipulate RGB and RGBA colours.

Classes:
Color -- class for storing and manipulating RGB colours
"""


# The number of RGB/RGBA colour components, and the maximum value components can take
RGB_COMPONENT_COUNT = 3
RGBA_COMPONENT_COUNT = 4
MAX_COMPONENT_VALUE = 255

# Values of commonly referenced colours
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# The index each RGBA colour component when stored as a tuple
R_INDEX = 0
G_INDEX = 1
B_INDEX = 2
A_INDEX = 3


class Color(object):

    """Contain properties and methods relating to manipulating colours.

    This class contains methods that can be used for managing and manipulating
    colours.
    Its properties allow access to red, green, blue and alpha components individually
    as well as the whole color. Luminance can also be accessed.

    Public methods:
    get_component_by_index -- return the component corresponding to a given index
    set_component_by_index -- set the value of the component at a given index
    copy -- make a copy of the Color instance
    """

    def __init__(self, red, green, blue, alpha=None):
        self.color = red, green, blue, alpha

    @property
    def color(self):
        if self.alpha == None:
            return self.red, self.green, self.blue
        else:
            return self.red, self.green, self.blue, self.alpha

    @color.setter
    def color(self, color_tuple):
        """Change red, green, blue, alpha and luminance appropriately when color is set."""

        self.__red = color_tuple[R_INDEX]
        self.__green = color_tuple[G_INDEX]
        self.__blue = color_tuple[B_INDEX]
        if len(color_tuple) == RGBA_COMPONENT_COUNT:
            self.__alpha = color_tuple[A_INDEX]
        self.__luminance = self.__calculate_luminance()

    @property
    def red(self):
        """Return the red component as an integer"""

        return self.__red

    @red.setter
    def red(self, value):
        """Set the red component to given integer and recalculate luminance"""

        self.__red = value
        self.__luminance = self.__calculate_luminance()

    @property
    def green(self):
        """REturn the green component as an integer"""

        return self.__green

    @green.setter
    def green(self, value):
        """Set the green component to given integer and recalculate luminance"""

        self.__green = value
        self.__luminance = self.__calculate_luminance()

    @property
    def blue(self):
        """Return the blue component as an integer"""

        return self.__blue

    @blue.setter
    def blue(self, value):
        """Set the blue component to given integer and recalculate luminance"""

        self.__blue = value
        self.__luminance = self.__calculate_luminance()

    @property
    def alpha(self):
        """Return the alpha component as an integer"""

        return self.__alpha

    @alpha.setter
    def alpha(self, value):
        """Set the value of the alpha component to given integer."""
        self.__alpha = value

    @property
    def luminance(self):
        """Return the luminance as an integer"""

        return self.__luminance

    def get_component_by_index(self, i):
        """Return colour component corresponding to given index.

        This methods allows access to colour components by their
        index. It should be used in cases where looping through
        the colours is necessary.
        """

        if i == R_INDEX:
            return self.red
        elif i == G_INDEX:
            return self.green
        elif i == B_INDEX:
            return self.blue
        elif i == A_INDEX:
            return self.alpha

    def set_component_by_index(self, i, value):
        """Set the colour component corresponding to given index.

        This methods allows colour component values to be set by their
        index. It should be used in cases where looping through
        the colours is necessary.
        """

        if i == R_INDEX:
            self.red = value
        elif i == G_INDEX:
            self.green = value
        elif i == B_INDEX:
            self.blue = value
        elif i == A_INDEX:
            self.alpha = value

    def copy(self):
        """Return a copy of the Color as a new instance"""

        return Color(*self.color)

    def __calculate_luminance(self):
        """Recalculate the luminance of the colour.

        This method recalculated the luminance of the stored colour.
        It should be called whenever any colour component changes.
        """

        lum = (self.red + self.green + self.blue)/3
        return lum

    def __add__(self, other):
        color = list(self.color)
        if isinstance(other, int):
            for i in range(len(self.color)):
                color[i] += other
                self.color = tuple(color)
            return self.color
        elif isinstance(other, tuple):
            for i in range(len(self.color)):
                color[i] += other[i]
                self.color = tuple(color)
            return self.color

    def __sub__(self, other):
        color = list(self.color)
        if isinstance(other, int):
            for i in range(len(self.color)):
                color[i] -= other
                self.color = tuple(color)
            return self.color
        elif isinstance(other, tuple):
            for i in range(len(self.color)):
                color[i] -= other[i]
                self.color = tuple(color)
            return self.color

    def __mul__(self, other):
        color = list(self.color)
        if isinstance(other, int):
            for i in range(len(self.color)):
                color[i] *= other
                self.color = tuple(color)
            return self.color

    def __eq__(self, other):
        if self.color == other.color:
            return True
        else:
            return False