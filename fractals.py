import numpy as np
import random
from PIL import Image


def translate(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min

    value_scaled = float(value - left_min) / float(left_span)

    return right_min + (value_scaled * right_span)


class Buddhabrot:
    def __init__(self):
        self.width = 1750
        self.height = 1000
        self.data = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.num_sample_points = 10000

        self.red_threshold = 5000
        print("Generating red points....")
        self.red_points = self.gen_points(self.red_threshold)
        print("Exposing red channel....")
        self.red_exposures = self.expose(self.red_points, self.red_threshold)
        print("Writing to red channel....")
        self.image_write(self.red_exposures, 'R')

        self.green_threshold = 500
        print("Generating green points....")
        self.green_points = self.gen_points(self.green_threshold)
        print("Exposing green channel....")
        self.green_exposures = self.expose(self.green_points, self.green_threshold)
        print("Writing to green channel....")
        self.image_write(self.green_exposures, 'G')

        self.blue_threshold = 50
        print("Generating blue points....")
        self.blue_points = self.gen_points(self.blue_threshold)
        print("Exposing blue channel....")
        self.blue_exposures = self.expose(self.blue_points, self.blue_threshold)
        print("Writing to blue channel....")
        self.image_write(self.blue_exposures, 'B')

        self.image = Image.fromarray(self.data)

    def display(self):
        self.image.show()

    def save(self, file_name):
        self.image.save(file_name)

    def gen_points(self, threshold):
        """ Returns a list of random points in complex plane outside of the Mandelbrot set"""
        # Generate an initial list of random points on the image
        points = []
        while len(points) < self.num_sample_points:
            random_val = complex(random.uniform(-2.5, 1), random.uniform(-1, 1))
            if not self.iterate(random_val, threshold):
                points.append(random_val)
                if round(len(points) / self.num_sample_points * 100, 2) % 10 == 0:
                    print("Progress:", round(len(points) / self.num_sample_points * 100, 2), "%")

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
        for num in complex_nums:
            if round(count / len(complex_nums) * 100, 2) % 10 == 0:
                print("Progress:", round(count / len(complex_nums) * 100, 2), "%")

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
                    self.data[y, x, 0] = int(translate(exposures[y, x], 0, max_exposure, 0, 255))

                elif channel == 'G':
                    self.data[y, x, 1] = int(translate(exposures[y, x], 0, max_exposure, 0, 255))

                elif channel == 'B':
                    self.data[y, x, 2] = int(translate(exposures[y, x], 0, max_exposure, 0, 255))

                else:
                    self.data[y, x] = [int(translate(exposures[y, x], 0, max_exposure, 0, 255)),
                                       int(translate(exposures[y, x], 0, max_exposure, 0, 255)),
                                       int(translate(exposures[y, x], 0, max_exposure, 0, 255))]



