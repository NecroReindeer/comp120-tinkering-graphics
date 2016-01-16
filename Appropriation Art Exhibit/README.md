#COMP120 Tinkering Graphics Project

Running the application from main.py will process the images and then display the outputs alongside the original images in a Kivy carousel. The images can be cycled through by swiping left and right.  

Running the exhibit.py directly will process the images and display the output images in the default image viewer.

##Additional Libraries and Frameworks Used:

[Pillow](https://python-pillow.github.io/)  
[Kivy](http://kivy.org/)

##Source Images Used:

**jegermeister.jpg** TrollfesT JegerMeister T-shirt design (I can't find the image online anymore)

**sad.jpg** Image made by me

**hug.png** Image made by me

**alf.png** Image made by me

##Application-Specific Modules
###character
Contains enemy and player classes

###color
Contains a class for storing and manipulating colours.

###effect
Contains classes relating to effects that can be applied to images.

###exhibit
Contains a function that processes and saves images for the gallery.

###painting
Contains a class for storing image data and manipulating images.

###point
Contains a class for storing and manipulating coordinate points.

##shape
Contains classes for drawing shapes. Currently only contains a class for circles.
