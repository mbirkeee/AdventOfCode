import sys
import numpy as np

class ExceptionDone(Exception):
    pass

ZERO    = ord('0')
NINE    = ord('9')
PERIOD  = ord('.')
GEAR    = ord('*')

class Runner(object):

    def __init__(self, filename):

        lines = []
        fp = None

        self._rows = None
        self._cols = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()

                if len(line) == 0:
                    continue

                lines.append(line)

                if self._cols is None:
                    self._cols = len(line)
                else:
                    if len(line) != self._cols:
                        raise ValueError("bad input")

        finally:
            if fp: fp.close()

        self._rows = len(lines)
        print("read %d lines" % len(lines))
        print("rows", self._rows, "cols", self._cols)

        self._array = np.zeros((self._rows, self._cols), dtype=np.uint8)

        for r, line in enumerate(lines):
            # print(line)
            for c, x in enumerate(line):
                # print(c)
                self._array[r,c] = ord(x)

    def get_value(self, item):
        if item >= ZERO and item <= NINE:
            return item - ZERO

    def check_for_symbol(self, r, c):

        for row in [r-1, r, r+1]:
            for col in [c-1, c, c+1]:
                try:
                    x = self._array[row,col]
                except:
                    continue

                if x >= ZERO and x <= NINE:
                    continue

                if x == PERIOD:
                    continue

                print("found adjacent symbol %s (%d)" % (chr(x), x))
                return True

        return False

    def check_for_gears(self, r, c, gear_keys):

        for row in [r-1, r, r+1]:
            for col in [c-1, c, c+1]:
                try:
                    x = self._array[row,col]
                except:
                    continue

                if x == GEAR:
                    gear_key = '%d-%d' % (row, col)
                    gear_keys.append(gear_key)

        return gear_keys



    def run1(self):

        number_flag = False
        symbol_flag = False
        number = 0
        total = 0

        for r in range(self._rows):
            for c in range(self._cols):
                x = self._array[r,c]

                value = self.get_value(x)
                if value is None:
                    # print("this is NOT a digit")

                    if number_flag:
                        # print("found number", number)
                        if symbol_flag:
                            # this number is next to a symbol
                            total += number

                    symbol_flag = False
                    number_flag = False
                    number = 0

                else:
                    # print(value)
                    number_flag = True
                    number *= 10
                    number += value
                    if self.check_for_symbol(r, c):
                        symbol_flag = True

        if number_flag:
            raise ValueError("found number and end of input")

        print("part 1 total", total)

    def run2(self):

        number_flag = False
        gear_flag = False
        gear_keys = []

        gear_map = {}

        number = 0
        total = 0

        for r in range(self._rows):
            for c in range(self._cols):
                x = self._array[r,c]

                value = self.get_value(x)
                if value is None:
                    # print("this is NOT a digit")

                    if number_flag:
                        # print("found number", number)
                        # There can be duplicate keys
                        gear_keys = list(set(gear_keys))
                        for gear_key in gear_keys:
                            # this number is next to a gear
                            print("number %d is next to gear %s" % (number, gear_key))
                            number_list = gear_map.get(gear_key, [])
                            number_list.append(number)
                            gear_map[gear_key] = number_list
                            # total += number

                    gear_keys = []
                    number_flag = False
                    number = 0

                else:
                    # print(value)
                    number_flag = True
                    number *= 10
                    number += value
                    gear_keys = self.check_for_gears(r, c, gear_keys)

        if number_flag:
            raise ValueError("found number and end of input")

        for gear_key, number_list in gear_map.items():
            print(gear_key, number_list)
            if len(number_list) != 2:
                continue

            total += number_list[0] * number_list[1]

        print("part 2 total", total)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    # runner.run1()
    runner.run2()
