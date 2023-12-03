



class Runner(object):

    def __init__(self):
        print("running")
        self._file_name = 'input_real.txt'
        # self._file_name = 'input_test.txt'
        # self._file_name = 'input_test_2.txt'

        self._part1_answer = 0
        self._part2_answer = None

        self._head_x = 0
        self._head_y = 0

        self._tail_x = 0
        self._tail_y = 0

        self._tail_positions = {}

        self.tail_visit()

    def tail_visit(self):
        key=(self._tail_x, self._tail_y)
        visits = self._tail_positions.get(key, 0) + 1
        self._tail_positions[key] = visits

        print("TAIL AT: X: %d Y: %d" % (self._tail_x, self._tail_y))

    def run(self):

        fp = open(self._file_name, 'r')
        for line in fp:
            self.process_line(line.strip())
        fp.close()

        print(self._tail_positions)
        print(len(self._tail_positions))

        self.print_map()
    #
    def print_map(self):

        min_x = max_x = min_y = max_y = 0
        for key, value in self._tail_positions.items():
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
                c = self._tail_positions.get(key, 0)
                if c == 0:
                    s = s +'.'
                else:
                    # s = s + "%d" % c
                    s += '*'
                x += 1
                if x > max_x: break

            print(s)
            y -= 1
            if y < min_y: break

    def process_line(self, line):
        # print(line)

        parts = line.split()
        # print(parts)
        direction = parts[0]
        steps = int(parts[1])

        print("direction: %s steps: %d" % (direction, steps))
        for _ in range(steps):
            if direction == 'L':
                self._head_x -= 1

            elif direction == 'R':
                self._head_x += 1

            elif direction == 'U':
                self._head_y += 1

            elif direction == 'D':
                self._head_y -= 1
            else:
                raise ValueError("bad dir")

            self.head_moved()

    def head_moved(self):
        print("HEAD: X: %4d Y: %4d" % (self._head_x, self._head_y))
        self.move_tail()

    def move_tail(self):

        diff = self._head_y - self._tail_y
        if abs(diff) > 1:

            if abs(diff) > 2:
                raise ValueError('unexpected diff %d')

            if diff > 0:
                self._tail_y += 1
            else:
                self._tail_y -= 1
            self._tail_x = self._head_x
            self.tail_visit()
            return

        diff = self._head_x - self._tail_x
        if abs(diff) >1:

            if abs(diff) > 2:
                raise ValueError('unexpected diff %d')

            if diff > 0:
                self._tail_x += 1
            else:
                self._tail_x -= 1
            self._tail_y = self._head_y
            self.tail_visit()

if __name__ == '__main__':
    runner = Runner()
    runner.run()
