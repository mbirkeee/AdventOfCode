import numpy as np
import math
import sys

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self):

        self._lines = []
        self._draw = []
        self._card_list = []

        for line in sys.stdin:
            self._lines.append(line.strip())

        # To add last card
        self._lines.append('')

        card = None
        card_row_index = 0

        for line in self._lines:
            # print(line)
            l = len(line)
            # print(l)
            if l > 50:
                self.get_draw(line)
                continue

            if l == 0:
                if card is not None:
                    self._card_list.append(card)

                print("new card")
                card = np.zeros((5,5))
                card_row_index = 0
                continue

            # Add this line to the card

            parts = line.split()
            # print(parts)

            if len(parts) != 5:
                raise ValueError("bad input")

            for i, part in enumerate(parts):
                # print("adding", i, part)
                card[card_row_index, i] = int(part)
            card_row_index += 1

    def print_cards(self):

        for card in self._card_list:
            print("====================================")
            shape = card.shape
            rows = shape[0]
            cols = shape[1]

            for row in range(rows):
                s = ''
                for col in range(cols):
                    s += "%5d" % card[row, col]
                print(s)

    def get_draw(self, line):
        print("draw line", line)
        parts = line.split(',')
        self._draw = [int(part.strip()) for part in parts]

    def run(self):
        print("run")
        # self.print_cards()

        for draw in self._draw:
            print("Draw: %d" % draw)
            self.dab(draw)
            # self.print_cards()

            loser_list = []

            for card in self._card_list:
                if self.is_winner(card):
                    print("card is a winner!!")
                    total = self.sum_unmarked(card)
                    print("total: %d draw: %d result: %d" % (total, draw, total * draw))

                else:
                    loser_list.append(card)

            self._card_list = loser_list

            if len(self._card_list) == 0:
                print("no cards left")
                break

    def is_winner(self, card):
        vector = np.sum(card, axis=0)
        for t in vector:
            if t > 5000:
                return True

        vector = np.sum(card, axis=1)
        for t in vector:
            if t > 5000:
                return True

    def sum_unmarked(self, card, ):

        total = 0
        shape = card.shape
        rows = shape[0]
        cols = shape[1]

        for row in range(rows):
            for col in range(cols):
                if card[row, col] < 1000:
                    total += card[row, col]

        return total

    def dab(self, draw):
        for card in self._card_list:
            shape = card.shape
            rows = shape[0]
            cols = shape[1]

            for row in range(rows):
                for col in range(cols):
                    if card[row, col] == draw:
                        card[row, col] += 1000

if __name__ == '__main__':
    runner = Runner()
    runner.run()
