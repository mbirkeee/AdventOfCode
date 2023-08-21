import sys
import numpy as np
import copy
import hashlib

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self, filename):

        if filename.startswith('t'):
            # this is test mode
            self._disks = [
                (5, 4),
                (2, 1)
            ]
        elif filename.startswith('p'):
            self._disks = [
                (17, 5),
                (19, 8),
                ( 7, 1),
                (13, 7),
                ( 5, 1),
                ( 3, 0),
                (11, 0)
            ]

        self._check = []
        self._found = []


    def run(self):


        time = 0

        while True:


#            print("time: %d ------------ " % time)

            mod_count = 0
            for i, disk in enumerate(self._disks):
                arrival_time = i + 1

                positions = disk[0]
                start = disk[1]
                position = time + arrival_time + start

                mod = position % positions
#                print("disk %d position %d mod: %d" % (i, position, mod))
                mod_count += mod

            if mod_count == 0:
                raise ValueError("done at time %d" % time)

            time += 1
            # input("continue...")

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
