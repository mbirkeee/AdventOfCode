"""

"""
import numpy as np
import sys
import math
import itertools

class Box(object):

    def __init__(self, line):

        # print("this is the box line", line)
        parts = line.split('x')
        # print(parts)

        length = int(parts[0])
        width = int(parts[1])
        height = int(parts[2])

        face_1 = length * width
        face_2 = length * height
        face_3 = width * height

        face_perimeter_1 = 2 *(length + width)
        face_perimeter_2 = 2 *(length + height)
        face_perimeter_3 = 2 *(width + height)

        smallest_face = min([face_1, face_2, face_3])
        # print(face_1, face_2, face_3, smallest_face)

        smallest_perimeter = min([face_perimeter_1, face_perimeter_2, face_perimeter_3])

        self._area = 2 * (face_3 + face_2 + face_1) + smallest_face

        volume = length * width * height

        self._ribbon = smallest_perimeter + volume

    def get_area(self):
        return self._area

    def get_ribbon(self):
        return self._ribbon

class Runner(object):

    def __init__(self, filename):

        self._lines = []
        self._box_list = []
        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                if len(line) == 0:
                    continue

                self._lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(self._lines))

        total_area = 0
        total_ribbon = 0

        for line in self._lines:
            box = Box(line)

            total_area += box.get_area()
            total_ribbon += box.get_ribbon()

        print("total area required", total_area)
        print("total ribbon required", total_ribbon)

    def run(self):
        print("run")

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
