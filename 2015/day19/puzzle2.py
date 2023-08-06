import sys

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

                if line.startswith('#'):
                    continue

                self._lines.append(line)

        finally:
            if fp: fp.close()

        self._replacement_list = []
        self._cache_hits = 0
        self._max_depth = 0
        # self._result = {}
        self._cache = {}
        self._target = None

        self._count_a = None

        print("read %d lines" % len(self._lines))
        self.initialize()




    def initialize(self):

        print("initialize")

        for row, line in enumerate(self._lines):
            print(line)
            parts = line.split('=>')
            if len(parts) == 2:
                start = parts[0].strip()
                stop = parts[1].strip()
                self._replacement_list.append((start, stop))

            elif len(parts) == 1:
                print("this is the target")
                self._target = line
                print("*"*80)
                print(self._target)
                print("*"*80)

                self._count_a = self._target.count('a')

    def matched_until(self, line1, line2):
        l = max(len(line1), len(line2))

        for i in range(l):
            if line1[i] != line2[i]:
                return i

    def process(self, medicine, depth_count):


        if medicine.count('a') > self._count_a:
            print("to many a's... about branch")
            return

        depth_count += 1

        if depth_count > self._max_depth:
            self._max_depth = depth_count


        print("depth: %d (%d) cache: %d (hits: %d) med: %s" %
              (depth_count, self._max_depth, len(self._cache),
               self._cache_hits, medicine))

        input("continue...")

        # matched_pos_max = 0
        # matched_list = []

        hits = 0
        next_pos = 0

        for item in self._replacement_list:
            start = item[0]
            stop = item[1]

            pos = medicine[next_pos:].find(start)
            print("check %s pos: %d" % (start, pos))
            if pos < 0:
                continue

#                pos = pos + next_pos
#                next_pos = pos + 1
            # print("pos: %d %s => %s" % (pos, start, stop))

            hits += 1

            before = medicine[0:pos]
            after = medicine[pos+len(start):]
            medicine_new = before + stop + after

            print("NEW: %s" % medicine_new)
            self.process(medicine_new, depth_count)


#        new_list = list(set(new_list))
#        self.process(new_list, depth_count)

        depth_count -= 1

    def run(self):

        print("run")
        print(self._replacement_list)

        self.process("HF", 0)
        self.process("OMg", 0)
        self.process("OMg", 0)
        return


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


