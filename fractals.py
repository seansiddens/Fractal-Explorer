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
        self.num_sample_points = sample_size
        self.image = Image.fromarray(self.data)
        self.brightness_factor = 2

    def render(self, threshold):
        print("Generating points....")
        points = self.gen_points(threshold)
        print("Exposing....")
        exposures = self.expose(points, threshold)
        print("Writing to image...")
        self.image_write(exposures)
        self.image = Image.fromarray(self.data)

    def render_color(self, red_threshold, green_threshold, blue_threshold):
        print("Generating red points....")
        red_points = self.gen_points(red_threshold)
        print("Exposing red channel....")
        red_exposures = self.expose(red_points, red_threshold)
        print("Writing to red channel....")
        self.image_write(red_exposures, 'R')

        print("Generating green points....")
        green_points = self.gen_points(green_threshold)
        print("Exposing green channel....")
        green_exposures = self.expose(green_points, green_threshold)
        print("Writing to green channel....")
        self.image_write(green_exposures, 'G')

        print("Generating blue points....")
        blue_points = self.gen_points(blue_threshold)
        print("Exposing blue channel....")
        blue_exposures = self.expose(blue_points, blue_threshold)
        print("Writing to blue channel....")
        self.image_write(blue_exposures, 'B')


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
        while len(points) < self.num_sample_points:
            random_val = complex(random.uniform(-2.5, 1), random.uniform(-1, 1))
            if not self.iterate(random_val, threshold):
                points.append(random_val)

                progress = len(points) / self.num_sample_points * 100
                if (progress - prev_progress) >= 1:
                    prev_progress = progress
                    print("Progress:", round(progress, 0), "%")

        return points

    def iterate(self, num, threshold):
        """ Iterates a number on the complex plane, returns True if part of set """

        c = num
        z = complex(0, 0)   # Initial starting value of Z
        for i in range(threshold):
            z = pow(z, 2) + c

            if z.real > 2 or z.imag > 2:
                return False
        return True

    def expose(self, complex_nums, threshold):
        """ Iterates a list of complex nums and tracks where they land in 2D array representing image """

        exposures = np.zeros((self.height, self.width))
        count = 1
        prev_progress = 0
        for num in complex_nums:
            progress = count / len(complex_nums) * 100
            if (progress - prev_progress) >= 1:
                prev_progress = progress
                print("Progress:", round(progress, 0), "%")

            c = num
            z = complex(0, 0)   # Initial starting value of Z
            for i in range(threshold):
                z = pow(z, 2) + c

                if z.real > 2 or z.imag > 2:
                    break

                pixel_loc = (int(translate(z.real, -2.5, 1, 0, self.width)), int(translate(z.imag, -1, 1, 0, self.height)))
                if 0 <= pixel_loc[0] < self.width and 0 <= pixel_loc[1] < self.height:
                    exposures[pixel_loc[1], pixel_loc[0]] += 1
            count += 1

        return exposures

    def image_write(self, exposures, channel=None):
        max_exposure = exposures.max()
        for y in range(self.height):
            for x in range(self.width):
                if channel == 'R':
                    self.data[y, x, 0] = int(translate(exposures[y, x], 0, max_exposure, 0, 255)*self.brightness_factor)

                elif channel == 'G':
                    self.data[y, x, 1] = int(translate(exposures[y, x], 0, max_exposure, 0, 255)*self.brightness_factor)

                elif channel == 'B':
                    self.data[y, x, 2] = int(translate(exposures[y, x], 0, max_exposure, 0, 255)*self.brightness_factor)

                elif channel is None:
                    self.data[y, x] = [int(translate(exposures[y, x], 0, max_exposure, 0, 255)*self.brightness_factor),
                                       int(translate(exposures[y, x], 0, max_exposure, 0, 255)*self.brightness_factor),
                                       int(translate(exposures[y, x], 0, max_exposure, 0, 255)*self.brightness_factor)]



