import sys
import itertools
from collections import Counter

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

        print("read %d lines" % len(self._lines))

        self._container_list = []
        self.initialize()


    def initialize(self):

        print("initialize")

        for index, line in enumerate(self._lines):
            volume = int(line)
            self._container_list.append(volume)

    def run(self):

        ways = 0

        print("run")
        print(self._container_list)
        print(len(self._container_list))

        for c in range(3, len(self._container_list) + 1):
            perm = itertools.combinations(self._container_list, c)

            temp = 0
            for i, item in enumerate(perm):
                # pass
                # print(item)
                if sum(item) == 150:
                    ways += 1
                    temp += 1
                # print(sum(item))
            print("items: %d combinations: %d  (%d)" % (c, i, temp))

        print("ways", ways)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


