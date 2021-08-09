"""
    Virtual Wheel plugin for Assetto corsa

    Author: Edward Ong
"""

import abc
import sys
import math

import ac
import acsys


app_window = None


def acMain(ac_version):
    app_name = "Virtual Wheel"
    ac.console('lol.')
    ac.console('ac version: {}'.format(ac_version))

    global app_window
    app_window = ac.newApp(app_name)
    ac.setSize(app_window, 100, 140)
    ac.setTitle(app_window, "")
    ac.drawBorder(app_window, 0)
    ac.setIconPosition(app_window, 0, -9001)
    ac.setBackgroundOpacity(app_window, 0)
    ac.addRenderCallback(app_window, update)

    return app_name


def update(delta_t):
    ac.console('update called')

    ac.setBackgroundOpacity(app_window, 0)
    wheel_degrees = ac.getCarState(0, acsys.CS.Steer)
    InGameWheelDrawer().display(wheel_degrees)
    draw_wheel(wheel_degrees)


from typing import Iterable, Tuple



class Point:
    """ Defines a point in a 2D cartesian space. """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # TODO(EDWARD): this is probably fucked - write some tests for this
    def rotate(self, rotation_degrees: float, rotate_about: 'Point') -> 'Point':
        # translate to origin
        translated_point = self.translate(-1 * rotate_about.x, -1 * rotate_about.y)

        # rotate about origin
        r = math.sqrt(translated_point.x ** 2 + translated_point.y ** 2)
        theta = math.atan2(translated_point.y, translated_point.x)
        new_theta = theta + rotation_degrees / 360 * 2 * math.pi
        new_x = r * math.cos(new_theta)
        new_y = r * math.sin(new_theta)

        return Point(new_x, new_y).translate(rotate_about.x, rotate_about.y)

    def translate(self, x: float, y: float) -> 'Point':
        return Point(x + self.x, y + self.y)


ShapePoints = Iterable[Point]


class Shape(abc.ABC):
    @abc.abstractmethod
    def generate_vectors(self) -> Iterable[ShapePoints]:
        pass


class Annulus(Shape):
    def __init__(self, inner_radius: float, outer_radius: float, origin: Point):
        centre_x = origin.x
        centre_y = origin.y
        radius = outer_radius
        thiccness = outer_radius - inner_radius
        self.vectors = []

        num_vertices_in_circle = 50
        for idx in range(num_vertices_in_circle):
            v1_x = centre_x + radius * math.sin(idx * 2 * math.pi / num_vertices_in_circle)
            v1_y = centre_y + radius * math.cos(idx * 2 * math.pi / num_vertices_in_circle)

            v2_x = centre_x + radius * math.sin((idx + 1) * 2 * math.pi / num_vertices_in_circle)
            v2_y = centre_y + radius * math.cos((idx + 1) * 2 * math.pi / num_vertices_in_circle)

            v3_x = centre_x + (radius - thiccness) * math.sin((idx + 1) * 2 * math.pi / num_vertices_in_circle)
            v3_y = centre_y + (radius - thiccness) * math.cos((idx + 1) * 2 * math.pi / num_vertices_in_circle)

            v4_x = centre_x + (radius - thiccness) * math.sin(idx * 2 * math.pi / num_vertices_in_circle)
            v4_y = centre_y + (radius - thiccness) * math.cos(idx * 2 * math.pi / num_vertices_in_circle)

            v1 = Point(v1_x, v1_y)
            v2 = Point(v2_x, v2_y)
            v3 = Point(v3_x, v3_y)
            v4 = Point(v4_x, v4_y)

            self.vectors.append([v1, v2, v3, v4])

    def generate_vectors(self) -> Iterable[ShapePoints]:
        return self.vectors


class Line(Shape):
    def __init__(self, start: Point, end: Point, thickness: float):
        line_angle_rad = math.atan2(end.y - start.y, end.x - start.x)
        delta_x = math.sin(line_angle_rad) * thickness / 2.
        delta_y = math.cos(line_angle_rad) * thickness / 2.

        x1_orig, y1_orig = start.x, start.y
        x2_orig, y2_orig = end.x, end.y

        x1 = x1_orig - delta_x
        y1 = y1_orig + delta_y
        v1 = Point(x1, y1)

        x2 = x2_orig - delta_x
        y2 = y2_orig + delta_y
        v2 = Point(x2, y2)

        x3 = x2_orig + delta_x
        y3 = y2_orig - delta_y
        v3 = Point(x3, y3)

        x4 = x1_orig + delta_x
        y4 = y1_orig - delta_y
        v4 = Point(x4, y4)

        self.vectors = [[v1, v2, v3, v4]]

    def generate_vectors(self) -> Iterable[ShapePoints]:
        return self.vectors


class Canvas:
    """
        Describe a finite size canvas which can be the target of zero or more of the following operations:
            - `add`: draw some shape on the canvas
            - `rotate`: rotate the entire canvas along with all previously added shapes about some point
        Once the desired canvas has been composed, then call `generate_vectors` to create a list of instructions
        on how to draw the resulting creation.
    """

    def __init__(self, size: Tuple[float, float]):
        self.canvas_size_x = size[0]
        self.canvas_size_y = size[1]

        # This defines a list of polygons,
        # where each polygon is defined by ordered collections of three of more coordinates,
        # where each coordinate defines a polygon vertex.
        self.vectors = []

    def add(self, shape: Shape) -> None:
        v = shape.generate_vectors()
        self.vectors += v

    def rotate(self, rotation_degrees: float, rotate_about: Point) -> None:
        """
            Rotate all previously defined shapes drawn on the canvas by the given rotation amount in degrees.
            - A rotation of zero degrees is equivalent to doing nothing.
            - Positive rotation is arbitrarily chosen to be clockwise rotation.
        """
        new_vectors = []
        for v in self.generate_vectors():
            new_vectors.append([p.rotate(rotation_degrees, rotate_about) for p in v])
        self.vectors = new_vectors

    def generate_vectors(self) -> Iterable[ShapePoints]:
        return self.vectors


import abc
class WheelDrawer:
    @abc.abstractmethod
    def paint(self, vectors: Iterable[ShapePoints]) -> None:
        raise NotImplementedError

    def display(self, wheel_rotation_degrees: float) -> None:
        c = Canvas(size=(10, 10))
        c.add(Annulus(inner_radius=3, outer_radius=4, origin=Point(5, 5)))
        c.add(Line(Point(0, 5), Point(10, 5), thickness=1))
        c.add(Line(Point(5, 5), Point(5, 0), thickness=1))
        c.rotate(rotation_degrees=wheel_rotation_degrees, rotate_about=Point(0, 0))
        vectors = c.generate_vectors()
        self.paint(vectors)


class InCameWheelDrawer(WheelDrawer):
    def paint(self, shape_points_collection: Iterable[ShapePoints]) -> None:
        ac.console('draw_quad called with params v1={}, v2={}, v3={}, v4={}'.format(v1, v2, v3, v4))
        for shape_points in shape_points_collection:
            assert len(list(shape_points)) == 4, "Sorry, non quadilateral shapes currently not supported"
            ac.glBegin(3)
            ac.glColor4f(1, 1, 1, 1)
            for point in shape_points:
                ac.glVertex2f(point.x, point.y)
            ac.glEnd()


class TestWheelDrawer(WheelDrawer):
    def paint(self, vectors: Iterable[ShapePoints]) -> None:
        print(f'TEST vectors {vectors}')


def main():
    TestWheelDrawer().display(wheel_rotation_degrees=90)


if __name__ == '__main__':
    main()
