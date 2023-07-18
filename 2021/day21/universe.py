
import itertools

class Player(object):

    def __init__(self, number, position, steps):

        self._n = number
        self._steps = steps

        # We are at the starting position with score 0
        key = self.key(position, 0)

        # At there starting position there ois just one universe
        self._status = { key: 1 }


    def key(self, pos, score):

        return "%d:%d" %(pos, score)

    def pos(self, key):
        parts = key.split(':')
        return int(parts[0])

    def score(self, key):
        parts = key.split(':')
        return int(parts[1])

    def split(self, split_count):

        for key, universes in self._status.items():
            self._status[key] = universes * split_count

    def print_status(self):
        for key, universes in self._status.items():

            pos = self.pos(key)
            score = self.score(key)

            print("player %d: pos: %s score: %d universes: %d" % (self._n, pos, score, universes))

    def play(self):

        print("player %d play ------------ " % self._n)

        new_status = {}

        for key, universes in self._status.items():

            pos = self.pos(key)
            score = self.score(key)

            print("player %d: pos: %s score: %d universes: %d" % (self._n, pos, score, universes))

            for steps, multiplier in self._steps.items():
                print("steps: %d times: %d" % (steps, multiplier))

                new_universes = universes * multiplier
                new_pos = pos + steps
                if new_pos > 10:
                    new_pos -= 10

                new_score = score + new_pos
                new_key = self.key(new_pos, new_score)

                new_status[new_key] = new_status.get(new_key, 0) + new_universes

        self._status = new_status
        self.print_status()



class Runner(object):


    def __init__(self):


        outcomes = [1,2,3]
        rolls = itertools.product(outcomes,repeat=3)

        steps = {}

        splits = 0
        for roll in rolls:
            print(roll)
            splits += 1
            s = sum(roll)
            print(s)

            steps[s] = steps.get(s, 0) + 1

        print(steps)

        self._splits = splits

        self._player1 = Player(1, 4, steps)
        self._player2 = Player(2, 10, steps)


    def run(self):

        roll = 0

        while True:

            roll += 1

            if roll % 2:
                player = self._player1
                other_player = self._player2

            else:
                player = self._player2
                other_player = self._player1

            player.play()

            # The other player will see its universes go up by a factor of 27
            # other_player.split(self._splits)

            input("continue....")
            if roll > 10:
                break



if __name__ == '__main__':

    runner = Runner()
    runner.run()
