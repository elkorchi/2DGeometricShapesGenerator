import turtle

from generator.shapes import *


class GeometricShapes:

    def __init__(self, destination, size, animation=False):
        turtle.colormode(255)
        turtle.setup(width=200, height=200)
        turtle.screensize(160, 160)
        turtle.hideturtle()
        turtle.tracer(animation)
        turtle.speed("slowest")

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
