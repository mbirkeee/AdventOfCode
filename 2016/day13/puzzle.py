import sys
import numpy as np
import copy

class ExceptionDone(Exception):
    pass


class Runner(object):

    def __init__(self, filename):

        if filename.startswith('t'):
            # this is test mode
            self._cols = 10
            self._rows = 7
            self._fav = 10

            self._row_tgt = 4
            self._col_tgt = 7

        elif filename.startswith('p'):
            # this is test mode
            self._cols = 100
            self._rows = 100
            self._fav = 1350

            self._row_tgt = 39
            self._col_tgt = 31

        self.initialize()

        self._map = None

        self._min_steps = None

        self.build_map()
        self.print()

        self._total_locations = {}

    def print(self):

        print("*"*80)
        for r in range(self._rows):
            line = ""
            for c in range(self._cols):
                if self._map[r, c] == 1:
                    line += '#'
                else:
                    line += '.'
            print(line)
        print("*"*80)

    def build_map(self):

        self._map = np.zeros((self._rows, self._cols))

        for r in range(self._rows):
            for c in range(self._cols):
            #    print(r,c, type(r), type(c))
                x = c
                y = r
                temp = x*x + 3*x + 2*x*y + y + y*y
                temp += self._fav
            #    print(temp)
                b = "{0:b}".format(temp)
            #    print(b)
                ones = 0
                for ch in b:
                    if ch == '1':
                        ones += 1
             #   print(ones)
             #   print("------")
                if ones % 2:
                    # number of ones is ODD
             #       print(r,c, type(r), type(c))
                    self._map[r,c] = 1


    def initialize(self):

        print("initialize")

    def move(self,  data):

        r = data['r']
        if r < 0 or r >= self._rows:
            return

        c = data['c']
        if c < 0 or c >= self._cols:
            return

        if self._map[r, c] == 1:
            return

        path = data['p']
        if (r, c) in path:
            return

        path.append((r, c))
        self._total_locations[(r,c)] = True
        depth_cur = data['d']

        # print("At %d, %d (depth: %d)" % (r, c, depth_cur))

        # if r == self._row_tgt and c == self._col_tgt:
        #     if self._min_steps is None or depth_cur < self._min_steps:
        #         self._min_steps = depth_cur
        #
        #     print("At destination!", depth_cur, self._min_steps)
        #
        # if self._min_steps is not None:
        #     if depth_cur >= self._min_steps:
        #         return

        if depth_cur >= 50:
            return


        data['d'] = depth_cur + 1

        data_copy = copy.deepcopy(data)
        data_copy['r'] = r - 1
        self.move(data_copy)

        data_copy = copy.deepcopy(data)
        data_copy['r'] = r + 1
        self.move(data_copy)

        data_copy = copy.deepcopy(data)
        data_copy['c'] = c - 1
        self.move(data_copy)

        data_copy = copy.deepcopy(data)
        data_copy['c'] = c + 1
        self.move(data_copy)

    def run(self):

        print("run")

        data = {
            'r' : 1,
            'c' : 1,
            'd' : 0,
            'p' : []
        }

        self.move(data)

        print(len(self._total_locations))

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
