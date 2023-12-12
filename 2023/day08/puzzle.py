import sys

class Runner(object):

    def __init__(self, filename):

        lines = []
        self._map = {}
        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                line = line.strip('.')
                if len(line) == 0:
                    continue
                lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(lines))

        for i, line in enumerate(lines):
            if i == 0:
                print("this is the route", line)
            else:
                line = line.replace(' ','')
                line = line.replace('(','')
                line = line.replace(')','')

                # print("MAP: %s" % line)
                parts = line.split('=')
                # print(parts)
                key = parts[0]
                items = parts[1].split(',')
                # print items
                self._map[key] = items

        print(self._map)

    def run1(self):
        print("run")


    def run2(self):

        self.run1()

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run1()
    # runner.run2()
