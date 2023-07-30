"""

"""
import sys



class Runner(object):

    def __init__(self, filename):

        self._wire_dict = {}
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

        self.initialize()

    def initialize(self):

        print("initialize")

    def process_line(self, line):

        line = line.strip('"')

        length = len(line)

        print("line: '%s'" % line)
        i = 0
        count = 0

        while i < length:
            c = line[i]
            print(c)
            if c == '\\':
                if i == length - 1:
                    # This is a special case of a \ at the end of the line
                    return count + 1

                if line[i+1] == '\\':
                    i += 1
                    count +=1
                elif line[i+1] == '"':
                    i += 1
                    count +=1
                elif line[i+1] == 'x':
                    i += 3
                    count += 1
            else:
                count += 1

            i += 1
            if i >= length:
                break

        #print("returning", count)

        return count

    def process_line2(self, line):

        # line = line.strip('"')
        line = line[1:-1]
        length = len(line)

        print("line: '%s'" % line)
        i = 0
        count = 0

        while i < length:
            c = line[i]
            # print(c)
            if c == '\\':
                count += 1
            elif c == '"':
                count += 1

            count += 1
            i += 1
            if i >= length:
                break

        count += 6
        print("returning", count)
        return count

    def run(self):

        total_len = 0
        length = 0

        for line in self._lines:
            total_len += len(line)
            # length += self.process_line(line)
            length += self.process_line2(line)

        print("total len", total_len)
        print("len", length)

        print("diff", length - total_len)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
