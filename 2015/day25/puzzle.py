import sys
import itertools
import math

from functools import reduce
import operator

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self):


        self._row = 2947
        self._col = 3029


    def run(self):

        print("run")

        row = 1
        col = 1
        number = 20151125
        while True:

            if row == self._row and col == self._col:
                print("answer", number)
                break


            #print("row: %d col %s number %d" % (row, col, number))

            number = number * 252533
            number = number % 33554393

            row -= 1

            if row == 0:
                row = col + 1
                col = 0
                print("starting at row", row)

            col += 1

            # input("continue...")

if __name__ == '__main__':

    runner = Runner()
    runner.run()
