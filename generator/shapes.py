from abc import ABC, abstractmethod

import numpy as np
import io
from PIL import Image
import uuid
from os import path


class AbstractShape(ABC):
    r"""
           Synthetic geometric shape generator, each shape is generated in a
           200x200 image then saved in a 'png' file.

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
        self.painter.setposition(-160, 160)
        self.painter.pendown()
        self.painter.begin_fill()

        self.painter.goto(160, 160)
        self.painter.goto(160, -160)
        self.painter.goto(-160, -160)
        self.painter.goto(-160, 160)

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
        self.radius = np.random.randint(10, 75)
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
            Save the current drawing to a PNG image, the generated image is then
            saved in the parametrized path.

            The name of the save image is as follows :
                [Type of shape]_[UUID].png

        :return: None
        """
        ps = self.painter.getscreen().getcanvas().postscript(
            colormode='color', pageheight=199, pagewidth=199
        )
        im = Image.open(io.BytesIO(ps.encode('utf-8')))
        im.save(path.join(
            self.destination,
            self.__class__.__name__ + "_" + str(uuid.uuid1()) + '.png'
        ), quality=100, format='png')

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
        self.painter.penup()
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

        if self.__class__.__name__ == 'Star':
            self.painter.goto(r_coordinates[4])
        else:
            self.painter.goto(r_coordinates[-1])

        self.painter.pendown()
        self.painter.begin_fill()

        if self.__class__.__name__ == 'Star':
            for item in r_coordinates[:-1]:
                self.painter.goto(item)
            self.painter.end_fill()
            self.painter.begin_fill()
            self.painter.goto(r_coordinates[-1])
            self.painter.goto(r_coordinates[-3])
            self.painter.goto(r_coordinates[-2])
        else:
            for item in r_coordinates:
                self.painter.goto(item)

        self.painter.end_fill()
        self.painter.hideturtle()

    @abstractmethod
    def get_shape_coordinates(self):
        """
            Get the coordinate of each points constructing a shape with no
            rotation.

            Those coordinates are calculated in function of the centered point
            which coordinates are (self.x, self.y)

        :return: List of pairs
        """
        raise NotImplementedError()


class AbstractPolygonShape(AbstractShape, ABC):

    number_of_vertices = None

    def get_shape_coordinates(self):

        if not self.number_of_vertices:
            raise NotImplementedError(
                "The number of vertices must be specified in sub classes."
            )

        coordinates = []
        for vertex in range(self.number_of_vertices):
            coordinates.append(
                (
                    self.radius * np.cos(
                        2 * np.pi * vertex / self.number_of_vertices
                    ) + self.x,
                    self.radius * np.sin(
                        2 * np.pi * vertex / self.number_of_vertices
                    ) + self.y
                )
            )
        return coordinates


class Triangle(AbstractPolygonShape):

    number_of_vertices = 3


class Square(AbstractPolygonShape):

    number_of_vertices = 4


class Pentagon(AbstractPolygonShape):

    number_of_vertices = 5


class Hexagon(AbstractPolygonShape):

    number_of_vertices = 6


class Heptagon(AbstractPolygonShape):

    number_of_vertices = 7


class Octagon(AbstractPolygonShape):

    number_of_vertices = 8


class Nonagon(AbstractPolygonShape):

    number_of_vertices = 9


class Circle(AbstractShape):

    def draw(self):

        self.painter.setposition(self.x, self.y - self.radius)

        self.painter.pendown()
        self.painter.begin_fill()
        self.painter.ht()
        self.painter.circle(self.radius)
        self.painter.end_fill()

    def get_shape_coordinates(self):
        pass


class Star(AbstractPolygonShape):

    def get_shape_coordinates(self):
        pentagon_coordinates = []
        for vertex in range(6):
            pentagon_coordinates.append(
                (
                    self.radius * np.cos(2 * np.pi * vertex / 5) + self.x,
                    self.radius * np.sin(2 * np.pi * vertex / 5) + self.y
                )
            )

        pentagon_coordinates[5] = self.get_point(pentagon_coordinates[0], pentagon_coordinates[2], pentagon_coordinates[1], pentagon_coordinates[3])

        coordinates = [
            pentagon_coordinates[2],
            pentagon_coordinates[4],
            pentagon_coordinates[1],
            pentagon_coordinates[3],
            pentagon_coordinates[0],
            pentagon_coordinates[5]
        ]

        return coordinates

    def line_params(self, point_1, point_2):
        x_1, y_1 = point_1[0], point_1[1]
        x_2, y_2 = point_2[0], point_2[1]
        k = (y_1 - y_2) / (x_1 - x_2)
        b = y_1 - k * x_1
        return k, b

    def get_point(self, point_0, point_2, point_1, point_3):
        k_1, b_1 = self.line_params(point_0, point_2)
        k_2, b_2 = self.line_params(point_1, point_3)
        x = (b_2 - b_1) / (k_1 - k_2)
        y = k_1 * x + b_1
        return (x, y)
