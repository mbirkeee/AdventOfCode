"""
"""

import sys
import math
import copy
import itertools

class ExceptionDone(Exception):
    pass

PAIR_START      = 1
PAIR_STOP       = 2
PAIR_SEP        = 3
PAIR_NUMBER     = 4

class Number(object):

    def __init__(self, s):
        self._items = []

        value = None

        for c in s:
            if c == '[':
                self._items.append([PAIR_START, 0])
                value = None
            elif c == ']':
                if value is not None:
                    self._items.append([PAIR_NUMBER, value])
                value = None
                self._items.append((PAIR_STOP, 0))
            elif c == ',':
                if value is not None:
                    self._items.append([PAIR_NUMBER, value])
                value = None
                self._items.append([PAIR_SEP, 0])
            else:
                x = int(c)
                if value is None:
                    value = 0
                value  += x

    def magnitude(self):

        items_copy = copy.deepcopy(self._items)

        while True:
            # print("start at beginning")
            for index, item in enumerate(self._items):

                if item[0] == PAIR_NUMBER and index == 0:
                    # We are done... this number contains the magnitude
                    # This process was destructive; restore the number (needed for part 2)
                    self._items = items_copy
                    return item[1]

                if item[0] == PAIR_START:
                    # This is the start of a pair... can it be replaced with a number?
                    if self._items[index+1][0] != PAIR_NUMBER:
                        continue
                    left = self._items[index+1][1]

                    if self._items[index+2][0] != PAIR_SEP:
                        continue

                    if self._items[index+3][0] != PAIR_NUMBER:
                        continue
                    right = self._items[index+3][1]

                    if self._items[index+4][0] != PAIR_STOP:
                        continue

                    # If here, then we can reduce this pair!
                    result = left * 3 + right * 2

                    # print("replace [%d,%d] with %d" %(left, right, result))
                    # Replace starting element with the magnitude
                    item[0] = PAIR_NUMBER
                    item[1] = result

                    # Delete the next 4 elements
                    for i in range(4):
                        del self._items[index+1]

                    # print("number is now -->: %s" % repr(self))
                    break

    def make_string(self):
        result = ""
        for item in self._items:
            if item[0] == PAIR_START:
                result += '['
            elif item[0] == PAIR_STOP:
                result += ']'
            elif item[0] == PAIR_SEP:
                result += ','
            else:
                result += '%d' % item[1]

        return result

    def __str__(self):
        # print("str called")
        return self.make_string()

    def __repr__(self):
        # print("repr called")
        return self.make_string()

    def __add__(self, n):
        """
        To add two snailfish numbers, we just make a new pair out of them
        """
        # print("add called")
        return Number('[%s,%s]' % (repr(self),repr(n)))

    def explode(self):
        # Return True if explode happened; False otherwise
        # print("explode called for >>%s<<" % repr(self))
        depth_count = 0

        for index, item in enumerate(self._items):
            # print(c)
            if item[0] == PAIR_START:
                depth_count += 1
                # print("depth_count: %d" % depth_count)

                if depth_count == 5:
                    # print("explode here")

                    delete_index = index

                    # Sanity test
                    next_item = self._items[index+1]

                    if next_item[0] != PAIR_NUMBER:
                        raise ValueError("expected a number")

                    value = next_item[1]

                    # Add left
                    for i in range(index-1, 0, -1):
                        prev_item = self._items[i]
                        if prev_item[0] == PAIR_NUMBER:
                            prev_item[1] += value
                            break

                    next_item = self._items[index+2]
                    if next_item[0] != PAIR_SEP:
                        raise ValueError("expected separator")

                    next_item = self._items[index+3]
                    value = next_item[1]

                    # Add right
                    for i in range(index+4, len(self._items)-1, 1):
                        next_item = self._items[i]

                        if next_item[0] == PAIR_NUMBER:
                            next_item[1] += value
                            break

                    # Each exploded pair consists of 5 sequential items
                    item = self._items[delete_index]
                    item[0] = PAIR_NUMBER
                    item[1] = 0

                    for i in range(4):
                        del self._items[delete_index+1]

                    return True


            elif item[0] == PAIR_STOP:
                depth_count -= 1
                # print("depth_count: %d" % depth_count)

        return False

    def split(self):
        # print("split called for %s" % repr(self))
        #
        for index, item in enumerate(self._items):
            # print(c)
            if item[0] == PAIR_NUMBER:
                value = item[1]
                if value >= 10:
                    left = math.floor(value/2)
                    right = math.ceil(value/2)

                    del self._items[index]

                    self._items.insert(index, [PAIR_STOP,   0])
                    self._items.insert(index, [PAIR_NUMBER, right])
                    self._items.insert(index, [PAIR_SEP,    0])
                    self._items.insert(index, [PAIR_NUMBER, left])
                    self._items.insert(index, [PAIR_START,  0])
                    return True

        return False

    def reduce(self):
        # print("reduce called for %s" % repr(self))

        while True:

            if self.explode():
                continue

            if self.split():
                continue

            # There is nothing more to be done
            break

class Runner(object):

    def __init__(self, filename):

        lines = []
        fp = None

        self._number_list = []

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                lines.append(line)

        finally:
            if fp: fp.close()

        for line in lines:
            # print("LINE: %s" % line)
            self._number_list.append(Number(line))

    def run(self):


        for i, n in enumerate(self._number_list):

            print("Adding %s" % repr(n))

            if i == 0:
                sum = n
            else:
                sum = sum + n
                sum.reduce()

        print("this is the sum")
        print(sum)
        #print("Number %d: %s" % (i, n))
        m = sum.magnitude()
        print("magnitude: %d" % m)

    def run2(self):

        indexes = [i for i in range(len(self._number_list))]
        combos = itertools.combinations(indexes, 2)

        max_mag = 0

        for combo in combos:
            print("add %s" % repr(combo))

            n1 = self._number_list[combo[0]]
            n2 = self._number_list[combo[1]]

            sum = n1 + n2
            sum.reduce()
            mag = sum.magnitude()

            if mag > max_mag:

                print("MEW MAX MAG!!!!")
                print(n1)
                print(n2)
                print(sum)
                print(mag)

                max_mag = mag

            sum = n2 + n1
            sum.reduce()
            mag = sum.magnitude()

            if mag > max_mag:

                print("MEW MAX MAG!!!!")
                print(n2)
                print(n1)
                print(sum)
                print(mag)

                max_mag = mag

        print("max_mag: %d" % max_mag)

    def test_reduce(self):

        # Get two numbers and add them
        n1 = Number('[[[[4,3],4],4],[7,[[8,4],9]]]')
        n2 = Number('[1,1]')

        n3 = n1 + n2

        # Now reduce the number
        print("before reduce")
        print(n3)
        n3.reduce()

        print("after reduce")
        print(n3)

    def test_explode(self, s):

        n = Number(s)

        print("before explode")
        print(n)
        n.explode()

        print("after explode")
        print(n)

    def test_split(self, s):

        n = Number(s)

        print("before split")
        print(n)
        n.split()

        print("after split")
        print(n)

    def test_magnitude(self, s):

        n = Number(s)

        print("number")
        print(n)
        m = n.magnitude()

        print("magnitude: %d" % m)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    # runner.run()
    runner.run2()
    # runner.test_magnitude('[9,1]')
    # runner.test_magnitude('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
    # runner.test_reduce()

    # runner.test_explode('[[[[[9,8],1],2],3],4]')
    # runner.test_explode('[7,[6,[5,[4,[3,2]]]]]')
    # runner.test_explode('[[6,[5,[4,[3,2]]]],1]')
    # runner.test_explode('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
    # runner.test_explode('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
    # runner.test_explode('[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]')



