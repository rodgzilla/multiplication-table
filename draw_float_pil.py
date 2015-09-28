import math
import sys 
from PIL import Image
from PIL import ImageDraw
import multiprocessing

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

def draw_lines(x, y, radius, lines, filename):
    """This function uses gfxdraw to draw the initial circle in white and
    the previously computed lines in red.

    """
    img = Image.new('RGB', (2 * x, 2 * y))
    draw = ImageDraw.Draw(img)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius))
    for p1, p2 in lines:
        draw.line((p1, p2), fill = (255, 0, 0))
    img.save(filename)

def iterate_range(steps, param_sequence, folder_name):
    file_number = 1
    img_name = folder_name + "/mult_" + "{0:06}".format(file_number) + ".png"
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    
if __name__ == '__main__':
    # number of points on the circle.
    point_number = int(sys.argv[1])
    # radius of the circle.
    radius = int(sys.argv[2])
    # multiplication table that we draw.
    multiplier = float(sys.argv[3])

    # The size of the window is (2 * radius + 40, 2 * radius + 40) so
    # the center of the screen is (radius + 20, radius + 20)
    x_center = y_center = radius + 20

    # We compute the coordinates of the points on the circle, the
    # lines between the points and then we draw these lines.
    lines = compute_lines(x_center, y_center, point_number, multiplier)
    draw_lines(x_center, y_center, radius, lines, 'pil_render.bmp')

