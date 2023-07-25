"""

"""
import numpy as np
import sys
import math
import itertools

class Runner(object):

    def __init__(self, filename):

        self._lines = []
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

        self._numbers = []

        for line in self._lines:
            self._numbers.append(int(line))


    def run(self):
        print("run")

        # print(self._numbers)

        items = itertools.combinations(self._numbers, 2)

        for item in items:
            print(item)
            if item[0] + item[1] == 2020:
                print("found")
                print(item)
                print(item[0] * item[1])
                break

    def run2(self):
        print("run2")

        # print(self._numbers)

        items = itertools.combinations(self._numbers, 3)

        for item in items:
            # print(item)
            if item[0] + item[1] + item[2] == 2020:
                print("found")
                print(item)
                print(item[0] * item[1] * item[2])
                break

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run2()
