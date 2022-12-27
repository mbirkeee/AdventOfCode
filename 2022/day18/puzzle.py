import itertools
import sys

X = 0
Y = 1
Z = 2

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self):
        # self._file_name = 'input_test.txt'
        self._file_name = 'input_real.txt'

        self._cubes = {}

        self._key_list_cubes = []
        self._key_list_water = []

        self._min_x = 99999999999
        self._min_y = 99999999999
        self._min_z = 99999999999

        self._max_x = -99999999999
        self._max_y = -99999999999
        self._max_z = -99999999999

        self._touch_count = 0

    def run(self):

        fp = open(self._file_name, 'r')
        lines = []
        for line in fp:
            line = line.strip()
            lines.append(line)

        fp.close()

        for i, line in enumerate(lines):
            self.add_cube(line, i)

        self.get_dimensions()
        self.process_plane( )

        self.shift_axes()
        self.get_dimensions()
        self.process_plane( )

        self.shift_axes()
        self.get_dimensions()
        self.process_plane( )

        print("touch count: %d" % self._touch_count)
        sides = len(self._cubes) * 6 - 2 * self._touch_count
        print("Part 1: surface area: %d" % sides)

        self._touch_count = 0

        # Part 2: Find surrounded cubes
        self._cubes = self.find_trapped()

        self.get_dimensions()
        self.process_plane( )

        self.shift_axes()
        self.get_dimensions()
        self.process_plane( )

        self.shift_axes()
        self.get_dimensions()
        self.process_plane( )

        print("touch count: %d" % self._touch_count)
        sides = len(self._cubes) * 6 - 2 * self._touch_count
        print("Part 2: surface area: %d" % sides)


    def find_trapped(self):
        """
        recursively flood the volume containing the lave droplet
        """

        trapped = {}
        trapped_index = 0

        x_range = 1 + self._max_x - self._min_x
        y_range = 1 + self._max_y - self._min_y
        z_range = 1 + self._max_z - self._min_z

        print("recursion depth: %d" % sys.getrecursionlimit())
        sys.setrecursionlimit(10000)
        print("recursion depth: %d" % sys.getrecursionlimit())

        print("overall dimensions: %d %d %d" % (x_range, y_range, z_range))
        total_volume = x_range * y_range * z_range
        print("volume: %d" % total_volume)
        print("len(cubes): %d" % len(self._key_list_cubes))

        drop = [self._min_x, self._min_y, self._min_z]

        if self.make_key(drop) in self._key_list_cubes:
            raise ValueError('bad starting point')

        self.process_drop(drop)

        print("len(water): %d" % len(self._key_list_water))


        for x in range(self._min_x, self._max_x + 1):
            for y in range(self._min_y, self._max_y + 1):
                for z in range(self._min_z, self._max_z + 1):
                    cube = [x,y,z]
                    key = self.make_key(cube)

                    if key in self._key_list_cubes:
                        continue

                    if key in self._key_list_water:
                        continue

                    # print("cube is inside: %s" % cube)
                    trapped[trapped_index] = cube
                    trapped_index += 1

        return trapped

    def process_drop(self, drop):
        # print("process drop: %s" % repr(drop))
        if drop[0] < self._min_x: return
        if drop[0] > self._max_x: return
        if drop[1] < self._min_y: return
        if drop[1] > self._max_y: return
        if drop[2] < self._min_z: return
        if drop[2] > self._max_z: return

        key = self.make_key(drop)

        if key in self._key_list_cubes:
            return

        if key in self._key_list_water:
            return

        # This drop of water can occupy this space:
        self._key_list_water.append(key)

        surrounding_drops = self.get_surrounding_cubes(drop)

        for child in surrounding_drops:
            self.process_drop(child)

    def get_surrounding_cubes(self, cube):

        result = [
            [cube[0] + 1, cube[1]    , cube[2]    ],
            [cube[0] - 1, cube[1]    , cube[2]    ],
            [cube[0]    , cube[1] + 1, cube[2]    ],
            [cube[0]    , cube[1] - 1, cube[2]    ],
            [cube[0]    , cube[1]    , cube[2] + 1],
            [cube[0]    , cube[1]    , cube[2] - 1]
        ]
        return result

    def process_plane(self):

        for y in range(self._min_y, self._max_y+1):
            for z in range(self._min_z, self._max_z+ 1):
                temp_list = []

                for cube in self._cubes.values():
                    if cube[1] == y and cube[2] == z:
                        temp_list.append(cube)

                # print("Y: %d Z: %d cubes: %s" % (y, z, temp_list))
                # print(temp_list)
                if len(temp_list) < 2: continue

                pairs = itertools.combinations(temp_list, 2)
                for pair in pairs:
                    # print("compare: %s" % repr(pair))
                    if abs( pair[0][0] - pair[1][0] ) == 1:
                        # print("Pairs touch!!!")
                        self._touch_count += 1

    def shift_axes(self):

        new = {}

        for index, cube in self._cubes.items():
            cube_new = [cube[1], cube[2], cube[0]]
            new[index] = cube_new

        self._cubes = new

    def get_dimensions(self):

        self._min_x = 99999999999
        self._min_y = 99999999999
        self._min_z = 99999999999

        self._max_x = -99999999999
        self._max_y = -99999999999
        self._max_z = -99999999999

        for cube in self._cubes.values():
            x = cube[0]
            y = cube[1]
            z = cube[2]

            if x < self._min_x: self._min_x = x
            if y < self._min_y: self._min_y = y
            if z < self._min_z: self._min_z = z
            if x > self._max_x: self._max_x = x
            if y > self._max_y: self._max_y = y
            if z > self._max_z: self._max_z = z

        # print(self._min_x, self._max_x)
        # print(self._min_y, self._max_y)
        # print(self._min_z, self._max_z)
        self.make_key_list()

    def make_key(self, cube):
        return '%d-%d-%d' % (cube[0], cube[1], cube[2])

    def make_key_list(self):

        key_list = []

        for cube in self._cubes.values():
            key_list.append(self.make_key(cube))

        self._key_list_cubes = key_list

    def add_cube(self, line, index):

        parts = line.split(',')

        cube = [
            int(parts[0].strip() ) * 1,
            int(parts[1].strip() ) * 1,
            int(parts[2].strip() ) * 1
        ]

        self._cubes[index] = cube

def test1():

    x = [1,2,3]
    y = itertools.combinations(x, 2)

    for pair in y:
        print(pair)

if __name__ == '__main__':
    # test1()
    runner = Runner()
    runner.run()
