import os
import sys

import numpy as np


EMPTY   = 0
VERT    = 1
HORIZ   = 2
NE      = 3
SE      = 4
SW      = 5
NW      = 6
START   = 7
OUTSIDE = 8

MAP = {
    'S' : START,
    '-' : HORIZ,
    '|' : VERT,
    'L' : NE,
    'J' : NW,
    '7' : SW,
    'F' : SE,
    '.' : EMPTY
}
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


        self._map = np.zeros((self._rows, self._cols), dtype=np.uint8)

        for r, line in enumerate(self._lines):
            print(line)
            for c, x in enumerate(line):

                self._map[r,c] = MAP[x]
                if x == 'S':
                    self._start = (r, c, START)

        print(self._map)

        print("Found start position at row %d col %d %d" % (self._start))



    def find_next(self, item):

        result = []

        r, c, kind = item
        # print("find next called, r:%d c:%d k:%d" % (r, c, kind))


        # Check UP (N)
        try:
            next = self._map[r-1, c]
            if next in [VERT, SW, SE, START]:
                # This one connect to N
                if kind in [START, VERT, NW, NE]:
                    result.append((r-1, c, next))
        except:
            pass

        # Check DOWN (S)
        try:
            next = self._map[r+1, c]
            if next in [VERT, NW, NE, START]:
                if kind in [START, VERT, SW, SE]:
                    result.append((r+1,c, next))
        except:
            pass

        # Check Left (W)
        try:
            next = self._map[r,c-1]
            if next in [HORIZ, SE, NE, START]:
                if kind in [START, HORIZ, SW, NW]:
                    result.append((r, c-1, next))
        except:
            pass

        # Check Right (E)
        try:
            next = self._map[r,c+1]
            if next in [HORIZ, SW, NW, START]:
                if kind in [START, HORIZ, NE, SE]:
                    result.append((r,c+1, next))
        except:
            pass

        return result



    def part1(self):
        print("part1")

        path = []
        next = self.find_next(self._start)

        # We should have two branches of the start position:
        print(next)

        if len(next) != 2:
            raise ValueError("expected 2 paths!")

        # choose the first path
        step = next[0]

        path.append(self._start)
        path.append(step)

        done = False
        # path_index = 2

        while True:
            next = self.find_next(step)

            if len(next) != 2:
                # Every step should have two next steps, forward and backward
                raise ValueError("expected")

            # print("ME: %s NEXT: %s PREV: %s" % (step, next, path[-2]))

            found_prev = False
            for item in next:
                if item == path[-2]:
                    # print("this is where we came from", path[-2])
                    found_prev = True
                else:
                    next_step = item

            # print("this is where we are going")
            # print("NEXT %s -> %s" % (step, next_step))
            path.append(next_step)
            step = next_step

            if item == path[0]:
                print("we are back at the start!")
                done = True
                break

            if not found_prev:
                print("ERROR did not find previous step!")
                done = True

            if done: break

        print("done")
        print("path", path)
        print(len(path))

        farthest = int( (len(path) - 1)/2 )

        print("part 1: farthest: %d" % farthest)

        return path


    def get(self, map, r, c):
        rows, cols = map.shape

        if r < 0 or r >= rows:
            #print("r", r, rows)
            raise ValueError()

        if c < 0 or c >= cols:
            #print("c", c, cols)
            raise ValueError()

        return map[r, c]

    def part2(self):

        print("part2")
        path = self.part1()

        print("create a new double sized array")


        rows = self._rows * 2
        cols = self._cols * 2
        map2 = np.zeros((rows, cols))

        for item in path:
            r, c, kind = item
            map2[r*2,c*2] = kind

        # Stretch the rows
        for r in range(rows):
            for c in range(cols):
                try:
                    left = self.get(map2, r, c-1)
                    right = self.get(map2, r, c+1)

                    if right in [START, HORIZ, NW, SW]:
                        if left in [START, HORIZ, NE, SE]:
                            map2[r, c] = HORIZ
                except:
                    pass

        self.print_map(map2)

        # Stretch the cols
        for c in range(cols):
            for r in range(rows):
                try:
                    above = self.get(map2, r-1, c)
                    below = self.get(map2, r+1, c)

                    if above in [START, VERT, SE, SW]:
                        if below in [START, VERT, NE, NW]:
                            map2[r, c] = VERT
                except:
                    pass


        self.print_map(map2)
        # return

        while True:
            map2, changes = self.find_out(map2)
            self.print_map(map2)
            print("changes", changes)
            if changes == 0:
                break

            # input("continue...")

        map3, inside = self.clean_up(map2)

        self.print_map(map3)
        print("part 2: inside: %d" % inside)

    def clean_up(self, map):

        inside = 0

        final = np.zeros((self._rows, self._cols))

        for r in range(self._rows):
            for c in range(self._cols):
                final[r,c] = map[r*2, c*2]
                if final[r,c] == EMPTY:
                    inside += 1
        return final, inside

    def find_out(self, map):

        changes = 0

        rows, cols = map.shape

        for r in range(rows):
            for c in range(cols):
                try:
                    if map[r,c] == EMPTY:
                        above = self.get(map, r-1, c)
                        below = self.get(map, r+1, c)
                        left =  self.get(map, r, c-1)
                        right = self.get(map, r, c+1)

                        if above == OUTSIDE or below == OUTSIDE or left == OUTSIDE or right == OUTSIDE:
                            map[r, c] = OUTSIDE
                            changes += 1
                except:
                    map[r,c] = OUTSIDE
                    changes += 1

        return map, changes


    def print_map(self, map):

        print("*"*80)
        rows, cols = map.shape

        for r in range(rows):
            s = ''
            for c in range(cols):
                if map[r, c] == EMPTY:
                    s = s + '.'
                elif map[r, c] == OUTSIDE:
                    s = s+ 'O'
                else:

                    s = s + '*'
            print(s)

    def part2_failed(self):
        print("part2")
        path = self.part1()

        # Loop through every point in the map: Determine if:
        # 1. The point is part of the loop pipe.
        # 2. If not part of the pipe, if it needs to cross the pipe an even number of times,
        #    it is not in the loop.  If it needs to cross an odd number of tines, it is in the loop

        path = [(item[0], item[1]) for item in path]
        print(path)

        result = 0

        for r in range(self._rows):

            for c in range(self._cols):
                item = (r,c)

                if item in path:
                    print("item in path")
                    continue

                print("consider item", item)

                row = r
                pipe_count = 0
                while True:
                    row += 1
                    if row >= self._rows:
                        break

                    next = (row, c)
                    print("test next", next)
                    if next in path:
                        pipe_count += 1

                if pipe_count % 2:
                    # Odd number of pipe crossings, item is in loop!
                    result += 1

                print("pipe crossings:", pipe_count)

        print("part 2: items in loop", result)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    # runner.part1()
    # runner.part2_failed1()
    runner.part2()