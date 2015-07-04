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

def draw_lines(img, x, y, radius, lines):
    """This function uses ImageDraw.Draw to draw the initial circle in
    white and the previously computed lines in red.

    """
    draw = ImageDraw.Draw(img)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius))
    for p1, p2 in lines:
        draw.line((p1, p2), fill = (255, 0, 0))

def generate_image(args):
    """This function creates the image, compute the lines given the
    current parameters, draw the lines and save the image.

    """
    filename, x_center, y_center, point_number, multiplier = args
    print("filename ->", filename, "center =", (x_center, y_center) , "points ->",
          point_number, "multiplier ->", multiplier)
    img = Image.new('RGB', (2 * x_center, 2 * y_center))
    lines = compute_lines(x_center, y_center, point_number, multiplier)
    draw_lines(img, x_center, y_center, radius, lines)
    img.save(filename)

def iterate_range(steps, x_center, y_center, radius, param_sequence,
                  folder_name):
    """This function creates the list of arguments taht will be used to
    compute images. Then, it creates the processus pool and compute
    the images using multiprocessing.Pool.map().

    """
    args_list = []
    file_number = 1
    for i in range(len(param_sequence) - 1):
        for j in range(steps):
            img_name = folder_name + "/mult_" + "{0:06}".format(file_number) + ".png"
            point_number_diff = param_sequence[i + 1][0] - param_sequence[i][0]
            point_number = int(round(param_sequence[i][0] + ((j * point_number_diff) / float(steps))))
            multiplier_diff = param_sequence[i + 1][1] - param_sequence[i][1]
            multiplier = param_sequence[i][1] + ((j * multiplier_diff) / float(steps))
            args_list.append((img_name, x_center, y_center, point_number, multiplier))
            file_number += 1

    print("Creating process pool")
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    print("Launching computations")
    pool.map(generate_image, args_list)
    print("Computations done")
    
if __name__ == '__main__':
    # the name of the folder in which the images will be saved.
    folder_name = sys.argv[1]
    # Radius of initial circle.
    radius = int(sys.argv[2])
    # Number of transition the algorithm will to through to get from a
    # formula of the list to the next one.
    steps = int(sys.argv[3])
    param_sequence = [(100, 17), (300, 17), (300, 47), (100, 47)]

    # The size of the window is (2 * radius + 40, 2 * radius + 40) so
    # the center of the screen is (radius + 20, radius + 20)
    x_center = y_center = radius + 20

    # We compute the coordinates of the points on the circle, the
    # lines between the points and then we draw these lines.
    iterate_range(steps, x_center, y_center, radius, param_sequence, folder_name)
#    lines = compute_lines(x_center, y_center, point_number, multiplier)
#    draw_lines(x_center, y_center, radius, lines, 'pil_render.bmp')
