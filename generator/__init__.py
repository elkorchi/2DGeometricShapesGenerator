import turtle

from generator.shapes import *


class GeometricShapes:

    def __init__(self, destination, size, animation=False):
        turtle.colormode(255)

        # the canvas substract a pixel from the height
        turtle.setup(width=200, height=201)
        turtle.screensize(160, 160)
        turtle.hideturtle()
        turtle.tracer(animation)

        container = turtle.Turtle()

        self.__size__ = size
        self.__shapes = [
            shape(
                destination, container
            ) for shape in AbstractShape.__subclasses__()
        ]

    def generate(self):
        for _ in range(self.__size__):
            for shape in self.__shapes:
                shape.generate()
