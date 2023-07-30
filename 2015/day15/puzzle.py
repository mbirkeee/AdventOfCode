import sys
import itertools
from collections import Counter

class Runner(object):

    def __init__(self, filename):

        self._lines = []
        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                line = line.strip('.')

                if len(line) == 0:
                    continue

                self._lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(self._lines))

        self._ingedients = {}
        self.initialize()


    def initialize(self):
        print("initialize")

        for ingredient, line in enumerate(self._lines):
            parts = line.split(' ')
            print(parts)
            print(len(parts))
            parts = [part.strip(',') for part in parts]

            if len(parts) != 11:
                raise ValueError("bad number of parts")

            name = parts[0]
            capacity = int(parts[2])
            durability = int(parts[4])
            flavor = int(parts[6])
            texture = int(parts[8])
            calories = int(parts[10])

            self._ingedients[ingredient] = {
                'n':name, 'd': durability, 'f':flavor, 't':texture, 'c':calories, 'p': capacity }


    def get_score(self, item):
        x = Counter(item)
        # print(x)
        score = 1
        calories = 0

        keys = ['d', 'f', 't', 'p']

        temp = {}
        for ingredient, meta in self._ingedients.items():
            volume = x.get(ingredient, 0)
            name = meta['n']
            # print(name, volume)
            for key in keys:
                worth = temp.get(key, 0)
                worth +=  (volume  * meta[key])
                temp[key] = worth

            calories += volume * meta['c']

        # print(calories)
        if calories != 500:
            return 0

        # print(temp)
        for key, worth in temp.items():
            if worth < 0:
                worth = 0
            score = score * worth

        return score


    def run(self):

        ingredient_count = range(len(self._ingedients))

        print("run")
        comb = itertools.combinations_with_replacement(ingredient_count, 100)

        max_score = 0
        for i, item in enumerate(comb):
            # print(item)

            score = self.get_score(item)
            if score > max_score:
                max_score = score
                print("new max_score", max_score)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


