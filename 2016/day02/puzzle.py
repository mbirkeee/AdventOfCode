import sys
import itertools
from collections import Counter

MAP = {
    (0,0) : 1,
    (0,1) : 2,
    (0,2) : 3,

    (1,0) : 4,
    (1,1) : 5,
    (1,2) : 6,

    (2,0) : 7,
    (2,1) : 8,
    (2,2) : 9,
}

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self, filename):

        self._lines = []
        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                self._lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(self._lines))

        self.initialize()


    def initialize(self):

        print("initialize")

        for index, line in enumerate(self._lines):
            print(line)

    def run(self):
        print("run")

        row = 1
        col = 1

        for line in self._lines:
            for c  in line:
                # print(c)
                if c == 'U':
                    row -= 1
                    if row < 0: row = 0

                elif c == 'D':
                    row += 1
                    if row > 2: row = 2

                elif c == 'R':
                    col += 1
                    if col > 2: col = 1

                elif c == 'L':
                    col -= 1
                    if col < 0: col = 0
                else:
                    raise ValueError("bad input")

            print("number: %d" % MAP.get((row, col)))

    def run2(self):

        row = 2
        col = 0

        map = {
            (0, 2): '1',

            (1, 1): '2',
            (1, 2): '3',
            (1, 3): '4',

            (2, 0): '5',
            (2, 1): '6',
            (2, 2): '7',
            (2, 3): '8',
            (2, 4): '9',

            (3, 1): 'A',
            (3, 2): 'B',
            (3, 3): 'C',

            (4, 2): 'D',
        }

        if(0, 1) not in map:
            print("NOT IN MAP!!!")

        for line in self._lines:
            for c  in line:
                # print(c)
                if c == 'U':
                    row -= 1
                    if (row, col) not in map: row += 1

                elif c == 'D':
                    row += 1
                    if (row, col) not in map: row -= 1

                elif c == 'R':
                    col += 1
                    if (row, col) not in map: col -= 1

                elif c == 'L':
                    col -= 1
                    if (row, col) not in map: col += 1

                else:
                    raise ValueError("bad input")

            print("number: %s" % map.get((row, col)))

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run2()


