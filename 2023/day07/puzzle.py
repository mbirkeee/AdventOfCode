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
        self._bid = int(parts[1])

        # print("hand: '%s' bid: %d" % (cards, self._bid))

        self._card_map = {}
        self._card_list = []
        self._card_list_old = []

        self._use_old_flag = False
        for c in cards:
            self._card_list.append(c)
            self._card_list_old.append(c)

        self.compute_rank()

    def compute_rank(self):

        self._card_map = {}
        for c in self._card_list:
            self._card_map[c] = self._card_map.get(c, 0) + 1

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

    def get_max_non_joker(self):
        max_rank = -1
        max_c = ''

        for c in self._card_list:
            if c == 'J': continue

            if CARD_RANK[c] > max_rank:
                max_rank = CARD_RANK[c]
                max_c = c
        return max_c

    def get_non_joker_multi(self, want_count):

        map = {}
        for c in self._card_list:
            if c == 'J':
                continue

            map[c] = map.get(c, 0) + 1

        for k, v in map.items():
            if v == want_count:
                return k

        raise ValueError("badness")

    def replace_joker(self, new_c):

        for i, c in enumerate(self._card_list):
            if c == 'J':
                self._card_list[i] = new_c

    def process_jokers(self):

        joker_count = self.get_joker_count()

        if joker_count == 0:
            return

        self._use_old_flag = True
        old_hand = self.get_hand_str()

        if joker_count == 5:
            # 5 jokers is a very special case... make highest possible hand
            self.replace_joker('A')

        elif joker_count == 4:
            # Make this hand into a 5 of a kind
            m = self.get_max_non_joker()
            self.replace_joker(m)

        elif joker_count == 3:
            # Make this hand into a 4 of a kind with value
            # of the highest non-joker hand
            m = self.get_max_non_joker()
            self.replace_joker(m)

        elif joker_count == 2:
            # if this is a full house make into 5
            # if this is 2 pair make into 4
            # if this is 1 pair the pair must be the jokers
            if self._kind == FULL_HOUSE:
                # The jokers must be the pair
                m = self.get_max_non_joker()

            elif self._kind == TWO_PAIR:
                m = self.get_non_joker_multi(2)

            elif self._kind == PAIR:
                # The joker must be the pair
                m = self.get_max_non_joker()

            else:
                raise ValueError("should not happen")

            self.replace_joker(m)

        elif joker_count == 1:
            if self._kind == FOUR:
                # Make into a 5 of a kind
                m = self.get_max_non_joker()

            elif self._kind == THREE:
                m = self.get_non_joker_multi(3)

            elif self._kind == TWO_PAIR:
                m = self.get_max_non_joker()

            elif self._kind == PAIR:
                m = self.get_non_joker_multi(2)

            else:
                m = self.get_max_non_joker()

            self.replace_joker(m)

        new_hand = self.get_hand_str()
        print("%d JOKERS:  %s --> %s" % (joker_count, old_hand, new_hand))
        self.compute_rank()

    def get_hand_str(self):

        return ''.join(self._card_list)

    def get_bid(self):
        return self._bid

    def get_kind(self):
        return self._kind

    def get_kind_str(self):
        return KIND[self._kind]

    def get_card_list(self):
        if self._use_old_flag:
            return self._card_list_old

        return self._card_list

    def get_joker_count(self):

        joker_count = 0
        for c in self._card_list:
            if c == 'J':
                joker_count += 1

        return joker_count

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
        my_card_list = self.get_card_list()

        for i in range(5):
            if CARD_RANK[other_card_list[i]] > CARD_RANK[my_card_list[i]]:
                return True

            elif CARD_RANK[other_card_list[i]] < CARD_RANK[my_card_list[i]]:
                return False

            else:
                # Still tied; keep going
                pass

        return False
        # raise ValueError("compare failed, what is wrong")

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
        self._hands.sort()

        for i, hand in enumerate(self._hands):
            print("hand", hand.get_hand_str(), "bid",
                  hand.get_bid(), "kind", hand.get_kind_str())

            rank = i + 1
            result = result + rank * hand.get_bid()

        print("result:", result)

    def run2(self):
        """
        246222607 is too low
        246307620 still too low
        """

        CARD_RANK['J'] = 1
        for hand in self._hands:
            hand.process_jokers()

        self.run1()

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    #runner.run1()
    runner.run2()
