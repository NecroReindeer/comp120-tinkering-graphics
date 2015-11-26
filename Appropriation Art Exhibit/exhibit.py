__author__ = 'Harriet'

import os
import time

import color
import effect
import painting


def show_gallery():
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
    colors = (color.Color(150, 0, 150),
              color.Color(150, 150, 0),
              color.Color(0, 150, 0),
              color.Color(0, 150, 150))
    tile_effect = effect.TileEffect(colors, 6, 2)
    effects.append(tile_effect)

    dot_effect = effect.DotEffect(10, 5, color.Color(*color.BLACK))
    effects.append(dot_effect)

    shuffle_effect = effect.ShuffleEffect(10, 3)
    effects.append(shuffle_effect)

    colors = (color.Color(255, 0, 255),
              color.Color(255, 255, 0),
              color.Color(0, 255, 255))
    colorchange_effect = effect.ThreeColorEffect(50, 0.9, colors)
    effects.append(colorchange_effect)

    for i in range(len(effects)):
        # So that it doesn't matter if there are more or
        # less paintings than effects
        start = time.clock()
        painting_index = i % len(effects)
        print '%s' % 'processing ' '%s' % filenames[i], '%s' % '... '
        effects[i].do_effect(paintings[painting_index])
        if __name__ == '__main__':
            paintings[painting_index].show()
        end = time.clock()
        print '%s' % filenames[i], '%s' % 'took ' '%f' % (end-start), '%s' % 'seconds'

    for i in range(len(paintings)):
        paintings[i].save(os.path.join(output_dir, filenames[i]))


if __name__ == '__main__':
    show_gallery()