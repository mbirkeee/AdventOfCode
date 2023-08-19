import sys
import copy
import itertools
from collections import Counter
import numpy as np

HM = 10
HG = 20
LM = 30
LG = 40

CHIPS = {
    HM : HG,
    LM : LG,
}

RTGS = [
    HG,
    LG,
]


NEXT_FLOOR = {
    1 : [2],
    2: [1, 3],
    3: [2, 4],
    4: [3]
}

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self, filename):

        if filename.startswith('t'):
            print("test")
            self._state = {
                'd': 0,
                'f': 1,
                'l' : {
                    HM: 1,
                    LM: 1,
                    HG: 2,
                    LG :3,
                }
            }

        else:
            print("production")

        self._repeat_map = {}

    def repeat(self, state):
        """
        Have we already been to this state?
        """
        print("check repeat")
        location = state['l']
        key = ''
        for thing, floor in location.items():
            key += "%d%d" % (thing, floor)

        key  = int(key)

        print("key", key)
        if key in self._repeat_map:
            return True

        self._repeat_map[key] = True
        return False

    def valid(self, state):
        # Check for
        locations = state['l']
        for chip in CHIPS.keys():
            print("check chip %d" % chip)
            floor = locations[chip]
            print("chip %d is on floor: %d" % (chip, floor))
        return True

    def move(self, state):

        if self.repeat(state):
            print("repeat state, do not continue")
            return

        # First, test if state is valid
        if not self.valid(state):
            print("invalid state, do not continue")
            return


        current_floor = state['f']
        current_depth = state['d']

        print("move called, floor: %d depth: %d" % (current_floor, current_depth))
        input("continue...")

        next_depth = current_depth + 1
        next_floors = NEXT_FLOOR[current_floor]

        things_to_move = self.combinations(state)
        print("things to move", things_to_move)

        for floor in next_floors:
            for thing_list in things_to_move:
                state_copy = copy.deepcopy(state)
                state_copy['f'] = floor
                state_copy['d'] = next_depth
                locations = state_copy['l']
                for thing in thing_list:
                    locations[thing] = floor

                self.move(state_copy)

    def run(self):
        print("called")

        self.move(self._state)

    def combinations(self, state):

        things = []
        current_floor = state['f']
        locations = state['l']
        for thing, floor in locations.items():
            if floor == current_floor:
                things.append(thing)

        result = []
        for l in range(len(things)):
            i = itertools.combinations(things, l+1)
            for t in i:
                result.append(t)

        return result

    def combinations_test(self):
        x = [1,2,3]

        for l in range(len(x)):
            i = itertools.combinations(x, l+1)
            for t in i:
                print(t)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
    #runner.combinations_test()
