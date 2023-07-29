"""

"""
import numpy as np
import sys
import math
import itertools

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

        print("read %d lines" % len(self._lines))

    def run1(self):

        # Set all the lights to off
        self._array = np.ones((1000,1000), dtype=np.int8)
        self._array *= -1


        for line in self._lines:

            parts = line.split(' ')
            if len(parts) == 5:
                # This is a turn on/off command
                start1, start2 = self.get_dims(parts[2])
                stop1, stop2 = self.get_dims(parts[4])
                if parts[1] == 'on':
                    self._array[start1:stop1+1,start2:stop2+1] = 1

                elif parts[1] == 'off':
                    self._array[start1:stop1+1,start2:stop2+1] = -1

                else:
                    raise ValueError('bad input')

            elif len(parts) == 4:
                # this is a toggle command
                start1, start2 = self.get_dims(parts[1])
                stop1, stop2 = self.get_dims(parts[3])
                self._array[start1:stop1+1,start2:stop2+1] *= -1

            else:
                raise ValueError('bad input')

        self._array += 1

        lights_on = np.sum(self._array) / 2

        print(lights_on)

    def run2(self):

        # Set all the lights to off
        self._array = np.zeros((1000,1000), dtype=np.int8)

        for line in self._lines:

            parts = line.split(' ')
            if len(parts) == 5:
                # This is a turn on/off command
                start1, start2 = self.get_dims(parts[2])
                stop1, stop2 = self.get_dims(parts[4])
                if parts[1] == 'on':
                    self._array[start1:stop1+1,start2:stop2+1] += 1

                elif parts[1] == 'off':
                    self._array[start1:stop1+1,start2:stop2+1] -= 1
                    self._array = self._array.clip(min=0)
                else:
                    raise ValueError('bad input')

            elif len(parts) == 4:
                # this is a toggle command
                start1, start2 = self.get_dims(parts[1])
                stop1, stop2 = self.get_dims(parts[3])
                self._array[start1:stop1+1,start2:stop2+1] += 2

            else:
                raise ValueError('bad input')

        lights_on = np.sum(self._array)

        print(lights_on)

    def get_dims(self, part):
        #$ print(part)

        parts = part.split(',')
        return int(parts[0]), int(parts[1])

    def run(self):
        print("run")


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run2()
