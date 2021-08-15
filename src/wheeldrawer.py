import abc
from shapes import ShapeCollection
from canvas import Canvas
from shapes import Annulus, Point, Line


class WheelDrawer:
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
