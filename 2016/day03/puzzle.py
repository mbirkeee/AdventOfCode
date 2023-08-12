import sys
import itertools
from collections import Counter

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self, filename):

        self._items = []
        self._lines = []

        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                self._lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(self._lines))

        self.initialize()

    def initialize(self):

        print("initialize")

        for index, line in enumerate(self._lines):
            # print(line)
            parts = line.split()
            item = (
                int(parts[0].strip()),
                int(parts[1].strip()),
                int(parts[2].strip()),
            )

            self._items.append(item)

    def run(self):
        print("run")

        valid_count = 0
        for item in self._items:
            print(item)
            if( item[0] + item[1] <= item[2] ):
                continue

            if( item[1] + item[2] <= item[0] ):
                continue

            if( item[2] + item[0] <= item[1] ):
                continue

            valid_count += 1

        print("valid", valid_count)

    def process_items(self, item_list):

        valid_count = 0

        tri0 = ( item_list[0][0], item_list[1][0], item_list[2][0] )
        tri1 = ( item_list[0][1], item_list[1][1], item_list[2][1] )
        tri2 = ( item_list[0][2], item_list[1][2], item_list[2][2] )

        for item in [tri0, tri1, tri2]:
            if( item[0] + item[1] <= item[2] ):
                continue

            if( item[1] + item[2] <= item[0] ):
                continue

            if( item[2] + item[0] <= item[1] ):
                continue

            valid_count += 1

        return valid_count

    def run2(self):

        valid_count = 0
        temp_list = []
        count = 0
        for item in self._items:
            temp_list.append(item)
            count += 1
            if count == 3:
                valid_count += self.process_items(temp_list)
                temp_list = []
                count = 0

        if count != 0:
            raise ValueError("expected 0 items")

        print("valid", valid_count)


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
    runner.run2()

