"""

"""
import numpy as np
import sys
import math
import itertools

import hashlib


class Runner(object):

    def __init__(self):

        self._key = 'reyedfim'
        # self._key = 'abc'

    def run(self):
        print("run")

        match = 0
        n = 0
        while True:

            s = '%s%d' % (self._key, n)
            x = hashlib.md5(s.encode('utf-8')).hexdigest()
            # print(x)
            if x.startswith('00000'):
                print(x)
                match += 1

            n += 1

            if match == 8:
                break

    def run2(self):
        print("run")

        result = [None, None, None, None, None, None, None, None]

        n = 0
        while True:

            s = '%s%d' % (self._key, n)
            x = hashlib.md5(s.encode('utf-8')).hexdigest()
            # print(x)
            if x.startswith('00000'):
                print(x)
                position = x[5]
                value = x[6]

                try:
                    p = int(position)
                    if p < 8:
                        if result[p] is None:
                            result[p] = value
                            print(result)

                        if None not in result:
                            break
                except:
                    pass
                # print(position, value)


            n += 1

if __name__ == '__main__':

    runner = Runner()
    # runner.run()
    runner.run2()

