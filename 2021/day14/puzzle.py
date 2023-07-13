import copy
import numpy as np
import math

import sys

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self, filename):

        self._steps = 40
        self._lines = []
        self._seq = []
        self._insert = {}

        self._pairs = {}

        f = open(filename, 'r')
        for line in f:
            self._lines.append(line.strip())
        f.close()

        for line in self._lines:
            self.process_line(line)

        self._seq_copy = copy.deepcopy(self._seq)

    def run_new(self):
        print("run")

        pairs = {}
        # Initialise the pairs
        for i in range(len(self._seq_copy) - 1):
            pair = ( self._seq_copy[i], self._seq_copy[i+1] )
            pairs[pair] = pairs.get(pair, 0) + 1

        first_char = self._seq_copy[0]
        last_char = self._seq_copy[-1]

        # print(pairs)
        step = 0
        while True:

            pairs_new = {}

            for pair, count in pairs.items():
                insert = self._insert.get(pair)
                pair1 = (pair[0], insert)
                pair2 = (insert, pair[1])

                pairs_new[pair1] = pairs_new.get(pair1, 0) + count
                pairs_new[pair2] = pairs_new.get(pair2, 0) + count

            # print(pairs_new)
            pairs = pairs_new

            step += 1
            if step >= self._steps:
                break

        temp = {}
        # process the result
        for pair, count in pairs.items():
             temp[pair[0]] = temp.get(pair[0], 0) + count
             temp[pair[1]] = temp.get(pair[1], 0) + count

        temp[first_char] += 1
        temp[last_char] += 1

        # print(temp)
        #
        l = []
        for c, count in temp.items():
            l.append((int(count/2), c))
        #
        l.sort()
        # print(l)
        #
        least = l[0]
        most = l[-1]
        #
        # print(least, most)
        #
        result = most[0] - least[0]
        print("part 2 result: %d" % result)

    def run_old(self):
        print("run")

        step = 0
        while True:

            new_seq = []
            pairs = []

            # Make a list of the pairs
            for i in range(len(self._seq) - 1):
                pairs.append( (self._seq[i], self._seq[i+1]) )

            for pair in pairs:
                insert = self._insert.get(pair)
                # print("pair: %s insert: %s" % (repr(pair), repr(insert)))
                new_seq.append(pair[0])
                if insert is not None:
                    new_seq.append(insert)
                #new_seq.append(pair[1])
            new_seq.append(pair[1])

            self._seq = new_seq

            # # print(''.join(self._seq))
            # print(len(self._seq))
            # if len(self._seq) > 10000000:
            #     break

            step += 1
            if step >= self._steps:
                break

        temp = {}
        # process the result
        for c in self._seq:
            temp.get(c, 0)
            temp[c] = temp.get(c, 0) + 1

        print(temp)

        l = []
        for c, count in temp.items():
            l.append((count, c))

        l.sort()
        print(l)

        least = l[0]
        most = l[-1]

        print(least, most)

        result = most[0] - least[0]
        print("part 1 result: %d" % result)

    def process_line(self, line):
        # print(line)

        if len(line) == 0:
            return

        parts =line.split('->')
        # print(parts)

        if len(parts) == 1:
            # print("this is the starting line")
            for c in line:
                self._seq.append(c)
            return

        elif len(parts) == 2:
            # print("got insructions")
            pair = parts[0].strip()
            insert = parts[1].strip()

            self._insert[(pair[0], pair[1])] = insert

        else:
            raise ValueError('bad input')

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    # runner.run_old()
    runner.run_new()

