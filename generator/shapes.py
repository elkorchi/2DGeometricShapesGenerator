from abc import ABC

import numpy as np
import io
from PIL import Image
import uuid
from os import path


class AbstractShape(ABC):
    r"""
        Synthetic geometric shape generator, each shape is generated in a
        150x150 image then saved in a 'jpg' file.

        Args:
            destination: storage folder path
    """

    def __init__(self, destination, painter):
        self.painter = painter
        self.destination = destination
        self.radius = None
        self.x = None
        self.y = None

    def __set_random_bg_color(self):
        """
        Set a random background color on the turtle canvas.

        Since it's not possible to set this value directly into the canvas we
        draw a rectangle that fill all the drawing window with a random filling
        color, which set indirectly a visual background color to the canvas.

        :return: None
        """
        color = np.random.randint(0, 255, 3)

        self.painter.fillcolor(color[0], color[1], color[2])
        self.painter.color(color[0], color[1], color[2])
        self.painter.penup()
        self.painter.setposition(-100, 100)
        self.painter.pendown()
        self.painter.begin_fill()

        for _ in range(4):
            self.painter.forward(400)
            self.painter.right(90)

        self.painter.end_fill()
        self.painter.penup()

    def __set_random_params(self):
        """
        Set all the common random parameters of a Shape :

            - random background color
            - random filling color
            - random perimeter (deduced from the circumscribed circle's radius)
            - random rotation angle
            - center of the circumscribed circle of a shape

        :return: None
        """
        self.painter.reset()

        self.__set_random_bg_color()
        color = np.random.randint(0, 255, 3)
        self.painter.fillcolor(color[0], color[1], color[2])
        self.painter.color(color[0], color[1], color[2])
        self.painter.penup()
        self.radius = np.random.randint(10, 50)
        self.rotation = np.deg2rad(np.random.randint(-180, 180))

        self.x, self.y = (
            np.random.randint(
                -80 + self.radius,
                80 - self.radius
            ),
            np.random.randint(
                -80 + self.radius,
                80 - self.radius
            )
        )

    def __save_drawing(self):
        """
            Save the current drawing to a JPG image, the generated image is then
            saved in the parametrized path.

            The name of the save image is as follows :
                [Type of shape]_[UUID].jpg

        :return: None
        """
        ps = self.painter.getscreen().getcanvas().postscript(
            colormode='color'
        )
        im = Image.open(io.BytesIO(ps.encode('utf-8')))
        im.save(path.join(
            self.destination,
            self.__class__.__name__ + "_" + str(uuid.uuid1()) + '.jpg'
        ))

    def generate(self):
        """
            Generate an image that contains a shape drown inside it, in function
            of the set of random parameters that where configured in the
            function ‘__set_random_params‘.

        :return: None
        """
        self.__set_random_params()
        self.draw()
        self.__save_drawing()

    def draw(self):
        """
        Draw a shape in function of the nature of the shape and the set of
        random params specified in '__set_random_params' function.

        First we get the coordinate of each point that construct a shape then
        we apply to those coordinates a rotation a round the centered point
        specified in self.x and self.y, the resulted matrix is then used to draw
        the given shape.

        :return: None
        """
        shape_coordinates = self.get_shape_coordinates()
        r_coordinates = []

        for item in shape_coordinates:
            r_coordinates.append(
                (
                    (item[0] - self.x) * np.cos(self.rotation) -
                    (item[1] - self.y) * np.sin(self.rotation) + self.x,

                    (item[0] - self.x) * np.sin(self.rotation) +
                    (item[1] - self.y) * np.cos(self.rotation) + self.y
                )
            )

        self.painter.goto(r_coordinates[-1])

        self.painter.pendown()
        self.painter.begin_fill()
        self.painter.hideturtle()

        for item in r_coordinates:
            self.painter.goto(item)

        self.painter.end_fill()

    def get_shape_coordinates(self):
        """
            Get the coordinate of each points constructing a shape with no
            rotation.

            Those coordinates are calculated in function of the centered point
            which coordinates are (self.x, self.y)

        :return: List of pairs
        """
        raise NotImplementedError()


class Triangle(AbstractShape):

    min_width = 20
    max_width = 80

    def get_shape_coordinates(self):
        coordinates = [
            (
                self.x, self.y + self.radius,
            ), (
                self.x - self.radius, self.y - self.radius,
            ), (
                self.x + self.radius, self.y - self.radius,
            )
        ]

        return coordinates


class Square(AbstractShape):

    def get_shape_coordinates(self):

        return [
            (
                self.x - self.radius, self.y - self.radius,
            ), (
                self.x + self.radius, self.y - self.radius,
            ), (
                self.x + self.radius, self.y + self.radius,
            ), (
                self.x - self.radius, self.y + self.radius,
            )
        ]


class Star(AbstractShape):

    min_width = 20
    max_width = 80

    def get_shape_coordinates(self):
        pentagon_coordinates = []
        for vertice in range(5):
            pentagon_coordinates.append(
                (
                    self.radius * np.cos(2 * np.pi * vertice / 5) + self.x,
                    self.radius * np.sin(2 * np.pi * vertice / 5) + self.y
                )
            )

        coordinates = [
            pentagon_coordinates[3],
            pentagon_coordinates[1],
            pentagon_coordinates[4],
            pentagon_coordinates[2],
            pentagon_coordinates[0],

        ]

        return coordinates


class Hexagon(AbstractShape):

    min_width = 20
    max_width = 40

    def get_shape_coordinates(self):
        coordinates = []
        for vertice in range(6):
            coordinates.append(
                (
                    self.radius * np.cos(2 * np.pi * vertice / 6) + self.x,
                    self.radius * np.sin(2 * np.pi * vertice / 6) + self.y
                )
            )
        return coordinates


class Circle(AbstractShape):

    min_width = 10
    max_width = 40

    def draw(self):

        self.painter.setposition(self.x, self.y - self.radius)

        self.painter.pendown()
        self.painter.begin_fill()
        self.painter.ht()
        self.painter.circle(self.radius)
        self.painter.end_fill()

    def get_shape_coordinates(self):
        pass


class Pentagon(AbstractShape):

    min_width = 20
    max_width = 40

    def get_shape_coordinates(self):
        coordinates = []
        for vertice in range(5):
            coordinates.append(
                (
                    self.radius * np.cos( * np.pi * vertice / 5) + self.x,
                    self.radius * np.sin(2 * np.pi * vertice / 5) + self.y
                )
            )
        return coordinates


class Heptagon(AbstractShape):

    min_width = 20
    max_width = 40

    def get_shape_coordinates(self):
        coordinates = []
        for vertice in range(7):
            coordinates.append(
                (
                    self.radius * np.cos(2 * np.pi * vertice / 7) + self.x,
                    self.radius * np.sin(2 * np.pi * vertice / 7) + self.y
                )
            )
        return coordinates


class Octagon(AbstractShape):

    min_width = 20
    max_width = 40

    def get_shape_coordinates(self):
        coordinates = []
        for vertice in range(8):
            coordinates.append(
                (
                    self.radius * np.cos(2 * np.pi * vertice / 8) + self.x,
                    self.radius * np.sin(2 * np.pi * vertice / 8) + self.y
                )
            )
        return coordinates
