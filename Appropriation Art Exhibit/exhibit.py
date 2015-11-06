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
    directory = "source-images"

    hug_painting = Painting(os.path.join(directory, "hug.png"))
    dot_effect = DotEffect(10, 5, BLACK)
    dot_effect.convert_to_dots(hug_painting)
    hug_painting.show()

    sad_painting = Painting(os.path.join(directory, "sad.jpg"))
    shuffle_effect = ShuffleEffect(10, 3)
    shuffle_effect.shuffle_image(sad_painting)
    sad_painting.show()

    new_colors = [(255, 0, 255),
                 (255, 255, 0),
                 (0, 255, 255)]

    jeger_painting = Painting(os.path.join(directory, "jegermeister.jpg"))
    colorchange_effect = ThreeColorEffect(50, 0.9, new_colors)
    colorchange_effect.replace_dominant_colors(jeger_painting)
    jeger_painting.show()


class Painting():
    """Store image data so that variables for the data do not
    need to be defined/passed in/to every function that uses them.
    """

    def __init__(self, img):
        if isinstance(img, str):
            self.img = Image.open(img)
        else:
            self.img = img

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

    def set_pixel(self, coordinates, color):
        """Set pixel at coordinates to color passed in as tuple"""
        self.pixels[coordinates] = color

    def get_pixel(self, coordinates):
        """Return the color of the pixel at coordinates as a tuple"""
        return self.pixels[coordinates]

    def clear_image(self, color):
        """Set image to a single color"""
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
    def __init__(self, radius, gap, background):
        self.radius = radius
        self.diameter = self.radius * 2
        self.gap = gap
        self.background = background

    def get_squaresize(self):
        """Set the size of the square of pixels that
        will be checked to an even number to account for
        rounding errors and returns it as an int.
        """
        if (self.diameter + self.gap) % 2 != 0:
            squaresize = self.diameter + self.gap + 1
        else:
            squaresize = self.diameter + self.gap
        return squaresize

    def draw_circles(self, canvas, pixels, centre, color):
        for pixel in pixels:
            distance_from_centre = get_distance(pixel, centre)         # Because every point on the circumference of a
            if distance_from_centre < self.radius:                     # circle is equal distance from the centre
                canvas.set_pixel(pixel, color)

    def convert_to_dots(self, painting):
        """Convert an image to be made up of circles of a
        given radius with the colour of the pixel at the
        centre of the circle on a background colour
        """
        squaresize = self.get_squaresize()
        first_centre = squaresize / 2                                  # So circles on top edge are fully visible
        canvas = painting.copy()
        canvas.clear_image(self.background)

        for x in range(first_centre, painting.width, squaresize):
            for y in range(first_centre, painting.height, squaresize):
                centre = x, y
                pixel_square = painting.get_square(centre, squaresize, squaresize)
                centre_color = painting.get_pixel(centre)
                self.draw_circles(canvas, pixel_square, centre, centre_color)
        painting.img = canvas.img


class ShuffleEffect():
    """Class that sets up effect to shuffle pixels in an image"""
    def __init__(self, shuffle_step, randomness):
        self.shuffle_step = shuffle_step
        self.randomness = randomness

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
                can_change = self.check_dominant_color(current_pixel,
                                                    current_component_index)

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
    def __init__(self, colors):
        colors.self = colors


show_gallery()