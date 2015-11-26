__author__ = 'Hat'

import os

from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage

import exhibit


class ExhibitApp(App):

    def build(self):
        directory = "output-images"
        exhibit.show_gallery()
        carousel = Carousel(direction='right')
        source = ["alf.png",
                 "hug.png",
                 "sad.jpg",
                 "jegermeister.jpg"]
        for filename in source:
            image = AsyncImage(source=(os.path.join(directory, filename)), allow_stretch=True)
            carousel.add_widget(image)
        return carousel

if __name__ == '__main__':
    ExhibitApp().run()