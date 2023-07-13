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

        self._flash_count = 0
        self._array = None
        self._queue = []

        f = open(filename, 'r')
        for line in f:
            self._lines.append(line.strip())
        f.close()

    def run(self):
        print("run")

        self._rows = len(self._lines)
        self._cols = len(self._lines[0])

        self._array = np.zeros((self._rows, self._cols), dtype=np.int32)

        print("rows: %d cols: %d" % (self._rows, self._cols))

        for row, line in enumerate(self._lines):
            for col, c in enumerate(line):
                self._array[row, col] = int(c)


        print(self._array)

        steps = 0
        while True:

            # First, queue add operation for every octopus
            for r in range(self._rows):
                for c in range(self._cols):
                    self._queue.append((r, c))

            while True:
                if len(self._queue) == 0:
                    break

                point = self._queue.pop(0)

                r = point[0]
                c = point[1]

                if r < 0 or r >= self._rows or c < 0 or c >= self._cols:
                    # out of bounds
                    continue

                count = self._array[r, c]
                count += 1
                self._array[r, c] = count

                if count == 10:
                    self._flash_count += 1
                    # print("this is a flash!!")
                    self._queue.append((r,   c-1 ))
                    self._queue.append((r,   c+1 ))
                    self._queue.append((r-1, c-1 ))
                    self._queue.append((r-1, c   ))
                    self._queue.append((r-1, c+1 ))
                    self._queue.append((r+1, c-1 ))
                    self._queue.append((r+1, c   ))
                    self._queue.append((r+1, c+1 ))

            zero_count = 0
            for r in range(self._rows):
                for c in range(self._cols):
                    if self._array[r, c] >= 10:
                        self._array[r, c] = 0
                        zero_count += 1

            # print(self._array)
            # input("continue...")



            steps += 1
            # if steps == 100:
            #     break

            if zero_count == (self._rows * self._cols):
                break

        print(self._array)
        print("Flash count: %d" % self._flash_count)
        print("sync at step: %d" % steps)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
