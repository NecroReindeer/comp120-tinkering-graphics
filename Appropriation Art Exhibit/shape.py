__author__ = 'Hat'

import point

class Circle():
    def __init__(self, centre, radius, color):
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
        """Draw a circle on the canvas

        Arguments:
        canvas -- instance of Painting object
        """
        # Using Bresenham's midpoint circle algorithm -- https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
        # Adapted from the C example halfway down the page
        # Then using the idea presented in the top answer at --
        # http://stackoverflow.com/questions/1201200/fast-algorithm-for-drawing-filled-circles
        x = self.radius
        y = 0
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