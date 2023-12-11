import sys
import itertools

FIVE        = 6
FOUR        = 5
FULL_HOUSE  = 4
THREE       = 3
TWO_PAIR    = 2
PAIR        = 1
HIGH_CARD   = 0

KIND = {
    FIVE        : "FIVE",
    FOUR        : "FOUR",
    FULL_HOUSE  : "FULL HOUSE",
    THREE       : "THREE",
    TWO_PAIR    : "TWO PAIR",
    PAIR        : "PAIR",
    HIGH_CARD   : "HIGH_CARD"
}

CARD_RANK = {
    'A' : 14,
    'K' : 13,
    'Q' : 12,
    'J' : 11,
    'T' : 10,
    '9' :  9,
    '8' :  8,
    '7' :  7,
    '6' :  6,
    '5' :  5,
    '4' :  4,
    '3' :  3,
    '2' :  2
}

class Hand(object):

    def __init__(self, line):

        parts = line.split()
        cards = parts[0]
        self._hand = cards
        self._bid = int(parts[1])

        # print("hand: '%s' bid: %d" % (cards, self._bid))

        self._card_map = {}
        self._card_list = []

        for c in cards:
            # print(c)
            self._card_map[c] = self._card_map.get(c, 0) + 1
            self._card_list.append(c)

        counts = [count for count in self._card_map.values()]
        counts.sort(reverse=True)

        # print(self._card_list)
        # print(counts)

        # Figure out the type
        if counts[0] == 5:
            self._kind = FIVE

        elif counts[0] == 4:
            self._kind = FOUR

        elif counts[0] == 3:
            if counts[1] == 2:
                self._kind = FULL_HOUSE
            else:
                self._kind = THREE

        elif counts[0] == 2:
            if counts[1] == 2:
                self._kind = TWO_PAIR
            else:
                self._kind = PAIR

        else:
            self._kind = HIGH_CARD

    def get_hand(self):
        return self._hand

    def get_bid(self):
        return self._bid

    def get_kind(self):
        return self._kind

    def get_kind_str(self):
        return KIND[self._kind]

    def get_card_list(self):
        return self._card_list

    def __lt__(self, other):
        # print("__lt__ called")
        # print(self._card_map)
        # print(self._card_list)

        other_kind = other.get_kind()

        if other_kind > self._kind:
            return True

        elif other_kind < self._kind:
            return False

        # These are the same kind so we need
        # to compare individual cards
        other_card_list = other.get_card_list()

        for i in range(5):
            if CARD_RANK[other_card_list[i]] > CARD_RANK[self._card_list[i]]:
                return True

            elif CARD_RANK[other_card_list[i]] < CARD_RANK[self._card_list[i]]:
                return False

            else:
                # Still tied; keep going
                pass

        raise ValueError("compare failed, what is wrong")

class Runner(object):

    def __init__(self, filename):

        lines = []
        self._hands = []
        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                line = line.strip('.')
                lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(lines))

        for line in lines:
            hand = Hand(line)
            self._hands.append(hand)


    def run1(self):
        print("run")

        result = 0
        # for hand in self._hands:
        #     print("bid: %d" % hand.get_bid())
        #     print("%s" % hand.get_hand())
        #    print("kind: %s" % hand.get_kind_str())

        self._hands.sort()
        # self._hands.reverse()

        for i, hand in enumerate(self._hands):
            print("hand", hand.get_hand(), "bid",
                  hand.get_bid(), "kind", hand.get_kind_str())

            rank = i + 1
            result = result + rank * hand.get_bid()

        print("part 1 result:", result)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run1()
