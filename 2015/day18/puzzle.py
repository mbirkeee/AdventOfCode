import sys
import itertools
from collections import Counter
import numpy as np

class Runner(object):

    def __init__(self, filename):

        self._lines = []
        fp = None

        line_len = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()

                if len(line) == 0:
                    continue

                if line_len is None:
                    line_len = len(line)
                else:
                    if line_len != len(line):
                        raise ValueError("bad line")

                self._lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(self._lines))

        self._cols = line_len
        self._rows = len(self._lines)

        # Put a 1 column border around the array
        self._array = np.zeros((self._rows+2, self._cols+2))
        print("rows", self._rows, "cols", self._cols)
        self.initialize()


    def initialize(self):

        print("initialize")

        for row, line in enumerate(self._lines):
            # print(line)
            for col, c in enumerate(line):
                # print(row, col, c)
                if c == '#':
                    self._array[row+1, col+1] = 1

        self.stuck_on()
        print(self._array)

    def stuck_on(self):
        self._array[1,1] = 1
        self._array[1,self._cols] = 1
        self._array[self._rows,1] = 1
        self._array[self._rows,self._cols] = 1

    def print_array(self):

        print("------------------------------------------------")
        for row in range(1,self._rows+1):
            line = ''
            for col in range(1, self._cols+1):
                if self._array[row, col] == 1:
                    line += '#'
                else:
                    line += '.'

            print(line)

    def process(self):

        array_new = np.zeros((self._rows+2, self._cols+2))

        for row in range(1,self._rows+1):
            for col in range(1, self._cols+1):
                surrounding = self._array[row-1:row+2,col-1:col+2]
                # print("--")
                # print(surrounding)
                on = int(np.sum(surrounding))

                if self._array[row, col] == 1:
                    # I am on
                    if on in [3,4]:
                        new = 1
                    else:
                        new = 0
                else:
                    # I am off
                    if on == 3:
                        new = 1
                    else:
                        new = 0

                array_new[row, col] = new

        self._array = array_new
        self.stuck_on()

    def run(self):

        print("run")
        self.print_array()

        for count in range(100):
            self.process()
            self.print_array()
            print("steps done", count+1)

        print(np.sum(self._array))

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


