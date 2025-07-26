import sys
import math
import itertools
import numpy as np



class Runner(object):

    def __init__(self, filename):

        self._groups = []
        lines = []

        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                if len(line) == 0:

                    if len(lines) > 0:
                        self._groups.append(self.make_array(lines))
                        lines = []
                else:
                    lines.append(line)

            if len(lines) > 0:
                self._groups.append(self.make_array(lines))
        finally:
            if fp: fp.close()

    def make_array(self, lines):
        # print(lines)
        cols = len(lines[0])
        rows = len(lines)

        array = np.zeros((rows, cols))
        for r in range(rows):
            line = lines[r]
            for c, ch in enumerate(line):
                if ch == '#': array[r,c] = 1

        return array

    def find_reflect(self, array):
        rows, cols = array.shape

        match_list = []

        for c in range(cols-1):

            c_left = c
            c_right = c + 1

            match = True

            while True:
                if not np.array_equal(array[:,c_left], array[:,c_right]):
                    match = False
                    break

                c_left -= 1
                if c_left < 0:
                    break

                c_right += 1
                if c_right >= cols:
                    break

            if match:
                # This returns after first reflecting line found
                match_list.append(c)

        return match_list


    def part1(self):

        score = 0

        for array in self._groups:

            # Check for vertical reflection
            match_list = self.find_reflect(array)
            if match_list:
                index = match_list[0]
                # print("FOUND MATCH AT COL", index)
                score += (index + 1)

            match_list = self.find_reflect(np.transpose(array))
            if match_list:
                # print("FOUND MATCH AT ROW", index)
                index = match_list[0]
                score += 100*(index+1)

        print("part1: total score", score)

    def part2(self):

        score = 0

        for array in self._groups:

            rows, cols = array.shape

            print("Check array -----------", rows, cols)

            #self.print_reflection_col(array, -1)
            #self.print_reflection_col(np.transpose(array), -1)

            match_original = {}

            # Check for vertical reflection
            match_list = self.find_reflect(array)
            if match_list:
                # print("FOUND ORIGINAL MATCH AT COL", index)
                index = match_list[0]
                key = "c%d" % index
                match_original[key] = True

            # Check for horizontal reflection
            match_list = self.find_reflect(np.transpose(array))
            if match_list:
                # print("FOUND ORIGINAL MATCH AT ROW", index)
                index = match_list[0]
                key = "r%d" % index
                match_original[key] = True

            print("match orig", match_original)

            match_new = {}

            for r in range(rows):
                for c in range(cols):
                    array_new = np.copy(array)

                    if array_new[r, c] == 0:
                        array_new[r, c] = 1
                    else:
                        array_new[r, c] = 0

                    match_list = self.find_reflect(array_new)
                    for index in match_list:
                        # print("FOUND SMUDGE MATCH AT COL", index)
                        key = "c%d" % index
                        match_new[key] = True
                        # self.print_reflection_col(array_new, index)

                    # Check for horizontal reflection
                    match_list = self.find_reflect(np.transpose(array_new))
                    for index in match_list:
                        # print("FOUND SMUDGE MATCH AT ROW", index)
                        key = "r%d" % index
                        match_new[key] = True
                        # self.print_reflection_row(array_new, index)

            # Sanity testing
            print("match new1", match_new)

            if len(match_new) == 0:
                if len(match_original) == 1:
                    print("NO SMUDGE MATCHES FOUND - KEEP ORIG")
                else:
                    raise ValueError("no smudge matches")

                match_new = match_original

            elif len(match_new) == 1:
                print("nothing changed")

                if len(match_original) != 1:
                    raise ValueError("something is wrong")

                for key in match_original.keys():
                    if key not in match_new:
                        raise ValueError("hmmmmm")

                match_new = match_original

            elif len(match_new) == 2:

                if len(match_original) != 1:
                    raise ValueError("no good")

                for key in match_original.keys():
                    if key not in match_new:
                        raise ValueError("hmmmmm")

                    try:
                        del match_new[key]
                    except:
                        pass

            else:
                raise ValueError("len new: %d" % len(match_new))

            print("match new2", match_new)

            if len(match_new) != 1:
                raise ValueError("nope")

            for key in match_new.keys():

                value = int(key[1:])
                print("key, value", key, value)

                if key[0] == 'c':
                    score += (value + 1)
                    self.print_reflection_col(array_new, value)
                elif key[0] == 'r':
                    score += 100*(value+1)
                    self.print_reflection_row(array_new, value)
                else:
                    raise ValueError("error")

            # input("continue...")

        print("part 2 total score", score)

    def print_reflection_col(self, array, col):

        print("*"*80)
        rows, cols = array.shape

        for r in range(rows):
            line = ''
            for c in range(cols):
                if array[r,c] == 0:
                    line += '.'
                else:
                    line += '#'


                if c == col:
                    line += ' | '
            print(line)

    def print_reflection_row(self, array, row):

        print("*"*80)
        rows, cols = array.shape

        for r in range(rows):
            line = ''
            for c in range(cols):
                if array[r,c] == 0:
                    line += '.'
                else:
                    line += '#'
            print(line)
            if r == row:
                print('-'*cols)


if __name__ == '__main__':

    # 30784 - too low (note... works for test input)
    # 47015 - too high
    runner = Runner(sys.argv[1])
    # runner.part1()
    runner.part2()

