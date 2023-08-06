import sys
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

                if line.startswith('#'):
                    continue

                self._lines.append(line)

        finally:
            if fp: fp.close()

        self._replacement_list = []
        self._target = None
        self._map = {}
        self._depth_count = 0
    #    self._start = 'e'

        self._cache = {}

        print("read %d lines" % len(self._lines))
        self.initialize()

    def initialize(self):

        print("initialize")

        for row, line in enumerate(self._lines):
            print(line)
            parts = line.split('=>')
            if len(parts) == 2:
                # print("this is a replacement")

                start = parts[0].strip()
                stop = parts[1].strip()

                self._replacement_list.append((start, stop))

#                if stop in self._map:
#                    raise ValueError("already have this!")
#
#                self._map[stop] = start

            elif len(parts) == 1:
                print("this is the target")
                self._target = line
                print("*"*80)
                print(self._target)
                print("*"*80)

            else:
                raise ValueError("bad input")


    def matched_until(self, line1, line2):
        l = max(len(line1), len(line2))

        for i in range(l):
            if line1[i] != line2[i]:
                return i

    def step(self, medicine):

        self._cache[medicine] = True

        if medicine == self._target:
            raise ValueError("FINISHED!!!! depth count: %d" % self._depth_count)

        matched_until = self.matched_until(medicine, self._target)
  #      print("matched until", matched_until)
        self._depth_count += 1

        print("%d match until: %d input: '%s'" % (self._depth_count, matched_until, medicine))
        input("continue..." )

        # Look for possible substitutions
        for item in self._replacement_list:
        # for start, stop in self._map.items():
            start = item[0]
            stop = item[1]
         #   print(start, stop)
            i = re.finditer(start, medicine)

            for p in i:
                pos = p.start()
                if pos != matched_until:
                    continue

                print("found", start, "at pos", pos)
                before = medicine[0:pos]
                after = medicine[pos+len(start):]
                new_medicine = before + stop + after

       #         if len(new_medicine) > 20:
                     # if not new_medicine.startswith(self._target[0:len(new_medicine) - 20]):
       #              if not new_medicine.startswith(self._target[0:20]):
       #                  self._depth_count -= 1
      # #              print("done -----------------------------------")
       #                  return

#                 if new_medicine in self._cache:
#                     print("cache hit")
#                     self._depth_count -= 1
#                     return
# #
                if len(new_medicine) > len(self._target) + 15:
                # if len(new_medicine) > 50:
#
                     self._depth_count -= 1
#       #              print("done -----------------------------------")
                     return

                self.step(new_medicine)

        self._depth_count -= 1
     #   print("done ---------------------------------------------------------------------")

    def run(self):

        print("run")

        medicine = 'e'

        while True:
            matched_until = self.matched_until(medicine, self._target)

            print("matched until: %d medicine: %s" % (matched_until, medicine))
            input("continue...")

            for item in self._replacement_list:
                start = item[0]
                stop = item[1]

                print("look for %s in %s" % (start, medicine[matched_until:]) )
                if medicine[matched_until:].startswith(start):
                    print("match --> change to", stop)
                    new_medicine = medicine[0:matched_until] + stop
                    medicine = new_medicine
                    break
                    # if self.matched_until(new_medicine, self._target) > matched_until:
                    #     print("%s ==> %s" % (medicine, new_medicine))
                    #

        print("no match")


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


