import sys
import os
sys.path.append(os.path.dirname(__file__))

from shapes import ShapeCollection, Shape, Point

try:
    from typing import Tuple
    CanvasSizeType = Tuple[float, float]
except ImportError:
    CanvasSizeType = 'canvassizetype'

    
class Canvas:
    """
    Describe a finite size canvas which can be the target of zero or more of the following operations:
        - `add`: draw some shape on the canvas
        - `rotate`: rotate the entire canvas along with all previously added shapes about some point
    Once the desired canvas has been composed, then call `generate_vectors` to create a list of instructions
    on how to draw the resulting creation.
    """

    def __init__(self, size: CanvasSizeType):
        self.canvas_size_x = size[0]
        self.canvas_size_y = size[1]

        # This defines a list of polygons,
        # where each polygon is defined by ordered collections of three of more coordinates,
        # where each coordinate defines a polygon vertex.
        self.vectors = []

    def add(self, shape: Shape) -> None:
        self.vectors += shape.generate_vectors()

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

    def generate_vectors(self) -> ShapeCollection:
        return self.vectors

    def scale(self, x: float) -> None:
        """Scale the canvas by the given amount."""
        new_vectors = []
        for v in self.vectors:
            new_vectors.append([Point(p.x * x, p.y * x) for p in v])
        self.vectors = new_vectors

    def translate(self, x: float, y: float) -> None:
        """Translate the canvas"""
        self.vectors = [[i.translate(x, y) for i in v] for v in self.vectors]
