import sys
import copy
import itertools
from collections import Counter
import numpy as np

class ExceptionDone(Exception):
    pass

class CMD(object):

    ON          = 1
    SLIDE_ROW   = 2
    SLIDE_COL   = 3

class Runner(object):

    def __init__(self, filename):

        self._lines = []
        self._cmd_list = []

        if filename.find('test') > 0:
            self._rows = 3
            self._cols = 7
        else:
            self._rows = 6
            self._cols = 50

        self._screen = np.zeros((self._rows, self._cols), dtype=np.uint8)

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

        self.initialize()

    def initialize(self):

        print("initialize")

        for line in self._lines:
            print(line)

            if line.startswith('rect'):
                cmd = CMD.ON
                parts = line[5:].split('x')
                print(parts)
                row = int(parts[1])
                col = int(parts[0])
                self._cmd_list.append( (cmd, row, col) )

            elif line.startswith('rotate column'):
                cmd = CMD.SLIDE_COL
                pos = line.find('x=')
                # print(line[pos+2:])
                parts = line[pos+2:].split('by')
                # print(parts)
                col = int(parts[0].strip())
                row = int(parts[1].strip())
                self._cmd_list.append( (cmd, row, col) )

            elif line.startswith('rotate row'):
                cmd = CMD.SLIDE_ROW
                pos = line.find('y=')
                # print(line[pos+2:])
                parts = line[pos+2:].split('by')
                row = int(parts[0].strip())
                col = int(parts[1].strip())
                self._cmd_list.append( (cmd, row, col) )

            else:
                raise ValueError("bad input")

    def print(self):
        print('*'*80)

        for r in range(self._rows):
            row = ''
            for c in range(self._cols):
                if self._screen[r,c] == 0:
                    row += '.'
                else:
                    row += '#'

            print(row)

    def cmd_on(self, r, c):
        self._screen[0:r,0:c] = 1

    def cmd_slide_row(self, r, c):
        # print('slide row')
        for _ in range(c):
            row = copy.deepcopy(self._screen[r,:])

            self._screen[r, 1:self._cols] = row[0:self._cols-1]
            self._screen[r,0] = row[self._cols-1]

        # print(row)

    def cmd_slide_col(self, r, c):
        # print('slide col')
        for _ in range(r):
            col = copy.deepcopy(self._screen[:,c])
            # print(col)
            # print("test1", col[0:self._rows-1] )
            # print("test2", col[self._rows-1] )

            self._screen[1:self._rows, c] = col[0:self._rows-1]
            # self.print()

            # print("setting %d to %d" % ( self._screen[0,c], col[self._rows-1] ))

            self._screen[0,c] = col[self._rows-1]
            # self.print()


            # print('slide done')

    def run_cmd(self, cmd):
        if cmd[0] == CMD.ON:
            self.cmd_on(cmd[1], cmd[2])
        elif cmd[0] == CMD.SLIDE_ROW:
            self.cmd_slide_row(cmd[1], cmd[2])
        elif cmd[0] == CMD.SLIDE_COL:
            self.cmd_slide_col(cmd[1], cmd[2])

    def run(self):
        print("called")

        for cmd in self._cmd_list:
            # print("cmd:", cmd)
            self.run_cmd(cmd)
            self.print()
            print(np.sum(self._screen))
            input("continue...")

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
