"""
    Assetto Corsa Virtual Wheel plugin
    Author: Edward Ong
"""

import ac
import acsys

import logging

PLUGIN_VERSION = "v0.2"

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)

logger = logging.getLogger("virtualwheel")
logger.addHandler(stream_handler)


from wheeldrawer import WheelDrawer

app_window = None

class InGameWheelDrawer(WheelDrawer):
    scale = 10
    translate = (0, 40)

    def paint(self, shape_points_collection) -> None:   
        for shape_points in shape_points_collection:
            assert len(list(shape_points)) == 4, "Sorry, non quadrilateral shapes currently not supported"
            ac.glBegin(3)
            ac.glColor4f(1, 1, 1, 1)
            for point in shape_points:
                ac.glVertex2f(point.x, point.y) == 1
            ac.glEnd()


def acMain(ac_version):
    app_name = "Virtual Wheel"

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
    assert app_window, "expected app_window to be initialised."
    ac.setBackgroundOpacity(app_window, 0)
    wheel_degrees = ac.getCarState(0, acsys.CS.Steer)
    InGameWheelDrawer().display(wheel_degrees)
