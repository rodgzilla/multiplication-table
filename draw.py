import math
import sys 
import pygame
from pygame import gfxdraw
from pygame import Color


def compute_number_to_circle_point(x, y, point_number, radius):
    angle = (2 * math.pi) / point_number
    return {i : (int(x + radius * math.sin(i * angle)), \
                 int(y + radius * math.cos(i * angle))) for i in range(point_number)}

def compute_lines(points, multiplier):
    n = len(points)
    res = []
    for source in range(n):
        destination = (source * multiplier) % n
        res.append((points[source], points[destination]))
    return res

def draw_lines(window, x, y, radius, lines):
    gfxdraw.circle(window, x, y, radius, Color(255, 255, 255,255))
    for p1, p2 in lines:
        gfxdraw.line(window, p1[0], p1[1], p2[0], p2[1], Color(255, 0, 0,255))

if __name__ == '__main__':
    point_number = int(sys.argv[1])
    radius = int(sys.argv[2])
    multiplier = int(sys.argv[3])
    pygame.init()

    x_center = y_center = radius + 20

    window = pygame.display.set_mode((2 * radius + 40, 2 * radius + 40))
    points = compute_number_to_circle_point(x_center, y_center,
                                            point_number, radius)
    lines = compute_lines(points, multiplier)
    draw_lines(window, x_center, y_center, radius, lines)
    pygame.image.save(window, 'render.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

