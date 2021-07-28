import sys
import ac
import acsys
import math


app_window = None


def acMain(ac_version):
    app_name = "Virtual Wheel"
    ac.console('lol.')
    ac.console('ac version: {}'.format(ac_version))

    global app_window
    app_window = ac.newApp(app_name)
    ac.setSize(app_window, 100, 140)
    ac.setTitle(app_window, "")
    ac.drawBorder(app_window, 0)
    ac.setIconPosition(app_window, 0, -9001)
    ac.setBackgroundOpacity(app_window, 0)
    ac.addRenderCallback(app_window, update)

    return app_name


def draw_wheel(degrees):
    ac.console('draw_wheel called with degrees = {}'.format(degrees))

    centre_x = 50
    centre_y = 50+40
    radius = 40
    thicc = 10

    # steering wheel
    # maybe just draw a fuckton of lines

    num_vertices_in_circle = 50
    for idx in range(num_vertices_in_circle):
        v1_x = centre_x + radius * math.sin(idx * 2 * math.pi / num_vertices_in_circle)
        v1_y = centre_y + radius * math.cos(idx * 2 * math.pi / num_vertices_in_circle)

        v2_x = centre_x + radius * math.sin((idx + 1) * 2 * math.pi / num_vertices_in_circle)
        v2_y = centre_y + radius * math.cos((idx + 1) * 2 * math.pi / num_vertices_in_circle)

        v3_x = centre_x + (radius - thicc) * math.sin((idx + 1) * 2 * math.pi / num_vertices_in_circle)
        v3_y = centre_y + (radius - thicc) * math.cos((idx + 1) * 2 * math.pi / num_vertices_in_circle)

        v4_x = centre_x + (radius - thicc) * math.sin(idx * 2 * math.pi / num_vertices_in_circle)
        v4_y = centre_y + (radius - thicc) * math.cos(idx * 2 * math.pi / num_vertices_in_circle)

        v1 = v1_x, v1_y
        v2 = v2_x, v2_y
        v3 = v3_x, v3_y
        v4 = v4_x, v4_y

        draw_quad(v1, v2, v3, v4)


    # spokes

    # horizontal spoke first
    radians = degrees / 360. * 2 * math.pi
    x1 = centre_x - radius * math.cos(radians)
    y1 = centre_y - radius * math.sin(radians)

    x2 = centre_x + radius * math.cos(radians)
    y2 = centre_y + radius * math.sin(radians)

    v1 = x1, y1
    v2 = x2, y2

    draw_thicc_line(v1, v2, thicc)

    # then vertical spoke

    x2 = centre_x - radius * math.sin(radians)
    y2 = centre_y + radius * math.cos(radians)

    v1 = centre_x, centre_y
    v2 = x2, y2

    draw_thicc_line(v1, v2, thicc)


def draw_quad(v1, v2, v3, v4):
    ac.console('draw_quad called with params v1={}, v2={}, v3={}, v4={}'.format(v1, v2, v3, v4))

    # ac.glBegin(acsys.GL.Lines)
    ac.glBegin(3)
    ac.glColor4f(1, 1, 1, 1)
    ac.glVertex2f(v1[0], v1[1])
    ac.glVertex2f(v2[0], v2[1])
    ac.glVertex2f(v3[0], v3[1])
    ac.glVertex2f(v4[0], v4[1])
    ac.glEnd()


def draw_thicc_line(v1, v2, thicc):
    line_angle_rad = math.atan2(v2[1]-v1[1], v2[0]-v1[0])
    delta_x = math.sin(line_angle_rad) * thicc / 2.
    delta_y = math.cos(line_angle_rad) * thicc / 2.

    x1_orig, y1_orig = v1
    x2_orig, y2_orig = v2

    x1 = x1_orig - delta_x
    y1 = y1_orig + delta_y
    v1 = x1, y1

    x2 = x2_orig - delta_x
    y2 = y2_orig + delta_y
    v2 = x2, y2

    x3 = x2_orig + delta_x
    y3 = y2_orig - delta_y
    v3 = x3, y3

    x4 = x1_orig + delta_x
    y4 = y1_orig - delta_y
    v4 = x4, y4

    draw_quad(v1, v2, v3, v4)


def update(delta_t):
    ac.console('update called')

    ac.setBackgroundOpacity(app_window, 0)
    wheel_degrees = ac.getCarState(0, acsys.CS.Steer)
    draw_wheel(wheel_degrees)
