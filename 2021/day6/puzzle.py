import numpy as np
import math
import sys

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self):

        self._filename = 'input_real.txt'

        self._fish = {}
        self._lines = []

        for i in range(9):
            self._fish[i] = 0

        f = open(self._filename, 'r')
        for line in f:
            self._lines.append(line.strip())
        f.close()

    def run(self):

        for line in self._lines:
            parts = line.split(',')
            for part in parts:
                timer = int( part.strip() )
                count = self._fish[timer]
                self._fish[timer] = count + 1


        day = 0
        while True:

            temp = self._fish[0]

            for i in range(0, 8):
                self._fish[i] = self._fish[i+1]
            self._fish[6] += temp
            self._fish[8] = temp

            day += 1
            # print(self._fish)
            if day >= 256:
                break

        total = sum(self._fish.values())
        print(total)

if __name__ == '__main__':
    runner = Runner()
    runner.run()
