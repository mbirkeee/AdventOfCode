import sys
import itertools
from collections import Counter

class ExceptionDone(Exception):
    pass


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

        # self.initialize()

    def initialize(self):

        print("initialize")



    def process_line(self, line):

        # print("process", line)
        print("----------------------------")
        in_bracket_count = 0
        valid_count = 0
        invalid_count = 0

        for i, c in enumerate(line):
            if c == '[':
                in_bracket_count += 1

            elif c == ']':
                in_bracket_count -= 1
         #       if in_bracket_count == 0:
         #           print("out of bracket")

            else:
          #      print(c)

                try:
                    if i < 1 or i >= len(line) - 2:
                        continue

                    if line[i+1] != c:
                        continue

                    # print("found a pair")

                    if line[i-1] != line[i+2]:
                        continue

                    # print("inside another pair")

                    if line[i-1] == c:
                       continue

         #           print(line)
         #           print("%d: %c%c%c%c" % (in_bracket_count, line[i-1], line[i], line[i+1], line[i+2]))


                    if line[i-1] == ']' or line[i-1] == '[':
                        continue

                    print("%d: %c%c%c%c" % (in_bracket_count, line[i-1], line[i], line[i+1], line[i+2]))

                    if in_bracket_count:
                        invalid_count += 1
                    else:
                        valid_count += 1

                except:
                    pass

#        print(valid_count, invalid_count)

        if valid_count and not invalid_count:
            print(line)
            print("VALID!!!!")
            return True

#        print("INVALID!!!!")
        return False

    def process_line2(self, line):

        # print("process", line)
        print("----------------------------")
        in_bracket_count = 0

        items = []

        for i, c in enumerate(line):
            if c == '[':
                in_bracket_count += 1

            elif c == ']':
                in_bracket_count -= 1

            else:

                try:
                    if i < 1 or i >= len(line) - 1:
                        continue

                    if line[i+1] == c:
                        continue

                    if line[i-1] != line[i+1]:
                        continue

                    if line[i-1] == ']' or line[i-1] == '[':
                        continue

                    # print("%d: %c%c%c" % (in_bracket_count, line[i-1], line[i], line[i+1]))

                    items.append(( in_bracket_count, line[i-1], line[i], line[i+1] ))
                except:
                    pass

        if len(items) < 2:
            return False

        it = itertools.combinations(items, 2)

        for pair in it:
            thing0 = pair[0]
            thing1 = pair[1]

            if thing0[0] == thing1[0]:
                continue

            if thing0[2] != thing1[1]:
                continue

            if thing0[1] != thing1[2]:
                continue

            print( "pair 0", thing0, 'pair 1', thing1 )

            return True

        return False


    def run(self):
        print("called")

        valid_count = 0
        for line in self._lines:
            if self.process_line(line):
                valid_count += 1
                print(valid_count)

        print("valid", valid_count)

    def run2(self):
        print("called")

        valid_count = 0
        for line in self._lines:
            if self.process_line2(line):
                valid_count += 1
                print(valid_count)

        print("valid", valid_count)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run2()
