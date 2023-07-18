"""
This is a tricky one !!!!

background starts out ad black (unlit) in every direction

that is, any random pixel away from the image calculates a 0 as the index to the next image.
In the example, index 0 points to an unlit pixel in the enhance algorithm.  So, the infinite
backgound just stys unlit.

BUT....

in the actual problem, index 0 points to a LIT pixel.  So, on the second iteration,
the infinite background becomes lit!

This must be taken into account!

"""

import sys
import numpy as np

class Runner(object):

    def __init__(self, filename):

        lines = []
        fp = None
        line_length = None

        try:
            fp = open(filename, 'r')

            line_count = 0
            for line in fp:
                line = line.strip()

                if len(line) == 0:
                    continue

                line_count += 1

                if line_count == 1:
                    print("this is the algoriothm")
                    if len(line) != 512:
                        raise ValueError("wanted 512; got %d" % len(line))

                    self._array_alg = None
                    self.make_array_alg(line)

                else:
                    if line_length is None:
                        line_length = len(line)
                    else:
                        if len(line) != line_length:
                            raise ValueError('unexpcted line length')

                    lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(lines))

        # for line in lines:
        #     print(line)

        self._array_image = None
        self.make_array_image(lines, line_length)

        print(self._array_image)
        self.print_image(self._array_image)

        self._flip_flag = False
        if self._array_alg[0] == 1:
            print("THIS SYSTEM WILL FLIP BACKGROUND ON THE FIRST ENHANCE!!!!")
            self._flip_flag = True

    def make_array_image(self, lines, line_length):

        rows = len(lines)
        cols = line_length

        self._array_image = np.zeros((rows, cols), dtype=np.uint32)

        for row, line in enumerate(lines):
            for col, c in enumerate(line):

                if c == '#':
                    self._array_image[row, col] = 1
                elif c == '.':
                    pass
                else:
                    raise ValueError("unexpcted char")

    def make_array_alg(self, line):
        self._array_alg = np.zeros((len(line)), dtype=np.uint32)

        for index, c in enumerate(line):
            # print("%d: %c" % (index, c))
            if c == '#':
                self._array_alg[index] = 1
            elif c == '.':
                pass
            else:
                raise ValueError("unexpected char")

        print(self._array_alg)

    def enhance(self, count):
        print("enhance %d!" % count)

        # Add an empty border around the image
        shape = self._array_image.shape

        rows = shape[0] + 2
        cols = shape[1] + 2

        if self._flip_flag and count %2 :
            temp = np.ones((rows, cols), dtype=np.uint32)
        else:
            temp = np.zeros((rows, cols), dtype=np.uint32)

        new_image = np.zeros((rows, cols), dtype=np.uint32)

        temp[1:rows-1,1:cols-1] = self._array_image

        # self.print_image(temp)
        # input("continue...")

        for row in range(rows):
            for col in range(cols):

                i = 0
                for r in [row-1, row, row+1]:
                    for c in [col-1, col, col+1]:

                        i *= 2

                        if r > 0 and c > 0 and r < rows and c < cols:
                            v = temp[r,c]
                        else:
                            if self._flip_flag and count %2 :
                                v = 1
                            else:
                                v = 0

                        i += v

                # print("got index: %d" % i)

                new_image[row, col] = self._array_alg[i]

        # if self._flip_flag and count == 0:
        #
        #     shape = new_image.shape
        #     rows = shape[0] + 2
        #     cols = shape[1] + 2
        #     temp2 = np.ones((rows, cols), dtype=np.uint32)
        #     temp2[1:rows-1,1:cols-1] = new_image
        #
        #     self._array_image = temp2
        #
        # else:
        self._array_image = new_image

    def run(self):
        print("run")

        for i in range(50):
            self.enhance(i)
            # self.print_image(self._array_image)

        self.print_image(self._array_image)

        l = np.sum(self._array_image)
        print("lit count: %d" % l)

    def print_image(self, image):
        shape = image.shape
        # print(shape)
        rows = shape[0]
        cols = shape[1]
        # print(rows, cols)

        print("-- ROWS: %d COLS: %d -------" % (rows, cols))
        for row in range(rows):
            line = ''
            for col in range(cols):

                if image[row, col] == 1:
                    line += '#'
                else:
                    line += '.'

            print(line)

        print("-"*80)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()

