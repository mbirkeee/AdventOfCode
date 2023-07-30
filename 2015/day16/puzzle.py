import sys
import itertools
from collections import Counter

class KEY(object):
    ELIMINATED = 'eliminated'

WANT = {
    'children'      : {'n': 3, 'op': '='},
    'cats'          : {'n': 7, 'op': '>'},
    'samoyeds'      : {'n': 2, 'op': '='},
    'pomeranians'   : {'n': 3, 'op': '<'},
    'akitas'        : {'n': 0, 'op': '='},
    'vizslas'       : {'n': 0, 'op': '='},
    'goldfish'      : {'n': 5, 'op': '<'},
    'trees'         : {'n': 3, 'op': '>'},
    'cars'          : {'n': 2, 'op': '='},
    'perfumes'      : {'n': 1, 'op': '='},
}

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
        self._map_sue = {}

        self.initialize()


    def initialize(self):

        print("initialize")

        for index, line in enumerate(self._lines):
            parts = line.split(' ')
            # print(len(parts))
            parts = [part.strip(',') for part in parts]
            parts = [part.strip(':') for part in parts]

            sue_number = int(parts[1])
            # Looks like all items have 8 parts
            if len(parts) != 8:
                raise ValueError("bad number of parts")

            sue = { KEY.ELIMINATED: False}

            for item in [(2,3),(4,5),(6,7)]:
                key = parts[item[0]]
                val = int(parts[item[1]])
                sue[key] = val
                # print(key, val)

            self._map_sue[sue_number] = sue
            # print(parts)

    def run(self):

        print("run")

        # Check children
        for sue, meta in self._map_sue.items():
            if meta[KEY.ELIMINATED] : continue

            for k, want_meta in WANT.items():
                want = want_meta['n']
                op = want_meta['op']
                have = meta.get(k)

                if have is not None:
                    if op == '=':
                        if have != want:
                            meta[KEY.ELIMINATED] = True
                            continue
                    elif op == '<':
                        if have >= want:
                            meta[KEY.ELIMINATED] = True
                            continue
                    elif op == '>':
                        if have <= want:
                            meta[KEY.ELIMINATED] = True
                            continue

        for sue, meta in self._map_sue.items():
            if meta[KEY.ELIMINATED] is not True:
                print("sue %d not eliminated" % sue)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


