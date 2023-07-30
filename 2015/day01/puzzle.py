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



    def run(self):
        print("run")

        line = self._lines[0]

        floor = 0
        for i, c in enumerate(line):
            # print(c)

            if c == '(':
                floor += 1
            elif c == ')':
                floor -= 1

                if floor == -1:
                    print("enter basement at index", i + 1)
                    break

            else:
                raise ValueError("bed input")

        print("floor", floor)
        # print(self._numbers)


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
