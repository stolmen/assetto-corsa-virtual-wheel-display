"""
    Assetto Corsa Virtual Wheel plugin
    Author: Edward Ong
"""

import ac
import acsys

import sys
import logging





PLUGIN_VERSION = "v0.1"



stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)

logger = logging.getLogger("virtualwheel")
logger.addHandler(stream_handler)


def ac_log_shit(msg):
    ac.console(msg)
    ac.log(msg)


from wheeldrawer import WheelDrawer

app_window = None

class InGameWheelDrawer(WheelDrawer):
    scale = 10

    def paint(self, shape_points_collection) -> None:
        ac_log_shit('drwawing {} vectors'.format(len(shape_points_collection)))
        ac_log_shit(str(shape_points_collection))
        for shape_points in shape_points_collection:
            if len(list(shape_points)) != 4:
                ac_log_shit("Sorry, non quadrilateral shapes currently not supported")
            # assert (
            #     len(list(shape_points)) == 4
            # ), "Sorry, non quadrilateral shapes currently not supported"
            ac.glBegin(3)
            ac.glColor4f(1, 1, 1, 1)
            for point in shape_points:
                ac_log_shit("drawing point ({}, {})".format(point.x, point.y))
                success = ac.glVertex2f(point.x, point.y) == 1
                ac_log_shit("{} drawing point ({}, {})".format('SUCCESS' if success else 'FAILURE', point.x, point.y))
            ac.glEnd()

def acMain(ac_version):
    logger.debug("`acMain` called")

    app_name = "Virtual Wheel"
    logger.info("AC version: {}".format(ac_version))
    logger.info("Python version: {}".format(sys.version_info))
    logger.info("virtualwheel version: {}".format(PLUGIN_VERSION))

    global app_window
    app_window = ac.newApp(app_name)
    ac.setSize(app_window, 1000, 1000)
    ac.setTitle(app_window, "")
    ac.drawBorder(app_window, 0)
    ac.setIconPosition(app_window, 0, -9001)
    ac.setBackgroundOpacity(app_window, 0)
    ac.addRenderCallback(app_window, update)

    return app_name

def update(delta_t):
    # logger.debug("`update` called")
    assert app_window, "app_window not yet initialised?"
    ac.setBackgroundOpacity(app_window, 0)
    wheel_degrees = ac.getCarState(0, acsys.CS.Steer)
    InGameWheelDrawer().display(wheel_degrees)

