import sys
import os
sys.path.append(os.path.dirname(__file__))

import abc
from shapes import ShapeCollection, Annulus, Point, Line
from canvas import Canvas


class WheelDrawer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def paint(self, vectors: ShapeCollection) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def scale(self) -> float:
        return 1

    def display(self, wheel_rotation_degrees: float) -> None:
        # Hide ends of rectangular spokes behind the wheel by shortening the rectangular sections to
        # less than the outer diameter of the wheel.
        offset = 0.5

        # TODO: maybe make these parameters user configurable
        width = 10
        height = 10
        wheel_rim_thickness = 1

        
        padding = 1

        c = Canvas(size=(width, height))

        c.add(
            Line(
                Point(offset+padding, height / 2),
                Point(width - offset-padding, height / 2),
                thickness=wheel_rim_thickness,
            )
        )
        c.add(
            Line(
                Point(width / 2, height / 2),
                Point(width / 2, height - offset-padding),
                thickness=wheel_rim_thickness,
            )
        )
        c.add(
            Annulus(
                inner_radius=(width / 2) - padding - wheel_rim_thickness,
                outer_radius=width / 2 - padding,
                origin=Point(width / 2, height / 2),
            )
        )
        c.rotate(
            rotation_degrees=wheel_rotation_degrees,
            rotate_about=Point(width / 2, height / 2),
        )
        c.scale(self.scale)
        vectors = c.generate_vectors()

        self.paint(vectors)
