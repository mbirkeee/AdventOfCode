import numpy as np
import math
import sys

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self):

        self._position = 0
        self._depth = 0
        self._aim = 0

        self._lines = []
        for line in sys.stdin:
            self._lines.append(line.strip())

    def run1(self):

        for line in self._lines:
            # print(line)
            parts = line.split()

            # print(parts)
            amount = int(parts[1].strip())
            cmd = parts[0].strip()

            if cmd.startswith('u'):
                self._depth -= amount
            elif cmd.startswith('d'):
                self._depth += amount
            elif cmd.startswith('f'):
                self._position += amount
            else:
                raise ValueError('bad cmd')

        print("depth", self._depth)
        print("position", self._position)

        print("parts1: %d" % (self._depth * self._position))

    def run2(self):


        for line in self._lines:
            parts = line.split()
            amount = int(parts[1].strip())
            cmd = parts[0].strip()

            if cmd.startswith('u'):
                self._aim -= amount
            elif cmd.startswith('d'):
                self._aim += amount
            elif cmd.startswith('f'):
                self._position += amount
                self._depth += self._aim * amount
            else:
                raise ValueError('bad cmd')

        print("depth", self._depth)
        print("position", self._position)

        print("parts1: %d" % (self._depth * self._position))


if __name__ == '__main__':
    runner = Runner()
    runner.run2()
