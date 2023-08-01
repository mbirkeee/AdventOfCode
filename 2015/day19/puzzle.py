import sys
import itertools
from collections import Counter
import numpy as np
import re

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

        self._map = {}
        self._target = None
        self._result = {}

        print("read %d lines" % len(self._lines))
        self.initialize()

    def initialize(self):

        print("initialize")

        for row, line in enumerate(self._lines):
            print(line)
            parts = line.split('=>')
            if len(parts) == 2:
                print("this is a replacement")

                start = parts[0].strip()
                stop = parts[1].strip()

                changes = self._map.get(start, [])
                changes.append(stop)
                self._map[start] = changes

            elif len(parts) == 1:
                print("this is the target")
                self._target = line

            else:
                raise ValueError("bad input")

    def run(self):

        print("run")
        print(self._map)

        for start, changes in self._map.items():

            i = re.finditer(start, self._target)
            for p in i:
                pos = p.start()
                before = self._target[0:pos]
                after = self._target[pos+len(start):]

                for change in changes:
                    new = before + change + after
                    # print(new)
                    self._result[new] = True
      #      parts = self._target.split(start)
      #      for change in changes:
      #          result = change.join(parts)
      #          print(result)
        print("len(result", len(self._result))


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


