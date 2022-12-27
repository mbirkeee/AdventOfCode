import numpy as np

class Deck(object):

    def __init__(self, length):
        self._array = np.arange(length)

    def print(self):
        print(self._array)

    def deal_in(self):
        self._array = np.flip(self._array)

    def cut(self, x):
        if x > 0:
            x = x
        else:
            x = len(self._array) - abs(x)

        c = np.copy(self._array)

        c[-x:] = self._array[:x]
        c[:-x] = self._array[x:]

        self._array = c

    def deal_x(self, x):

        l = len(self._array)

        c = np.copy(self._array)

        put = 0
        for i in range(l):

            c[put] = self._array[i]
            put += x
            if put >= l:
                put -= l

        self._array = c

    def get_card(self, x):
        return self._array[x]

    def find_card(self, x):

        for i in range(len(self._array)):
            if self._array[i] == x:
                return i

        raise ValueError("card not found")

class Runner(object):

    def __init__(self):
        self._file_name = 'input_real.txt'
        self._deck = Deck(10007)

    def run(self):

        lines = []
        fp = open(self._file_name, 'r')

        for line in fp:
            lines.append(line.strip())
        fp.close()

        loop_count = 0
        first_found = None
        while True:

            for line in lines:
                self.process_line(line)

            # p = self._deck.find_card(2019)

            card = self._deck.get_card(4096)
            print("card at 4096: %d" % card)
            # if first_found is None:
            #     print("2019 in position %d" % p)
            #     first_found = p
            #
            # elif p == first_found:
            #     print("loop: %d card %d is at position: %d" % (loop_count, 2019, p))

            loop_count += 1

    def process_line(self, line):
        # print(line)

        if line.startswith('deal into new'):
            self._deck.deal_in()

        elif line.startswith('cut '):
            parts = line.split()
            x = int(parts[1].strip())
            self._deck.cut(x)

        elif line.startswith('deal with inc'):
            parts = line.split()
            x = int(parts[3])
            self._deck.deal_x(x)

        else:
            raise ValueError('bad deal')

    def test_deal_in(self):
        x = Deck(10)
        x.deal_in()
        x.print()

    def test_cut(self):
        x = Deck(10)
        x.cut(3)
        x.print()

        x = Deck(10)
        x.cut(-4)
        x.print()

    def test_deal_x(self):
        x = Deck(10)
        x.deal_x(3)
        x.print()

    def test1(self):
        x = Deck(10)
        x.deal_x(7)
        x.deal_in()
        x.deal_in()
        x.print()

    def test2(self):
        x = Deck(10)
        x.cut(6)
        x.deal_x(7)
        x.deal_in()
        x.print()

    def test3(self):
        x = Deck(10)
        x.deal_x(7)
        x.deal_x(9)
        x.cut(-2)
        x.print()

    def test4(self):
        x = Deck(10)
        x.deal_in()
        x.cut(-2)
        x.deal_x(7)
        x.cut(8)
        x.cut(-4)
        x.deal_x(7)
        x.cut(3)
        x.deal_x(9)
        x.deal_x(3)
        x.cut(-1)
        x.print()

if __name__ == '__main__':
    runner = Runner()
    # runner.test_deal_in()
    # runner.test_cut()
    # runner.test_deal_x()
    # runner.test1()
    # runner.test3()
    # runner.test4()
    runner.run()
