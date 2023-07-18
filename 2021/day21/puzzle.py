"""

"""

import sys

class ExceptionDone(Exception):
    pass

class Player(object):

    def __init__(self, n, starting_pos):
        self._n = n
        self._pos = starting_pos
        self._score = 0

    def move(self, rolls):

        steps = rolls[0] + rolls[1] + rolls[2]
        # print("move %d steps" % steps)

        self._pos = self._pos + steps
        self._pos = self._pos % 10

        if self._pos == 0:
            self._pos = 10

        self._score += self._pos

        print("player %d: move: %d pos: %d scrore %d" % (self._n, steps, self._pos, self._score))


        if self._score >= 1000:
            raise ExceptionDone

    def get_score(self):
        return self._score

class Runner(object):

    def __init__(self, filename):

        if filename == 'test':
            self._player_1 = Player(1, 4)
            self._player_2 = Player(2, 8)
        else:
            self._player_1 = Player(1, 10)
            self._player_2 = Player(2, 2)

        self._dice = 0
        self._roll_count = 0

    def roll(self, count):

        self._roll_count += count

        result = []

        for i in range(count):

            self._dice += 1
            if self._dice > 100:
                self._dice = 1

            result.append(self._dice)

        return result


    def run(self):
        print("run")

        try:
            while True:

                rolls = self.roll(3)
                self._player_1.move(rolls)

                rolls = self.roll(3)
                self._player_2.move(rolls)
        except ExceptionDone:
            print("done")
            print(self._roll_count)

        score1 = self._player_1.get_score()
        score2 = self._player_2.get_score()

        if score1 < score2:
            lowest = score1
        else:
            lowest = score2

        print(lowest*self._roll_count)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()

