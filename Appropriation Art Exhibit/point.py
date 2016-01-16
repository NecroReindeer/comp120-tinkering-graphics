__author__ = 'Hat'

import math


class Point(object):
    """Class for storing and manipulating coordinates of points.
    Properties allow access to x coordinate as an int, y coordinate
    as an int, and coordinates as a tuple.
    """
    def __init__(self, x, y):
        self.coordinates = x, y

    @property
    def coordinates(self):
        return self.__x, self.__y

    @coordinates.setter
    def coordinates(self, (x, y)):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    def get_distance(self, other):
        """Return distance between this point and another point as a float."""
        x_distance = other.x - self.x
        y_distance = other.y - self.y
        distance = math.sqrt(x_distance**2.0 + y_distance**2.0)
        return distance