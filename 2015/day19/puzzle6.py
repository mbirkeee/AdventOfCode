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

        self._print_count = 0

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

                self._replacement_list.append((stop, start))

            elif len(parts) == 1:
                self._result[line] = True
                self._medicine = line
            else:
                raise ValueError("bad input")


    def process(self, medicine, depth_count):


        if medicine in self._cache:
            # print("cache hit: %d" % len(self._cache))
            self._cache_hits += 1
            return

        self._cache[medicine] = True
     #   if len(self._cache) > 10000000:
     #       self._cache = {}

        self._print_count += 1
        if self._print_count >= 10000:
            print("depth: %d (%d) cache: %d (hits: %d) med: %s" %
                  (depth_count, self._max_depth, len(self._cache), self._cache_hits, medicine))
            self._print_count = 0
    #    input("continue with %s..." % medicine)

        depth_count += 1

        if depth_count > self._max_depth:
            self._max_depth = depth_count

        hits = 0

        for item in self._replacement_list:
            start = item[0]
            stop = item[1]
            pos = medicine.find(start)
            if pos < 0:
                continue

     #       print("%s %d depth: %d hit %s ==> %s" %
     #             (medicine, pos, depth_count, start, stop))

            hits += 1
            # medicine_copy = copy.deepcopy(medicine)
            before = medicine[0:pos]
            after = medicine[pos+len(start):]
            medicine_new = before + stop + after

            # print("pos: %d %s => %s" % (pos, start, stop))
            if medicine_new == 'OMg':
                raise ValueError("Done on depth %d" % depth_count)

            if medicine_new == 'HF':
                raise ValueError("Done on depth %d" % depth_count)

            if medicine_new == 'NAl':
                raise ValueError("Done on depth %d" % depth_count)

            self.process(medicine_new, depth_count)

        if hits == 0:
            print("no hits depth: %d (%d) cache: %d med: %s" %
              (depth_count, self._max_depth, len(self._cache), medicine))

        depth_count -= 1

    def run(self):

        print("run")
        print(self._replacement_list)
        print(self._result)

        step = 0

        medicine = self._medicine

        self.process(medicine, 0)


#         while True:
#
#             step += 1
#
#             result_new = {}
#
#             for medicine in self._result.keys():
#                 # print("step: %d Consider medicine: %s" % (step, medicine))
#
#
#                 for item in self._replacement_list:
#                     start = item[0]
#                     stop = item[1]
#
# #                    print("replace %s ==> %s" % (start, stop))
#
#                     pos = 0
#                     while True:
# #                        print("step: %d check at pos %d (%s)" % (step, pos, medicine[pos:]))
#
#                         new_pos = medicine[pos:].find(start)
#                         if new_pos < 0:
#                             break
#
#                         new_pos += pos
#                         # print("match!! pos: %d new_pos %d" % (pos, new_pos))
#
#                         medicine_copy = copy.deepcopy(medicine)
#
#      #                   print("match %s at pos %d" % (start, new_pos))
#                         before = medicine_copy[0:new_pos]
#                         after = medicine_copy[new_pos+len(start):]
#
# #                        medicine_new = before + "--" + stop + "--" + after
#                         medicine_new = before + stop + after
# #                        print("medicine    : %s" % medicine_copy)
# #                        print("medicine new: %s" % medicine_new)
#
#                         if medicine_new == 'OMg':
#                             raise ValueError("Done on step %d" % step)
#
#                         if medicine_new == 'HF':
#                             raise ValueError("Done on step %d" % step)
#
#                         if medicine_new == 'NAl':
#                             raise ValueError("Done on step %d" % step)
# # e => OMg
# # e => HF
# # e => NAl
#
#                         if medicine_new == 'e':
#                             raise ValueError("Done on step %d" % step)
#
#                         if len(medicine_new) == 1:
#                             raise ValueError("Done on step %d" % step)
#
#                         result_new[medicine_new] = True
#
#                         # Start the next seach only one position forward
#                         pos = new_pos + 1
#
#                         #  input("continue...")
#
#             print("step: %d number of results: %d" % (step, len(result_new)))
# #            input("continue ....")
#
#             if len(result_new) == 0:
#                 break
#
#             self._result = result_new

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


