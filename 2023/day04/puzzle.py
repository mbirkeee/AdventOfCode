import sys
import math

class ExceptionDone(Exception):
    pass


class Card(object):
    def __init__(self, line):
        # print("card line: %s" % line)
        line = line.strip()
        parts = line.split(':')
        name = parts[0]
        # print("Name: %s" % name)

        parts = parts[1].split('|')
        # print(parts[0])

        self._numbers_win = [int(part.strip()) for part in parts[0].split()]
        self._numbers_have =  [int(part.strip()) for part in parts[1].split()]
        # print("winners", self._numbers_win)
        # print("have", self._numbers_have)

    def get_match_count(self):

        match_count = 0
        for number in self._numbers_have:
            if number in self._numbers_win:
                match_count += 1

        return match_count

class Runner(object):

    def __init__(self, filename):

        lines = []
        self._cards = []

        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()

                if len(line) == 0:
                    continue

                lines.append(line)

        finally:
            if fp: fp.close()

        for line in lines:
            card = Card(line)
            self._cards.append(card)

    def run1(self):
        print("run")

        total_score = 0

        for card in self._cards:
            match_count = card.get_match_count()
            # print(match_count)

            if match_count == 0:
                score = 0
            elif match_count == 1:
                score = 1
            else:
                score = int(math.pow(2, (match_count-1)))

            print("score: %s" % score)
            total_score += score

        print("part 1: total score: %d" % total_score)

    def run2(self):

        map_win_count = {}
        map_have = {}
        kind_count = 0

        processed_count = 0

        # Initialize the maps
        for i, card in enumerate(self._cards):
            match_count = card.get_match_count()
            map_win_count[i]= match_count
            map_have[i] = 1
            kind_count += 1

        max_kind = i
        run_flag = True

        # Run until done
        while True:

            match_flag = False
            for i in range(kind_count):
                have = map_have[i]
                if have == 0:
                    continue

                processed_count += 1
                match_flag = True
                match_count = map_win_count[i]
                print("have a card of type %d; it matches %d" % (i, match_count))

                # Remove processed card from those we have
                map_have[i] = map_have[i] - 1

                # Add cards that we won
                for j in range(match_count):
                    add_kind = i + j + 1
                    if add_kind > max_kind:
                        break

                    print("add card of type %d" % add_kind)
                    map_have[add_kind] = map_have[add_kind] + 1

                if match_flag:
                    break

            if not match_flag:
                break

        print("part 2 done; processed:", processed_count)


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    # runner.run1()
    runner.run2()
