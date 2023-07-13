import copy
import numpy as np
import math

import sys

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self, filename):

        self._lines = []
        self._dots = []

        self._map = {}

        self._max_r = None
        self._max_c = None

        self._array = None
        self._commands = []

        f = open(filename, 'r')
        for line in f:
            self._lines.append(line.strip())
        f.close()

    def run(self):
        print("run")

        for line in self._lines:
            self.process_line(line)

        # Build array
        self._array = np.zeros((self._max_r+1, self._max_c+1), dtype=np.int32)

        # for i in range(self._max_r+1):
        #     self._array[i,:] = i

        # for i in range(self._max_c+1):
        #     self._array[:,i] = i

        for dot in self._dots:
            self._array[dot[0], dot[1]] = 1

        # print(self._array)

        array = self._array
        for command in self._commands:
            print(command)
            if command[0] == 'x':
                array = self.fold(array, col=command[1])
            else:
                array = self.fold(array, row=command[1])

        # array = self.fold(row=7)
        # array = self.fold(col=5)
        # array = self.fold(col=655)

        self.print_array(array)

        dot_count = np.sum(array)
        print("dot count: %d" % dot_count)

    def print_array(self, array):
        shape = array.shape
        rows = shape[0]
        cols = shape[1]

        for r in range(rows):
            s = ''
            for c in range(cols):
                if array[r, c] > 0:
                    s += '#'
                else:
                    s += ' '
            print(s)

    def fold(self, array, col=None, row=None):

        shape = array.shape
        rows = shape[0]
        cols = shape[1]

        print("fold", shape)

        if row is not None:
            # The row must be in the center
            middle_row = int(math.floor(rows/2.0))

            if middle_row != row:
                raise ValueError("bad input %d %d" % (middle_row, row))

            print("fold up at row", row)
            top = array[0:middle_row,:]
            bottom = array[middle_row + 1:,:]

#            print(top)
#            print(bottom)

            bottom = np.flipud(bottom)
#            print(bottom)

            folded = top + bottom
            # print("*"*80)
            # print(folded)

            folded = np.clip(folded, 0, 1)
            # print("*"*80)
            # print(folded)

            return folded

        if col is not None:
            # The col must be in the center
            middle_col = int(math.floor(cols/2.0))

            if middle_col != col:
                raise ValueError("bad input %d %d" % (middle_col, col))

            print("fold at col", col)

            left = array[:,0:middle_col]
            right = array[:, middle_col + 1:]

#             print(left)
#             print(right)

            right = np.fliplr(right)
            # print(right)

            folded = left + right
            # print("*"*80)
            # print(folded)

            folded = np.clip(folded, 0, 1)
            # print("*"*80)
            # print(folded)

            return folded


    def process_line(self, line):
        # print(line)

        if len(line) == 0:
            return

        if line.startswith('fold'):
            print("got fold command")
            parts = line.split()
            temp = parts[2]
            parts = temp.split('=')
            # print(parts)
            self._commands.append((parts[0], int(parts[1])))
            return

        parts = line.split(',')

        c = int(parts[0])   # x is column
        r = int(parts[1])   # y is row

        self._dots.append((r, c))

        if self._max_r is None or r > self._max_r:
            self._max_r = r

        if self._max_c is None or c > self._max_c:
            self._max_c = c


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()

