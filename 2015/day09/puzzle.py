import sys
import itertools

class Runner(object):

    def __init__(self, filename):

        self._map_stars = {}
        self._map_distance = {}
        self._lines = []
        self._star_index = 0

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

    def get_star_index(self, star):
        index = self._map_stars.get(star)
        if index is None:
            self._star_index += 1
            self._map_stars[star] = self._star_index
            index = self._star_index

        return index

    def initialize(self):

        print("initialize")
        for line in self._lines:
            parts = line.split(' ')
            print(parts)
            star1 = parts[0]
            star2 = parts[2]
            distance = int(parts[4])

            index1 = self.get_star_index(star1)
            index2 = self.get_star_index(star2)

            self._map_distance[(index1,index2)] = distance
            self._map_distance[(index2,index1)] = distance

        # for k, v in self._map_distance.items():
        #     print(k, v)

    def run(self):

        print(self._map_stars)
        stars = [1,2,3,4,5,6,7,8]
        hops = itertools.permutations(stars)
        min_distance = None
        max_distance = None

        for i, hop_list in enumerate(hops):

            total_distance = 0
            print(i, hop_list)
            print(type(hop_list))
            start = hop_list[0]

            for hop in hop_list[1:]:
                pair = (start, hop)
                distance = self._map_distance.get(pair)
                start = hop
                print("pair", pair, "distance", distance)
                total_distance += distance

            if min_distance is None or total_distance < min_distance:
                min_distance = total_distance

            if max_distance is None or total_distance > max_distance:
                max_distance = total_distance

            # if i > 10:
            #     break

        print("min_distance", min_distance)
        print("max_distance", max_distance)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
