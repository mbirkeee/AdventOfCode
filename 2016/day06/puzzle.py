import sys
import itertools
from collections import Counter

class ExceptionDone(Exception):
    pass


class Runner(object):

    def __init__(self, filename):

        self._lines = []
        self._room_list = []

        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                self._lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(self._lines))

        self._map_pos = {}
        self.initialize()

    def initialize(self):

        print("initialize")

        for index, line in enumerate(self._lines):
            print(line)


    def add_line(self, line):

        for index, c in enumerate(line):
            pos = self._map_pos.get(index, {})
            count = pos.get(c, 0)
            pos[c] = count + 1
            self._map_pos[index] = pos



    def run(self):
        print("called")

        for line in self._lines:
            self.add_line(line)

        for index, v in self._map_pos.items():
            chars = [(count, c) for c, count in v.items()]
            chars.sort()
            print(index, chars)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
