"""Contain a function that processes and saves images for the gallery.

This module has a function that applies specific effects to specific images
and saves them for the Appropriation Art Exhibit.
"""

# Standard python libraries
import os
import time

# Own modules
import color
import effect
import painting


def show_gallery():
    """Apply effects to and display images.

    This function applies effects to images that will be
    used for the Appropriation Art Exhibit and saves the
    outputted images.
    If this function is run directly from this module, it
    will display the images in the default windows image
    viewer.

    Note that it takes a few minutes to process all of the images.
    """

    input_dir = "source-images"
    output_dir = "output-images"

    filenames = ["alf.png",
                 "hug.png",
                 "sad.jpg",
                 "jegermeister.jpg"]

    paintings = []
    for filename in filenames:
        paintings.append(painting.Painting(os.path.join(input_dir, filename)))

    effects = []
    # These colour values were arrived at through experimentation
    colors = (color.Color(150, 0, 150),             # Pinky colour
              color.Color(150, 150, 0),             # Yellowy colour
              color.Color(0, 150, 0),               # Light green
              color.Color(0, 150, 150))             # Light blue
    # Posterisation level 6 looked good when experimenting, and I wanted a 2x2 grid.
    tile_effect = effect.TileEffect(colors, 6, 2)
    effects.append(tile_effect)

    # Circle size and gap arrived at through experimentation
    dot_effect = effect.DotEffect(10, 5, color.Color(*color.BLACK))
    effects.append(dot_effect)

    # Shuffle step and randomness arrived at through experimentation
    shuffle_effect = effect.ShuffleEffect(10, 3)
    effects.append(shuffle_effect)

    colors = (color.Color(*color.MAGENTA),
              color.Color(*color.YELLOW),
              color.Color(*color.CYAN))
    # Theshold and difference arrived at through experimentation
    colorchange_effect = effect.ThreeColorEffect(50, 0.9, colors)
    effects.append(colorchange_effect)

    for i in range(len(effects)):
        if len(effects) == len(paintings):
            start = time.clock()
            # So that you can see its doing something
            print '%s' % 'processing ' '%s' % filenames[i], '%s' % '... '

            effects[i].do_effect(paintings[i])
            if __name__ == '__main__':
                paintings[i].show()

            end = time.clock()
            # So that you can see progress has been made
            print '%s' % filenames[i], '%s' % 'took ' '%f' % (end-start), '%s' % 'seconds'

        else:
            raise GalleryError("Number of input images is not equal to number of effects.")

    for i in range(len(paintings)):
        paintings[i].save(os.path.join(output_dir, filenames[i]))


class GalleryError(Exception):
    pass


if __name__ == '__main__':
    show_gallery()