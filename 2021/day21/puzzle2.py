"""

"""
import math
import sys
import itertools

class ExceptionDone(Exception):
    pass

class Player(object):

    def __init__(self, n, starting_pos):
        self._n = n
        self._pos = starting_pos


        self._probabilies = None

    def set_probabilies(self, probabilies):
        self._probabilies = probabilies

    def move(self, universes):

        for steps, probability in self._probabilies.items():
            print("STEPS: %s, PROB: %d" % (steps, probability))

        print("player %d move" % self._n)

class Runner(object):

    def __init__(self, filename):

        if filename == 'test':
            self._player_1 = Player(1, 4)
            self._player_2 = Player(2, 8)
        else:
            self._player_1 = Player(1, 10)
            self._player_2 = Player(2, 2)

        combinations = itertools.product([1,2,3], repeat=3)

        self._probabilies = {}

        combo_count = 0
        for combo in combinations:
            # print(combo)
            steps = sum(combo)
            combo_count += 1
            count = self._probabilies.get(steps, 0)
            count += 1
            self._probabilies[steps] = count

        self._universes = combo_count

        self._player_1.set_probabilies(self._probabilies)
        self._player_2.set_probabilies(self._probabilies)

        # print(self._probability)

    def run(self):
        print("run")

        roll = 1

        universes = self._universes

        while True:
            roll += 1

            u = math.pow(universes, roll)
            print("universes:", u)


            if roll % 2:
                player = self._player_1
            else:
                player = self._player_2

            player.move(u)

            if roll > 10:
                break

        print("done")

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
    # runner.run()

