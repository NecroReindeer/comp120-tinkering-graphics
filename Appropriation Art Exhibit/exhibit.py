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
    colors = [(150, 0, 150),
              (150, 150, 0),
              (0, 150, 0),
              (0, 150, 150)]
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
    def __init__(self, color):
        self.color = list(color)

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = list(value)
        self.__luminance = self.recalculate_luminance()

    @property
    def red(self):
        """Red component as an integer"""
        return self.__color[0]

    @red.setter
    def red(self, value):
        self.__color[0] = value
        self.recalculate_luminance()

    @property
    def green(self):
        """Green component as an integer"""
        return self.__color[1]

    @green.setter
    def green(self, value):
        self.__color[1] = value
        self.recalculate_luminance()

    @property
    def blue(self):
        """Blue component as an integer"""
        return self.__color[2]

    @blue.setter
    def blue(self, value):
        self.__color[2] = value
        self.recalculate_luminance()

    @property
    def luminance(self):
        return self.__luminance

    def recalculate_luminance(self):
        lum = (self.red + self.green + self.blue)/3
        return lum

    def __add__(self, other):
        if isinstance(other, int):
            for i in range(len(self.color)):
                self.color[i] += other
            return self.color
        elif isinstance(other, tuple):
            for i in range(len(self.color)):
                self.color[i] += other[i]
            return self.color

    def __sub__(self, other):
        if isinstance(other, int):
            for i in range(len(self.color)):
                self.color[i] -= other
            return self.color
        elif isinstance(other, tuple):
            for i in range(len(self.color)):
                self.color[i] -= other[i]
            return self.color

    def __mul__(self, other):
        if isinstance(other, int):
            for i in range(len(self.color)):
                self.color[i] *= other
            return self.color

    def get_color(self):
        return tuple(self.color)

    def set_color(self, color):
        self.color = color


class Painting():
    """Store image data so that variables for the data do not
    need to be defined/passed in/to every function that uses them.
    """

    def __init__(self, img):
        """Takes an object instance of type Image or a string"""
        if isinstance(img, str):
            self.__img = Image.open(img)
        else:
            self.__img = img

    @property
    def pixels(self):
        return self.__img.load()

    @property
    def width(self):
        return self.__img.size[0]

    @property
    def height(self):
        return self.__img.size[1]

    @property
    def mode(self):
        return self.__img.mode

    def show(self):
        """Show the image in default image viewer"""
        self.__img.show()

    def copy(self):
        """Return a copy of the Painting instance"""
        img_copy = self.__img.copy()
        painting_copy = Painting(img_copy)
        return painting_copy

    def save(self, path):
        """Save the image in the location specified by path (path is a string)"""
        self.__img.save(path)

    def paste(self, painting, box):
        self.__img.paste(painting.__img, box)

    def resize(self, size):
        """Returns a copy of a painting resized to a specified size"""
        resized_img = self.__img.resize(size)
        new_painting = Painting(resized_img)
        return new_painting

    def set_image(self, new_image):
        if isinstance(new_image, Image.Image):
            self.__img = new_image
        if isinstance(new_image, Painting):
            self.__img = new_image.__img

    def get_image(self):
        return self.__img

    def set_pixel(self, coordinates, color):
        """Set pixel at coordinates to color passed in as tuple"""
        self.pixels[coordinates] = color

    def get_pixel(self, coordinates):
        """Return the color of the pixel at coordinates as a tuple"""
        return self.pixels[coordinates]

    def clear_image(self, color):
        """Set image to a single color from a tuple"""
        blank_img = Image.new(self.mode, (self.width, self.height), color)
        self.__img = blank_img

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

    def draw_circle(self, canvas, pixels, centre, color):
        """Draw a circle

        Arguments:
        canvas -- Painting instance that the circles will be drawn on
        pixels -- List of pixel coordinates that will be checked
        centre -- Tuple containing coordinates of the centre of the circle
        color -- Tuple containing color component values for color of circle
        """
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
                self.draw_circle(canvas, pixel_square, centre, centre_color)
        painting.set_image(canvas)


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
        painting.set_image(new_painting)

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
                current_color = Color(current_pixel)
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
                                new_color = Color(target_color)
                                new_color.set_color(new_color + (difference * iterations))
                                paintings[i].set_pixel(current_coordinate, new_color.get_color())
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
                current_painting = paintings[index % len(paintings)]                # So that it doesn't matter if there are more tiles than colours
        return canvas

show_gallery()