"""

"""
import numpy as np
import sys
import math
import itertools

class Santa(object):

    def __init__(self):
        self._row = 0
        self._col = 0

        key = '0,0'

        # Starting position gets a present!
        self._visits = {key:1}

    def move(self, c):
        if c == '^':
            self._row += 1
        elif c == '>':
            self._col += 1
        elif c == '<':
            self._col -= 1
        elif c == 'v':
            self._row -= 1
        else:
            raise ValueError("bad input")

        key = '%d,%d' % (self._row, self._col)

        count = self._visits.get(key, 0)
        count += 1
        self._visits[key] = count

    def get_visits(self):
        return self._visits

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

        santa1 = Santa()
        santa2 = Santa()

        for i, c in enumerate(line):
            if i % 2:
                santa1.move(c)
            else:
                santa2.move(c)

        visits1 = santa1.get_visits()
        visits2 = santa2.get_visits()

        for key, value in visits2.items():
            count = visits1.get(key, 0)
            count += value
            visits1[key] = count

        print('at least 1 present', len(visits1))

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
