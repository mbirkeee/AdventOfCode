import sys
import copy
import itertools
from collections import Counter
import numpy as np

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

        self._input = None
        self._output = None
        self._ip = 0
        self._input_length = 0

        self.initialize()

    def initialize(self):

        print("initialize")

        if len(self._lines) != 1:
            raise ValueError("bad input")

        self._input = self._lines[0]
        self._input_length = len(self._input)
        self._output = ''

    def handle_repeat(self):
        temp = ''

        # Sanity check
        if self._input[self._ip] != '(':
            raise ValueError("bad input")

        while True:
            self._ip += 1
            c = self._input[self._ip]
            if c == ')':
                self._ip += 1
                break
            else:
                temp += c

        # print("HANDLE REPEAT GOT!!!!", temp)
        parts = temp.split('x')
        repeat_len = int(parts[0])
        repeat_count = int(parts[1])

        for _ in range(repeat_count):
            tp = self._ip
            for _ in range(repeat_len):
                self._output += self._input[tp]
                tp += 1

        part2 = True
        if part2:
            pass
        else:
            self._ip = tp


    def run(self):
        print("called")
        print("INPUT", self._input)
        while self._ip < self._input_length:

            c = self._input[self._ip]
            if c == '(':
                self.handle_repeat()
            else:
                self._output += c
                self._ip += 1


        print("OUPUT", self._output)
        print("length", len(self._output))


    def run2(self):


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
    runner.run2()
