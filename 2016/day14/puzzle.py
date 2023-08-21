import sys
import numpy as np
import copy
import hashlib

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self, filename):

        if filename.startswith('t'):
            # this is test mode
            self._base = 'abc'

        elif filename.startswith('p'):
            self._base = 'ahsbgdzn'

        self._check = []
        self._found = []

    def print_found(self):
        for item in self._found:
            print(item)

    def find_five(self, csum, want):

        want *= 5
        pos = csum.find(want)
        if pos < 0:
            return False
        return True

    def find_three(self, csum):

        for i in range(1, len(csum) - 1):
            c = csum[i]
            if csum[i-1] == c and csum[i+1] == c:
                return c

        return None

    def process_check(self, n, csum):

        keep = []
        for item in self._check:
            # print("check", item, "in", csum)

            c = item[0]

            if self.find_five(csum, c):
                # This is a match!
                print("found a match!!!!!!!")
                self._found.append(item)
                if len(self._found) == 64:
                    self.print_found()
                    raise ValueError("done!!")

                continue

            if n - item[1] >= 1000:
                print("discard item", item)
                continue

            keep.append(item)
            # input("continue...")

        self._check = keep

    def stretch(self, csum):

        for _ in range(2016):
            csum = hashlib.md5(csum.encode('utf-8')).hexdigest()

        return csum

    def run(self):

        print("run")

        n = 0
        while True:

            s = '%s%d' % (self._base, n)
            csum = hashlib.md5(s.encode('utf-8')).hexdigest()

            csum = self.stretch(csum)

            self.process_check(n, csum)

            c = self.find_three(csum)
            if c is not None:
                print("triple", c, "in", csum)
                self._check.append((c, n))

            n += 1
if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
