import sys
import itertools
from collections import Counter

MAP = {
    'R' : {'N': 'E', 'E':'S', 'S':'W', 'W':'N'},
    'L' : {'N': 'W', 'W':'S', 'S':'E', 'E':'N'}
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



        self._move_list = []
        self._route_list = []
        self._coord_list = []

        self.initialize()


    def initialize(self):

        print("initialize")

        for index, line in enumerate(self._lines):
            parts = line.split(',')

            for part in parts:
                part = part.strip()
                dir = part[0]
                amount = int(part[1:])
                #print(dir, amount)
                self._move_list.append((dir, amount))

    def check_route(self, coord):

        # print(self._coord_list)

        prev_coord = self._coord_list[-1]
        # print(coord)
        # print(prev_coord)

        diff_row = coord[0] - prev_coord[0]
        diff_col = coord[1] - prev_coord[1]

        if diff_row:
            # We moved along rows
            if coord[0] > prev_coord[0]:
                for r in range(prev_coord[0], coord[0]):
                    p = (r + 1, coord[1])
                    if p in self._route_list:
                        raise ExceptionDone("been here before: %s" % repr(p))
                    self._route_list.append(p)

            else:
                for r in range(coord[0], prev_coord[0], -1):
                    p = (r - 1, coord[1])

                    if p in self._route_list:
                        raise ExceptionDone("been here before: %s" % repr(p))
                    self._route_list.append(p)
        else:
            # We moved along col
            if coord[1] > prev_coord[1]:
                for c in range(prev_coord[1], coord[1]):
                    p = (coord[0], c + 1)

                    if p in self._route_list:
                        raise ExceptionDone("been here before: %s" % repr(p))
                    self._route_list.append(p)
            else:
                for c in range(coord[1], prev_coord[1], -1):
                    p = (coord[0], c - 1)

                    if p in self._route_list:
                        raise ExceptionDone("been here before: %s" % repr(p))
                    self._route_list.append(p)

        self._coord_list.append(coord)

    def run(self):

        print("run")

        row = 0
        col = 0
        dir = 'N'

        coord = (0, 0)
        self._coord_list.append(coord)

        for move in self._move_list:
            amount = move[1]
            turn = move[0]

            map = MAP.get(turn)
            dir = map.get(dir)

            if dir == 'N':
                row += amount
            elif dir == 'E':
                col += amount
            elif dir == 'S':
                row -= amount
            elif dir == 'W':
                col -= amount

            coord = (row, col)

            self.check_route(coord)



        print(row, col)

        print("answer", abs(row)+abs(col))

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


