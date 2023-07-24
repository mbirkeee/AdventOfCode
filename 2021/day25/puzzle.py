"""

"""
import numpy as np
import sys
import math

EMPTY = ord('.')
LEFT = ord('>')
DOWN = ord('v')

class Runner(object):

    def __init__(self, filename):


        self._lines = []
        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                if len(line) == 0:
                    continue

                self._lines.append(line)

        finally:
            if fp: fp.close()


        print("read %d lines" % len(self._lines))

        self._rows = len(self._lines)
        self._cols = None

        self._map = None

        for row, line in enumerate(self._lines):
            cols = len(line)

            if self._cols is None:
                self._cols = cols
            else:
                if cols != self._cols:
                    raise ValueError("bad input")

            if self._map is None:
                self._map = np.zeros((self._rows, self._cols), dtype=np.uint32)
                print("rows: %d cols: %d" % (self._rows, self._cols))

            for col, c in enumerate(line):
                self._map[row, col] = ord(c)

    def print(self):

        print("-------------------------------------------------")
        for row in range(self._rows):
            s = ''
            for col in range(self._cols):
                s += chr(self._map[row,col])
            print(s)

    def step(self):

        move_list_left = []
        for row in range(self._rows):
            for col in range(self._cols):

                if self._map[row, col] != LEFT:
                    continue
                col_next = (col + 1) if col < (self._cols-1) else 0
                # print(row,  col, col_next)

                if self._map[row, col_next] != EMPTY:
                    continue

                move_list_left.append((row, col, col_next))

        # print("move list left", len(move_list_left))

        for move in move_list_left:
            row = move[0]
            col = move[1]
            col_next = move[2]
            self._map[row, col] = EMPTY
            self._map[row, col_next] = LEFT



        move_list_down = []
        for row in range(self._rows):
            for col in range(self._cols):

                if self._map[row, col] != DOWN:
                    continue
                row_next = (row + 1) if row < (self._rows-1) else 0

                if self._map[row_next, col] != EMPTY:
                    continue

                move_list_down.append((row, col, row_next))

        # print("move list down", len(move_list_down))

        for move in move_list_down:
            row = move[0]
            col = move[1]
            row_next = move[2]
            self._map[row, col] = EMPTY
            self._map[row_next, col] = DOWN

        return len(move_list_left) + len(move_list_down)

    def run(self):
        print("run")
        self.print()

        steps = 0
        while True:
            moves = self.step()

            steps += 1
            print("step: %d moves: %d" % (steps, moves))
            # self.print()
            if moves == 0:
                break

            # input("continue...")
        print("moves stopped after %d steps" % steps)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
