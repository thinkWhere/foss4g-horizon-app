import math
from height_data import HeightData
from PIL import Image

"""
Line Of Sight Map
"""

MAX_DISTANCE = 50000
SAMPLE_DISTANCE = 50
MILS = 6400
CHECK_DISTANCE = 25


def get_distance_colour(distance):
    """
    Calculates a colour based on the distance in metres (green -> getting blue-ier -> white)
    :param distance:
    :return: r, g, b
    """
    red = (255 * distance) // MAX_DISTANCE
    green = 255
    blue = (2 * 255 * distance) // MAX_DISTANCE
    if red > 255:
        red = 255
    if blue > 255:
        blue = 255
    return red, green, blue


def add_alpha(colour, alpha):
    """
    Add an alpha value to the colour
    :param colour:
    :param alpha:
    :return:
    """
    return colour[0], colour[1], colour[2], alpha


class DistanceColourRange:
    """
    Calculates colours to use based on a gradual change between 2 distance colours and a count of colours required
    """
    def __init__(self, count, start, end):
        """
        Initialises the start colour, and deltas to add per colour required
        :param count:
        :param start:
        :param end:
        """
        self.index = 0
        self.start_red, self.start_green, self.start_blue = get_distance_colour(start)
        end_red, end_green, end_blue = get_distance_colour(end)
        self.delta_red = (end_red - self.start_red) / count
        self.delta_green = (end_green - self.start_green) / count
        self.delta_blue = (end_blue - self.start_blue) / count

    def get_next_colour(self):
        """
        Caulculates and returns the next colour and increments the index
        :return:
        """
        red = self.start_red + round(self.index * self.delta_red)
        green = self.start_green + round(self.index * self.delta_green)
        blue = self.start_blue + round(self.index * self.delta_blue)
        self.index += 1
        return red, green, blue


class LineOfSightCalculator:
    def __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.h = h
        self.height_data = HeightData()
        self.sample_intervals = self._calculate_sample_intervals()
        self.height_values = []

        if self.h is None:
            self.h = self.height_data.get_height(self.x, self.y) + 2.0

    def get_bearing_line_of_sight(self, bearing):
        x_ratio = math.sin(bearing / 3200 * math.pi)
        y_ratio = math.cos(bearing / 3200 * math.pi)
        max_angle = -1000
        last_angle = 0
        peaks = []
        for iterator in list(range((MAX_DISTANCE // SAMPLE_DISTANCE)-1)):
            dist = (iterator + 1) * 50
            sample_x = self.x + (x_ratio * dist)
            sample_y = self.y + (y_ratio * dist)
            if bearing == 0:
                current_height = self.height_data.get_height(sample_x, sample_y)
                self.height_values.append(current_height)
            elif self.sample_intervals[iterator] < 2 or ((bearing % self.sample_intervals[iterator]) == 0):
                current_height = self.height_data.get_height(sample_x, sample_y)
                self.height_values[iterator] = self.height_data.get_height(sample_x, sample_y)
            else:
                current_height = self.height_values[iterator]

            angle = ((current_height - self.h) * 1000) // dist
            if iterator > 0 and angle < last_angle and angle > max_angle:
                peaks.append((int(last_angle), dist - 50))
                max_angle = last_angle
            last_angle = angle
        return peaks

    @staticmethod
    def _calculate_sample_intervals():
        angles = []
        for dist in list(range(SAMPLE_DISTANCE, MAX_DISTANCE, SAMPLE_DISTANCE)):
            interval = (CHECK_DISTANCE * 1000) // dist
            angles.append(interval)
        return angles


class LineOfSightMap:
    def __init__(self, x, y, h=None):
        self.bearings = []
        self.calculator = LineOfSightCalculator(x, y, h)
        self.observation_height = self.calculator.h

    def create_map(self):
        for bearing in list(range(6400)):
            self.bearings.append(self.calculator.get_bearing_line_of_sight(bearing))

    def create_image(self, filename):
        img = Image.new('RGBA', (6400, 1600))
        pixels = img.load()
        for i in range(img.size[0]):
            # Last peak at -800
            last_peak = -800
            last_distance = 0
            # Loop round peaks
            for peak, distance in self.bearings[i]:
                # print("{0} -> {1} ({2} -> {3})".format(last_peak, peak, last_distance, distance))
                # Calculate the colour range from the last distance to this one
                calc_colours = DistanceColourRange(peak - last_peak, last_distance, distance)
                # Fill colours into image
                for j in range(last_peak + 1, peak, 1):
                    pixels[i, 800-j] = add_alpha(calc_colours.get_next_colour(), 64)
                # Draw peak in red (for now)
                pixels[i, 800-peak] = add_alpha(get_distance_colour(distance), 128)
                # Update last peak and last distance
                last_peak = peak
                last_distance = distance
            # Fill in gap to the top
            # for j in range(last_peak, 801, 1):
            #    pixels[i, 800-j] = (0, 0, 0)
        img.save(filename)

    def is_visible(self, bearing, elevation, distance):
        """
        Check if a particular elevation/distance is visible on a particular bearing
        :param bearing:
        :param elevation:
        :param distance:
        :return:
        """
        bearing_to_check = self.bearings[bearing]
        for peak, peak_distance in bearing_to_check:
            if distance < peak_distance:
                return True
            elif peak > elevation:
                return False
            # else check next peak
        return True
