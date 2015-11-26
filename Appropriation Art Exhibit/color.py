__author__ = 'Hat'


# The number of colour components, in this case, 3 (red, green and blue)
NUMBER_OF_COLOR_COMPONENTS = 3

RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


class Color(object):
    """Class for manipulating colours. Properties allow access
    to red, green, blue and alpha components as integers as well
    as the whole color as a tuple.
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
        """Change red, green, blue, alpha and luminance
        appropriately when color is set.
        """
        #Argument is a tuple so that length can be accessed
        self.__red = color_tuple[0]
        self.__green = color_tuple[1]
        self.__blue = color_tuple[2]
        if len(color_tuple) == 4:
            self.__alpha = color_tuple[3]
        self.__luminance = self.calculate_luminance()

    @property
    def red(self):
        """Red component as an integer"""
        return self.__red

    @red.setter
    def red(self, value):
        """Set the red component to an integer and recalculate luminance"""
        self.__red = value
        self.__luminance = self.calculate_luminance()

    @property
    def green(self):
        """Green component as an integer"""
        return self.__green

    @green.setter
    def green(self, value):
        """Set the green component to an integer and recalculate luminance"""
        self.__green = value
        self.__luminance = self.calculate_luminance()

    @property
    def blue(self):
        """Blue component as an integer"""
        return self.__blue

    @blue.setter
    def blue(self, value):
        """Set the blue component to an integer and recalculate luminance"""
        self.__blue = value
        self.__luminance = self.calculate_luminance()

    @property
    def alpha(self):
        return self.__alpha

    @alpha.setter
    def alpha(self, value):
        self.__alpha = value

    @property
    def luminance(self):
        return self.__luminance

    def get_component_by_index(self, i):
        """Allow access to color components by index"""
        if i == 0:
            return self.red
        elif i == 1:
            return self.green
        elif i == 2:
            return self.blue
        elif i == 3:
            return self.alpha

    def set_component_by_index(self, i, value):
        """Set color components by index"""
        if i == 0:
            self.red = value
        elif i == 1:
            self.green = value
        elif i == 2:
            self.blue = value
        elif i == 3:
            self.alpha = value

    def calculate_luminance(self):
        # Luminance needs to be recalculated whenever any color
        # component changes
        lum = (self.red + self.green + self.blue)/3
        return lum

    def copy(self):
        """Return the Color as a new instance"""
        return Color(*self.color)

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