"""
    Virtual Wheel plugin for Assetto corsa

    Author: Edward Ong
"""

try:
    import ac
    import acsys
except ImportError:
    print("Failed to import ac stuff. Is this being run outside of the AC context?")

from wheeldrawer import WheelDrawer


app_window = None


class InGameWheelDrawer(WheelDrawer):
    scale = 1

    def paint(self, shape_points_collection) -> None:
        for shape_points in shape_points_collection:
            assert (
                len(list(shape_points)) == 4
            ), "Sorry, non quadilateral shapes currently not supported"
            ac.glBegin(3)
            ac.glColor4f(1, 1, 1, 1)
            for point in shape_points:
                ac.glVertex2f(point.x, point.y)
            ac.glEnd()


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
