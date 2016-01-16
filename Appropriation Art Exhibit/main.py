"""Contain a class that builds a Kivy application.

This file contains a class for a Kivy application that
displays both the input and output images.
"""


# Standard Python libraries
import os

# External libraries
from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage

# Own modules
import exhibit


class ExhibitApp(App):
    """Display the original images and new images.

    This Kivy App displays each original image followed
    by the processed image in a Kivy carousel.
    """

    def build(self):
        """Return the Kivy carousel of gallery images when the app is run."""

        try:
            exhibit.show_gallery()
        except exhibit.GalleryError:
            print "Number of input images is not equal to number of effects."
            return

        output_dir = "output-images"
        input_dir = "source-images"

        carousel = Carousel(direction='right')
        source = ["alf.png",
                 "hug.png",
                 "sad.jpg",
                 "jegermeister.jpg"]
        for filename in source:
            original_image = AsyncImage(source=(os.path.join(input_dir, filename)), allow_stretch=True)
            carousel.add_widget(original_image)
            new_image = AsyncImage(source=(os.path.join(output_dir, filename)), allow_stretch=True)
            carousel.add_widget(new_image)
        return carousel

if __name__ == '__main__':
    ExhibitApp().run()