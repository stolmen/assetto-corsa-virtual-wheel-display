import abc
import typing
import math


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


ShapePoints = typing.Sequence[
    Point
]  # The definition of a shape through a collection of vertices
ShapeCollection = typing.Sequence[ShapePoints]  # Collection of shapes


class Shape(abc.ABC):
    @abc.abstractmethod
    def generate_vectors(self) -> ShapeCollection:
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

        for (inner_1, inner_2), (outer_1, outer_2) in zip(
            pair(inner_points), pair(outer_points)
        ):
            self.vectors.append(
                [
                    inner_1,
                    outer_1,
                    outer_2,
                    inner_2,
                ]
            )

    def generate_vectors(self) -> ShapeCollection:
        return self.vectors

    @staticmethod
    def _points_on_a_circle(origin: Point, radius: float, n: int) -> ShapePoints:
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

    def generate_vectors(self) -> ShapeCollection:
        return self.vectors
