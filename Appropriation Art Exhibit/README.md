#COMP120 Tinkering Graphics Project
Source code contained within exhibit.py.

Dot effect now uses Bresenham's midpoint circle algorithm to draw circles (https://en.wikipedia.org/wiki/Midpoint_circle_algorithm). This has made it simpler and fixed the problem where circles were not drawn to the very edge of the image.  
I may adapt the dot effect so that it is able to convert images to be made out of other shapes.

Some methods can be made more general, such as the one that returns a list of pixel coordinates in a square.

I intend to make the colour changing effect work with both RGB and RGBA images, as currently it only works with RGB.

Tile effect needs tidying up and is currently quite slow.


##Source Images Used:

**jegermeister.jpg** TrollfesT JegerMeister T-shirt design (I can't find the image online anymore)

**sad.jpg** Image made by me

**hug.png** Image made by me

**alf.png** Image made by me
