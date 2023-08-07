import sys
import itertools
import math

from functools import reduce
import operator

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
                line = line.strip('.')

                if len(line) == 0:
                    continue

                self._lines.append(line)

        finally:
            if fp: fp.close()

        self._weights = []
        print("read %d lines" % len(self._lines))
        self.initialize()


    def initialize(self):

        print("initialize")

        for index, line in enumerate(self._lines):
            # print(line)
            self._weights.append(int(line))

            # parts = line.split(' ')
            # print(len(parts))
            # parts = [part.strip(',') for part in parts]
            # parts = [part.strip(':') for part in parts]

    def prod(self, iterable):
        return reduce(operator.mul, iterable, 1)

    def run(self):

        print("run")

        print(self._weights)
        total = sum(self._weights)
        print("total weight: %d" % total)
        print("group weight: %d" % (total // 4))

        target = total // 4

        groups = []

        qe_min = None

        for r in range(2, len(self._weights)):

            found = 0

            c = itertools.combinations(self._weights, r)

            for item in c:
                # print(item)
                if sum(item) == target:
                    print("found a group!!!", item)
                    found += 1
                    groups.append(item)

            if found > 0:
                break

        for i, item in enumerate(groups):
            print(i, item)
            qe = self.prod(item)
            if qe_min is None or qe < qe_min:
                qe_min = qe

        print("min qe", qe_min)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
