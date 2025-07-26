import sys
import numpy as np

SPACE           = 46
MIRROR_LEFT     = 92
VERTICAL        = 124
HORIZONTAL      = 45
MIRROR_RIGHT    = 47
VERTICAL_USED   = 1
HORIZONTAL_USED = 2

LEFT    = 1
RIGHT   = 2
UP      = 3
DOWN    = 4

class Beam(object):

    _class_index = 0

    def __init__(self, r, c, rows, cols, direction):
        self._r = r
        self._c = c
        self._direction = direction
        self._index = Beam._class_index
        Beam._class_index += 1
        self._rows = rows
        self._cols = cols
        self._path = []
        self._done = False

    def step(self, map):

        beam = None

        old_r = self._r
        old_c = self._c

        if self._direction == RIGHT:
            self._c += 1

            if self._c >= self._cols:
                self._done = True
                return

            kind = map[self._r, self._c]

            if kind == SPACE or kind == HORIZONTAL or kind == HORIZONTAL_USED:
                # Do nothing
                pass

            elif kind == MIRROR_LEFT:
                self._direction = DOWN

            elif kind == MIRROR_RIGHT:
                self._direction = UP

            elif kind == VERTICAL:
                map[self._r, self._c] = VERTICAL_USED
                self._direction = UP
                beam = Beam(self._r, self._c, self._rows, self._cols, DOWN)
                # print("beam %d splitting" % self._index)

            elif kind == VERTICAL_USED:
                self._done = True
                return


        elif self._direction == UP:
            self._r -= 1
            if self._r < 0:
                self._done = True
                return

            kind = map[self._r, self._c]
            if kind == SPACE or kind == VERTICAL or kind == VERTICAL_USED:
                pass

            elif kind == MIRROR_LEFT:
                self._direction = LEFT

            elif kind == MIRROR_RIGHT:
                self._direction = RIGHT

            elif kind == HORIZONTAL:
                map[self._r, self._c] = HORIZONTAL_USED
                self._direction = LEFT
                beam = Beam(self._r, self._c, self._rows, self._cols, RIGHT)
                # print("beam %d splitting" % self._index)

            elif kind == HORIZONTAL_USED:
                self._done = True
                return

        elif self._direction == DOWN:
            self._r += 1
            if self._r >= self._rows:
                self._done = True
                return

            kind = map[self._r, self._c]
            if kind == SPACE or kind == VERTICAL or kind == VERTICAL_USED:
                pass

            elif kind == MIRROR_LEFT:
                self._direction = RIGHT

            elif kind == MIRROR_RIGHT:
                self._direction = LEFT

            elif kind == HORIZONTAL:
                self._direction = LEFT
                map[self._r, self._c] = HORIZONTAL_USED

                beam = Beam(self._r, self._c, self._rows, self._cols, RIGHT)
                # print("beam %d splitting" % self._index)

            elif kind == HORIZONTAL_USED:
                self._done = True
                return

        elif self._direction == LEFT:
            self._c -= 1
            if self._c < 0:
                self._done = True
                return

            kind = map[self._r, self._c]

            if kind == SPACE or kind == HORIZONTAL or kind == HORIZONTAL_USED:
                # Do nothing
                pass

            elif kind == MIRROR_LEFT:
                self._direction = UP

            elif kind == MIRROR_RIGHT:
                self._direction = DOWN

            elif kind == VERTICAL:
                map[self._r, self._c] = VERTICAL_USED

                self._direction = UP
                beam = Beam(self._r, self._c, self._rows, self._cols, DOWN)
                # print("beam %d splitting" % self._index)

            elif kind == VERTICAL_USED:
                self._done = True
                return

        else:
            raise ValueError("not implemented")

        # print("beam %d (%d, %d) -> (%d, %d)" % (self._index, old_r, old_c, self._r, self._c))

        # print("POSITION: r: %d c: %d" % (self._r, self._c))
        self._path.append((self._r, self._c))

        return beam

    def get_path(self):
        return self._path

    def get_index(self):
        return self._index

    def done(self):
        return self._done

class Runner(object):

    def __init__(self, filename):

        fp = None

        lines = []

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

        rows = len(lines)
        cols = len(lines[0])


        self._map = np.zeros((rows, cols))

        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                self._map[r,c] = ord(ch)

        print(self._map)
        self._beams_done = []

    def purge(self, beam_list):

        beam_list_not_done = []

        for beam in beam_list:
            if beam.done():
                self._beams_done.append(beam)
            else:
                beam_list_not_done.append(beam)

        return beam_list_not_done


    def part1(self, r, c, direction):

        rows, cols = self._map.shape

        beam_list = []

        # Create the first beam
        beam = Beam(r, c, rows, cols, direction)

        beam_list.append(beam)

        while True:

            # If there are no beams left to process we are done
            if len(beam_list) == 0:
                break

            new_beams = []
            for beam in beam_list:

                new_beam = beam.step(self._map)

                if new_beam is not None:
                    new_beams.append(new_beam)

            # Add any new beams to the list
            beam_list.extend(new_beams)
            beam_list = self.purge(beam_list)

            # print("End of loop:  Beams Active: %s Done: %d" % (len(beam_list), len(self._beams_done)))
            # input("continue...")

        # print("We are done!!!")
        # print("number of beams done", len(self._beams_done))

        hit_count = np.zeros((rows, cols))

        steps = []

        for beam in self._beams_done:
            path = beam.get_path()
            for step in path:
                # print("Beam %d path (%d, %d)" % (beam.get_index(), step[0], step[1]))
                steps.append(step)

        steps = list(set(steps))
        print("Part1: energized tiles: %d" % len(steps))
        self._beams_done = []
        
        return len(steps)

    def part2(self):

        self._map_copy = np.copy(self._map)

        rows, cols = self._map.shape

        results = []

        for r in range(rows):
            self._map = np.copy(self._map_copy)
            result = self.part1(r, -1, RIGHT)
            results.append(result)

        for r in range(rows):
            self._map = np.copy(self._map_copy)
            result = self.part1(r, cols, LEFT)
            results.append(result)

        for c in range(cols):
            self._map = np.copy(self._map_copy)
            result = self.part1(-1, c, DOWN)
            results.append(result)

        for c in range(cols):
            self._map = np.copy(self._map_copy)
            result = self.part1(rows, c, UP)
            results.append(result)

        print("part2: max coverage: %d" % max(results))

if __name__ == '__main__':

    # 11127 is too high

    runner = Runner(sys.argv[1])
    # runner.part1(0, -1, RIGHT)
    runner.part2()

