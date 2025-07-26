import os
import sys
import itertools


import numpy as np

class Galaxy(object):

    def __init__(self, index, r, c):
        self._index = index
        self._r_orig = r
        self._c_orig = c

        self._r_new = r
        self._c_new = c

        self._add = 999999


    def expand_row(self, row):
        if self._r_orig > row:
            self._r_new += self._add

    def expand_col(self, col):
        if self._c_orig > col:
            self._c_new += self._add

    def get_loc(self):
        return (self._r_new, self._c_new)

class Runner(object):

    def __init__(self, filename):

        self._lines = []

        fp = None

        self._rows = None
        self._cols = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()

                if len(line) == 0: continue

                self._lines.append(line)
                self._cols = len(line)

        finally:
            if fp: fp.close()

        self._rows = len(self._lines)
        print("ROWS: %d COLS: %d" % (self._rows, self._cols))

    def part2(self):

        map = np.zeros((self._rows, self._cols))
        galaxy_dict = {}
        galaxy_index = 1

        # Make galaxy objects and initial map
        for r, line in enumerate(self._lines):
            for c, ch in enumerate(line):
                if ch == '#':
                    galaxy_dict[galaxy_index] = Galaxy(galaxy_index, r, c)
                    map[r,c] = galaxy_index
                    galaxy_index += 1

                else:
                    map[r,c] = 0

        # print(galaxy_dict)

        # Make a list if the indexes of empty rows and cols
        empty_rows = []
        for r in range(self._rows):
            # print("row: %d sum: %d" % (r, np.sum(map[r,:])))
            if np.sum(map[r,:]) == 0:
                empty_rows.append(r)

        empty_cols = []
        for c in range(self._cols):
            if np.sum(map[:,c]) == 0:
                empty_cols.append(c)

        print("empty rows", empty_rows)
        print("empty cols", empty_cols)

        for row in empty_rows:
            # This is an empty row
            for galaxy in galaxy_dict.values():
                galaxy.expand_row(row)

        for col in empty_cols:
            # This is an empty row
            for galaxy in galaxy_dict.values():
                galaxy.expand_col(col)


        galaxy_list = [k for k in galaxy_dict.keys()]
        # Now get a list of all galaxy
        print(galaxy_list)

        total_distance = 0
        for pair in itertools.combinations(galaxy_list, 2):
            # print(pair)

            galaxy1 = galaxy_dict[pair[0]]
            galaxy2 = galaxy_dict[pair[1]]

            loc1 = galaxy1.get_loc()
            loc2 = galaxy2.get_loc()

            distance = self.get_distance(loc1, loc2)

            total_distance += distance

        print("part2: total distance: %d" % total_distance)


    def part1(self):
        print("part1")

        map = np.zeros((self._rows, self._cols))
        galaxy_count = 1


        for r, line in enumerate(self._lines):
            for c, ch in enumerate(line):
                if ch == '#':
                    map[r,c] = galaxy_count
                    galaxy_count += 1
                else:
                    map[r,c] = 0

        self.print_map(map)

        # Make a list if the indexes of empty rows and cols
        empty_rows = []
        for r in range(self._rows):
            # print("row: %d sum: %d" % (r, np.sum(map[r,:])))

            if np.sum(map[r,:]) == 0:
                empty_rows.append(r)

        empty_cols = []
        for c in range(self._cols):
            if np.sum(map[:,c]) == 0:
                empty_cols.append(c)

        print("empty rows", empty_rows)
        print("empty cols", empty_cols)

        new_rows = self._rows + len(empty_rows)
        new_cols = self._cols + len(empty_cols)

        map2 = np.zeros((new_rows, new_cols))

        row2 = 0
        for r in range(self._rows):
            if r in empty_rows:
                row2 += 1

            col2 = 0
            for c in range(self._cols):
                if c in empty_cols:
                    col2 += 1

                map2[row2, col2] = map[r,c]
                col2 += 1
            row2 += 1

        self.print_map(map2)

        # Now we have to get a list of all the galaxies
        self._rows = new_rows
        self._cols = new_cols


        galaxies = {}
        for r in range(self._rows):
            for c in range(self._cols):
                value = int(map2[r,c])
                if value > 0:
                    galaxies[value] = (r,c)

        print(galaxies)

        galaxy_list = [k for k in galaxies.keys()]
        # Now get a list of all galaxy
        print(galaxy_list)

        total_distance = 0
        for pair in itertools.combinations(galaxy_list, 2):
            #print(pair)

            loc1 = galaxies[pair[0]]
            loc2 = galaxies[pair[1]]

            distance = self.get_distance(loc1, loc2)

            total_distance += distance

        print("part1: total distance: %d" % total_distance)

    def get_distance(self, loc1, loc2):

        r = abs(loc1[0] - loc2[0])
        c = abs(loc1[1] - loc2[1])

        return r+c

    def print_map(self, map):

        rows, cols = map.shape
        for r in range(rows):
            line = ''
            for c in range(cols):
                if map[r,c] > 0:
                    line += '%d' % map[r,c]
                else:
                    line += '.'
            print(line)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.part1()
    runner.part2()
    #runner.part2()