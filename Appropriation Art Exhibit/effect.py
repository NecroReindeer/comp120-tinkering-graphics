__author__ = 'Hat'

import random

from PIL import Image

import color
import painting
import point
import shape

class Effect():
    """Abstract class for effects"""
    def do_effect(self, painting):
        raise NotImplementedError("Subclasses must implement do_effect")


class DotEffect(Effect):
    """Set up effect that changes the image to be made out of circles."""
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
                centre = point.Point(x, y)
                centre_color = painting.get_pixel_color(centre)
                circle = shape.Circle(centre, self.radius, centre_color)
                circle.draw(canvas)
        painting.img = canvas


class ShuffleEffect(Effect):
    """Set up effect to shuffle pixels in an image"""
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
                current_coordinate = point.Point(x, y)
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
    """Set up effect to change pixels with a colour component above threshold to the
    relative colour in replacement_colors, then change every other colour to black.
    """
    def __init__(self, threshold, difference, replacement_colors):
        """Initialises the properties.

        Arguments:
        threshold -- value that the color component must be at to change
        difference -- amount that the component value must be larger than the other two
        replacement_colors -- colors that each dominant component will be replaced by
        """
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
        for component_index in range(color.NUMBER_OF_COLOR_COMPONENTS):
            self.change_dominant_color(component_index, painting)
        self.change_rest_to_black(painting)

    def check_dominant_color(self, current_color, target_component_index):
        """Check if the colour component at target_component_index in a pixel is
        greater than the other components * difference, and above threshold
        """
        can_change = True
        for component_index in range(color.NUMBER_OF_COLOR_COMPONENTS):
            current_component_value = current_color.get_component_by_index(component_index)
            component_being_checked = current_color.get_component_by_index(target_component_index)

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
                current_coordinate = point.Point(x, y)
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
                current_coordinate = point.Point(x, y)
                current_pixel_color = painting.get_pixel_color(current_coordinate)
                if current_pixel_color not in self.replacement_colors:
                    painting.set_pixel_color(current_coordinate, color.Color(*color.BLACK))


class TileEffect(Effect):
    def __init__(self, colors, levels, size):
        """Initialise the properties for the colors the posterisation
        will be based on, the level of posterisation, and the number
        of tiles on each side of the square
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
        paintings = self.get_paintings(painting)
        paintings = self.color_posterise(paintings)
        new_painting = self.tile_images(paintings)
        painting.img = new_painting

    def get_paintings(self, painting):
        """Resize the paintings to the tile size and add
        copies of them for each color to a list
        """
        paintings = []
        tile_size = self.get_tile_size(painting)
        smaller_painting = painting.resize(tile_size)
        for i in range(self.number_of_colors):
            new_painting = smaller_painting.copy()
            paintings.append(new_painting)
        return paintings

    def color_posterise(self, paintings):
        """Posterise paintings with colours in self.colors as a base
        and add each painting to a list.
        """

        # All paintings in paintings are the same at this point, so
        # just using paintings[0] to get the data from the image
        for x in range(paintings[0].width):
            for y in range(paintings[0].height):
                current_coordinate = point.Point(x, y)
                current_pixel_color = paintings[0].get_pixel_color(current_coordinate)
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

    def get_canvas_size(self, painting):
        """Get the tile size such that the resulting image is
        roughly the same size as the original image.
        """
        canvas_width = painting.width * self.size
        canvas_height = painting.height * self.size
        return canvas_width, canvas_height

    def tile_images(self, paintings):
        """Tile each Painting in paintings in a grid of self.size*self.size tiles.
        Make resulting Painting the same size as the original.
        Loop back to first Painting in paintings if there are more tiles than colors provided.

        Arguments:
        paintings -- list of Painting object instances
        """
        index = 0
        current_painting = paintings[index]
        # Can use any of the paintings to get the size as they are all same size
        canvas = painting.Painting(Image.new(current_painting.mode, self.get_canvas_size(current_painting)))

        for x in range(0, canvas.width, current_painting.width):
            for y in range(0, canvas.height, current_painting.height):
                coordinates = point.Point(x, y)
                canvas.paste(current_painting, coordinates)
                index += 1
                # So that it doesn't matter if there are more tiles than colours
                current_painting = paintings[index % len(paintings)]
        return canvas