"""
This one was not scaling so I wrote an algorithm to compute the total risk to get to any point.
Look at the total risk of each of the 4 surrounding locations, and add it to the risk of
the location under consideration.  If its lower than what I have, then we use the new lowest risk.
Keep iterating overall the locations in the map until there are no changes; then the destination
location will contain the lowest risk.

Note that his algoritm finds the lowest risk but NOT the path
"""

import numpy as np

import sys

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self, filename):


        lines = []
        self._risk = {}

        f = open(filename, 'r')
        for line in f:
            line = line.strip()
            if line:
                lines.append(line.strip())
        f.close()

        self._rows_orig = len(lines)
        self._cols_orig = len(lines[0])

        self._expand_factor = 5
        self._rows = self._rows_orig * self._expand_factor
        self._cols = self._cols_orig * self._expand_factor

        # For original input data
        self._data_orig = np.zeros((self._rows_orig, self._cols_orig))

        self._data = np.zeros((self._rows, self._cols))
        self._total = np.zeros((self._rows, self._cols))

        # Read in the data after the arrays have been allocated
        for row, line in enumerate(lines):
            self.process_line(row, line)

    def process_line(self, row, line):
        # print(line)
        if len(line) != (self._cols_orig):
            raise ValueError('bad input')

        for col, v in enumerate(line):
            self._data_orig[row, col] = int(v)

    # def get_neighbours(self, path):
    #     # Get the last item off the path:
    #
    #     result = []
    #     last = path[-1]
    #
    #     up = ( last[0], last[1] - 1)
    #     if up not in path:
    #         risk = self._risk.get(up)
    #         if risk is not None:
    #             result.append(up)
    #
    #     down = ( last[0], last[1] + 1)
    #     if down not in path:
    #         risk = self._risk.get(down)
    #         if risk is not None:
    #             result.append(down)
    #
    #     left = ( last[0] - 1, last[1])
    #     if left not in path:
    #         risk = self._risk.get(left)
    #         if risk is not None:
    #             result.append(left)
    #
    #     right = ( last[0] + 1, last[1])
    #     if right not in path:
    #         risk = self._risk.get(right)
    #         if risk is not None:
    #             result.append(right)
    #
    #     return result

    def part2(self):

        print("set up for part 2")
        for row in range(self._rows_orig):
            line = ""
            for col in range(self._cols_orig):
                line += '%d' % self._data_orig[row, col]
            print(line)

        for r in range(self._expand_factor):
            for c in range(self._expand_factor):

                add = r + c

                for rr in range(self._rows_orig):
                    for cc in range(self._cols_orig):
                        value = self._data_orig[rr, cc]
                        value += add
                        if value > 9:
                            value -= 9

                        new_row = rr + r * self._rows_orig
                        new_col = cc + c * self._cols_orig

                        # print(new_row, new_col, value)
                        self._data[(new_row, new_col)] = value

#                replicate_count += 1
#                print("replicate", replicate_count, r, c)


        for row in range(self._rows):
            line = ""
            for col in range(self._cols):
                line += '%d' % self._data[row, col]
            print(line)

    def iterate(self):

        change_count = 0
        for row in range(self._rows):
            for col in range(self._cols):

                if row == 0 and col == 0:
                    continue

                have = self._total[row, col]

                # Left
                for pair in [ (row-1, col), (row+1, col), (row, col-1), (row,col+1) ]:
                    # print("consider", pair)
                    try:
                        if pair[0] < 0 or pair[0] >= self._rows:
                            # print("ignore", pair)
                            continue
                        if pair[1] < 0 or pair[1] >= self._cols:
                            # print("ignore", pair)
                            continue

                        new = self._total[pair[0], pair[1]]
                        if new < 0:
                            # print("ignore new nan")
                            continue

                        new = new + self._data[row, col]

                        # print(row, col, have, new)
                        # input("continue...")

                        if have < 0 or new < have:
                            self._total[row, col] = new
                            have = new
                            # print("use new -----------", new)
                            change_count += 1
                        else:
                            # print("no change", have, new)
                            pass

                    except Exception as err:
                        print("exceptin", pair, err)

        return change_count

    def run(self):
        print("run")
        print("rows", self._rows_orig)
        print("cols", self._cols_orig)
        self.part2()

        # Put NaN in the total array
        for  row in range(self._rows):
            for col in range(self._cols):
                self._total[row, col] = -1

        # Starting position adds nothing
        self._data_orig[0, 0] = 0
        self._total[0, 0] = 0

        # Iterate over the total array until no more changes are made
        temp_count = 0
        while True:
            changes = self.iterate()
            print("changes: %d" % changes)

            if changes == 0:
                break

            # temp_count += 1
            # if temp_count >= 10:
            #     break

        print("result", self._total[self._rows - 1, self._cols-1])
        print("Done")
        return

        # paths = [[(0,0)]]
        #
        # step = 0
        # while True:
        #
        #     new_paths = []
        #
        #     for path in paths:
        #         neighbours = self.get_neighbours(path)
        #         for n in neighbours:
        #             new_path = copy.deepcopy(path)
        #             new_path.append(n)
        #             new_paths.append(new_path)
        #
        #     paths = self.purge_paths(new_paths)
        #
        #     if self.check_done(paths):
        #         break
        #
        #     step += 1
        #     print("Step: %d Paths:" % step)
        #
        #     # for i, path in enumerate(paths):
        #     #     print("  %d -- %s" % (i, repr(path)))
        #
        #     # input("Continue...")

    # def check_done(self, paths):
    #
    #     end = (self._rows_orig - 1, self._cols_orig - 1)
    #
    #     finished_paths = []
    #     for path in paths:
    #         last = path[-1]
    #         # print("compare", last, end)
    #         if last == end:
    #             finished_paths.append(path)
    #
    #     if len(finished_paths) == 0:
    #         return False
    #
    #     winner = self.lowest_risk(finished_paths)
    #
    #     risk = self.path_risk(winner)
    #
    #     print("BEST PATH IS: %d" % risk)
    #     return True
    #
    # def purge_paths(self, paths):
    #     """
    #     There are only so many point in the map, so at any point keep only
    #     the path with the lowest score
    #     """
    #
    #     # Loop through all the paths and make a dict of endpoints
    #
    #     last_dict = {}
    #     old_count = len(paths)
    #
    #     for path in paths:
    #         last = path[-1]
    #
    #         path_list = last_dict.get(last, [])
    #         path_list.append(path)
    #         last_dict[last] = path_list
    #
    #     new_paths = []
    #
    #     for last, value in last_dict.items():
    #         # print("last point: %s path count: %d" % (repr(last), len(value)))
    #         path = self.lowest_risk(value)
    #         new_paths.append(path)
    #
    #     new_count = len(new_paths)
    #
    #     print("Purge: %d -> %d" % (old_count, new_count))
    #     return new_paths
    #
    # def lowest_risk(self, paths):
    #     if len(paths) == 1:
    #         return paths[0]
    #
    #     low_risk = None
    #     best_path = None
    #     for path in paths:
    #         risk = self.path_risk(path)
    #         # risk = sum( [self._risk[point] for point in path ] )
    #         if low_risk is None or risk < low_risk:
    #             low_risk = risk
    #             best_path = path
    #
    #     return best_path
    #
    # def path_risk(self, path):
    #     if len(path) < 2:
    #         return 0
    #
    #     risk = sum( [self._risk[point] for point in path ] ) - self._risk[(0,0)]
    #     return risk



if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


