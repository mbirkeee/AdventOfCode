import sys


class Thing(object):

    def __init__(self, seq):

        parts = seq.split(' ')
        self._seq = [int(part) for part in parts]

        self._stack = []
        self._stack2 = []

    def process(self):

        last = len(self._seq)

        self._stack.append(self._seq[-1])
        self._stack2.append(self._seq[0])

        print(self._seq)

        new_seq = []
        for i in range(1, last):

            value = self._seq[i] - self._seq[i-1]
            # print("value", value)
            new_seq.append(value)

        self._seq = new_seq

        if sum(self._seq) == 0: return False

        return True

    def finalize(self):
        print(self._stack)
        return sum(self._stack)

    def finalize2(self):
        print("stack2", self._stack2)
        # return self._stack2[0] - sum(self._stack2[1:])

        val = 0
        i = len(self._stack2) - 1

        while i >= 0:
            val = self._stack2[i] - val
            i -= 1

        print("VAL", val)
        return val

class Runner(object):

    def __init__(self, filename):

        self._lines = []

        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                line = line.strip('.')
                if len(line) == 0:
                    continue

                self._lines.append(line)

        finally:
            if fp: fp.close()


    def part1(self):
        print("part1")

        print("read %d lines" % len(self._lines))

        total = 0
        for i, line in enumerate(self._lines):
            print("--- ", line)

            thing = Thing(line)
            while thing.process():
                pass

            result = thing.finalize()
            print(result)
            total += result

        print("Part 1 total:", total)

    def part2(self):
        print("part2")

        print("read %d lines" % len(self._lines))

        total = 0
        for i, line in enumerate(self._lines):
            print("--- ", line)

            thing = Thing(line)
            while thing.process():
                pass

            result = thing.finalize2()
            print(result)
            total += result

        print("Part 2 total:", total)



if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    # runner.part1()
    runner.part2()
