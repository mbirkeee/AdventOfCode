import copy
import numpy as np
import math
import sys

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass


OPEN = ['{', '[', '<', '(']
CLOSE = ['}', ']', '>', ')']

PAIR = {
    '{': '}',
    '[': ']',
    '<': '>',
    '(': ')'
}

SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

CLOSE_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

class Runner(object):

    def __init__(self, filename):

        self._lines = []
        self._error_score = 0

        f = open(filename, 'r')
        for line in f:
            self._lines.append(line.strip())
        f.close()

        self._stack = []
        self._close_scores = []

    def run(self):
        print("run")

        for line in self._lines:

            try:
                self.process_line(line)
            except Exception as err:
                print("Error: %s" % repr(err))

        print("Part 1: Error score: %d" % self._error_score)

        self._close_scores.sort()
        # print(self._close_scores)

        count = len(self._close_scores)
        count = int(math.floor(count/2))

        print(self._close_scores[count])

    def process_line(self, line):
        # print("process %s" % line)

        stack = []

        for c in line:
            # print(c)
            if len(stack) == 0:
                # We expect an opening char
                if c in OPEN:
                    stack.append(c)
                else:
                    raise ValueError("expected opening, got '%s'" % c)
            else:
                # There is stuff on the stack, can be open or close
                if c in OPEN:
                    stack.append(c)
                elif c in CLOSE:
                    open = stack.pop(-1)
                    if c != PAIR[open]:
                        self._error_score += SCORE[c]
                        raise ValueError("expected %c, got %c" % (PAIR[open], c))

                else:
                    raise ValueError("unexpected char: %s" % c)

        if len(stack) == 0:
            print("Line is OK")
        else:
            print("line not finished")
            close_score = 0
            while len(stack):
                close_score *= 5
                open = stack.pop(-1)
                close = PAIR[open]
                print("must add a %c" % close)
                close_score += CLOSE_SCORE[close]
            self._close_scores.append(close_score)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
