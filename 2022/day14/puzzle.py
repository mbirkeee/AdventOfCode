
STONE = 1
SAND = 2

class ExceptionDone(Exception):
    pass
#
# class ExceptionOrderBad(Exception):
#     pass
#
# class ExceptionOrderGood(Exception):
#     pass

class Node(object):

    def __init__(self, x, y, kind, map):
        self._x = x
        self._y = y
        self._kind = kind
        self._map = map
        self._max_y = None

    def set_max_y(self, val):
        self._max_y = val

    def get_key(self):
        return (self._x, self._y)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_kind(self):
        return self._kind

    def fall(self):

        x = self._x
        y = self._y

        # Get the node below
        if (y) >= (self._max_y + 1):
             # We are on the floor
             # self._y = y+1
             self._map[self.get_key()] = self
             # print("on the floor (%d,%d)" % (self._x, self._y))

             return False

        below = self._map.get((x, y+1))
        if below is None:
            self._y = y+1
            # print("fall to (%d,%d)" % (self._x, self._y))

            # if self._y > self._max_y:
            #      raise ExceptionDone()
            return True


        # elif below.get_kind() == STONE:
        #     print("landed on a stone (%d,%d)" % (self._x, self._y))
        #     self._map[self.get_key()] = self
        #     return False

        else:
            # Check to the left
            spot = self._map.get((x-1, y+1))
            if spot is None:
                self._x = x-1
                self._y = y+1
                # print("move to (%d,%d)" % (self._x, self._y))

                return True

            spot = self._map.get((x+1, y+1))
            if spot is None:
                self._x = x+1
                self._y = y+1
                # print("move to (%d,%d)" % (self._x, self._y))
                return True

            # If we made it to here we are stuck
            # print("stuck (%d,%d)" % (self._x, self._y))
            self._map[self.get_key()] = self
            return False


class Runner(object):

    def __init__(self):
        # self._file_name = 'input_test.txt'
        self._file_name = 'input_real.txt'

        self._min_x = self._max_x = self._min_y = self._max_y = None

        self._map = {}

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
        try:
            grain_count = 0
            while True:
                grain_count += 1
                print("grain: %d" % grain_count)
                # create a grain of sand

                plugged = self._map.get((500,0))
                if plugged:
                    print("plugged!!!")
                    break

                sand = Node(500, 0, SAND, self._map)
                sand.set_max_y(self._max_y)
                while True:
                    if not sand.fall():
                        break

                # if grain_count >= 100:
                #     break

        except ExceptionDone as err:
            print("into the abyss!!!")

        self.get_dimensions()

        self.print_map()

    def get_xy(self, input):
        parts = input.split(',')
        x = int(parts[0].strip())
        y = int(parts[1].strip())
        return x, y

    def yield_index(self, start, stop):
        if stop < start:
            stop, start = start, stop
        for i in range(start, stop+1):
            yield i

    def process_line(self, line):
        # print("------------------ LINE %s" % line)
        segments = line.split('->')
        segments = [segment.strip() for segment in segments]
        segment_count = len(segments)

        for i in range(segment_count-1):
            start = segments[i]
            stop = segments[i+1]

            start_x, start_y = self.get_xy(start)
            stop_x,  stop_y  = self.get_xy(stop)

            # print("Segment: '%s' -> '%s'" % (start, stop))

            if start_x == stop_x:
                # print("iterate over y")
                x = start_x
                for y in self.yield_index(start_y, stop_y):
                    node = Node(x, y, STONE, self._map)
                    self._map[node.get_key()]=node
            elif start_y == stop_y:
                # print("iterate over x")
                y = start_y
                for x in self.yield_index(start_x, stop_x):
                    node = Node(x, y, STONE, self._map)
                    self._map[node.get_key()]=node
                    # print(x,y)

    def get_dimensions(self):
        for node in self._map.values():
            x = node.get_x()
            y = node.get_y()

            if self._min_x is None or x < self._min_x:
                self._min_x = x

            if self._max_x is None or x > self._max_x:
                self._max_x = x

            if self._min_y is None or y < self._min_y:
                self._min_y = y

            if self._max_y is None or y > self._max_y:
                self._max_y = y


    def print_map(self):

        for y in range(0, self._max_y + 2):
            s = ""
            for x in range(self._min_x-1, self._max_x+2):
                node = self._map.get((x,y))
                if node is None:
                    s += ' '
                else:
                    if node.get_kind() == STONE:
                        s += '#'
                    else:
                        s += 'o'

            print(s)

if __name__ == '__main__':
    runner = Runner()
    runner.run()
