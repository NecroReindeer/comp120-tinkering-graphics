"""Contain classes relating to effects that can be applied to images.

This module contains classes relating to effects that can be set up and
then applied to an image.

Classes:
Effect -- Abstract class that particular effects are subclasses of
DotEffect(Effect) -- An effect that creates a pointillism-like image
ShuffleEffect(Effect) -- An effect that shuffles the pixels in an image
ThreeColorEffect(Effect) -- An effect that reduces an image to three colors
TileEffect(Effect) -- an effect that posterises and tiles an image
"""

# Standard libraries
import random

# External libraries
from PIL import Image

# Own modules
import color
import painting
import point
import shape


class Effect():

    """Abstract class for effects.

    This class is an abstract class that all effects will inherit from.
    It has one method that should be implemented in all of its subclasses.
    """

    def do_effect(self, painting):
        raise NotImplementedError("Subclasses must implement do_effect")


class DotEffect(Effect):

    """Store fields and methods used to create a dot effect.

    This class contains fields and methods that relate to creating
    a pointillism-like dot effect on an image.

    Public methods:
    do_effect -- applies the effect to the supplied Painting
    """

    def __init__(self, radius, gap, background):
        """Initialises the properties.

        Arguments:
        radius -- radius of the circle as an int
        gap -- gap between the circles as an int
        background -- background colour of the image as a color.Color
        """

        self.__radius = radius
        self.__gap = gap
        self.__background = background

    @property
    def radius(self):
        return self.__radius

    @property
    def diameter(self):
        # Diameter is twice the radius
        return self.__radius*2

    @property
    def gap(self):
        return self.__gap

    @property
    def background(self):
        return self.__background

    def do_effect(self, painting):
        """Process an image so that it is made up of circles.

        This method processes an image so that it is made up of circles
        of a supplied radius, on top of a given background colour.
        The color of the circles correspond to the pixel that would have
        been at its centre.
        """

        distance_between_centres = self.diameter + self.gap
        # Half of distance so that circles fully visible on top and left edges
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

    """Store fields and methods used to create a shuffle effect.

    This class contains fields and methods that relate to shuffling the
    pixels in an image.

    Public methods:
    do_effect -- applies the effect to the supplied Painting
    """

    def __init__(self, shuffle_step, randomness):
        """Initialise the properties.

        Arguments:
        shuffle_step -- base amount that the pixels are allowed to move as an int
        randomness -- amount that the shuffle_step is allowed to vary for each pixel as an int
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
        """Process an image so that its pixels are shuffled.

        This method processes an image so that the pixels of the
        image are shuffled with nearby pixels.
        """

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
        """Return a random square size.

        This method returns a random integer based on the
        shuffle step and randomness that will be used for
        the square size.
        The square size is random so that the resulting image
        is less uniform and grid-like.
        """

        squaresize = random.randrange(self.shuffle_step,
                                      self.shuffle_step * self.randomness)
        return squaresize


class ThreeColorEffect(Effect):

    """Store fields and methods used to reduce an image three colours.

    This class contains fields and methods that relate to processing an
    image so that it is only made up of three colours and a background colour.

    Public methods:
    do_effect -- applies the effect to the supplied Painting
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
        """Process an image so that it is made up of three colours and black.

        This method processes an image so that it is made up of three colours and
        a background colour iof black. The colour the pixels are changed to are
        dependant on the dominant colour component of the pixel.
        Note that this effect is currently only compatible with RGB images that
        don't have an alpha channel.
        """

        for component_index in range(color.NUMBER_OF_COLOR_COMPONENTS):
            self.change_dominant_color(component_index, painting)
        self.change_rest_to_black(painting)

    def change_dominant_color(self, current_component_index, painting):
        """Change the pixel to the appropriate replacement colour.

        This method changes the colour of the pixel to the replacement
        colour corresponding to the dominant colour component of the pixel.

        Arguments:
        current_component_index -- the index of the RGB colour component to be checked
        painting -- the Painting to be processed
        """

        for x in range(painting.width):
            for y in range(painting.height):
                current_coordinate = point.Point(x, y)
                current_pixel_color = painting.get_pixel_color(current_coordinate)
                can_change = self.check_dominant_color(current_pixel_color, current_component_index)

                if can_change:
                    painting.set_pixel_color(current_coordinate, self.replacement_colors[current_component_index])

    def check_dominant_color(self, current_pixel_color, target_component_index):
        """Check if the target colour component in a pixel is dominant.

        This method check if the colour component at target_component_index
        in a pixel is above the threshold and suitable greater than the other
        two colour components.
        The amount that the colour component must be greater than each of the
        other colour components multiplied by the effect's difference property.
        If the colour component passes these two checks, this method returns True.
        Otherwise, it returns False.
        """

        can_change = True

        for current_component_index in range(color.NUMBER_OF_COLOR_COMPONENTS):
            current_component_value = current_pixel_color.get_component_by_index(current_component_index)
            component_being_checked = current_pixel_color.get_component_by_index(target_component_index)

            if current_component_index != target_component_index:
                if (current_component_value >= component_being_checked * self.difference):
                    can_change = False
            elif current_component_value <= self.threshold:
                can_change = False

        return can_change

    def change_rest_to_black(self, painting):
        """Change the remaining pixels to black.

        This method changes the colour of any pixel that
        isn't one of the replacement_colors to black.
        """

        for x in range(painting.width):
            for y in range(painting.height):
                current_coordinate = point.Point(x, y)
                current_pixel_color = painting.get_pixel_color(current_coordinate)
                if current_pixel_color not in self.replacement_colors:
                    painting.set_pixel_color(current_coordinate, color.Color(*color.BLACK))


class TileEffect(Effect):

    """Store fields and methods used to posterise and tile an image.

    This class contains fields and methods that relate to posterising an
    image based on given colours and then tiling them in a grid.

    Public methods:
    do_effect -- applies the effect to the supplied Painting
    """

    def __init__(self, colors, levels, size):
        """Initialises the properties.

        Arguments:
        colors -- a list of Colors that the posterisation will be based on
        levels -- the number of posterisation levels as an integer
        size -- the number of tiles vertically and horizontally as an integer
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
        """Process an image so that it is posterised and tiled.

        This method processes an image so that the resulting image is
        made up of tiles that are smaller, posterised versions of the original
        image.
        The posterisations are based on  each of the colors in the colors property.
        """

        paintings = self.get_paintings(painting)
        # No need to assign/return as lists in python are passed by reference!
        self.color_posterise(paintings)
        new_painting = self.tile_images(paintings)
        painting.img = new_painting

    def get_paintings(self, painting):
        """Return a list of copies of the painting suitable for tiling.

        This method resizes the painting so that the resulting
        image after tiling is roughly the same size as the original image.
        It then adds a number of copies of the painting corresponding to
        the number of colours to a list and returns it.
        """

        paintings = []
        smaller_painting = self.resize_painting(painting)

        for i in range(self.number_of_colors):
            new_painting = smaller_painting.copy()
            paintings.append(new_painting)
        return paintings

    def resize_painting(self, painting):
        """Return a copy of the painting that is the size of a tile.

        This method resizes the painting so that the resulting image
        after tiling is roughly the same size as the original image.
        It then returns the resized painting.
        """

        tile_size = self.get_tile_size(painting)
        smaller_painting = painting.resize(tile_size)
        return smaller_painting

    def color_posterise(self, paintings):
        """Posterise each painting in the supplied list.

        This method posterises each painting in the supplied list
        based on the colours in self.colors.
        """

        # All paintings in paintings are the same at this point, so
        # arbitrarily using paintings[0] to get the data from the image
        for x in range(paintings[0].width):
            for y in range(paintings[0].height):
                current_coordinate = point.Point(x, y)
                current_pixel_color = paintings[0].get_pixel_color(current_coordinate)
                lum_step = float(color.MAX_COMPONENT_VALUE) / self.levels
                difference = color.MAX_COMPONENT_VALUE / self.levels

                if current_pixel_color.luminance <= lum_step:
                    for i in range(self.number_of_colors):
                        target_color = self.colors[i].copy()
                        paintings[i].set_pixel_color(current_coordinate, target_color)
                else:
                    lum = lum_step
                    next_lum = lum + lum_step
                    iterations = 1

                    # Cycle through the luminance thresholds
                    while lum < color.MAX_COMPONENT_VALUE:
                        if lum < current_pixel_color.luminance <= next_lum:
                            for i in range(self.number_of_colors):
                                target_color = self.colors[i].copy()
                                target_color.color = target_color + (difference * iterations)
                                paintings[i].set_pixel_color(current_coordinate, target_color)
                            # Move on to next pixel when threshold is found
                            break

                        else:
                            lum = next_lum
                            next_lum = lum + lum_step
                            iterations += 1

    def get_tile_size(self, painting):
        """Return the size of that each tile should be.

        This method returns the size that each tile should be
        as a tuple such that the resulting image will be roughly
        the same size as the original image.
        """

        tile_width = painting.width / self.size
        tile_height = painting.height / self.size
        return tile_width, tile_height

    def get_canvas_size(self, painting):
        """Return the size that the new painting will be.

        Returns the size that the resulting painting after tiling
        will be as a tuple.
        """

        canvas_width = painting.width * self.size
        canvas_height = painting.height * self.size
        return canvas_width, canvas_height

    def tile_images(self, paintings):
        """Tile each painting in the list into a grid of the given size.

        This method tiles each Painting in the supplied list of paintings
        in a grid of self.size*self.size tiles.
        It loops back to first Painting in paintings if there are more tiles
        than colors provided.

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