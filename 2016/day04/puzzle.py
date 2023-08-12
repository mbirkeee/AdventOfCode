import sys
import itertools
from collections import Counter

class ExceptionDone(Exception):
    pass

class Room(object):
    def __init__(self, line):
        print(line)

        # Get the checksum
        pos = line.find('[')

        self._cksum = line[pos+1:-1]

        parts = line[:pos].split('-')
        # print(parts)
        self._sector_id = int(parts[-1])
        print(self._sector_id)

        self._name = "".join(parts[:-1])
        print(self._name)

    def key(self, item):

        x = 255 - ord(item[1])
        k = "%04d_%03d" % (item[0], x)
        # print(k)
        return k

    def valid(self):

        char_dict = {}
        for c in self._name:
            count = char_dict.get(c, 0)
            char_dict[c] = count + 1

        # print(char_dict)

        items = [(v, k) for k, v in char_dict.items()]
        # print(items)
        s = sorted(items, key=self.key, reverse=True)

        # for item in s:
        #     print("sorted", item)


        cksum = ''
        for i in range(5):
            cksum += s[i][1]

        print("cksum", cksum, self._cksum)

        if cksum == self._cksum:
            return True

        return False

    def get_sector_id(self):
        return self._sector_id

    def decrypt(self):

        first = ord('a')
        last = ord('z')

        spread = last - first + 1

#        print(first, last)
#        print("sector_id", self._sector_id)
        move = self._sector_id % 26

#        print(move)

        decypted = ''
        for c in self._name:
            new_ord = ord(c) + move
            if new_ord > last:
                new_ord -= spread

#           print("%c %d -> %d" % (c, ord(c), new_ord))

            decypted += chr(new_ord)

        print("%d: %s" % (self._sector_id, decypted))

class Runner(object):

    def __init__(self, filename):

        self._lines = []
        self._room_list = []

        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                self._lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(self._lines))

        self.initialize()

    def initialize(self):

        print("initialize")

        for index, line in enumerate(self._lines):
            # print(line)

            room = Room(line)
            self._room_list.append(room)


    def run(self):
        print("called")

        sector_id_total = 0

        valid_count = 0
        for room in self._room_list:
            if room.valid():
                valid_count += 1
                sector_id_total += room.get_sector_id()

        print("valid_count", valid_count)
        print("sector_id_total", sector_id_total)


    def run2(self):
        for room in self._room_list:
            room.decrypt()

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
    runner.run2()

