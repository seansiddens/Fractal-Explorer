import math
import numpy as np
import random
from PIL import Image


def translate(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min

    value_scaled = float(value - left_min) / float(left_span)

    return right_min + (value_scaled * right_span)


class Buddhabrot:
    def __init__(self, width, height, sample_size):
        self.width = width
        self.height = height

        self.data = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.exposures = np.zeros((3, self.height, self.width))

        self.batches = 10
        self.batch_size = sample_size // self.batches
        self.sample_size = self.batch_size * self.batches

        self.image = Image.fromarray(self.data)
        self.brightness_factor = 1
        self.threshold = 5000

    def render(self):
        current_batch = 1
        while current_batch <= self.batches:
            print("Starting batch:", current_batch)
            points = self.gen_points(self.threshold)
            self.expose(points)
            current_batch += 1

        self.image_write(color_mode=False)
        self.image = Image.fromarray(self.data)

    def render_color(self):
        current_batch = 1
        while current_batch <= self.batches:
            print("Starting batch:", current_batch)
            points = self.gen_points(self.threshold)
            self.expose(points)
            current_batch += 1

        self.image_write(color_mode=True)
        self.image = Image.fromarray(self.data)

    def display(self):
        self.image.show()

    def save(self, file_name):
        self.image.save(file_name)

    def gen_points(self, threshold):
        """ Returns a list of random points in complex plane outside of the Mandelbrot set"""
        prev_progress = 0
        # Generate an initial list of random points on the image
        points = []
        while len(points) < self.batch_size:
            random_val = complex(random.uniform(-2.5, 1), random.uniform(-1, 1))
            if not self.iterate(random_val, threshold):
                points.append(random_val)

                progress = len(points) / self.batch_size * 100
                if (progress - prev_progress) >= 1:
                    prev_progress = progress
                    print("Progress:", round(progress, 0), "%")

        return points

    def iterate(self, num, threshold):
        """ Iterates a number on the complex plane, returns True if part of set """
        p = math.sqrt(((num.real - .25) ** 2) + (num.imag ** 2))
        if (num.real <= p - 2 * (p**2) + .25) and (16 >= (num.real+1)**2 + num.imag**2):
            return True

        c = num
        z = complex(0, 0)   # Initial starting value of Z
        old_z = z
        for i in range(threshold):
            z = pow(z, 2) + c

            if z.real > 2 or z.imag > 2:
                return False

            if z == old_z:
                break

            if (i & (i-1) == 0) and (i != 0):
                old_z = z

        return True

    def expose(self, complex_nums):
        """ Iterates a list of complex nums and tracks where they land in 2D array representing image """
        red_threshold = 5000
        green_threshold = 500
        blue_threshold = 50

        count = 1
        prev_progress = 0
        for num in complex_nums:
            progress = count / len(complex_nums) * 100
            if (progress - prev_progress) >= 1:
                prev_progress = progress
                print("Progress:", round(progress, 0), "%")

            c = num
            z = complex(0, 0)   # Initial starting value of Z
            for i in range(red_threshold):
                z = pow(z, 2) + c

                if z.real > 2 or z.imag > 2:
                    break

                pixel_loc = (int(translate(z.real, -2.5, 1, 0, self.width)), int(translate(z.imag, -1, 1, 0, self.height)))
                if 0 <= pixel_loc[0] < self.width and 0 <= pixel_loc[1] < self.height:
                    if i <= red_threshold:
                        self.exposures[0, pixel_loc[1], pixel_loc[0]] += 1
                    if i <= green_threshold:
                        self.exposures[1, pixel_loc[1], pixel_loc[0]] += 1
                    if i <= blue_threshold:
                        self.exposures[2, pixel_loc[1], pixel_loc[0]] += 1

            count += 1

    def image_write(self, color_mode=False):
        red_max = self.exposures[0].max()
        print(red_max)
        green_max = self.exposures[1].max()
        print(green_max)
        blue_max = self.exposures[2].max()
        print(blue_max)

        if color_mode is True:
            for y in range(self.height):
                for x in range(self.width):
                    self.data[y, x] = [(255*math.sqrt(self.exposures[0, y, x]) / math.sqrt(red_max)),
                                       (255*math.sqrt(self.exposures[1, y, x]) / math.sqrt(green_max)),
                                       (255*math.sqrt(self.exposures[2, y, x]) / math.sqrt(blue_max))]

        else:
            for y in range(self.height):
                for x in range(self.width):
                    self.data[y, x] = [(255*math.sqrt(self.exposures[0, y, x]) / math.sqrt(red_max)),
                                       (255*math.sqrt(self.exposures[0, y, x]) / math.sqrt(red_max)),
                                       (255*math.sqrt(self.exposures[0, y, x]) / math.sqrt(red_max))]
