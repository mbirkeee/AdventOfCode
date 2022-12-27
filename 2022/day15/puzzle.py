import numpy as np
import time

class ExceptionDone(Exception):
    pass

class Sensor(object):

    def __init__(self, sx, sy, bx, by):
        # print("Sensor: x: %d y: %d bx: %d by: %d" % (sx, sy, bx, by))

        self._sx = sx
        self._sy = sy
        self._bx = bx
        self._by = by
        dist_x = abs(sx - bx)
        dist_y = abs(sy - by)

        self._dist = dist_x + dist_y

    def get_border(self):
        new_dist = self._dist + 1

        pairs = []

        y1 = self._sy
        y2 = self._sy
        for x in range(self._sx - new_dist, self._sx + 1):
            pairs.append((x,y1))
            pairs.append((x,y2))
            y1 += 1
            y2 -= 1

        for x in range(self._sx, self._sx + new_dist + 1):
            y1 -= 1
            y2 += 1
            pairs.append((x,y1))
            pairs.append((x,y2))


        # print("X: %d Y: %d --- dist: %d" % (self._sx, self._sy, self._dist))
        # print(pairs)

        return list(set(pairs))

    def get_coords(self):
        return self._sx, self._sy

    def get_dist(self):
        return self._dist

    def get_x_min(self):
        return self._sx - self._dist

    def get_x_max(self):
        return self._sx + self._dist

    def is_beacon(self, x, y):
        if x == self._bx and y == self._by:
            return True
        return False

    def is_covered(self, x, y):

        dist_x = abs(self._sx - x)
        dist_y = abs(self._sy - y)

        dist = dist_x + dist_y
        if dist <= self._dist:
            return True
        return False

    def is_covered2(self, x, y):

        dist_x = abs(self._sx - x)
        dist_y = abs(self._sy - y)

        dist = dist_x + dist_y

        if dist > self._dist:
            print("not covered")
            return x

        skip_to = self._sx + dist_x + 1
        print("skip %d -> %d" % (x, skip_to))
        return skip_to


        # dist = dist_x + dist_y
        # if dist <= self._dist:
        #     skip_ahead = self._dist - dist_y
        #     return skip_ahead
        #
        # return 0

    def get_coverage_row(self, y, start_x, stop_x, array, i):

        size = stop_x - start_x

        y_dist = abs(self._sy - y)

        if y_dist > self._dist:
            # This row has no coverage
            # return result
            return

        range = self._dist - y_dist
        x_begin = self._sx - range
        x_end = self._sx + range

        if x_begin < start_x: x_begin = start_x
        if x_end > stop_x: x_end = stop_x

        array[i, x_begin:x_end+1] = 1
        return

class Runner(object):

    def __init__(self):
        # self._file_name = 'input_test.txt'
        # self._file_name = 'input_test2.txt'
        self._file_name = 'input_real.txt'

        self._min_x = None
        self._max_x = None

        self._sensors = []
        self._array = None

    def run(self):

        fp = open(self._file_name, 'r')
        lines = []
        for line in fp:
            line = line.strip()
            lines.append(line)

        fp.close()

        # build the map
        for line in lines:
            self.process_line(line)

        self.get_dimensions()

        print("min x: %d max x: : %d" % (self._min_x, self._max_x))

        # Part 1
        # self.search_row(2000000)

        # self.search_beacon(4000000,4000000)
        # self.search_beacon(20,20)
        # self.search_beacon2(4000000, 4000000)
        self.search_border(20, 20)
        self.search_border(4000000, 4000000)

    def search_border(self, max_x, max_y):

        for sensor in self._sensors:
            pairs = sensor.get_border()
            for pair in pairs:
                x = pair[0]
                y = pair[1]
                if x < 0 or x > max_x:
                    continue
                if y < 0 or y > max_y:
                    continue

                covered = False
                for sensor in self._sensors:
                      if sensor.is_covered(x, y):
                        covered = True
                        break

                if not covered:
                    print("X: %d, Y: %d not covered!!" % (x, y))

    def search_beacon2(self, max_x, max_y):

        t = time.time()

        counter1 = 0
        counter2 = 0

        for y in range(max_y + 1):
            for x in range(max_x + 1):
                covered = False
                for i, sensor in enumerate(self._sensors):
                    if sensor.is_covered(x, y):
                        covered = True
                        break

                if not covered:
                    print("X: %d, Y: %d not covered!!" % (x, y))

            counter1 += 1
            counter2 += 1
            if counter2 >= 100:
                n = time.time()

                elapsed = n - t
                print("Count: %d, elapsed: %.2f" % (counter1, elapsed))
                t = n
                counter2 = 0


    def search_beacon(self, max_x, max_y):

        t = time.time()

        size = (len(self._sensors), max_x+1)
        self._array = np.zeros(size, dtype=np.int32)

        result = np.zeros((max_x+1), dtype=np.int32)

        counter1 = 0
        counter2 = 0
        # # First, do rows


        for y in range(0, max_y + 1):
            self._array *= 0
            for i, sensor in enumerate(self._sensors):
                sensor.get_coverage_row(y, 0, max_x+1, self._array, i)
                # np.sum(self._array, axis=0, out=result)
                # r = np.where(result==0)[0]
                # if len(r) == 0:
                #     print("can quit early")
                #     break
                # print(r)
            # print(self._array)
            np.sum(self._array, axis=0, out=result)

            # print(result)

            r = np.where(result==0)[0]
            # print(r.shape)

            if len(r) == 1:
                print("Y: %d" % y)
                print(r)
                # break

            counter1 += 1
            counter2 += 1
            if counter2 >= 100:
                n = time.time()

                elapsed = n - t
                print("Count: %d, elapsed: %.2f" % (counter1, elapsed))
                t = n
                counter2 = 0

    def search_row(self, row):

        covered = []
        beacons = []

        y = row
        for x in range(self._min_x, self._max_x):
            # print(x, y)
            for sensor in self._sensors:
                if sensor.is_covered(x, y):
                    covered.append((x,y))

                if sensor.is_beacon(x, y):
                    beacons.append((x, y))

        covered = list(set(covered))
        beacons = list(set(beacons))
        print("covered count: %d" % len(covered))
        print("beacon count: %d" % len(beacons))

        print("No beacons: %d" % (len(covered) - len(beacons)))

    def get_dimensions(self):

        for sensor in self._sensors:
            min_x = sensor.get_x_min()
            max_x = sensor.get_x_max()

            if self._min_x is None or min_x < self._min_x:
                self._min_x = min_x

            if self._max_x is None or max_x > self._max_x:
                self._max_x = max_x

    def get_val(self, item):
        parts = item.split('=')
        # print(parts)
        return int(parts[1].strip(' ,:'))

    def process_line(self, line):
        print("------------------ LINE %s" % line)
        parts = line.split()
        # print(parts)
        sx = self.get_val(parts[2])
        sy = self.get_val(parts[3])

        bx = self.get_val(parts[8])
        by = self.get_val(parts[9])

        sensor = Sensor(sx, sy, bx, by)
        self._sensors.append(sensor)

if __name__ == '__main__':
    runner = Runner()
    runner.run()
