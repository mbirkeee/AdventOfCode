import sys
import copy
import itertools
from collections import Counter
import numpy as np
import re

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

        self._cache_hits = 0
        self._max_depth = 0
        self._result = {}
        self._cache = {}
        self._replacement_list = []
        self._replacement_list_ar = []
        self._print_count = 0

        self._steps = 0

        print("read %d lines" % len(self._lines))
        self.initialize()

    def initialize(self):

        print("initialize")

        for row, line in enumerate(self._lines):
            print(line)
            if line.startswith('#'):
                print("skip", line)
                continue

            parts = line.split('=>')
            if len(parts) == 2:
                start = parts[0].strip()
                stop = parts[1].strip()

                if stop.endswith('Ar'):
                    self._replacement_list_ar.append((stop, start))
                else:
                    self._replacement_list.append((stop, start))

            elif len(parts) == 1:
                self._result[line] = True
                self._medicine = line
            else:
                raise ValueError("bad input")



    def reduce_ar(self, medicine):
        """
        Replace as many "Ar" as possible
        :param medicine:
        :return:
        """
        while True:
            hits = 0
            for item in self._replacement_list_ar:
                start = item[0]
                stop = item[1]
                pos = medicine.find(start)
                if pos < 0:
                    continue
                hits += 1

                print("Ar reduce: %s ==> %s" % (start, stop))
                # medicine_copy = copy.deepcopy(medicine)
                before = medicine[0:pos]
                after = medicine[pos+len(start):]
                medicine = before + stop + after
                self._steps += 1

            if hits == 0:
                break

        return medicine

    def reduce(self, medicine):

        possible_replacements = []

        for item in self._replacement_list:
            start = item[0]
            stop = item[1]
            pos = medicine.find(start)
            if pos < 0:
                continue

            possible_replacements.append((pos, item))

        possible_replacements.sort()
        thing = possible_replacements[0]
        pos = thing[0]
        item = thing[1]
        start = item[0]
        stop = item[1]

        before = medicine[0:pos]
        after = medicine[pos+len(start):]
        medicine = before + stop + after
        self._steps += 1
        print("reduce: %d %s ==> %s" % (pos, start, stop))

        return medicine

    def run(self):

        print("run")
        print(self._replacement_list)
        print(self._result)

        medicine = self._medicine

        while True:

            medicine = self.reduce_ar(medicine)
            medicine = self.reduce(medicine)

            print(medicine)

            input("%d continue..." % self._steps)




#        self.process(medicine, 0)



if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


