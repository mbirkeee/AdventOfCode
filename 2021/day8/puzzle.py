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

        self._lines = []

        self._unique_count = 0

        f = open(filename, 'r')
        for line in f:
            self._lines.append(line.strip())
        f.close()

    def run(self):
        print("run")

        total = 0
        for line in self._lines:
            i, o = self.process_line(line)
            total += self.process_group( i, o )

        print( "Part2: %d" % total )

    def process_group(self, i, o ):
        both = copy.deepcopy(i)
        both.extend( copy.deepcopy(o) )

        example_one = None
        example_four = None
        example_seven = None

        # print(both)
        # print(i, o)
        print("========================")

        # Require an example 1, 4, and 7
        for item in both:
            l = len(item)
            if l == 2:
                example_one = item
            elif l == 3:
                example_seven = item
            elif l == 4:
                example_four = item

        if example_four is None or example_one is None or example_seven is None:
            raise ValueError("not enough info")

        # print(example_one, example_four, example_seven)
        example_special = self.make_special(example_one, example_four)

        # print("example special", example_special)

        total = 0

        for number in o:

            value = None
            # print("check output", o)

            l = len(number)
            if l == 2:
                value = 1
            elif l == 3:
                value = 7
            elif l == 4:
                value = 4
            elif l == 7:
                value = 8
            elif l == 5:
                # This count be a 2, 3 or 5
                if self.contains(number, example_seven):
                    value = 3
                else:
                    if self.contains(number, example_special ):
                        value = 5
                    else:
                        value = 2
            elif l == 6:
                if self.contains(number, example_seven ):
                    if self.contains(number, example_four ):
                        value = 9
                    else:
                        value = 0
                else:
                    value = 6

            else:
                raise ValueError("bad number")

            if value is None:
                raise ValueError("bad number")

            total = total * 10
            total += value

        print("Got number: %d" % total)
        return total

    def contains(self, number, check):

        num_chars = [c for c in number]
        check_chars = [c for c in check]

        for c in check_chars:
            if c not in num_chars:
                return False
        return True

    def make_special(self, example_one, example_four):

        example_special = ''

        one_chars = [c for c in example_one]
        four_chars = [c for c in example_four]

        for c in four_chars:
            if c not in one_chars:
                example_special += c

        return example_special

    def process_line(self, line):

        i = []
        o = []

        parts = line.split('|')
        # print( parts[0], parts[1] )

        temp = parts[0]
        items = temp.split()

        # print(items)
        for item in items:
            # print(item)
            i.append( item.strip() )

        temp = parts[1]
        items = temp.split()
        for item in items:
            o.append( item.strip() )

        return i, o

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
