"""Contain a class for storing and manipulating coordinate points.

This module contains a class that can be used to store and
manipulate (x, y) coordinates.

Classes:
Point -- class for storing and manipulating coordinates
"""


import math


class Point(object):

    """Contain methods and properties for storing and manipulating coordinates.

    This class contains methods and properties related to the manipulation
    of coordinates.
    Its properties allow access to x coordinate and y coordinate individually
    as integers, and coordinates as a tuple.
    """

    def __init__(self, x, y):
        """Initialise the properties.

        Arguments:
        x -- x-coordinate as a tuple
        y -- y-coordinate as a tuple
        """

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

        # Pythagoras' theorem
        distance = math.sqrt(x_distance**2.0 + y_distance**2.0)
        return distance