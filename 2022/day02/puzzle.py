class Runner(object):

    def __init__(self):
        print("running")


        self._count_draw = 0
        self._count_me = 0
        self._count_them = 0

        self._expect_win = 0
        self._expect_lose = 0
        self._expect_draw = 0

        self._total_points = 0

    def run(self):

        fp = open('input.txt', 'r')


        for line in fp:
            line = line.strip()
            # print(line)

            parts = line.split(' ')
            # print(parts)

            them = MAP[parts[0]]
            outcome = OUTCOME[parts[1]]

            me = self.choose(them, outcome)

            points = self.game(them, me)

            self._total_points += points

        fp.close()

        print('win: %d (%d)' %  (self._count_me, self._expect_win))
        print('lose: %d (%d)' % (self._count_them, self._expect_lose))
        print('draw: %d (%d)' % (self._count_draw, self._expect_draw))

        print("TOTAL POINTS: %d" % self._total_points)


    def choose(self, them, outcome):
        if outcome == DRAW:
            self._expect_draw += 1
            return them

        elif outcome == LOSE:
            self._expect_lose += 1
            if them == ROCK:
                return SCISSORS

            elif them == PAPER:
                return ROCK

            elif them == SCISSORS:
                return PAPER

        elif outcome == WIN:
            self._expect_win += 1
            if them == ROCK:
                return PAPER

            elif them == PAPER:
                return SCISSORS

            elif them == SCISSORS:
                return ROCK

        raise ValueError("error!!!")

    def game(self, them, me):

        winner = None

        if them == me:
            winner = 'draw'
        else:

            if them == ROCK:
                if me == PAPER:
                    winner = 'me'
                else:
                    winner = 'them'
            elif them == PAPER:
                if me == SCISSORS:
                    winner = 'me'
                else:
                    winner = 'them'

            elif them == SCISSORS:
                if me == ROCK:
                    winner = 'me'
                else:
                    winner = 'them'

        if winner is None:
            raise ValueError("NO WINNER")

        points = me

        if winner == 'me':
            self._count_me += 1
            points += 6

        elif winner == 'them':
            self._count_them += 1

        elif winner == 'draw':
            self._count_draw += 1
            points += 3

        else:
            raise ValueError("error here")

        print('them: %d me: %d WINNER: %s (points: %d)' % (them, me, winner, points))

        return points

if __name__ == '__main__':
    runner = Runner()
    runner.run()
