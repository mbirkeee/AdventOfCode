import sys
import math
import itertools
import numpy as np
import matplotlib.pyplot as plt


NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

class Runner(object):

    def __init__(self, filename):

        lines = []

        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                if len(line) == 0:
                    break

                lines.append(line)

        finally:
            if fp: fp.close()

        # print(lines)
        cols = len(lines[0])
        rows = len(lines)

        array = np.zeros((rows, cols))
        for r in range(rows):
            line = lines[r]
            for c, ch in enumerate(line):
                if ch == '#':
                    array[r,c] = 2
                elif ch == 'O':
                    array[r,c] = 1

        self._array = array

    def part1(self):

        array = self._array

        array = self.tilt(array, NORTH)
        self.print_array(array)
        weight = self.get_weight(array)
        print("part1: weight", weight)

    def part2(self):
        array = self._array

        weightlist = []


        max_index = 500

        cycle = 0
        while True:
            array = self.tilt(array, NORTH)
            array = self.tilt(array, WEST)
            array = self.tilt(array, SOUTH)
            array = self.tilt(array, EAST)
            weight = self.get_weight(array)
            weightlist.append(weight)

            print("CYCLE", cycle, "WEIGHT", weight)
            # self.print_array(array)
            # input("continue...")
            cycle += 1

            if cycle == max_index:
                break

        value1 = weightlist[-1]
        value2 = weightlist[-2]
        value3 = weightlist[-3]
        value4 = weightlist[-4]
        value5 = weightlist[-5]

        match_indexes = []

        # Find a bunch of matching patters
        for i in range(max_index -1 , 100, -1):
            if weightlist[i] != value1:
                continue

            if weightlist[i-1] != value2:
                continue


            if weightlist[i-2] != value3:
                continue


            if weightlist[i-3] != value4:
                continue


            if weightlist[i-4] != value5:
                continue

            # print("Got match at index", i)
            match_indexes.append(i)

        print("match indexes", match_indexes)

        diff1 = match_indexes[0] - match_indexes[1]
        diff2 = match_indexes[1] - match_indexes[2]
        diff3 = match_indexes[2] - match_indexes[3]

        print("diffs", diff1, diff2, diff3)

        if diff1 == diff2 == diff3:
            pass
        else:
            raise ValueError("cound not determine repeating pattern length")

        print("repeating pattern length", diff1)

        cycles_left = 1000000000 - max_index
        cycles_remaining = cycles_left % diff1
        print("cycles remaining", cycles_remaining)

        for _ in range(cycles_remaining):
            array = self.tilt(array, NORTH)
            array = self.tilt(array, WEST)
            array = self.tilt(array, SOUTH)
            array = self.tilt(array, EAST)

        weight = self.get_weight(array)
        print("part2: weight", weight)

        # for i, value in enumerate(weightlist):
        #
        #     # Lets try to find a repeating pattern
        #     if weightlist[-1] == weightlist[i]
        #         print("repeat at position", i, value, weightlist[i], weightlist[i-1], weightlist[i-2])

        if False:
            # Compute the autocorrelation
            ac = self.autocorrelation(np.array(weightlist))
            print(ac)

            plt.plot(ac)
            plt.title("Autocorrelation")
            plt.xlabel("Lag")
            plt.ylabel("Autocorrelation")
            plt.show()

    def autocorrelation(self, signal):
        # Subtract the mean to remove DC offset
        signal = signal - np.mean(signal)

        # Compute the autocorrelation
        result = np.correlate(signal, signal, mode='full')

        # Normalize the result to range from -1 to 1
        # result = result[result.size // 2:]  # Keep only the positive lags
        result /= np.max(np.abs(result))  # Normalize to max absolute value

        return result

    def print_array(self, array):
        rows, cols = array.shape

        print("*"*cols)

        for r in range(rows):
            line = ''
            for c in range(cols):
                if array[r,c] == 0:
                    line += '.'
                elif array[r,c] == 1:
                    line += 'O'
                else:
                    line += '#'
            print(line)


    def get_weight(self, array):

        weight = 0

        rows, cols = array.shape

        for r in range(rows):
            for c in range(cols):
                if array[r, c] == 1:
                    # This is a rollable rock
                    weight += rows - r

        return weight


    def tilt(self, array_in, direction):


        if direction == NORTH:
            array = np.copy(array_in)
        elif direction == WEST:
            array = np.rot90(array_in, k=3)
        elif direction == SOUTH:
            array = np.rot90(array_in, k=2)
        elif direction == EAST:
            array = np.rot90(array_in, k=1)


        rows, cols = array.shape

        for r in range(rows):
            for c in range(cols):

                if array[r, c] != 1:
                    continue
                    # This is a rollable rock

                r_new = r
                while r_new > 0:
                    if array[r_new-1, c] == 0:

                        # This rock can roll up
                        array[r_new-1, c] = 1
                        array[r_new, c] = 0

                        r_new -= 1
                    else:
                        break


        if direction == WEST:
            array = np.rot90(array, k=1)
        elif direction == SOUTH:
            array = np.rot90(array, k=2)
        elif direction == EAST:
            array = np.rot90(array, k=3)

        return array

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    # runner.part1()
    runner.part2()

