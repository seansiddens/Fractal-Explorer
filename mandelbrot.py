import fractals
import scipy.misc as smp
import math
import random
import datetime
import seaborn as sns
import numpy as np
import PIL
from PIL import Image
import time
start_time = time.time()


def lerp(value, start1, stop1, start2, stop2):
    start_range = stop1 - start1
    target_range = stop2 - start2

    scale = target_range / start_range

    return start2 + (scale * value)


def translate(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min

    value_scaled = float(value - left_min) / float(left_span)

    return right_min + (value_scaled * right_span)


def mandelbrot(width, height, real_range, imag_range, depth):
    """ Returns a rendering of mandelbrot set """
    data = np.zeros((height, width, 3), np.uint8)  # pixel color data for image

    iteration_counts = np.zeros((height, width))  # Pairs each pixel with iteration count
    unique_colors = set()

    max_iterations = depth
    total_iterations = 0
    for y in range(height):
        print(str(y / height * 100) + "%")
        for x in range(width):
            xO = lerp(x, 0, width, real_range[0], real_range[1])
            yO = lerp(y, 0, height, imag_range[0], imag_range[1])

            c = complex(xO, yO)
            z = 0
            num = pow(z, 2) + c
            iterations = 0
            while num.real < 2 and num.imag < 2 and iterations <= max_iterations:
                num = pow(num, 2) + c
                iterations += 1

            iteration_counts[y, x] = iterations
            unique_colors.add(iterations)

    #print("# of iteration values:", len(unique_colors))

    color_palette = sns.color_palette('hls', len(unique_colors)+1)
    for i in range(len(color_palette)):
        rgb_value = []
        for value in color_palette[i]:
            value *= 255
            rgb_value.append(value)
        color_palette[i] = rgb_value

    #print("Length of color palette ", len(color_palette))

    for y in range(len(data)):
        print(str(y / height * 100) + "%")
        for x in range(len(data[y])):
            if iteration_counts[y, x] >= max_iterations:
                data[y, x] = [0, 0, 0]
            else:
                data[y, x] = color_palette[int(iteration_counts[y, x])]

    im = Image.fromarray(data)
    return im


def buddhabrot(width, height, num_points, threshold):
    data = np.zeros((height, width, 3), dtype=np.uint8)  # pixel color data for image

    initial_points = gen_points(num_points, threshold)  # random points are not part of the set - used in final iteration
    exposures = expose(initial_points, threshold, width, height)
    data = image_write(data, exposures, 'R')

    initial_points = gen_points(num_points, 500)
    exposures = expose(initial_points, 500, width, height)
    data = image_write(data, exposures, 'G')

    initial_points = gen_points(num_points, 50)
    exposures = expose(initial_points, 50, width, height)
    data = image_write(data, exposures, 'B')

    img = Image.fromarray(data)
    img.show()
    img.save("out.png")


def image_write(buffer, exposures, channel=None):
    max_exposure = exposures.max()
    for y in range(len(buffer)):
        for x in range(len(buffer[y])):
            if channel == 'R':
                buffer[y, x] = [int(translate(exposures[y, x], 0, max_exposure, 0, 255)),
                                0,
                                0]
            elif channel == 'G':
                buffer[y, x] = [0,
                                int(translate(exposures[y, x], 0, max_exposure, 0, 255)),
                                0]
            elif channel == 'B':
                buffer[y, x] = [0,
                                0,
                                int(translate(exposures[y, x], 0, max_exposure, 0, 255))]
            else:
                buffer[y, x] = [int(translate(exposures[y, x], 0, max_exposure, 0, 255)),
                                int(translate(exposures[y, x], 0, max_exposure, 0, 255)),
                                int(translate(exposures[y, x], 0, max_exposure, 0, 255))]

    return buffer


def gen_points(num, threshold):
    """ Returns a list of random points in complex plane outside of the Mandelbrot set"""
    print("Generating points....")
    # Generate an initial list of random points on the image
    points = []
    while len(points) < num:
        random_val = complex(random.uniform(-2.5, 1), random.uniform(-1, 1))
        if not iterate(random_val, threshold):
            points.append(random_val)
            print("Progress:", round(len(points) / num * 100, 2), "%")

    return points


def iterate(num, threshold):
    """ Iterates a number on the complex plane, returns True if part of set """

    c = num
    z = complex(0, 0)   # Initial starting value of Z
    for i in range(threshold):
        z = pow(z, 2) + c

        if z.real > 2 or z.imag > 2:
            return False
    return True


def expose(complex_nums, threshold, width, height):
    """ Iterates a list of complex nums and tracks where they land in 2D array representing image """
    print("Beginning exposures")

    exposures = np.zeros((height, width))
    count = 1
    for num in complex_nums:
        print("Progress:", round(count / len(complex_nums) * 100, 2), "%")
        c = num
        z = complex(0, 0)   # Initial starting value of Z
        for i in range(threshold):
            z = pow(z, 2) + c

            if z.real > 2 or z.imag > 2:
                break

            pixel_loc = (int(translate(z.real, -2.5, 1, 0, width)), int(translate(z.imag, -1, 1, 0, height)))
            if 0 <= pixel_loc[0] < width and 0 <= pixel_loc[1] < height:
                exposures[pixel_loc[1], pixel_loc[0]] += 1
        count += 1

    return exposures


if __name__ == "__main__":
    REAL_WINDOW = (-2.5, 1)
    IMAG_WINDOW = (-1, 1)

    WIDTH = 1750
    HEIGHT = 1000
    THRESHOLD = 500
    NUM_POINTS = 1000

    b = fractals.Buddhabrot(3500, 2000, 10000000)
    b.render()
    b.display()
    b.save('test-10000000n.png')

    #
    # SCALE = 150
    #
    # IMG_WIDTH = int((REAL_WINDOW[1] - REAL_WINDOW[0]) * SCALE)
    # IMG_HEIGHT = int((IMAG_WINDOW[1] - IMAG_WINDOW[0]) * SCALE)
    #
    # mandelbrot = mandelbrot(IMG_WIDTH, IMG_HEIGHT, REAL_WINDOW, IMAG_WINDOW, 100)
    # mandelbrot.save('out.png')

    # mandelbrot(zoom_width, zoom_height, zoom_real, zoom_imag, 100).save('zoom.png')

    total_time = time.time() - start_time
    print(round(total_time, 2), "s")

