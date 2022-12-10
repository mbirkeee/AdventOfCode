

class Knot(object):

    def __init__(self, name):

        self._name = name
        self._x = 0
        self._y = 0

        self._visits = {(0,0):1}

    def name(self):
        return self._name

    def get_pos(self):
        return self._x, self._y

    def follow(self, leader):

        l_x, l_y = leader.get_pos()

        diff_y = l_y - self._y
        diff_x = l_x - self._x

        if diff_x == 0 and diff_y == 0:
            return

        if abs(diff_x) > 1 and abs(diff_y) > 1:
            print("knot: %s -> BIG JUMP X: %d  Y: %d!!!" % (self._name, abs(diff_x), abs(diff_y)))
            # Must move diagonally
            if diff_x > 0:
                self._x += 1
            else:
                self._x -= 1

            if diff_y > 0:
                self._y += 1
            else:
                self._y -= 1
            self.visit()

        elif abs(diff_y) > 1:

            if abs(diff_y) > 2:
                raise ValueError('A: knot: %s unexpected diff X: %d Y: %d' % (self._name, diff_x, diff_y))

            # steps = abs(diff_y) - 1
            if diff_y > 0:
                self._y += 1
            else:
                self._y -= 1
            self._x = l_x
            self.visit()

        elif abs(diff_x) > 1:

            if abs(diff_x) > 2:
                raise ValueError('B: knot: %s unexpected diff X: %d Y: %d' % (self._name, diff_x, diff_y))

            if diff_x > 0:
                self._x += 1
            else:
                self._x -= 1
            self._y = l_y
            self.visit()

        # else:
        #     raise ValueError('C: knot: %s unexpected diff X: %d Y: %d' % (self._name, diff_x, diff_y))


    def move(self, direction):

        if direction == 'L':
            self._x -= 1

        elif direction == 'R':
            self._x += 1

        elif direction == 'U':
            self._y += 1

        elif direction == 'D':
            self._y-= 1

        self.visit()

    def visit(self):
        key=(self._x, self._y)
        visits = self._visits.get(key, 0) + 1
        self._visits[key] = visits

    def print_location_count(self):
        print("Knot: %s: locations: %d" % (self._name, len(self._visits)))

    def print_map(self):

        min_x = max_x = min_y = max_y = 0
        for key, value in self._visits.items():
            x = key[0]
            y = key[1]
            if x < min_x: min_x = x
            if x > max_x: max_x = x
            if y < min_y: min_y = y
            if y > max_y: max_y = y

        y = max_y

        while True:
            x = min_x
            s = ''

            while True:

                key = (x, y)
                c = self._visits.get(key, 0)
                if c == 0:
                    s = s +'.'
                else:
                    s += '*'
                x += 1
                if x > max_x: break

            print(s)
            y -= 1
            if y < min_y: break


class Runner(object):

    def __init__(self):
        self._file_name = 'input_real.txt'
        # self._file_name = 'input_test.txt'
        # self._file_name = 'input_test_2.txt'

        knot_list = ['H','1','2','3','4','5','6','7','8','9']

        # knot_list = ['H','1']
        self._knots = []
        for name in knot_list:
            self._knots.append(Knot(name))

    def run(self):

        fp = open(self._file_name, 'r')
        line_count = 0
        for line in fp:
            self.process_line(line.strip())
            line_count += 1
            # if line_count == 2:
            #     break
        fp.close()

#         head = self._knots[0]
#         head.print_map()
#         head.print_location_count()

        tail = self._knots[-1]
        tail.print_map()
        tail.print_location_count()

        # for knot in self._knots:
        #     x, y = knot.get_pos()
        #     name = knot.name()
        #     print("knot: %s pos: X: %d Y: %d" % (name, x, y))

    def process_line(self, line):
        # print(line)
        parts = line.split()
        direction = parts[0]
        steps = int(parts[1])

        for _ in range(steps):
            head = self._knots[0]
            head.move(direction)

            for i in range(len(self._knots) - 1):
                leader = self._knots[i]
                follower = self._knots[i+1]
                follower.follow(leader)

            # self.print_test()

    def get_knot(self, x, y):
        c = '.'

        for knot in self._knots:
            kx, ky = knot.get_pos()
            if kx == x and ky == y:
                c = knot.name()
                break

        return c

    def print_test(self):

        print("######################################################")
        y = 8

        while True:

            x = 0

            s = ''
            while True:

                letter = self.get_knot(x, y)
                s += letter

                x += 1
                if x > 8:
                    break
            print(s)
            y -= 1
            if y < 0:
                break


if __name__ == '__main__':
    runner = Runner()
    runner.run()
