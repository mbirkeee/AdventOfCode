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

                if line.startswith('#'):
                    continue

                self._lines.append(line)

        finally:
            if fp: fp.close()

        self._replacement_list = []
        self._target = None
        self._map = {}

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

                self._replacement_list.append((start, stop))
                if stop in self._map:
                    raise ValueError("already have this!")

                self._map[stop] = start

            elif len(parts) == 1:
                print("this is the target")
                self._target = line
            else:
                raise ValueError("bad input")

    def run(self):

        print("run")
        print(self._map)
        replacement_count = 0

        l = []
        replacement_list = []
        for start, stop in self._map.items():
            print(start, stop)
            l.append((len(start), start, stop))

        l.sort()
        l.reverse()
        
        for item in l:
            replacement_list.append((item[1], item[2]))

        print(l)
        # return


        while True:

            changed = False
            # for old, new in self._map.items():
            for item in replacement_list:
                old = item[0]
                new = item[1]
                p = self._target.find(old)
                if p >= 0:
                    before = self._target[0:p]
                    after = self._target[p+len(old):]
                    fixed = before + new + after

                    print(self._target, " ==> ", fixed)
                    self._target = fixed
                    replacement_count += 1
                    changed = True
                    # break

            if not changed:
                break

            print(replacement_count)
            print(self._target)
            if self._target == 'e':
                break

        # for start, changes in self._map.items():
        #
        #     i = re.finditer(start, self._target)
        #     for p in i:
        #         pos = p.start()
        #         before = self._target[0:pos]
        #         after = self._target[pos+len(start):]
        #
        #         for change in changes:
        #             new = before + change + after
        #             self._target
        #             # print(new)
        #             self._result[new] = True
      #      parts = self._target.split(start)
      #      for change in changes:
      #          result = change.join(parts)
      #          print(result)
#        print("len(result", len(self._result))


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


