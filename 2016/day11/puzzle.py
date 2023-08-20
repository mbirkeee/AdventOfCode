import sys
import copy
import itertools
from collections import Counter
import numpy as np

M1 = 10
G1 = 20
M2 = 30
G2 = 40
M3 = 50
G3 = 60
M4 = 70
G4 = 80
M5 = 90
G5 = 100

M6 = 110
G6 = 120

M7 = 130
G7 = 140

CHIPS = {
    M1 : G1,
    M2 : G2,
    M3 : G3,
    M4 : G4,
    M5 : G5,
    M6 : G6,
    M7 : G7
}

FRY = {
    M1 : [G2, G3, G4, G5, G6, G7],
    M2 : [G1, G3, G4, G5, G6, G7],
    M3 : [G1, G3, G4, G5, G6, G7],
    M4 : [G1, G2, G3, G5, G6, G7],
    M5 : [G1, G2, G3, G4, G6, G7],
    M6 : [G1, G2, G3, G4, G5, G7],
    M7 : [G1, G2, G3, G4, G5, G6],
}


NEXT_FLOOR = {
    1 : [2],
    2: [1, 3],
    3: [2, 4],
    4: [3]
}

# INVALID_PAIRS = [
#     (10, 40),
#     (20, 30)
# ]

NAME = {
    G1: "HG ",
    M1: "HM ",
    G2: "LG ",
    M2: "LM "
}

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self, filename):

        if filename.startswith('t'):
            self._state = {
                'd': 0,
                'f': 1,
                'l' : {
                    M1: 1,
                    M2: 1,
                    G1: 2,
                    G2 :3,
                }
            }
            self._chips = [M1, M2]
            # self._state = {
            #     'd': 0,
            #     'f': 3,
            #     'l' : {
            #         HM: 3,
            #         LM: 3,
            #         HG: 4,
            #         LG :4,
            #     }
            # }

        elif filename.startswith('p1'):
            print("production 1")

            self._state = {
                'd': 0,
                'f': 1,
                'l' : {
                    M1: 1,
                    G1: 1,
                    G2: 1,
                    G3: 1,

                    M2 :2,
                    M3 :2,

                    G4: 3,
                    M4: 3,
                    G5: 3,
                    M5: 3,
                }
            }
            self._chips = [M1, M2, M3, M4, M5]

        elif filename.startswith('p2'):
            print("production 2")

            self._state = {
                'd': 0,
                'f': 1,
                'l' : {
                    M1: 1,
                    G1: 1,
                    G2: 1,
                    G3: 1,

                    M6 : 1,
                    M7 : 1,
                    G6 : 1,
                    G7 : 1,

                    M2 :2,
                    M3 :2,

                    G4: 3,
                    M4: 3,
                    G5: 3,
                    M5: 3,
                }
            }
            self._chips = [M1, M2, M3, M4, M5, M6, M7]

        self._repeat_map = {}

        self._min_steps = 200

        self._visit_count = 0

    def repeat_orig(self, state):
        """
        Have we already been to this state?
        """
        # print("check repeat")
        location = state['l']
        depth = state['d']

        key = '%d' % state['f']
        for thing, floor in location.items():
            key += "%d%d" % (thing, floor)

        key = int(key)

        # print("key", key)
        old_depth = self._repeat_map.get(key)
        if old_depth is not None and depth >= old_depth:
            return True

        self._repeat_map[key] = depth
        return False

    def repeat(self, state):
        """
        Have we already been to this state?
        """
        # print("check repeat")
        location = state['l']
        depth = state['d']

        key = '%d' % state['f']

        pairs = []
        for chip in self._chips:
            floor = location[chip]
            gen = CHIPS[chip]
            floor2 = location[gen]
            pairs.append("%d%d" % (floor, floor2))

        pairs.sort()
    #    print(pairs)

        for p in pairs:
            key += p

     #   for thing, floor in location.items():
     #       key += "%d%d" % (thing, floor)

        key = int(key)

        # print("key", key)
        old_depth = self._repeat_map.get(key)
        if old_depth is not None and depth >= old_depth:
            return True

        self._repeat_map[key] = depth
        return False

    # def print(self, state):
    #
    #
    #     print("================================")
    #     elevator = state['f']
    #     locations = state['l']
    #
    #     for f in [4, 3, 2, 1 ]:
    #         line = "F%d  " % f
    #         if elevator == f:
    #             line += "E  "
    #         else:
    #             line += '.  '
    #         for thing in [HG, HM, LG, LM]:
    #             if locations[thing] == f:
    #                 line += NAME[thing]
    #             else:
    #                 line += ".  "
    #         print(line)




    def valid(self, state):

        locations = state['l']
        for chip in self._chips:
            rtg = CHIPS[chip]
            # print("check chip %d" % chip)
            floor = locations[chip]
            if locations[rtg] == floor:
                # Chip is protected by its RTG
                continue

            can_fry_list = FRY[chip]
            for can_fry in can_fry_list:
                if locations.get(can_fry, 0 ) == floor:
                    # print("chip %d fried by %d on floor %d!!!!!!" % (chip, can_fry, floor))
                    return False

            # print("chip %d is on floor: %d" % (chip, floor))
        # print("this is VALID!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return True

    def done(self, state):
        locations = state['l']
        for thing, floor in locations.items():
            if floor != 4:
                return False

        # everything is on 4th floor!!
        return True

    def move(self, state):

        if self.done(state):
            print("DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", state['d'])
            steps = state['d']
            if steps < self._min_steps:
                self._min_steps = steps
            return

        if self.repeat(state):
            # print("repeat state, do not continue")
            return

        # Test if state is valid
        if not self.valid(state):
            # print("invalid state, do not continue")
            return

        self._visit_count += 1

        # self.print(state)

        current_floor = state['f']
        current_depth = state['d']

        if current_depth > self._min_steps:
            return

        if current_depth == 0:
            print("move called, floor: %d depth: %d" % (current_floor, current_depth))
            print(state)
        # input("continue...")

        next_depth = current_depth + 1
        next_floors = NEXT_FLOOR[current_floor]

        things_to_move = self.combinations(state)
        if current_depth == 0:
            print("next_floors: %s things to move: %s" % (repr(next_floors), things_to_move))
            input("continue...")

        for floor in next_floors:
            for thing_list in things_to_move:
                state_copy = copy.deepcopy(state)
                state_copy['f'] = floor
                state_copy['d'] = next_depth
                locations = state_copy['l']
                for thing in thing_list:
                    locations[thing] = floor

                if current_depth == 0:
                    print("move to %s" % repr(state_copy))

                self.move(state_copy)

    def run(self):
        print("called")

        self.move(self._state)

        # print(self._done_steps)
        print(self._visit_count)
        print(self._min_steps)

    def combinations(self, state):

        things = []
        current_floor = state['f']
        locations = state['l']
        for thing, floor in locations.items():
            if floor == current_floor:
                things.append(thing)

        result = []
        for l in [1, 2]:
            i = itertools.combinations(things, l)
            for t in i:
                # if len(t) == 2:
                #     if t[0] == HM and t[1] == LG:
                #         print("INVALID PAIR TO MOVE!!!!")
                #         continue
                #     if t[1] == HM and t[0] == LG:
                #         print("INVALID PAIR TO MOVE!!!!")
                #         continue
                #         # raise ValueError("invalid pair")
                #
                #     if t[0] == LM and t[1] == HG:
                #         print("INVALID PAIR TO MOVE!!!!")
                #         continue
                #
                #     if t[1] == LM and t[0] == HG:
                #         print("INVALID PAIR TO MOVE!!!!")
                #         # raise ValueError("invalid pair")
                #         continue

                result.append(t)

        return result

    def combinations_test(self):
        x = [1,2,3]

        for l in [1, 2]:
            i = itertools.combinations(x, l+1)
            for t in i:
                print(t)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
    #runner.combinations_test()
