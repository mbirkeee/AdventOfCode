import copy

class ExceptionDone(Exception):
    pass

AFTER_ROCKS = 1000000000000


ROCK_TYPES = [0,1,2,3,4]

WIDTH = 7

LEFT = '<'
RIGHT = '>'

class Point(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_y(self):
        return self._y

    def get_x(self):
        return self._x

    def is_at(self, x, y):
        # print(x, y, self._x, self._y)
        if self._x == x and self._y == y:
            return True
        return False

    def move_left(self, d=1):
        self._x -= d

    def move_right(self,d=1):
        self._x += d

    def move_up(self, d=1):
        self._y += d

    def move_down(self, d=1):
        self._y -= d

    def hit_left(self):
        if self._x < 0:
            return True
        return False

    def hit_right(self):
        if self._x >= WIDTH:
            return True
        return False

    def hit_bottom(self):
        if self._y < 0:
            return True
        return False

    def print_xy(self):
        print("X: %d Y: %d" % (self._x, self._y))

class Rock(object):

    def __init__(self, type, count):
        self._count = count
        self._type = type
        self._bottom = 0
        self._left = 0

        if type == 0:
            self._points = [Point(0,0), Point(1,0), Point(2,0), Point(3,0)]
            self._height = 1
            self._width = 4

        elif type == 1:
            self._points = [Point(1,0), Point(0, 1), Point(1,1), Point(2,1), Point(1,2)]
            self._height = 3
            self._width = 3

        elif type == 2:
            self._points = [Point(0,0), Point(1,0), Point(2,0), Point(2,1), Point(2, 2)]
            self._height = 3
            self._width = 3

        elif type == 3:
            self._points = [Point(0,0), Point(0,1), Point(0,2), Point(0,3)]
            self._height = 4
            self._width = 1

        elif type == 4:
            self._points = [Point(0,0), Point(0,1), Point(1,0), Point(1,1)]
            self._height = 2
            self._width = 2

        else:
            raise ValueError("bad rock")

        self._shape_points = copy.deepcopy(self._points)

    def get_type(self):
        return self._type

    def init_y(self, value):
        self.move_up(d=value)

    def init_x(self, value):
        self.move_right(d=value)

    def move_up(self,d=1):
        for point in self._points:
            point.move_up(d=d)

    def move_down(self,d=1):
        for point in self._points:
            point.move_down(d=d)

    def move_right(self,d=1):
        for point in self._points:
            point.move_right(d=d)

    def move_left(self,d=1):
        for point in self._points:
            point.move_left(d=d)

    def has_point(self, x, y):

        for point in self._points:
            if point.is_at(x, y):
                return True
        return False

    def has_shape_point(self, x, y):

        for point in self._shape_points:
            if point.is_at(x, y):
                return True
        return False

    def hit_left(self):
        for point in self._points:
            if point.hit_left():
                return True
        return False

    def hit_right(self):
        for point in self._points:
            if point.hit_right():
                return True
        return False

    def hit_bottom(self):
        for point in self._points:
            if point.hit_bottom():
                return True
        return False

    def get_top(self):
        max_top = 0
        for point in self._points:
            top = point.get_y()
            if top > max_top:
                max_top = top
        return max_top

    def print_points(self):
        for point in self._points:
            point.print_xy()

    def print_shape(self):

        for y in range(self._height-1, -1, -1):
            s = ''
            for x in range(self._width):
                if self.has_shape_point(x, y):
                    s += '*'
                else:
                    s += ' '
            print(s)

    def get_count(self):
        return self._count

    def hit_rock(self, rock):
        for point in self._points:
            if rock.has_point( point.get_x(), point.get_y() ):
                return True
        return False

class Runner(object):

    def __init__(self):
        # self._file_name = 'input_test.txt'
        # self._file_name = 'input_test2.txt'
        self._file_name = 'input_real.txt'

        self._rock_count = 0
        self._jet_index = 0
        self._rock_index = 0
        self._fallen_rocks = []
        self._jet = None
        self._first_repeat = None

        self._repeat = {}

    def run(self):

        fp = open(self._file_name, 'r')
        lines = []
        for line in fp:
            line = line.strip()
            lines.append(line)

        fp.close()

        if len(lines) != 1:
            raise ValueError("lines != 1")

        # Get the list of jet directions
        self._jet = [ c for c in lines[0]]
        # print(jet)

        # for rock_type in ROCK_TYPES:
        #     print("-------------------")
        #     rock = Rock(rock_type)
        #     rock.print_shape()
        #     print("-------------------")

        height = 0
        counter = 0
        rp = 0
        repeat_key = None
        last_height = 0

        while True:

            rock = self.get_next_rock()
            rock.init_x(2)
            rock.init_y(height + 3)

            # print("++++++++++++++++++++++++++++++++++++++++++++++++++")
            # rock.print_shape()

            jet_str = ''
            while True:

                jet = self.get_next_jet()
                jet_str += jet

                if jet == LEFT:
                    # print("try to move left")
                    rock.move_left()
                    if not self.good_spot(rock):
                        # print("cant move left, move back")
                        rock.move_right()

                elif jet == RIGHT:
                    # print("try to move right")
                    rock.move_right()
                    if not self.good_spot(rock):
                        # print("cant move right, move back")
                        rock.move_left()

                else:
                    raise ValueError('bad jet')

                # print("try to move down")
                rock.move_down()

                if not self.good_spot(rock):
                    rock.move_up()

                    if self._jet_index == 0:
                        print("Jet index == 0, rock_index: %d" % self._rock_index)

                    key = jet_str + "%d" % rock.get_type()

                    rp = self._repeat.get(key, 0)
                    rp += 1
                    self._repeat[key] = rp

                    # if key == '>><<0':
                    if key == '>><<>>><<<>>>><<<>4':
                    # if key == '<<><<<>>>><>><<<>><<><<<<><>>>><<<>>><3':
                    # if self._first_repeat is None and rp > 1:
                         # print("got first repeat at rock: %d" % rock.get_count())
                         self._first_repeat = rock.get_count()
                         repeat_key = key

                    new_height = rock.get_top() + 1
                    if new_height > height:
                        height = new_height

                    if repeat_key and repeat_key == key:
                        height_diff = height - last_height
                        last_height = height
                        print("repeat at rock: %d height: %d h_diff: %d" % (rock.get_count(), height, height_diff))

                    rock_count = rock.get_count()
                    type = rock.get_type()
                    # rock.print_points()
                    print("rock %d (%d) stopped; jets: %s (%d) total height: %d" % (rock_count, type, jet_str, self._jet_index, height))
                    self._fallen_rocks.append(rock)
                    if len(self._fallen_rocks) > 500:
                        self._fallen_rocks.pop(0)
                    break

            # counter += 1
            # if counter >= 1000:
            #     singles = 0
            #     for k, v in self._repeat.items():
            #         print("key: %s times: %d" % (k, v))
            #         if v == 1:
            #             singles +=1
            #
            #     counter = 0
            #     print("------ size of repeat dict: %d (singles: %d)" % (len(self._repeat), singles))

            # self.print_tower(height+5)
            if rock.get_count() == 3325:
                break

        print("height: %d" % height)
        # rock.print_shape()
        print("len(jet): %d" % len(self._jet))

        # self.print_tower(height + 5)

    def print_tower(self, height):

        for y in range(height, -1, -1):
            s = ""
            for x in range(WIDTH):
                if self.rock_at(x, y):
                    s += '#'
                else:
                    s += '.'
            l = "%4d  %s" % (y, s)
            print(l)
        print("--------------")

    def rock_at(self, x, y):
        for rock in self._fallen_rocks:
            if rock.has_point(x, y):
                return True
        return False

    def good_spot(self, rock):

        if rock.hit_bottom():
            # print("hit bottom")
            return False

        if rock.hit_right():
            # print("hit right")
            return False

        if rock.hit_left():
            # print("hit left")
            return False

        # print("check if this hit another rock")
        for fallen_rock in self._fallen_rocks:
            if fallen_rock.hit_rock(rock):
                return False

        return True

    def get_next_rock(self):
        self._rock_count += 1
        rock = Rock(self._rock_index, self._rock_count)
        self._rock_index += 1
        if self._rock_index == len(ROCK_TYPES):
            self._rock_index = 0
        return rock

    def get_next_jet(self):
        jet = self._jet[self._jet_index]
        self._jet_index += 1
        if self._jet_index == len(self._jet):
            self._jet_index = 0
        return jet

def test_1():

    first_rock = 35
    repeat_blocks = 35
    repeat_height = 53

    # subtract 1 from the repeat rock
    r = AFTER_ROCKS - first_rock

    repeat_count = int(r / repeat_blocks)
    print("repeat_count: %d" % repeat_count)

    left_over = r - (repeat_count * repeat_blocks)
    print("left_over: %d" % left_over)

    height = repeat_count * repeat_height

    get_height = first_rock + repeat_blocks + left_over
    print("get_height: %d" % get_height)
    # height at 103 (35 + 53 + 30) =

    height = height + 131 - repeat_height

    print(height)

def test_2():

    first_rock = 1429
    repeat_blocks = 1725
    repeat_height = 2728

    # subtract 1 from the repeat rock
    r = AFTER_ROCKS - first_rock

    repeat_count = int(r / repeat_blocks)
    print("repeat_count: %d" % repeat_count)

    left_over = r - (repeat_count * repeat_blocks)
    print("left_over: %d" % left_over)

    height = repeat_count * repeat_height

    get_height = first_rock + repeat_blocks + left_over
    print("get_height: %d" % get_height)
    # height at 103 (35 + 53 + 30) =

    height = height + 5215 - repeat_height

    print(height)
    # Not correct   1581449275320
    # is too low    1581449274354
    # is too low    1581449274350
    # is to low     1581449273727
if __name__ == '__main__':
    runner = Runner()
    # test_1()
    test_2()
    # runner.run()
