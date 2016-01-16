"""Contain a classes for drawing shapes.

This module contains classes for drawing shapes onto an
existing image.
It currently only contains a class for circles.

Classes:
Circle -- class for storing circle information and drawing circles
"""

# Own module
import point


class Circle():

    """Store data required for drawing circles.

    This class stores the information required to draw a circle
    and contains a method for drawing a circle on a given image.
    """

    def __init__(self, centre, radius, color):
        """Initialise the properties.

        Arguments:
        centre -- the centre of the circle as a point.Point
        radius -- the radius of the circle
        color -- the colour of the circle as a color.Color
        """

        self.__centre = centre
        self.__radius = radius
        self.__color = color

    @property
    def centre(self):
        return self.__centre

    @property
    def radius(self):
        return self.__radius

    @property
    def color(self):
        return self.__color

    def draw(self, canvas):
        """Draw a circle on the supplied image.

        This method draws a circle corresponding to the instance's
        properties onto the supplied image.

        Note:
        It draws the circle using the midpoint circle algorithm described
        here - https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
        This code is adapted from the C example halfway down the Wikipedia page.
        The circle is then filled using the idea in the top answer at -
        http://stackoverflow.com/questions/1201200/fast-algorithm-for-drawing-filled-circles

        Arguments:
        canvas -- instance of painting.Painting object to be used as a canvas
        """

        # All of the literals in this method were used in the algorithm
        # I was not sure what they represent so left them as literals
        x = self.radius
        y = 0
        # Named this variable the same as in the example on Wikipedia
        decision_over_2 = 1 - x

        while y <= x:
            for x_coord in range(self.centre.x - y, self.centre.x + y):
                coord = point.Point(x_coord, self.centre.y - x)
                if canvas.is_in_image(coord):
                    canvas.set_pixel_color(coord, self.color)

            for x_coord in range(self.centre.x - x, self.centre.x + x):
                coord = point.Point(x_coord, self.centre.y - y)
                if canvas.is_in_image(coord):
                    canvas.set_pixel_color(coord, self.color)

            for x_coord in range(self.centre.x - x, self.centre.x + x):
                coord = point.Point(x_coord, self.centre.y + y)
                if canvas.is_in_image(coord):
                    canvas.set_pixel_color(coord, self.color)

            for x_coord in range(self.centre.x - y, self.centre.x + y):
                coord = point.Point(x_coord, self.centre.y + x)
                if canvas.is_in_image(coord):
                    canvas.set_pixel_color(coord, self.color)

            y += 1
            if decision_over_2 <= 0:
                decision_over_2 += 2 * y + 1
            else:
                x -= 1
                decision_over_2 += 2 * (y - x) + 1