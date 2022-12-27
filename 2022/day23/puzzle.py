import numpy as np

class Elf(object):

    def __init__(self, x, y, map, map_proposed):

        self._x = x
        self._y = y

        self._x_proposed = None
        self._y_proposed = None

        self._map = map
        self._map_proposed = map_proposed

        self.nw = None
        self.n  = None
        self.ne = None
        self.e  = None
        self.se = None
        self.s  = None
        self.sw = None
        self.w  = None

        self._func_list = [
            self.move_north,
            self.move_south,
            self.move_west,
            self.move_east
        ]

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def move_north(self):
        if self.nw is None and self.n is None and self.ne is None:
            self._x_proposed = self._x
            self._y_proposed = self._y-1
            return True
        return False

    def move_south(self):
        if self.sw is None and self.s is None and self.se is None:
            self._x_proposed = self._x
            self._y_proposed = self._y+1
            return True
        return False

    def move_west(self):
        if self.sw is None and self.w is None and self.nw is None:
            self._x_proposed = self._x-1
            self._y_proposed = self._y
            return True
        return False

    def move_east(self):
        if self.se is None and self.e is None and self.ne is None:
            self._x_proposed = self._x+1
            self._y_proposed = self._y
            return True
        return False

    def propose_move(self):

        self._x_proposed = None
        self._y_proposed = None

        self.nw = self._map.get(( self._x-1, self._y-1 ))
        self.n  = self._map.get(( self._x,   self._y-1 ))
        self.ne = self._map.get(( self._x+1, self._y-1 ))
        self.e  = self._map.get(( self._x+1, self._y   ))
        self.se = self._map.get(( self._x+1, self._y+1 ))
        self.s  = self._map.get(( self._x,   self._y+1 ))
        self.sw = self._map.get(( self._x-1, self._y+1 ))
        self.w  = self._map.get(( self._x-1, self._y   ))

        if self.nw is None and self.n is None \
            and self.ne is None and self.e is None \
            and self.se is None and self.s is None \
            and self.sw is None and self.w is None:
            return

        for func in self._func_list:
            if func():
                count = self._map_proposed.get((self._x_proposed, self._y_proposed), 0)
                self._map_proposed[(self._x_proposed, self._y_proposed)] = count + 1
                return

    def move(self):

        func = self._func_list.pop(0)
        self._func_list.append(func)

        if self._x_proposed is None and self._y_proposed is None:
            return False

        count = self._map_proposed[(self._x_proposed, self._y_proposed)]

        if count > 1:
            return False

        elif count == 1:
            self._x = self._x_proposed
            self._y = self._y_proposed
            return True

        else:
            raise ValueError("move error")

class Runner(object):

    def __init__(self):
        # self._file_name = 'input_test.txt'
        # self._file_name = 'input_test_1.txt'
        self._file_name = 'input_real.txt'

        self._elf_list = []

        self._min_x = None
        self._max_x = None
        self._min_y = None
        self._max_y = None

        self._map = {}
        self._map_proposed = {}

    def run(self):

        fp = open(self._file_name, 'r')
        lines = []
        for line in fp:
            lines.append(line.strip())

        fp.close()

        for y, line in enumerate(lines):

            for x, c in enumerate(line):
                if c == '#':
                    elf = Elf(x, y, self._map, self._map_proposed)
                    self._elf_list.append(elf)

        round = 0
        while True:
            self.build_map()
            self.propose_moves()
            move_count = self.move()
            # self.print_map()

            if move_count == 0:
                print("we are done")
                break

            round += 1
            print("round: %5d moved: %5d =========================" % (round, move_count))

            # if round == 10:
            #     print("finished 10 rounds")
            #     break

            # input("continue...")

        self.print_map()

    def propose_moves(self):
        self._map_proposed.clear()
        for elf in self._elf_list:
            elf.propose_move()

    def move(self):
        move_count = 0
        for elf in self._elf_list:
            if elf.move():
                move_count += 1

        return move_count

    def get_bounds(self):

        for elf in self._elf_list:
            x = elf.get_x()
            y = elf.get_y()

            if self._min_x is None or x < self._min_x:
                self._min_x = x

            if self._max_x is None or x > self._max_x:
                self._max_x = x

            if self._min_y is None or y < self._min_y:
                self._min_y = y

            if self._max_y is None or y > self._max_y:
                self._max_y = y

    def build_map(self):

        self._map.clear()
        for elf in self._elf_list:
            self._map[(elf.get_x(), elf.get_y())] = elf

    def print_map(self):

        empty_spaces = 0
        self.get_bounds()
        self.build_map()

        for y in range(self._min_y, self._max_y + 1):
            s = ''
            for x in range(self._min_x, self._max_x + 1):
                elf = self._map.get((x, y))
                if elf is None:
                    s += '.'
                    empty_spaces += 1
                else:
                    s += '#'
            print(s)

        print("Empty spaces: %d" % empty_spaces)

if __name__ == '__main__':
    runner = Runner()
    runner.run()
