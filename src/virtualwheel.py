"""
    Assetto Corsa Virtual Wheel plugin
    Author: Edward Ong
"""

import ac
import acsys

import sys
import logging


class AcHandler(logging.Handler):
    def emit(self, record):
        ac.console(record)


ac_handler = AcHandler()
ac_handler.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ac_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger = logging.getLogger("virtualwheel")
logger.addHandler(ac_handler)
logger.addHandler(stream_handler)


try:
    from wheeldrawer import WheelDrawer

    app_window = None

    class InGameWheelDrawer(WheelDrawer):
        scale = 1

        def paint(self, shape_points_collection) -> None:
            for shape_points in shape_points_collection:
                assert (
                    len(list(shape_points)) == 4
                ), "Sorry, non quadrilateral shapes currently not supported"
                ac.glBegin(3)
                ac.glColor4f(1, 1, 1, 1)
                for point in shape_points:
                    ac.glVertex2f(point.x, point.y)
                ac.glEnd()

    def acMain(ac_version):
        logger.debug("`acMain` called")

        app_name = "Virtual Wheel"
        logger.info("AC version: {}".format(ac_version))
        logger.info("Python version: {}".format(sys.version_info))

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
        logger.debug("`update` called")
        assert app_window, "app_window not yet initialised?"
        ac.setBackgroundOpacity(app_window, 0)
        wheel_degrees = ac.getCarState(0, acsys.CS.Steer)
        InGameWheelDrawer().display(wheel_degrees)


except:
    logger.exception("Unexpected exception occurred!")
