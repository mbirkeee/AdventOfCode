import numpy as np
import math
import sys

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self):
        self._increasing_count = 0

    def run(self):
        prev = None

        for line in sys.stdin:
            val = int(line.strip())
            if prev is not None:
                if val > prev:
                    self._increasing_count += 1
            prev = val

        print(self._increasing_count)

    def run2(self):
        # Part 2
        window = [None, None, None]
        prev = None

        for i, line in enumerate(sys.stdin):
            window[i % 3] = int(line.strip())

            try:
                val = sum(window)
            except Exception as err:
                continue

            if prev is not None:
                if val > prev:
                    self._increasing_count += 1
            prev = val

        print(self._increasing_count)


if __name__ == '__main__':
    runner = Runner()
    runner.run2()
