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
        self._basins = {}
        self._basin_sizes = []

        self._array = None
        self._checked = None
        self._rows = None
        self._cols = None

        f = open(filename, 'r')
        for line in f:
            self._lines.append(line.strip())
        f.close()



    def run(self):
        print("run")

        self._rows = len(self._lines)
        self._cols = len(self._lines[0])
        basin_index = 0

        print("rows", self._rows, "cols", self._cols)

        self._array = np.zeros( (self._rows, self._cols), dtype=np.uint32)
        self._checked = np.zeros( (self._rows, self._cols), dtype=np.uint32)

        for row, line in enumerate(self._lines):
            for col, c in enumerate(line):
                # print(row, col, int(c))
                self._array[row, col] = int(c)

        result = 0

        for row in range(self._rows):
            for col in range(self._cols):

                value = self._array[row, col]

                # Check above
                if row > 0:
                    if self._array[row-1, col] <= value:
                        continue

                # check below
                if row < self._rows-1:
                    if self._array[row+1, col] <= value:
                        continue

                # check left
                if col > 0:
                    if self._array[row, col-1] <= value:
                        continue

                # check right
                if col < self._cols-1:
                    if self._array[row, col+1] <= value:
                       continue

                # print("Found a low point!!!!", value, row, col)

                self._basins[basin_index] = (row, col)
                basin_index += 1

                result += (1 + value)

        print("Part 1 result", result)

        # Now move on to part two.  It says that 9s are not in a basin, and
        # every other point belongs to exactly one basin.  So we can "draw"
        # borders between the basins where the 9s are

        self.print_map()

        for basin_index, point in self._basins.items():
            count = 0
            count = self.check_point(point[0], point[1], count)
            print("basin: %d row: %d col: %d size: %d" % (basin_index, point[0], point[1], count))
            self._basin_sizes.append(count)

        self._basin_sizes.sort()
        self._basin_sizes.reverse()

        print("Part 2: %d" % (self._basin_sizes[0] * self._basin_sizes[1] * self._basin_sizes[2] ))

    def check_point(self, row, col, count):

        # print("check point", row, col)

        if self._checked[row, col] == 1:
            return count

        if self._array[row, col] == 9:
            return count

        self._checked[row, col] = 1

        # Check above
        if row > 0:
            count = self.check_point( row-1, col, count)
        #
        # Check below
        if row < self._rows-1:
            count = self.check_point( row+1, col, count)
        #
        # Check right
        if col < self._cols-1:
            count = self.check_point( row, col+1, count)
        #
        # check left
        if col > 0:
            count = self.check_point( row, col-1, count)

        count += 1

        return count

    def print_map(self):

        for r in range(self._rows):
            s = ''
            for c in range(self._cols):
                if self._array[r, c] == 9:
                    s += '#'
                else:
                    s += '.'
            print(s)

    def process_line(self, line):
        print(line)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
