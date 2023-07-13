import numpy as np
import math
import sys

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self, filename):

        self._lines = []

        self._min = None
        self._max = None
        self._min_fuel = None

        f = open(filename, 'r')
        for line in f:
            self._lines.append(line.strip())
        f.close()

    def run(self):

        crab_count = 0
        for line in self._lines:
            parts = line.split(',')

            crab_count = len(parts)
            array1 = np.zeros(crab_count, dtype=np.int32)

            # print(array1)
            print("number of crabs: %d" % crab_count)

            for i, part in enumerate(parts):
                array1[i] = int( part.strip() )

        self._max = int(np.max(array1))
        self._min = int(np.min(array1))

        print("max: %d min: %d" % (self._max, self._min))

        #print(array1)
        for i in range(self._min, self._max + 1):
            pos = np.ones(crab_count, dtype=np.int32) * i
            # print(pos)
            total_dist = pos - array1
            # print(total_dist)
            # print(abs(total_dist))
            # fuel = sum(abs(total_dist))

            for j in range(len(total_dist)):
                steps = abs(total_dist[j])
                cost = sum( [c for c in range(steps, 0, -1)] )
                total_dist[j] = cost

            fuel = sum(abs(total_dist))
            if self._min_fuel is None or fuel < self._min_fuel:
                self._min_fuel = fuel

        print("Minimum fuel: %d" % self._min_fuel)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
