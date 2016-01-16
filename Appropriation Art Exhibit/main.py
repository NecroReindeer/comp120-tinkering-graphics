__author__ = 'Hat'

import os

from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage

import exhibit


class ExhibitApp(App):

    def build(self):
        output_dir = "output-images"
        input_dir = "source-images"
        exhibit.show_gallery()
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