import sys
import itertools

class Map(object):

    def __init__(self, name):

        self._name = name
        self._ranges = []
        self._result = []

    def get_name(self):
        return self._name

    def add_range(self, item):

        parts = item.split(' ')

        r = [int(part) for part in parts]

        # Swap the input order so that we have src, dest, width
        self._ranges.append((r[1], r[0], r[2]))

    def map(self, item):

        for r in self._ranges:
            source = r[0]
            dest = r[1]
            width = r[2]
            if item >= source and item < (source + width):
                diff = item - source
                return dest + diff

        return item

    def map_one_range(self, item):

        boundaries = []

        item_start = item[0]
        item_end = item_start + item[1]

        # Add the boundaries of the input seed range
        boundaries.append(item_start)
        boundaries.append(item_end)

        # Add the boundaries of each mapper range
        for r in self._ranges:
            boundaries.append(r[0])
            boundaries.append(r[0] + r[2])

        # There can be duplicate boundaries
        boundaries = list(set(boundaries))

        # Must be in ascending order for chuck computation
        boundaries.sort()

        # Make list of all possible ranges (i.e.,
        # chunks between all boundaries
        chunk_list = []
        for i in range(len(boundaries) - 1):
            chunk_start = boundaries[i]
            chunk_end   = boundaries[i+1]
            chunk_list.append((chunk_start, chunk_end))

        # Check each chunk
        for chunk in chunk_list:
            chunk_start = chunk[0]
            chunk_end = chunk[1]

            if chunk_start < item_start or chunk_start >= item_end:
                # print("this chunk is NOT in the seed range; punt")
                continue

            matching_range = None

            # Check chunk against all mapping ranges
            for r in self._ranges:
                range_start = r[0]
                range_end = r[0] + r[2]
                if chunk_start >= range_start and chunk_start < range_end:
                    # print("====== this chunk is mapped!!!")
                    matching_range = r
                    break

            # Save mapped chunks as (start, width)
            chunk_width = chunk_end - chunk_start

            if matching_range:
                # Apply mapping function
                chunk_start += (matching_range[1] - matching_range[0])

            self._result.append((chunk_start, chunk_width))

    def map_ranges(self, item_ranges):

        for item_range in item_ranges:
            self.map_one_range(item_range)

        return self._result

    def test_source_overlap(self):
        """
        this is just a test to see if any source ranges
        overlap.  I dont think they should
        """
        x = itertools.combinations(self._ranges, 2)

        for item in x:
            r1 = item[0]
            r2 = item[1]

            r1_start = r1[0]
            r2_start = r2[0]
            r1_end = r1_start + r1[2] - 1
            r2_end = r2_start + r2[2] - 1

            if r1_start >= r2_start:
                if r1_start <= r2_end:
                    raise ValueError("overlap 1")

            if r1_end >= r2_start:
                if r1_end <= r2_end:
                    raise ValueError("overlap 2")

            if r2_start >= r1_start:
                if r2_start <= r1_end:
                    raise ValueError("overlap 3")

            if r2_end >= r1_start:
                if r2_end <= r1_end:
                    raise ValueError("overlap 4")

class Runner(object):

    def __init__(self, filename):

        self._lines = []
        self._maps = []
        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                line = line.strip('.')
                self._lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(self._lines))

        for line in self._lines:
            if len(line) == 0:
                continue

            if line.startswith('seeds:'):
                line = line[len('seeds:'):].strip()
                parts = line.split(' ')
                self._seeds = [int(part) for part in parts]

            elif line.find('map') > 0:

                map = Map(line)
                self._maps.append(map)
            else:
                map.add_range(line)

    def run1(self):

        results = []

        for map in self._maps:
            print("MAP: %s" % map.get_name())

        for seed in self._seeds:
            print("consider seed: %d" % seed)
            item = seed
            for map in self._maps:
                item_new = map.map(item)
                print("map %s item %d --> %d" %
                      (map.get_name(), item, item_new))
                item = item_new

            print("final", item_new)
            results.append(item_new)

        print("part 1 min result:", min(results))

    def test_overlap(self):
        for map in self._maps:
            map.test_source_overlap()

    def run2(self):
        # Make seed ranges
        i = 0
        seed_ranges = []

        for _ in range(len(self._seeds)//2):
            start = self._seeds[i]
            width = self._seeds[i+1]
            seed_ranges.append((start, width))
            i += 2

        for map in self._maps:
            seed_ranges = map.map_ranges(seed_ranges)

        print("Done; got %d ranges" % len(seed_ranges))

        # First element in each range is minimum; find
        # smallest minimum
        range_mins = [s[0] for s in seed_ranges]

        print("part 2 answer:", min(range_mins))

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run1()
    runner.test_overlap()
    runner.run2()