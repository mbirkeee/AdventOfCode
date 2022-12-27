import numpy as np

STATE_MAP = 0
STATE_ROUTE = 1

TURN_RIGHT  = 'R'
TURN_LEFT   = 'L'

RIGHT   = 0
DOWN    = 1
LEFT    = 2
UP      = 3

class ExceptionDone(Exception):
    pass

TURN_MAP = {
    UP : {
        TURN_RIGHT: RIGHT,
        TURN_LEFT: LEFT
    },
    DOWN: {
        TURN_RIGHT: LEFT,
        TURN_LEFT: RIGHT
    },
    RIGHT : {
        TURN_RIGHT: DOWN,
        TURN_LEFT: UP
    },
    LEFT: {
        TURN_RIGHT: UP,
        TURN_LEFT:DOWN
    },
}

class Edge(object):

    def __init__(self, start_in, stop_in, dir_in, start_out, stop_out, dir_out):

        self._input = self.make_array(start_in, stop_in)
        self._output = self.make_array(start_out, stop_out)

        self._dir_in = dir_in
        self._dir_out = dir_out
        print("*"*80)
        print(self._input)
        print(self._output)

        if len(self._input) != 50:
            raise ValueError("bad input: %d" % len(self._input))

        if len(self._output) != 50:
            raise ValueError("bad output: %d start: %s stop:%s " %
                             (len(self._output), repr(start_out), repr(stop_out)))

    def find(self, x, y, dir):

        if dir != self._dir_in:
            return None, None, None

        try:
            index = self._input.index((x,y))
            new_point = self._output[index]
            return new_point[0], new_point[1], self._dir_out

        except:
            pass

        return None, None, None


    def make_array(self, start, stop):

        x_start = start[0]
        x_stop = stop[0]

        y_start = start[1]
        y_stop = stop[1]

        len_x = x_stop - x_start
        len_y = y_stop - y_start

        if abs(len_x) == 49:
            if len_y != 0:
                raise ValueError("bad y input")

            # X input varies
            if len_x > 0:
                # print("here 1")
                array = [ (x, y_start) for x in range(x_start, x_stop+1)]
            else:
                # print("here 2")
                array = [(x, y_start) for x in range(x_start, x_stop-1, -1)]

        elif len_x == 0:
            if abs(len_y) != 49:
                raise ValueError("bad y input: y: %d" % len_y)

            # Y input varies
            if len_y > 0:
                # print("here 3")
                array = [ (x_start, y) for y in range(y_start, y_stop+1)]
            else:
                # print("here 4", y_start, y_stop)
                array = [ (x_start, y) for y in range(y_start, y_stop-1, -1)]
        else:
            raise ValueError("bad x")

        return array


class Point(object):

    def __init__(self, x, y, wall=False):
        # print("add point", x, y, wall)
        self._x = x
        self._y = y
        self._wall = wall
        self._occupied = False
        self._facing = None
        self._map = None
        self._max_x = 0
        self._max_y = 0
        self._edgeman = None

    def set_edgeman(self, edgeman):
        self._edgeman = edgeman

    def set_size(self, x, y):
        self._max_x = x
        self._max_y = y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_map(self, map):
        self._map = map

    def turn(self, direction):

        meta = TURN_MAP[self._facing]
        self._facing = meta[direction]

    def get_facing(self):
        return self._facing

    def set_facing(self, facing):
        self._facing = facing

    def move(self, steps):

        # print("move")
        point = self

        for i in range(steps):
            new_x = point.get_x()
            new_y = point.get_y()

            print("move", i, new_x, new_y )

            facing = point.get_facing()
            if facing == RIGHT:
                new_x += 1
            elif facing == LEFT:
                new_x -= 1
            elif facing == UP:
                new_y -= 1
            else:
                new_y += 1

            new_point = self._map.get((new_x, new_y))

            if new_point is None:
                # new_point = self.get_wrapped_point()
#                new_x, new_y, new_facing = self.get_wrapped_point(self._x, self._y, self._facing)
                n_x, n_y, new_facing = self._edgeman.get_next_point(point.get_x(), point.get_y(), point.get_facing() )

                if n_x is None:
                    raise ValueError("failed to find edge point: x: %d y: %d" % point.get_x(), point.get_y() )

                new_point = self._map.get((n_x, n_y))
                facing = new_facing

            if new_point.is_wall():
                # print("hit a wall... this point is the new current position")
                return point

            point = new_point
            point.set_occupied(True)
            point.set_facing(facing)

        return point



    def get_wrapped_point_part_1(self):

        # print("get_wrapped_point called for x %d: y: %d facing: %d" % (self._x, self._y, self._facing))
        if self._facing == RIGHT:
            # Get the leftmost poin in this line:
            for x in range(self._max_x):
                new_point = self._map.get((x,self._y))
                if new_point is not None:
                    return new_point

        if self._facing == LEFT:
            for x in range(self._max_x -1, -1, -1):
                new_point = self._map.get((x,self._y))
                if new_point is not None:
                    return new_point

        if self._facing == UP:
            # print("facing up")
            for y in range(self._max_y - 1, -1, -1):
                # print("testing up location", self._x, y)
                new_point = self._map.get((self._x,y))
                if new_point is not None:
                    return new_point

        if self._facing == DOWN:
            for y in range(self._max_y):
                new_point = self._map.get((self._x,y))
                if new_point is not None:
                    return new_point

        print("error: point x %d y: %d facing: %d" % (self._x, self._y, self._facing))
        raise ValueError("returning a None!!!!")

    def set_occupied(self, facing):
        self._occupied = True
        self._facing = facing

    def is_wall(self):
        return self._wall

    def get_char(self):
        if self._wall:
            return '#'

        if not self._occupied:
            return '.'

        if self._facing == RIGHT:
            return '>'

        if self._facing == LEFT:
            return '<'

        if self._facing == UP:
            return '^'

        if self._facing == DOWN:
            return 'v'

        raise ValueError('bad setting')

class EdgeManager(object):

    def __init__(self):

        edges = [
            [ (100,  49), (149,  49), DOWN,  ( 99,  50), ( 99,  99), LEFT  ],
            [ ( 99,  50), ( 99,  99), RIGHT, (100,  49), (149,  49), UP    ],

            [ (149,   0), (149,  49), RIGHT, ( 99, 149), ( 99, 100), LEFT  ],
            [ ( 99, 149), ( 99, 100), RIGHT, (149,   0), (149,  49), LEFT  ],

            [ ( 49, 150), ( 49, 199), RIGHT, ( 50, 149), ( 99, 149), UP    ],
            [ ( 50, 149), ( 99, 149), DOWN,  ( 49, 150), ( 49, 199), LEFT  ],

            [ (  0, 199), ( 49, 199), DOWN,  (100,   0), (149,   0), DOWN  ],
            [ (100,   0), (149,   0),   UP,  (  0, 199), ( 49, 199),   UP  ],

            [ (  0, 150), (  0, 199), LEFT,  ( 50,   0), ( 99,   0), DOWN  ],
            [ ( 50,   0), ( 99,   0), UP,    (  0, 150), (  0, 199), RIGHT ],

            [ (  0, 100), ( 49, 100), UP,    ( 50,  50), ( 50,  99), RIGHT ],
            [ ( 50,  50), ( 50,  99), LEFT,  (  0, 100), ( 49, 100), DOWN  ],

            [ (  0, 100), (  0, 149), LEFT,  ( 50,  49), ( 50,   0), RIGHT ],
            [ ( 50,  49), ( 50,   0), LEFT,  (  0, 100), (  0, 149), RIGHT ]
        ]

        self._edge_list = []

        for meta in edges:
            # print(meta)
            edge = Edge(*meta)
            self._edge_list.append(edge)

    def get_next_point(self, x, y, dir):

        for edge in self._edge_list:
            x_next, y_next, dir_next = edge.find(x, y, dir)
            if x_next is not None:
                # print("found next point!!!!")
                return x_next, y_next, dir_next

        raise ValueError("did not find next point!!!", x, y, dir)


class Runner(object):

    def __init__(self):
        # self._file_name = 'input_test.txt'
        self._file_name = 'input_real.txt'

        self._route_index = 0
        self._state = STATE_MAP
        self._route_string = None
        self._map_lines = []
        self._route = []
        self._map = {}
        self._max_x = 0
        self._max_y = 0
        self._current_location = None
        self._edgemen = EdgeManager()

    def run(self):

        fp = open(self._file_name, 'r')
        lines = []
        for line in fp:
            lines.append(line)

        fp.close()

        for line in lines:
            self.process_line(line)

        self.build_map()
        self.build_route()
        self.print_route()
        self._current_location = self.set_start()

        try:
            for route in self.get_next():
                # print("route: %s" % repr(route))
                if route in [TURN_RIGHT, TURN_LEFT]:
                    self._current_location.turn(route)
                else:
                    self._current_location = self._current_location.move(route)

                # self.print_map()
                # input("continue...")
        finally:
            # pass
            self.print_map()

        self.print_map()

        # Done
        x = self._current_location.get_x() + 1
        y = self._current_location.get_y() + 1
        facing = self._current_location.get_facing()

        print(x,y,facing)

        result = 1000 * y + 4 * x + facing
        print("Result: %d" % result)

    def get_next(self):
        for route in self._route:
            yield route

    def set_start(self):

        y = 0
        x = 0
        for x in range(self._max_x):
            p = self._map.get((x,y))
            if p is None:
                continue
            self._current_point = p
            p.set_occupied(RIGHT)
            return p

        raise ValueError('start error')

    def print_map(self):
        print(self._max_x, self._max_y)

        for y in range(self._max_y):
            s = '%4d  ' % y
            for x in range(self._max_x):

                p = self._map.get((x,y))
                if p is None:
                    s += ' '
                else:
                    s += p.get_char()
            print(s)

    def build_map(self):

        for line in self._map_lines:
            if len(line) > self._max_x:
                self._max_x = len(line)
            self._max_y += 1

        for y, line in enumerate(self._map_lines):
            for x in range(len(line)):
                p = line[x]
                if p == ' ' or p == '\n':
                    continue

                if p == '.':
                    point = Point(x, y)
                elif p == '#':
                    point = Point(x, y, wall=True)
                else:
                    raise ValueError('bad point: %s' % repr(line[x]))

                self._map[(x,y)] = point

        for point in self._map.values():
            point.set_map(self._map)
            point.set_size(self._max_x, self._max_y)
            point.set_edgeman(self._edgemen)

    def print_route(self):
        for step in self._route:
            print("Route: %s" % repr(step))

    def build_route(self):

        s = ''
        for c in self._route_string:
            print(c)
            if c in [TURN_RIGHT, TURN_LEFT]:
                if s:
                    self._route.append(int(s))
                    s = ''
                self._route.append(c)
            else:
                s += c
        if s:
            self._route.append(int(s))


    def process_line(self, line):

        if len(line) == 1:
            self._state = STATE_ROUTE
            # print("switch")
            return

        if self._state == STATE_MAP:
            # print("add map line", line)
            self._map_lines.append(line)
        else:
            self._route_string  = line.strip()
            # print('route', self._route)

def test1():
    em = EdgeManager()

    result = em.get_next_point(100, 0, UP)
    print(result)

if __name__ == '__main__':
    runner = Runner()
    # test1()
    runner.run()
