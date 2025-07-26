import sys
import numpy as np

class Box(object):

    def __init__(self, index):
        self._index = index
        self._lens_list = []

    def get_power(self):

        if len(self._lens_list) == 0:
            return 0

        result = 0
        for slot, item in enumerate(self._lens_list):

            result +=  (self._index + 1) * (slot + 1) * item[1]

        return result

    def add_lens(self, label, focal_len):

        for item in self._lens_list:
            if item[0] == label:
                item[1] = focal_len
                return

        self._lens_list.append([label, focal_len])

    def remove_lens(self, label):

        lens_list_new = []

        for item in self._lens_list:
            if item[0] == label:
                continue

            lens_list_new.append(item)

        self._lens_list = lens_list_new

    def print(self):
        if len(self._lens_list) == 0:
            return

        line = "BOX %d: " % self._index

        for lens in self._lens_list:
            l = " [%s %d]" % (lens[0], lens[1])
            line += l

        print(line)

class Runner(object):

    def __init__(self, filename):

        lines = []

        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                if len(line) == 0:
                    break

                lines.append(line)

        finally:
            if fp: fp.close()

        for line in lines:
            print("LINE", line)

        self._parts = lines[0].split(',')

        # for i, part in enumerate(self._parts):
        #     print("PART %d: '%s'" % (i, part))

    def hash(self, item):
        # print("---- '%s' ----" % item)
        value = 0

        for c in item:
            # print("ORD %c: %d" % (c, ord(c)))
            value += ord(c)
            value *= 17

            x = int(value // 256)
            value = int(value) - int(x * 256)

        # print("hash return", value)
        return value

    def part1(self):

        print("part1")
        value = 0
        for part in self._parts:
            h = self.hash(part)
            print("part:", part, "hash", h)
            value += h

        print("part1 result:", value)


    def print_boxes(self, box_map):

        for key, box in box_map.items():
            box.print()

    def hash2(self, item):
        # print("---- '%s' ----" % item)

        pos = item.find('=')

        if pos > 0:
            parts = item.split('=')

            # print("ADD LENS:", parts)
            label = parts[0]
            index = self.hash(label)
            focal_len = int(parts[1])

            return label, index, focal_len

        if item[-1] != '-':
            raise ValueError("bad value")

        label = item[:-1]
        index = self.hash(label)
        return label, index, None

    def part2(self):
        print("part2")

        box_map = {}
        for i in range(256):
            box_map[i] = Box(i)

        for part in self._parts:

            label, index, focal_len = self.hash2(part)
            # print("index", index)
            box = box_map.get(index)

            if focal_len is None:
                # This is a minus
                # print("label", label, "index", index, "-")
                box.remove_lens(label)
            else:
                # print("label", label, "index", "focal_len", focal_len)
                box.add_lens(label, focal_len)

            # self.print_boxes(box_map)
            # input("continue")

        total_power = 0
        for i, box in box_map.items():
            box_power = box.get_power()
            print("box %d power %d" % (i, box_power))
            total_power += box.get_power()

        print("part 2: total power", total_power)


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    # runner.part1()
    runner.part2()

