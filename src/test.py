import pygame
from wheeldrawer import WheelDrawer
from shapes import ShapeCollection


class TestWheelDrawer(WheelDrawer):
    scale = 600 / 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pygame.init()
        self.screen = pygame.display.set_mode(size=(600, 600))

    def paint(self, vectors: ShapeCollection) -> None:
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
