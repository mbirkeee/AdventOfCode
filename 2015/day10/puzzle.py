import sys
import itertools

class Runner(object):

    def __init__(self, line):

        self._line = line
        self._digits = []

    def run(self):

        print(self._line)
        for c in self._line:
            self._digits.append(int(c))


        for _ in range(50):
            self.iterate()

    def iterate(self):
        # print("iterate")

        digits_new = []

        prev_digit = None

        count = 0
        digit = 0

        for d in self._digits:
            if prev_digit is None:
                count = 1
                prev_digit = d
            else:
                if d == prev_digit:
                    count += 1
                else:
                    # This is a new digit; emit
                    digits_new.append(count)
                    digits_new.append(prev_digit)
                    count = 1
                    prev_digit = d

        # must append last item
        digits_new.append(count)
        digits_new.append(d)
        self._digits = digits_new

        print(len(self._digits))

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
