__author__ = 'Harriet'

import random
import math
import os

from PIL import Image
from PIL import ImageDraw


# The number of colour components, in this case, 3 (red, green and blue)
NUMBER_OF_COLOR_COMPONENTS = 3

RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


def get_distance(first_point, second_point):
    """Return distance between 2 coordinates as a float

    Arguments:
    first_point -- first coordinate tuple
    second_point -- second coordinate tuple
    """
    x_distance = second_point[0] - first_point[0]
    y_distance = second_point[1] - first_point[1]
    distance = math.sqrt(x_distance**2.0 + y_distance**2.0)
    return distance


def show_gallery():
    input_dir = "source-images"
    output_dir = "output-images"

    filenames = ["alf.png",
                 "hug.png",
                 "sad.jpg",
                 "jegermeister.jpg"]

    paintings = []
    for filename in filenames:
        paintings.append(Painting(os.path.join(input_dir, filename)))

    effects = []
    colors = (Color(150, 0, 150),
              Color(150, 150, 0),
              Color(0, 150, 0),
              Color(0, 150, 150))
    tile_effect = TileEffect(colors, 6, 2)
    effects.append(tile_effect)

    dot_effect = DotEffect(10, 5, Color(*BLACK))
    effects.append(dot_effect)

    shuffle_effect = ShuffleEffect(10, 3)
    effects.append(shuffle_effect)

    colors = (Color(255, 0, 255),
              Color(255, 255, 0),
              Color(0, 255, 255))
    colorchange_effect = ThreeColorEffect(50, 0.9, colors)
    effects.append(colorchange_effect)

    for i in range(len(effects)):
        effects[i].do_effect(paintings[i])
        paintings[i].show()

    for i in range(len(paintings)):
        paintings[i].save(os.path.join(output_dir, filenames[i]))


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


class Color(object):
    """Class for manipulating colours"""
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
        self.__red = value
        self.__luminance = self.calculate_luminance()

    @property
    def green(self):
        """Green component as an integer"""
        return self.__green

    @green.setter
    def green(self, value):
        self.__green = value
        self.__luminance = self.calculate_luminance()

    @property
    def blue(self):
        """Blue component as an integer"""
        return self.__blue

    @blue.setter
    def blue(self, value):
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
        if i == 0:
            return self.red
        elif i == 1:
            return self.green
        elif i == 2:
            return self.blue
        elif i == 3:
            return self.alpha

    def set_component_by_index(self, i, value):
        if i == 0:
            self.red = value
        elif i == 1:
            self.green = value
        elif i == 2:
            self.blue = value
        elif i == 3:
            self.alpha = value

    def calculate_luminance(self):
        lum = (self.red + self.green + self.blue)/3
        return lum

    def copy(self):
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
                coord = Point(x_coord, self.centre.y - x)
                if canvas.is_in_image(coord):
                    canvas.set_pixel_color(coord, self.color)

            for x_coord in range(self.centre.x - x, self.centre.x + x):
                coord = Point(x_coord, self.centre.y - y)
                if canvas.is_in_image(coord):
                    canvas.set_pixel_color(coord, self.color)

            for x_coord in range(self.centre.x - x, self.centre.x + x):
                coord = Point(x_coord, self.centre.y + y)
                if canvas.is_in_image(coord):
                    canvas.set_pixel_color(coord, self.color)

            for x_coord in range(self.centre.x - y, self.centre.x + y):
                coord = Point(x_coord, self.centre.y + x)
                if canvas.is_in_image(coord):
                    canvas.set_pixel_color(coord, self.color)

            y += 1
            if decision_over_2 <= 0:
                decision_over_2 += 2 * y + 1
            else:
                x -= 1
                decision_over_2 += 2 * (y - x) + 1


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
        if isinstance(new_image, Painting):
            self.__img = new_image.__img
        elif isinstance(new_image, Image.Image):
            self.__img = new_image
        elif isinstance(new_image, str):
            self.__img = Image.open(new_image)

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
        return Color(*self.pixels[coordinates.coordinates])

    def clear_image(self, color):
        """Set image to a single color"""
        blank_img = Image.new(self.mode, (self.width, self.height), color.color)
        self.img = blank_img

    def is_in_image(self, point):
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
                coord = Point(x, y)
                if self.is_in_image(coord):
                    pixel_square.append(coord)
        return pixel_square


class Effect():
    """Abstract class for effects"""
    def do_effect(self, painting):
        raise NotImplementedError("Subclasses must implement do_effect")

class DotEffect(Effect):
    """An effect that changes the image to be made out of circles."""
    def __init__(self, radius, gap, background):
        """Initialises the properties.

        Arguments:
        radius -- radius of the circle as an int
        gap -- gap between the circles as an int
        background -- background colour of the image as a tuple
        """
        self.__radius = radius
        self.__gap = gap
        self.__background = background

    @property
    def radius(self):
        return self.__radius

    @property
    def diameter(self):
        return self.__radius*2

    @property
    def gap(self):
        return self.__gap

    @property
    def background(self):
        return self.__background

    def do_effect(self, painting):
        """Convert an image to be made up of circles of a
        given radius with the colour of the pixel at the
        centre of the circle on a given background colour
        """
        distance_between_centres = self.diameter + self.gap
        # So that circles on top and left edges are fully visible
        first_centre = distance_between_centres/2
        canvas = painting.copy()
        canvas.clear_image(self.background)

        for x in range(first_centre, painting.width, distance_between_centres):
            for y in range(first_centre, painting.height, distance_between_centres):
                centre = Point(x, y)
                centre_color = painting.get_pixel_color(centre)
                circle = Circle(centre, self.radius, centre_color)
                circle.draw(canvas)
        painting.img = canvas


class ShuffleEffect(Effect):
    """Class that sets up effect to shuffle pixels in an image"""
    def __init__(self, shuffle_step, randomness):
        """Initialise the properties.

        Arguments:
        shuffle_step -- base amount that the pixels are allowed to move as an int
        randomness -- amount that the shuffle_step is allowed to vary for each pixel
        """
        self.__shuffle_step = shuffle_step
        self.__randomness = randomness

    @property
    def shuffle_step(self):
        return self.__shuffle_step

    @property
    def randomness(self):
        return self.__randomness

    def do_effect(self, painting):
        """Swap each pixel in an image with a random nearby pixel"""
        original_painting = painting.copy()
        for x in range(0, painting.width, self.shuffle_step):
            for y in range(0, painting.height, self.shuffle_step):
                current_coordinate = Point(x, y)
                squaresize = self.get_random_squaresize()
                pixel_square = original_painting.get_square(current_coordinate,
                                                         squaresize, squaresize)
                shuffled_pixel_square = pixel_square
                random.shuffle(shuffled_pixel_square)

                for pixel in pixel_square:
                    new_pixel_color = original_painting.get_pixel_color(pixel)
                    pixel_to_be_replaced = shuffled_pixel_square.pop()
                    painting.set_pixel_color(pixel_to_be_replaced, new_pixel_color)

    def get_random_squaresize(self):
        """Return a random integer to be used for the
        lengths of the sides of a square in order to make
        the resulting picture look less uniform and grid-like
        """
        squaresize = random.randrange(self.shuffle_step,
                                      self.shuffle_step * self.randomness)
        return squaresize


class ThreeColorEffect(Effect):
    def __init__(self, threshold, difference, replacement_colors):
        self.__threshold = threshold
        self.__difference = difference
        self.__replacement_colors = replacement_colors

    @property
    def threshold(self):
        return self.__threshold

    @property
    def difference(self):
        return self.__difference

    @property
    def replacement_colors(self):
        return self.__replacement_colors

    def do_effect(self, painting):
        """Change pixels with a colour component above threshold to
        relative colour in replacementColors, then changes every other colour to black.
        """
        for component_index in range(NUMBER_OF_COLOR_COMPONENTS):
            self.change_dominant_color(component_index, painting)
        self.change_rest_to_black(painting)

    def check_dominant_color(self, color, target_component_index):
        """Check if the colour component at target_component_index in a pixel is
        greater than the other components * difference, and above threshold
        """
        can_change = True
        for component_index in range(NUMBER_OF_COLOR_COMPONENTS):
            current_component_value = color.get_component_by_index(component_index)
            component_being_checked = color.get_component_by_index(target_component_index)

            if component_index != target_component_index:
                if (current_component_value >= component_being_checked * self.difference):
                    can_change = False
            elif current_component_value <= self.threshold:
                can_change = False
        return can_change

    def change_dominant_color(self, current_component_index, painting):
        """Change the colour of pixels that pass the checks in checkDominantColor()
        to the colour in replacementColors with the same index as the colour
        component with the highest value

        Arguments:
        current_component_index -- the colour component to be checked
        """
        for x in range(painting.width):
            for y in range(painting.height):
                current_coordinate = Point(x, y)
                current_pixel_color = painting.get_pixel_color(current_coordinate)
                can_change = self.check_dominant_color(current_pixel_color, current_component_index)

                if can_change:
                    painting.set_pixel_color(current_coordinate, self.replacement_colors[current_component_index])

    def change_rest_to_black(self, painting):
        """Change the colour of any pixel in the image that
        isn't in replacementColors to black.
        """
        for x in range(painting.width):
            for y in range(painting.height):
                current_coordinate = Point(x, y)
                current_pixel_color = painting.get_pixel_color(current_coordinate)
                if current_pixel_color not in self.replacement_colors:
                    painting.set_pixel_color(current_coordinate, Color(*BLACK))


class TileEffect(Effect):
    def __init__(self, colors, levels, size):
        """Initialise the colors the posterisation will be based on,
        the level of posterisation, and the number of tiles on
        each side of the square
        """
        self.__colors = colors
        self.__levels = levels
        self.__size = size

    @property
    def colors(self):
        return self.__colors

    @property
    def number_of_colors(self):
        return len(self.colors)

    @property
    def levels(self):
        return self.__levels

    @property
    def size(self):
        return self.__size

    def do_effect(self, painting):
        paintings = self.color_posterise(painting)
        new_painting = self.tile_images(paintings)
        painting.img = new_painting

    def get_paintings(self, painting):
        paintings = []
        for i in range(self.number_of_colors):
            new_painting = painting.copy()
            paintings.append(new_painting)
        return paintings

    def color_posterise(self, painting):
        """Posterise paintings with colours in self.colors as a base
        and add each painting to a list.
        """
        paintings = self.get_paintings(painting)

        for x in range(painting.width):
            for y in range(painting.height):
                current_coordinate = Point(x, y)
                current_pixel_color = painting.get_pixel_color(current_coordinate)
                lum_step = 255.0 / self.levels
                difference = 255 / self.levels

                if current_pixel_color.luminance <= lum_step:
                    for i in range(self.number_of_colors):
                        target_color = self.colors[i].copy()
                        paintings[i].set_pixel_color(current_coordinate, target_color)
                else:
                    lum = lum_step
                    next_lum = lum + lum_step
                    iterations = 1

                    while lum < 255:
                        if lum < current_pixel_color.luminance <= next_lum:
                            for i in range(self.number_of_colors):
                                target_color = self.colors[i].copy()
                                target_color.color = target_color + (difference * iterations)
                                paintings[i].set_pixel_color(current_coordinate, target_color)
                            break
                        else:
                            lum = next_lum
                            next_lum = lum + lum_step
                            iterations += 1
        return paintings

    def get_tile_size(self, painting):
        """Get the tile size such that the resulting image is the
        same size as the original image.
        """
        tile_width = painting.width / self.size
        tile_height = painting.height / self.size
        return tile_width, tile_height

    def tile_images(self, paintings):
        """Tile each Painting in paintings in a grid of self.size*self.size tiles.
        Make resulting Painting the same size as the original.
        Loop back to first Painting in paintings if there are more tiles than colors provided

        Arguments:
        paintings -- list of Painting object instances
        """
        index = 0
        current_painting = paintings[index]
        tile_size = self.get_tile_size(current_painting)
        canvas = Painting(Image.new(current_painting.mode, current_painting.size))

        for x in range(0, canvas.width, tile_size[0]):
            for y in range(0, canvas.height, tile_size[1]):
                tile = current_painting.resize(tile_size)
                coordinates = Point(x, y)
                canvas.paste(tile, coordinates)
                index += 1
                # So that it doesn't matter if there are more tiles than colours
                current_painting = paintings[index % len(paintings)]
        return canvas

show_gallery()