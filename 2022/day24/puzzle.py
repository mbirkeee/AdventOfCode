import numpy as np

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

class Blizzard(object):

    def __init__(self, x, y, direction, max_x, max_y):

        self._x = x
        self._y = y
        self._dir = direction
        self._max_x = max_x
        self._max_y = max_y
        # print(x, y, self._max_x, self._max_y)

    def move(self):
        x = self._x
        y = self._y

        if self._dir == '<':
            self._x -= 1
            if self._x < 0:
                self._x = self._max_x

        elif self._dir == '^':
            self._y -= 1
            if self._y < 0:
                self._y = self._max_y

        elif self._dir == '>':
            self._x += 1
            if self._x > self._max_x:
                self._x = 0

        elif self._dir == 'v':
            self._y += 1
            if self._y > self._max_y:
                self._y = 0

        else:
            raise ValueError('bad dir')

        # print("move", x, y , self._dir, self._x, self._y)

    def get_position(self):
        return self._x, self._y, self._dir

class Runner(object):

    def __init__(self):
        self._file_name = 'input_test.txt'
        self._file_name = 'input_real.txt'
        self._blizzard_list = []
        self.paths_new = []

        self._map = {}

        self._target = None
        self._paths = []

    def run(self):

        fp = open(self._file_name, 'r')
        lines = []
        for line in fp:
            lines.append(line.strip())

        fp.close()

        line_count = len(lines)
        lines2 = []
        for i, line in enumerate(lines):
            if i == 0 or i == line_count - 1:
                print("skipping line: %s" % line)
                continue
            lines2.append(line.strip('#'))

        self._max_y = len(lines2) - 1
        self._max_x = len(lines2[0]) - 1

        for y, line in enumerate(lines2):
            for x, c in enumerate(line):
                if c in ['<', '^', '>', 'v']:
                    b = Blizzard(x, y, c, self._max_x, self._max_y)
                    self._blizzard_list.append(b)

        print("-------------------------------")
        self.build_map()
        self.print_map()

        routes = [
            (  (0, -1),                         (self._max_x, self._max_y)  ),
            (  (self._max_x, self._max_y+1),    (0, 0)                      ),
            (  (0, -1),                         (self._max_x, self._max_y)  )
        ]

        minute = 0
        while True:

            done= False
            if self._target is None:
                print("pop route")
                try:
                    route = routes.pop(0)
                except:
                    input("done")
                    done = True

                if done:
                    break

                self._paths = [route[0]]
                self._target = route[1]
                self._starting_point = route[0]

                print("starting: self._paths: %s" % repr(self._paths))
                print("target: %s" % repr(self._target))
                input("continue...")

            minute += 1
            self.move_blizzard()
            self.build_map()
            print("minute: %d -------------------" % minute)

            self._paths_new = []

            done = False
            for point in self._paths:
                try:
                    self.move(point)

                except ExceptionDone:
                    print("we are done!!!!!!!!")
                    done = True
                    break

            if done:
                print("done a route!!!!")
                self._target = None
                self._paths = 0
            else:
                self._paths = list(set(self._paths_new))

                self.print_map()
                print("paths: %d" % len(self._paths))
                # input("continue...")

    def move(self, point):

        x = point[0]
        y = point[1]

        # if x == self._max_x and y == self._max_y:
        #     raise ExceptionDone("done!!")

        if x == self._target[0] and y == self._target[1]:
            raise ExceptionDone("done!!")

        # We can *always* be in the starting point
        self._paths_new.append((self._starting_point))

        if y == -1:
            # print("this is a special case")
            if self._map.get((x, y+1)) is None:
                # print("start: can move down")
                self._paths_new.append((x, y+1))
                # print("wait start")
            # We can wait here even if we want to move
            # self._paths_new.append((x,y))
            return

        if y == self._max_y + 1:
            # print("this is a special case")
            if self._map.get((x, y-1)) is None:
                # print("start: can move up")
                self._paths_new.append((x, y-1))
            else:
                # print("wait start")
                self._paths_new.append((x,y))
            return

        if y > 0:
            if self._map.get((x, y-1)) is None:
                # print("can move up")
                self._paths_new.append((x, y-1))

        if y < self._max_y:
            if self._map.get((x, y+1)) is None:
                # print("can move down")
                self._paths_new.append((x, y+1))

        if x > 0:
            if self._map.get((x-1, y)) is None:
                # print("can move left")
                self._paths_new.append((x-1, y))

        if x < self._max_x:
            if self._map.get((x+1, y)) is None:
                # print("can move right")
                self._paths_new.append((x+1, y))

        if self._map.get((x, y)) is None:
            self._paths_new.append((x, y))

    #
    # def make_move(self, move):
    #     if move == 'd':
    #         self._y += 1
    #     elif move == 'r':
    #         self._x += 1
    #     elif move == 'u':
    #         self._y -= 1
    #     elif move == 'l':
    #         self._x -= 1
    #     else:
    #         print("bad move")
    #
    #     if self._x == self._max_x and self._y == self._max_y:
    #         print("made it to the end!!!!")
    #
    # def get_moves(self):
    #
    #     moves = []
    #     if self._y == -1:
    #         print("this is a special case")
    #         if self._map.get((self._x, self._y + 1)) is None:
    #             print("can move down")
    #             moves.append('d')
    #         return moves
    #
    #     if self._y > 0:
    #         if self._map.get((self._x, self._y - 1)) is None:
    #             print("can move up")
    #             moves.append('u')
    #
    #     if self._y < self._max_y:
    #         if self._map.get((self._x, self._y + 1)) is None:
    #             print("can move down")
    #             moves.append('d')
    #
    #     if self._x > 0:
    #         if self._map.get((self._x - 1, self._y)) is None:
    #             print("can move left")
    #             moves.append('l')
    #
    #     if self._x < self._max_x:
    #         if self._map.get((self._x + 1, self._y)) is None:
    #             print("can move right")
    #             moves.append('r')
    #
    #     if len(moves) == 0:
    #         print("must wait; nowhere to go")
    #         if self._map.get((self._x, self._y)) is not None:
    #             raise  ValueError("this path is a dead end!!!")
    #
    #
    #     return moves

    def move_blizzard(self):

        for b in self._blizzard_list:
            b.move()

    def build_map(self):
        self._map.clear()
        for b in self._blizzard_list:
            x, y, d = b.get_position()

            count = self._map.get((x, y))
            if count is None:
                count = d
            else:
                try:
                    int(count)
                    count += 1
                except:
                    count = 2

            if count not in ['^', '<', 'v', '>', 2,3,4]:
                raise ValueError("bad count")

            self._map[(x, y)] = count

    def print_map(self):

        for y in range(self._max_y + 1):
            s = ''
            for x in range(self._max_x + 1):

                if (x, y) in self._paths:
                    s += "E"
                else:
                    count = self._map.get((x, y))
                    # print("got: %s" % repr(count))
                    if count is None:
                        s += '.'
                    else:
                        try:
                            s += '%d' % int(count)
                        except:
                            s += count
            print(s)

if __name__ == '__main__':
    runner = Runner()
    runner.run()
