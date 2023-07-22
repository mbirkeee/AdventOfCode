"""

"""
import numpy as np
import sys
import itertools

X = 0
Y = 1
Z = 2

class ExceptionDone(Exception):
    pass


class Cuboid(object):

    def __init__(self, index, on):

        self._index = index
        self._on = on

        self._use = True

        self._start_x = self._stop_x = None
        self._start_y = self._stop_y = None
        self._start_z = self._stop_z = None

    def __repr__(self):

        if self._on:
            sw = "ON "
        else:
            sw = 'OFF'
        return "Ind: %3d %s USE: %5s x: volume: %8d X: %6d..%6d Y: %6d..%6d Z: %6d..%6d" % (
            self._index,
            sw, repr(self._use),
            self.get_volume(),
            self._start_x, self._stop_x,
            self._start_y, self._stop_y,
            self._start_z, self._stop_z)



    def shift_axis(self, axis, value):

        # print("---------------cuboid shifting axis by %d" % value)
        # print(self)
        if axis == X:
            self._start_x += value
            self._stop_x += value

        elif axis == Y:
            self._start_y += value
            self._stop_y += value

        elif axis == Z:
            self._start_z += value
            self._stop_z += value
        else:
            raise ValueError('bad axis')
        # print(self)

    def contains(self, x=None, y=None, z=None):

        if x is not None:
            if x < self._start_x or x > self._stop_x:
                return False

        if y is not None:
            if y < self._start_y or y > self._stop_y:
                return False

        if z is not None:
            if z < self._start_z or z > self._stop_z:
                return False

        return True

    def get_volume(self):

        x = self._stop_x - self._start_x
        y = self._stop_y - self._start_y
        z = self._stop_z - self._start_z

        return x * y * z

    def get_on(self):
        return self._on

    def get_use(self):
        return self._use

    def get_dim(self, part):

        # print(">%s<" % part)
        part = part[2:]

        parts = part.split('..')
        # print(parts)

        start = int(parts[0])
        stop = int(parts[1])

        if start > stop:
            print("swap start stop")
            start, stop = stop, start

        if abs(start) > 50 or abs(stop) > 50:
            self._use = False

        return start, stop

    def set_dimensions_from_input(self, line):

        parts = line.split(',')

        self._start_x, self._stop_x = self.get_dim(parts[0])
        self._start_y, self._stop_y = self.get_dim(parts[1])
        self._start_z, self._stop_z = self.get_dim(parts[2])

    def set_start_stop(self, axis, start, stop):
        if axis == X:
            self._start_x = start
            self._stop_x = stop

        elif axis == Y:
            self._start_y = start
            self._stop_y = stop

        elif axis == Z:
            self._start_z = start
            self._stop_z = stop

    def get_next(self):

        for x in range(self._start_x, self._stop_x + 1):
            for y in range(self._start_y, self._stop_y + 1):
                for z in range(self._start_z, self._stop_z + 1):
                    yield (x,y,z)

    def get_start_stop(self, axis):
        if axis == X:
            return self._start_x, self._stop_x
        if axis == Y:
            return self._start_y, self._stop_y
        if axis == Z:
            return self._start_z, self._stop_z

    def get_intersection(self, other):

        # X direction
        other_start_x, other_stop_x = other.get_start_stop(X)
        start_x = max(self._start_x, other_start_x)
        stop_x = min(self._stop_x, other_stop_x)

        if stop_x < start_x:
            return None

        # Y direction
        other_start_y, other_stop_y = other.get_start_stop(Y)
        start_y = max(self._start_y, other_start_y)
        stop_y = min(self._stop_y, other_stop_y)

        if stop_y < start_y:
            return None

        # Z direction
        other_start_z, other_stop_z = other.get_start_stop(Z)
        start_z = max(self._start_z, other_start_z)
        stop_z = min(self._stop_z, other_stop_z)

        if stop_z < start_z:
            return None

        # These cubes must intersect
        cuboid = Cuboid(-1, 1)

        cuboid.set_start_stop(X, start_x, stop_x)
        cuboid.set_start_stop(Y, start_y, stop_y)
        cuboid.set_start_stop(Z, start_z, stop_z)

        return cuboid

class Runner(object):

    def __init__(self, filename):


        self._max_x = 0
        self._min_x = 0

        self._max_y = 0
        self._min_y = 0

        self._max_z = 0
        self._min_z = 0

        self._cuboid_index = 0
        lines = []
        fp = None

        self._cuboid_list = []

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(lines))

        for line in lines:
            parts = line.split(' ')

            if parts[0] == 'on':
                on = 1
            else:
                on = 0

            cuboid = Cuboid(self._cuboid_index, on)
            self._cuboid_index += 1

            cuboid.set_dimensions_from_input(parts[1])

            self._cuboid_list.append(cuboid)

    def print_cuboids(self):

        for cuboid in self._cuboid_list:
            print(cuboid)

    def part1(self):
        """
        Just filter out the big cuboids and use the ones in the middle
        """
        use_list = []

        for cuboid in self._cuboid_list:
            if not cuboid.get_use():
                continue
            use_list.append(cuboid)

        self._cuboid_list = use_list
        self.run()

    def run(self):
        print("run")
        self.print_cuboids()

        self.boundaries()

        self.shift_axis(X, abs(self._min_x))
        self.shift_axis(Y, abs(self._min_y))
        self.shift_axis(Z, abs(self._min_z))

        self.boundaries()

        indices_x = self.get_indices(X)
        indices_y = self.get_indices(Y)

        # for x in indices_x:
        #     print("X index", x)
        # for y in indices_y:
        #     print("Y index", y)

        rectangle_count = 0
        total_area = 0
        total_bits = 0

        for x_index, x in enumerate(indices_x[:-1]):
            for y_index, y in enumerate(indices_y[:-1]):

                next_x = indices_x[x_index+1]
                next_y = indices_y[y_index+1]

                area = (next_x - x) * (next_y - y)

                # print("check rectangle %d at %d,%d area %d" % (rectangle_count, x, y,area))
                # print("next_x", next_x)
                # print("next_y", next_y)

                rectangle_count += 1
                total_area += area

                bits_on = self.process_column_z(x, y, self._max_z)
                bits_on *= area

                total_bits += bits_on
        print("total rectangles: %d total area: %d" % (rectangle_count, total_area))
        print("total bits", total_bits)

    def process_column_z(self, x, y, max_z):
        # print("process column at %d,%d" % (x, y))

        result = np.zeros((max_z+1), dtype = np.uint8)

        for cuboid in self._cuboid_list:
            if not cuboid.contains(x=x, y=y):
                continue

            start, stop = cuboid.get_start_stop(Z)
            on = cuboid.get_on()

            if on:
                result[start:stop+1] = 1
                #print(result)
            else:
                result[start:stop+1] = 0

            #print(result)

        return np.sum(result)

    def get_indices(self, axis):

        indices = []
        for cuboid in self._cuboid_list:

            start, stop = cuboid.get_start_stop(axis)
            # print(start, stop)
            indices.append(start)
            indices.append(stop+1)

        indices = list(set(indices))
        indices.sort()

        return indices

    def shift_axis(self, axis, value):
        for cuboid in self._cuboid_list:
            cuboid.shift_axis(axis, value)

    def run_simple(self):
        print("run")

        result = {}

        for cuboid in self._cuboid_list:

            if not cuboid.get_use(): continue

            on = cuboid.get_on()

            for cube in cuboid.get_next():
                # print(cube)

                if on:
                    result[cube] = 1
                else:
                    try:
                        del result[cube]
                    except:
                        pass

            # raise ValueError("temp stop")

        print(len(result))

    def boundaries(self):

        self._max_x = 0
        self._min_x = 0

        self._max_y = 0
        self._min_y = 0

        self._max_z = 0
        self._min_z = 0

        for cuboid in self._cuboid_list:

            start_x, stop_x = cuboid.get_start_stop(X)
            start_y, stop_y = cuboid.get_start_stop(Y)
            start_z, stop_z = cuboid.get_start_stop(Z)

            if start_x < self._min_x:
                self._min_x = start_x

            if start_y < self._min_y:
                self._min_y = start_y

            if start_z < self._min_z:
                self._min_z = start_z

            if stop_x > self._max_x:
                self._max_x = stop_x

            if stop_y > self._max_y:
                self._max_y = stop_y

            if stop_z > self._max_z:
                self._max_z = stop_z

        print("X: min: %6d MAX %6d" % (self._min_x, self._max_x))
        print("Y: min: %6d MAX %6d" % (self._min_y, self._max_y))
        print("Z: min: %6d MAX %6d" % (self._min_z, self._max_z))

    # def run2(self):
    #     print("run2")
    #
    #     print_count = 0
    #
    #     for cuboid in self._cuboid_list:
    #         print(cuboid)
    #
    #     count = len(self._cuboid_list)
    #
    #     i = itertools.combinations(range(count), 2)
    #     for item in i:
    #
    #         cuboid1 = self._cuboid_list[item[0]]
    #         cuboid2 = self._cuboid_list[item[1]]
    #
    #         result = cuboid1.get_intersection(cuboid2)
    #         if result is None:
    #             # print("cuboids do NOT intersect")
    #             pass
    #         else:
    #             print("cuboids ----------------------------------")
    #             print(cuboid1)
    #             print(cuboid2)
    #             print(result)
    #             print_count += 1
    #             if print_count > 20:
    #                 print_count = 0
    #                 input("continue...")

    def test_intersect(self):

        cuboid1 = self._cuboid_list[0]
        cuboid2 = self._cuboid_list[1]

        result = cuboid1.get_intersection(cuboid2)

        print(cuboid1)
        print(cuboid2)
        print(result)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    # runner.print_cuboids()
    # runner.part1()
    # runner.boundaries()
    runner.run()
    #runner.test_intersect()
    #runner.run2()
