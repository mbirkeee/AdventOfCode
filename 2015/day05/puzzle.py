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



    def run(self):
        print("run")

        count_bad = 0
        count_good = 0

        for line in self._lines:

            print("line: '%s'" % line)

            pair_flag = False

            for pair in ['ab', 'cd', 'pq', 'xy']:
                if line.find(pair) >= 0:
                    print("found %s in %s... BAD" % (pair, line))
                    pair_flag = True
                    break

            if pair_flag:
                count_bad += 1
                continue

            vowel_count = 0
            prev_char = None
            double_flag = False

            for c in line:
                if c in ['a', 'e', 'i', 'o', 'u']:
                    vowel_count += 1

                if prev_char is None:
                    prev_char = c
                else:
                    if c == prev_char:
                        double_flag = True
                prev_char = c

            if vowel_count < 3:
                print("only %d vowels %s... BAD" % (vowel_count,line))
                count_bad += 1
                continue

            if not double_flag:
                print("no double in %s... BAD" % (line))
                count_bad += 1
                continue

            count_good += 1

        print("good", count_good)
        print("bad", count_bad)

    def run2(self):

        print("run")

        count_bad = 0
        count_good = 0

        for line in self._lines:

            # print("line: '%s'" % line)

            pair_list = []
            c_prev_prev = None
            c_prev = None

            for index, c in enumerate(line):
                if c_prev is None:
                    c_prev = c
                else:
                    pair = '%c%c' % (c_prev, c)

                    pair_list.append((pair, index))

                c_prev = c

            # Now check the pairs
            combinations = itertools.combinations(range(len(pair_list)), 2)
            # print(combinations)
            # print(pair_list)


            flag_good = False
            for combination in combinations:
                # print(combination)
                pair1 = pair_list[combination[0]]
                pair2 = pair_list[combination[1]]

                if pair1[0] != pair2[0]:
                    continue

                if abs( pair2[1] - pair1[1] ) < 2:
                    # print("this is an overlapping pair; ignore")
                    continue

                # print("found repeating pair %s" % pair1[0])
                flag_good = True
                break
                # print("compare %s to %s" % ( repr(pair1), repr(pair2) ))

            if not flag_good:
                print("%s: BAD" % line)
                count_bad += 1
                continue

            c_prev = None
            c_prev_prev = None
            flag_good = False

            for index, c in enumerate(line):

                if c_prev == None:
                    c_prev = c
                else:
                    if c_prev_prev == None:
                        c_prev_prev = c_prev
                        c_prev = c
                    else:
                        if c_prev_prev == c:
                            flag_good = True
                            break

                        c_prev_prev = c_prev
                        c_prev = c

            if not flag_good:
                print("%s: BAD" % line)

                count_bad += 1
                continue

            count_good += 1
            print("%s: GOOD" % line)

        print("good", count_good)
        print("bad", count_bad)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    # runner.run()
    runner.run2()
