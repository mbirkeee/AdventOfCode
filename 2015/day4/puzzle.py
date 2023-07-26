"""

"""
import numpy as np
import sys
import math
import itertools

import hashlib


class Runner(object):

    def __init__(self, key):

        self._key = key


    def run(self):
        print("run")

        n = 0
        while True:

            s = '%s%d' % (self._key, n)
            x = hashlib.md5(s.encode('utf-8')).hexdigest()
            # print(x)
            if x.startswith('000000'):
                print(n)
                break

            n += 1


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
