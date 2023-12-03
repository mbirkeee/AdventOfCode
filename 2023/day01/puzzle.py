import sys

class ExceptionDone(Exception):
    pass

CHECK = [
    'zero',
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
]

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

        self._program = []
        print("read %d lines" % len(self._lines))
        self.initialize()


    def initialize(self):

        print("initialize")

    def run(self):

        print("run")

        total = 0

        for line in self._lines:
            print("LINE: %s" % line)

            first_number = None
            last_number = None

            for i, c in enumerate(line):

                number = None
                if c.isdigit():
                    number = int(c)

                else:
                    check = line[i:]
                    #print(check)

                    for x, s in enumerate(CHECK):
                        print("---", x, s, "---", check)
                        if check.startswith(s):
                            number = x
                            break

                if number is None:
                    continue

                last_number = number

                if first_number is None:
                    first_number = last_number

            print(first_number, last_number)

            value = int('%d%d' % (first_number, last_number))

            print(value)

            total += value

        print("this is the total", total)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
