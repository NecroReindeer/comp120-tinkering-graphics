__author__ = 'Harriet'

import random
import math
import os

from PIL import Image


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

    file = "alf.png"
    colors = ((150, 0, 150),
              (150, 150, 0),
              (0, 150, 0),
              (0, 150, 150))
    dog_painting = Painting(os.path.join(input_dir, file))
    tile_effect = TileEffect(colors, 6, 2)
    tile_effect.color_tile(dog_painting)
    dog_painting.show()
    dog_painting.save(os.path.join(output_dir, file))

    file = "hug.png"
    hug_painting = Painting(os.path.join(input_dir, file))
    dot_effect = DotEffect(10, 5, BLACK)
    dot_effect.convert_to_dots(hug_painting)
    hug_painting.show()
    hug_painting.save(os.path.join(output_dir, file))

    file = "sad.jpg"
    sad_painting = Painting(os.path.join(input_dir, file))
    shuffle_effect = ShuffleEffect(10, 3)
    shuffle_effect.shuffle_image(sad_painting)
    sad_painting.show()
    sad_painting.save(os.path.join(output_dir, file))

    file = "jegermeister.jpg"
    new_colors = [(255, 0, 255),
                 (255, 255, 0),
                 (0, 255, 255)]
    jeger_painting = Painting(os.path.join(input_dir, file))
    colorchange_effect = ThreeColorEffect(50, 0.9, new_colors)
    colorchange_effect.replace_dominant_colors(jeger_painting)
    jeger_painting.show()
    jeger_painting.save(os.path.join(output_dir, file))


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

    def calculate_luminance(self):
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

class Circle():
    def __init__(self, centre_coordinates, radius, color):
        self.__centre = centre_coordinates
        self.__radius = radius
        self.__color = color

    @property
    def x_centre(self):
        return self.__centre[0]

    @property
    def y_centre(self):
        return self.__centre[1]

    @property
    def radius(self):
        return self.__radius

    @property
    def color(self):
        return self.__color

    def isInImage(self, canvas, x, y):
        if 0 < x < canvas.width and 0 < y < canvas.height:
            return True

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
            for x_coord in range(self.x_centre - y, self.x_centre + y):
                y_coord = self.y_centre - x
                if self.isInImage(canvas, x_coord, y_coord):
                    canvas.set_pixel((x_coord, y_coord), self.color)

            for x_coord in range(self.x_centre - x, self.x_centre + x):
                y_coord = self.y_centre - y
                if self.isInImage(canvas, x_coord, y_coord):
                    canvas.set_pixel((x_coord, y_coord), self.color)

            for x_coord in range(self.x_centre - x, self.x_centre + x):
                y_coord = self.y_centre + y
                if self.isInImage(canvas, x_coord, y_coord):
                    canvas.set_pixel((x_coord, y_coord), self.color)

            for x_coord in range(self.x_centre - y, self.x_centre + y):
                y_coord = self.y_centre + x
                if self.isInImage(canvas, x_coord, y_coord):
                    canvas.set_pixel((x_coord, y_coord), self.color)

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

    @property
    def pixels(self):
        return self.img.load()

    @property
    def width(self):
        return self.img.size[0]

    @property
    def height(self):
        return self.img.size[1]

    @property
    def mode(self):
        return self.img.mode

    def show(self):
        """Show the image in default image viewer"""
        self.img.show()

    def copy(self):
        """Return a copy of the Painting instance"""
        img_copy = self.img.copy()
        painting_copy = Painting(img_copy)
        return painting_copy

    def save(self, path):
        """Save the image in the location specified by path (path is a string)"""
        self.img.save(path)

    def paste(self, painting, box):
        self.img.paste(painting.img, box)

    def resize(self, size):
        """Returns a copy of a painting resized to a specified size"""
        resized_img = self.img.resize(size)
        new_painting = Painting(resized_img)
        return new_painting

    def set_pixel(self, coordinates, color):
        """Set pixel at coordinates to color passed in as tuple"""
        self.pixels[coordinates] = color

    def get_pixel(self, coordinates):
        """Return the color of the pixel at coordinates as a tuple"""
        return self.pixels[coordinates]

    def clear_image(self, color):
        """Set image to a single color from a tuple"""
        blank_img = Image.new(self.mode, (self.width, self.height), color)
        self.img = blank_img

    def get_square(self, centre, width, height):
        """Return a list of pixel coordinates contained in a square
        of specified size around a central point

        Arguments
        centre -- the central point of the square
        width -- the width of the square
        height -- the height of the square
        """
        pixel_square = []

        start_x = centre[0] - width/2
        end_x = centre[0] + width/2

        start_y = centre[1] - height/2
        end_y = centre[1] + height/2

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                if 0 < x < self.width and 0 < y < self.height:
                    pixel_square.append((x,y))
        return pixel_square


class DotEffect():
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
        return self.__radius * 2

    @property
    def gap(self):
        return self.__gap

    @property
    def background(self):
        return self.__background

    def convert_to_dots(self, painting):
        """Convert an image to be made up of circles of a
        given radius with the colour of the pixel at the
        centre of the circle on a given background colour
        """
        distance_between_centres = self.diameter + self.gap
        # So that circles on top and left edges are fully visible
        first_centre = distance_between_centres / 2
        canvas = painting.copy()
        canvas.clear_image(self.background)

        for x in range(first_centre, painting.width, distance_between_centres):
            for y in range(first_centre, painting.height, distance_between_centres):
                centre = x, y
                centre_color = painting.get_pixel(centre)
                circle = Circle(centre, self.radius, centre_color)
                circle.draw(canvas)
        painting.img = canvas


class ShuffleEffect():
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

    def get_random_squaresize(self):
        """Return a random integer to be used for the
        lengths of the sides of a square in order to make
        the resulting picture look less uniform and grid-like
        """
        squaresize = random.randrange(self.shuffle_step,
                                      self.shuffle_step * self.randomness)
        return squaresize

    def shuffle_image(self, painting):
        """Swap each pixel in an image with a random nearby pixel"""
        original_painting = painting.copy()
        for x in range(0, painting.width, self.shuffle_step):
            for y in range(0, painting.height, self.shuffle_step):
                current_coordinate = (x,y)
                squaresize = self.get_random_squaresize()
                pixel_square = original_painting.get_square(current_coordinate,
                                                         squaresize, squaresize)
                shuffled_pixel_square = pixel_square
                random.shuffle(shuffled_pixel_square)

                for pixel in pixel_square:
                    pixel_to_move = original_painting.get_pixel(pixel)
                    pixel_to_be_replaced = shuffled_pixel_square.pop()
                    painting.set_pixel(pixel_to_be_replaced, pixel_to_move)


class ThreeColorEffect():
    def __init__(self, threshold, difference, replacement_colors):
        self.threshold = threshold
        self.difference = difference
        self.replacement_colors = replacement_colors

    def replace_dominant_colors(self, painting):
        """Change pixels with a colour component above threshold to
        relative colour in replacementColors, then changes every other colour to black.
        """
        for component_index in range(NUMBER_OF_COLOR_COMPONENTS):
            self.change_dominant_color(component_index, painting)
        self.change_rest_to_black(painting)

    def check_dominant_color(self, pixel, target_component_index):
        """Check if the colour component at target_component_index in a pixel is
        greater than the other components * difference, and above threshold
        """
        can_change = True
        for component_index in range(NUMBER_OF_COLOR_COMPONENTS):
            current_component_value = pixel[component_index]
            component_being_checked = pixel[target_component_index]

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
                current_coordinate = x, y
                current_pixel = painting.get_pixel(current_coordinate)
                can_change = self.check_dominant_color(current_pixel, current_component_index)

                if can_change:
                    painting.set_pixel(current_coordinate, self.replacement_colors[current_component_index])

    def change_rest_to_black(self, painting):
        """Change the colour of any pixel in the image that
        isn't in replacementColors to black.
        """
        for x in range(painting.width):
            for y in range(painting.height):
                current_coordinate = x, y
                current_pixel = painting.get_pixel(current_coordinate)
                if current_pixel not in self.replacement_colors:
                    painting.set_pixel(current_coordinate, BLACK)


class TileEffect:
    def __init__(self, colors, levels, size):
        """Initialise the colors the posterisation will be based on,
        the level of posterisation, and the number of tiles on
        each side of the square
        """
        self.colors = colors
        self.levels = levels
        self.size = size

    def color_tile(self, painting):
        paintings = self.color_posterise(painting)
        new_painting = self.tile_images(paintings)
        painting.img = new_painting

    def get_paintings(self, painting):
        paintings = []
        for i in range(len(self.colors)):
            new_painting = painting.copy()
            paintings.append(new_painting)
        return paintings

    def color_posterise(self, painting):
        """Posterise paintings with colours in self.colors as a base
        and add each painting to a list.
        """
        paintings = self.get_paintings(painting)
        number_of_colors = len(self.colors)

        for x in range(painting.width):
            for y in range(painting.height):
                current_coordinate = x, y
                current_pixel = painting.get_pixel(current_coordinate)
                current_color = Color(*current_pixel)
                lum_step = 255.0 / self.levels
                difference = 255 / self.levels

                if current_color.luminance <= lum_step:
                    for i in range(number_of_colors):
                        target_color = self.colors[i]
                        paintings[i].set_pixel(current_coordinate, target_color)
                else:
                    lum = lum_step
                    next_lum = lum + lum_step
                    iterations = 1

                    while lum < 255:
                        if lum < current_color.luminance <= next_lum:
                            for i in range(number_of_colors):
                                target_color = self.colors[i]
                                new_color = Color(*target_color)
                                new_color.color = new_color + (difference * iterations)
                                paintings[i].set_pixel(current_coordinate, new_color.color)
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
        """Tile each Painting in paintings in a grid of self.size*self.size.
        Loop back to first Painting if there are more tiles than colors provided

        Arguments:
        paintings -- list of Painting object instances
        """
        index = 0
        current_painting = paintings[index]
        tile_size = self.get_tile_size(current_painting)
        canvas_size = current_painting.width, current_painting.height
        canvas = Painting(Image.new(current_painting.mode, canvas_size))

        for x in range(0, canvas.width, tile_size[0]):
            for y in range(0, canvas.height, tile_size[1]):
                tile = current_painting.resize(tile_size)
                coordinates = x, y
                canvas.paste(tile, coordinates)
                index += 1
                # So that it doesn't matter if there are more tiles than colours
                current_painting = paintings[index % len(paintings)]
        return canvas

show_gallery()