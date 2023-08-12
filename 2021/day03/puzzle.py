import numpy as np
import math
import sys

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self):

        self._lines = []

        for line in sys.stdin:
            self._lines.append(line.strip())

    def run(self):

        rows = len(self._lines)
        cols = len(self._lines[0])

        halfway = rows/2

        print("rows, cols", rows, cols)

        array = np.zeros( (rows, cols))

        for row, line in enumerate(self._lines):
            for col, c in enumerate(line):
                array[row, col] = int(c)

        # print(array)

        vector = np.sum(array, axis=0)
        print(vector)

        gamma = 0
        epsilon = 0
        for v in vector:
            print(v)
            gamma *= 2
            epsilon *= 2
            if v == halfway:
                raise ValueError("bad input")

            if v > halfway:
                gamma += 1
            else:
                epsilon += 1

        print("gamma", gamma, "epsilon", epsilon)

        print("Part 1: result: %d" % (gamma * epsilon))

        a = np.copy(array)
        b = np.copy(array)

        oxy_rating = self.get_rating(a, rows, cols, 'oxy')
        co2_rating = self.get_rating(b, rows, cols, 'co2')

        print("oxy_rating", oxy_rating)
        print("co2_rating", co2_rating)

        print("Part 2 result: %d" % (oxy_rating * co2_rating))

    def get_rating(self, array, rows, cols, kind):

        remaining = rows

        for col in range(cols):

            ones = 0
            zeros = 0

            # First count the number of 1s and 0s in the col of interest
            for row in range(rows):
                if array[row, col] == 1:
                    ones += 1
                elif array[row, col] == 0:
                    zeros += 1
                else:
                    continue

            print("ones", ones, "zeros", zeros)

            if ones == zeros:
                if kind == 'oxy':
                    keep = 1
                else:
                    keep = 0

            elif ones > zeros:
                if kind == 'oxy':
                    keep = 1
                else:
                    keep = 0
            else:
                if kind == 'oxy':
                    keep = 0
                else:
                    keep = 1

            for row in range(rows):
                if array[row, col] == -1:
                    continue

                if array[row, col] == keep:
                    continue

                # Discard this row entirely
                print("keep: %d discard col: %d; row %d: %s" % (keep, col, row, array[row,:]))
                array[row,:] = -1
                remaining -= 1
                if remaining == 1:
                    print("We have found the number we are looking for")

                    for r in range(rows):
                        if array[r, 0] != -1:
                            result = 0
                            for c in range(cols):
                                result *= 2
                                result += array[r, c]
                            return result
                    raise  ValueError("bad result")

if __name__ == '__main__':
    runner = Runner()
    runner.run()
