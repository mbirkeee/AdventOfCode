import queue
import itertools

import math

p1_wins = 0
p2_wins = 0

class Node(object):

    def __init__(self, p1_pos, p2_pos, p1_score, p2_score, universes, check, queue, steps, multiplier):


        self._p1_pos = p1_pos
        self._p2_pos = p2_pos

        self._p1_score = p1_score
        self._p2_score = p2_score

        self._universes = universes
        self._multiplier = multiplier
        self._steps = steps
        self._queue = queue

        self._check = check

    def process(self):

        # print("process called!")

        global p1_wins
        global p2_wins


        if self._steps is None or self._multiplier is None:
            pass

        else:

            self._universes = self._universes *self._multiplier

            if self._check == 1:
                self._p1_pos += self._steps
                if self._p1_pos > 10:
                    self._p1_pos -= 10

                self._p1_score += self._p1_pos

                if self._p1_score >= 21:
                    print("P1 wins! universes: %d" % self._universes)
                    p1_wins += self._universes
                    return
                self._check = 2

            else:
            # self._universes = self._universes * self._multiplier

                self._p2_pos += self._steps
                if self._p2_pos > 10:
                    self._p2_pos -= 10

                self._p2_score += self._p2_pos

                if self._p2_score >= 21:
                    print("P2 wins! universes: %d" % self._universes)
                    p2_wins += self._universes

                    return
                self._check = 1

        # print("check", self._check)

        node = Node(self._p1_pos, self._p2_pos, self._p1_score, self._p2_score, self._universes, self._check, self._queue, 3, 1)
        self._queue.put(node)

        node = Node(self._p1_pos, self._p2_pos, self._p1_score, self._p2_score, self._universes, self._check, self._queue, 4, 3)
        self._queue.put(node)

        node = Node(self._p1_pos, self._p2_pos, self._p1_score, self._p2_score, self._universes, self._check, self._queue, 5, 6)
        self._queue.put(node)

        node = Node(self._p1_pos, self._p2_pos, self._p1_score, self._p2_score, self._universes, self._check, self._queue, 6, 7)
        self._queue.put(node)

        node = Node(self._p1_pos, self._p2_pos, self._p1_score, self._p2_score, self._universes, self._check, self._queue, 7, 6)
        self._queue.put(node)

        node = Node(self._p1_pos, self._p2_pos, self._p1_score, self._p2_score, self._universes, self._check, self._queue, 8, 3)
        self._queue.put(node)

        node = Node(self._p1_pos, self._p2_pos, self._p1_score, self._p2_score, self._universes, self._check, self._queue, 9, 1)
        self._queue.put(node)

class Runner(object):


    def __init__(self):


        outcomes = [1,2,3]
        rolls = itertools.product(outcomes,repeat=3)

        steps = {}

        splits = 0
        for roll in rolls:
            # print(roll)
            splits += 1
            s = sum(roll)
            # print(s)

            steps[s] = steps.get(s, 0) + 1

        # print(steps)
        self._splits = splits

        self._queue = queue.Queue()



    def run(self):


        global p1_wins
        global p2_wins


        node = Node(10, 2, 0, 0, 1, 1, self._queue, None, None)


        self._queue.put(node)

        while True:

            try:
                node = self._queue.get(block=False)
                node.process()

            except queue.Empty:

                print("done!!!")
                break

        print(p1_wins)
        print(p2_wins)

if __name__ == '__main__':

    runner = Runner()
    runner.run()
