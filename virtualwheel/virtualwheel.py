"""
    Virtual Wheel plugin for Assetto corsa

    Author: Edward Ong
"""

import abc
import math
from typing import Iterable, Tuple

try:
    import ac
    import acsys
except ImportError:
    print("Failed to import ac stuff. Is this being run outside of the AC context?")


import pygame

app_window = None


def acMain(ac_version):
    app_name = "Virtual Wheel"
    ac.console("lol.")
    ac.console("ac version: {}".format(ac_version))

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
    ac.console("update called")

    ac.setBackgroundOpacity(app_window, 0)
    wheel_degrees = ac.getCarState(0, acsys.CS.Steer)
    InGameWheelDrawer().display(wheel_degrees)


class Point:
    """Defines a point in a 2D cartesian space."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def rotate(self, rotation_degrees: float, rotate_about: "Point") -> "Point":
        # translate to origin
        translated_point = self.translate(-1 * rotate_about.x, -1 * rotate_about.y)

        # rotate about origin
        r = math.sqrt(translated_point.x ** 2 + translated_point.y ** 2)
        theta = math.atan2(translated_point.y, translated_point.x)
        new_theta = theta + rotation_degrees / 360 * 2 * math.pi
        new_x = r * math.cos(new_theta)
        new_y = r * math.sin(new_theta)

        # translate back to rotate_about Point
        return Point(new_x, new_y).translate(rotate_about.x, rotate_about.y)

    def translate(self, x: float, y: float) -> "Point":
        return Point(x + self.x, y + self.y)


ShapePoints = Iterable[Point]


class Shape(abc.ABC):
    @abc.abstractmethod
    def generate_vectors(self) -> Iterable[ShapePoints]:
        pass


class Annulus(Shape):
    def __init__(self, inner_radius: float, outer_radius: float, origin: Point):
        num_components = 50
        self.vectors = []
        inner_points = self._points_on_a_circle(
            origin=origin, radius=inner_radius, n=num_components
        )
        outer_points = self._points_on_a_circle(
            origin=origin, radius=outer_radius, n=num_components
        )

        def pair(x):
            x = list(x)  # this is bad. can I somehow not fully evaluate the iterable?
            for i in range(len(x)):
                yield x[i], x[(i + 1) % len(x)]

        for (inner_1, inner_2), (outer_1, outer_2) in zip(pair(inner_points), pair(outer_points)):
            self.vectors.append(
                [
                    inner_1,
                    outer_1,
                    outer_2,
                    inner_2,
                ]
            )

    def generate_vectors(self) -> Iterable[ShapePoints]:
        return self.vectors

    @staticmethod
    def _points_on_a_circle(origin: Point, radius: float, n: int) -> Iterable[Point]:
        return [
            Point(0, radius)
            .rotate(rotation_degrees=i * 360 / n, rotate_about=Point(0, 0))
            .translate(origin.x, origin.y)
            for i in range(n)
        ]


class Line(Shape):
    def __init__(self, start: Point, end: Point, thickness: float):
        line_angle_rad = math.atan2(end.y - start.y, end.x - start.x)
        delta_x = math.sin(line_angle_rad) * thickness / 2.0
        delta_y = math.cos(line_angle_rad) * thickness / 2.0

        self.vectors = [
            [
                Point(start.x - delta_x, start.y + delta_y),
                Point(end.x - delta_x, end.y + delta_y),
                Point(end.x + delta_x, end.y - delta_y),
                Point(start.x + delta_x, start.y - delta_y),
            ]
        ]

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
        self.vectors: Iterable[ShapePoints] = []

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

    def scale(self, x: float) -> None:
        """Scale the canvas by the given amount."""
        new_vectors = []
        for v in self.vectors:
            new_vectors.append([Point(p.x * x, p.y * x) for p in v])
        self.vectors = new_vectors


import abc


class WheelDrawer:
    @abc.abstractmethod
    def paint(self, vectors: Iterable[ShapePoints]) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def scale(self) -> float:
        return 1

    def display(self, wheel_rotation_degrees: float) -> None:
        # Hide ends of rectangular spokes behind the wheel by shortening the rectangular sections to
        # less than the outer diameter of the wheel.
        offset = 0.5

        width = 10
        height = 10
        wheel_rim_thickness = 1

        c = Canvas(size=(width, height))
        c.add(
            Annulus(
                inner_radius=(width / 2) - wheel_rim_thickness,
                outer_radius=width / 2,
                origin=Point(width / 2, height / 2),
            )
        )
        c.add(
            Line(
                Point(offset, height / 2),
                Point(width - offset, height / 2),
                thickness=wheel_rim_thickness,
            )
        )
        c.add(
            Line(
                Point(width / 2, height / 2),
                Point(width / 2, height - offset),
                thickness=wheel_rim_thickness,
            )
        )
        c.rotate(
            rotation_degrees=wheel_rotation_degrees,
            rotate_about=Point(width / 2, height / 2),
        )
        c.scale(self.scale)
        vectors = c.generate_vectors()
        self.paint(vectors)


class InGameWheelDrawer(WheelDrawer):
    scale = 1

    def paint(self, shape_points_collection: Iterable[ShapePoints]) -> None:
        # ac.console(
        #     "draw_quad called with params v1={}, v2={}, v3={}, v4={}".format(
        #         v1, v2, v3, v4
        #     )
        # )
        for shape_points in shape_points_collection:
            assert (
                len(list(shape_points)) == 4
            ), "Sorry, non quadilateral shapes currently not supported"
            ac.glBegin(3)
            ac.glColor4f(1, 1, 1, 1)
            for point in shape_points:
                ac.glVertex2f(point.x, point.y)
            ac.glEnd()


class TestWheelDrawer(WheelDrawer):
    scale = 600 / 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pygame.init()
        self.screen = pygame.display.set_mode(size=(600, 600))

    def paint(self, vectors: Iterable[ShapePoints]) -> None:
        self.screen.fill((0, 0, 0, 0))
        for shape_points in vectors:
            print(f"drawing {[(i.x, i.y) for i in shape_points]}")
            # pygame.display.flip()
            pygame.draw.polygon(
                self.screen, (255, 255, 255), [(i.x, i.y) for i in shape_points]
            )
        pygame.display.flip()


def main():
    import time

    drawer = TestWheelDrawer()
    for i in range(-181, 181):
        drawer.display(i)
        time.sleep(0.015)


if __name__ == "__main__":
    main()
