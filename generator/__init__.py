import turtle

from generator.shapes import *


class GeometricShapes:

    __GENERATORS__ = [
        Triangle, Circle, Heptagon, Octagon, Hexagon, Square, Star,
        Nonagon, Pentagon
    ]

    def __init__(self, destination, size, animation=False):
        turtle.colormode(255)

        # the canvas substract a pixel from the height
        turtle.setup(width=200, height=200)
        turtle.hideturtle()
        turtle.tracer(animation)

        container = turtle.Turtle()

        self.__size__ = size
        self.__shapes = [
            generator(
                destination, container
            ) for generator in self.__GENERATORS__
        ]

    def generate(self):
        for _ in range(self.__size__):
            for shape in self.__shapes:
                shape.generate()
