import numpy as np
import math
import sys

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self):

        self._map = {}
        self._lines = []
        self._segments = []
        self._min_x = self._min_y = self._max_x = self._max_y = None

        for line in sys.stdin:
            self._lines.append(line.strip())

    def run(self):

        for line in self._lines:
            self.process_line(line)

        self.build_map()
        self.print_map()

        overlaps = self.get_overlaps()

        print("Part 1: %d" % overlaps)

    def get_overlaps(self):
        total = 0
        for count in self._map.values():
            if count > 1:
                total += 1
        return total

    def get_sequence(self, start, stop):

        if start > stop:
            for p in range(start, stop-1, -1):
                yield p
        else:
            for p in range(start, stop+1):
                yield p

    def get_points(self, segment):

        points = []
        start = segment[0]
        stop = segment[1]

        if start[0] == stop[0]:
            # This is a vertical line
            for y in self.get_sequence( start[1], stop[1] ):
                points.append( (start[0], y))

        elif start[1] == stop[1]:
            # this is a horizontal line
            for x in self.get_sequence( start[0], stop[0] ):
                points.append( (x, start[1] ))

        else:
            x_list = [x for x in self.get_sequence( start[0], stop[0] ) ]
            y_list = [y for y in self.get_sequence( start[1], stop[1] ) ]

            for i in range(len(x_list)):
                points.append( (x_list[i], y_list[i]) )

        return points

    def build_map(self):

        for segment in self._segments:
            points = self.get_points(segment)

            for point in points:
                # print(point)
                count = self._map.get(point, 0)
                self._map[point] = count + 1

    def print_map(self):

        for y in range(self._min_y, self._max_y + 1):
            s = ''
            for x in range(self._min_x, self._max_x + 1):
                point = (x, y)
                count = self._map.get(point, 0)
                if count == 0:
                    s += "  ."
                else:
                    s += "%3d" % count

            print(s)

    def get_xy(self, point):
        parts = point.split(',')
        x = int(parts[0].strip())
        y = int(parts[1].strip())

        if self._max_x is None or x > self._max_x:
            self._max_x = x

        if self._min_x is None or x < self._min_x:
            self._min_x = x

        if self._max_y is None or y > self._max_y:
            self._max_y = y

        if self._min_y is None or y < self._min_y:
            self._min_y = y

        return x,y

    def process_line(self, line):

        parts = line.split('->')
        # print(parts)
        start = parts[0]
        stop = parts[1]

        x_start, y_start = self.get_xy(start)
        x_stop, y_stop = self.get_xy(stop)

        self._segments.append( ((x_start, y_start), (x_stop, y_stop)))


if __name__ == '__main__':
    runner = Runner()
    runner.run()
