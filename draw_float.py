import math
import sys 
import pygame
from pygame import gfxdraw
from pygame import Color


def compute_number_to_circle_point(x, y, point_number, radius):
    """This function compute a dictonary which associates to each number
    its coordinates on the circle.

    """
    angle = (2 * math.pi) / point_number
    return {i : (int(x + radius * math.sin(i * angle)), \
                 int(y + radius * math.cos(i * angle))) for i in range(point_number)}

def compute_lines(x_center, y_center, point_number, multiplier):
    """For each point x of the circle, this function computes (x *
    multiplier) mod len(points) and add the coordinates of the source
    and of the destination of the segment to the result list.

    """
    angle = (2 * math.pi) / point_number
    res = []
    for i in range(point_number):
        x_src = int(x_center + radius * math.sin(i * angle))
        y_src = int(y_center + radius * math.cos(i * angle))
        dst_value = (i * multiplier) % point_number
        x_dst = int(x_center + radius * math.sin(dst_value * angle))
        y_dst = int(y_center + radius * math.cos(dst_value * angle))
        res.append(((x_src, y_src), (x_dst, y_dst)))
    return res

def draw_lines(window, x, y, radius, lines):
    """This function uses gfxdraw to draw the initial circle in white and
    the previously computed lines in red.

    """
    gfxdraw.circle(window, x, y, radius, Color(255, 255, 255,255))
    for p1, p2 in lines:
        gfxdraw.line(window, p1[0], p1[1], p2[0], p2[1], Color(255, 0, 0,255))

if __name__ == '__main__':
    # number of points on the circle.
    point_number = int(sys.argv[1])
    # radius of the circle.
    radius = int(sys.argv[2])
    # multiplication table that we draw.
    multiplier = float(sys.argv[3])
    pygame.init()

    # The size of the window is (2 * radius + 40, 2 * radius + 40) so
    # the center of the screen is (radius + 20, radius + 20)
    window = pygame.display.set_mode((2 * radius + 40, 2 * radius + 40))
    x_center = y_center = radius + 20

    # We compute the coordinates of the points on the circle, the
    # lines between the points and then we draw these lines.
    lines = compute_lines(x_center, y_center, point_number, multiplier)
    draw_lines(window, x_center, y_center, radius, lines)

    # We save the picture.
    pygame.image.save(window, 'render.png')

    # The window stays open until it is closed manually by the user.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

