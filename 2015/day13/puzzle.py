import sys
import itertools

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

        print("read %d lines" % len(self._lines))

        self._map_index_to_person = {}
        self._map_person_to_index = {}
        self._person_index = 0

        self.initialize()

    def initialize(self):
        print("initialize")


        # First, initialize a dict with all the people
        for line in self._lines:
            parts = line.split(' ')
            # print(parts)
            # print(len(parts))
            if len(parts) != 11:
                raise ValueError("bad number of parts")

            name = parts[0]
            if name not in self._map_person_to_index:
                self._map_index_to_person[self._person_index] = {'name':name}
                self._map_person_to_index[name] = self._person_index
                self._person_index += 1


        print(self._map_index_to_person)

        for line in self._lines:
            parts = line.split(' ')
            person = parts[0]

            if parts[2] == 'gain':
                factor = 1
            else:
                factor = -1

            amount = int(parts[3]) * factor
            neighbour = parts[10]
            print(person, amount, neighbour)
            person_index = self._map_person_to_index[person]
            neighbour_index = self._map_person_to_index[neighbour]

            meta = self._map_index_to_person.get(person_index)
            meta[neighbour_index] = amount
            self._map_index_to_person[person_index] = meta

        print(self._map_index_to_person)

    def compute_gain(self, item):

        # print(item)
        gain = 0
        for i, person_index in enumerate(item):
            # print(person_index)
            left = i -1
            if i < 0:
                i = len(item) - 1
            person_index_left = item[left]
            right = i + 1
            if right >= len(item):
                right = 0

            person_index_right = item[right]

            # print("left", person_index_left, "person", person_index, "right", person_index_right)

            meta = self._map_index_to_person.get(person_index)

            if meta is None:
                # print("no meta for", person_index)
                continue

            gain += meta.get(person_index_left, 0)
            gain += meta.get(person_index_right, 0)
        # print("gain", gain)
        return gain

    def run(self):

        perm = itertools.permutations(range(len(self._map_index_to_person) + 1 ))

        max_gain = None

        for i, item in enumerate(perm):
            gain = self.compute_gain(item)
            # print("gain", gain)
            if max_gain is None or gain > max_gain:
                max_gain = gain
                print("max_gain", gain)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
