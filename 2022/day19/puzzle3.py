import itertools
import copy
from queue import Queue
import math

ORE             = 0
CLAY            = 1
OBSIDIAN        = 2
GEODE           = 3
ROBOT_ORE       = 4
ROBOT_CLAY      = 5
ROBOT_OBSIDIAN  = 6
ROBOT_GEODE     = 7
BUY_ROBOT       = 8

class ExceptionDone(Exception):
    pass


class Runner(object):

    def __init__(self):
        self._file_name = 'input_test.txt'
        self._file_name = 'input_real.txt'

        self._expect_parts = None
        self._blueprints = {}
        self._states = []
        self._states_new = []
        self._blueprint = None

        self._max_minutes = 32

    def run(self):

        fp = open(self._file_name, 'r')
        lines = []
        for line in fp:
            line = line.strip()
            lines.append(line)

        fp.close()

        for line in lines:
            self.process_line(line)

        for item, value in self._blueprints.items():
            print("blueprint: %d: %s" % (item, repr(value)))

        total_score = 0
        for blueprint_number, blueprint in self._blueprints.items():

            # Initiatlize the blueprint
            self._blueprint = blueprint
            self._max_clay =  self._blueprint[2][1]
            self._max_ore = max(blueprint[0], blueprint[1], blueprint[2][0], blueprint[3][0])
            # self._max_ore = max(blueprint[1], blueprint[2][0], blueprint[3][0])
            self._max_obsidian = blueprint[3][1]

            print("MAX ore: %d" % self._max_ore)
            print("MAX clay: %d" % self._max_clay)
            print("MAX obsidian: %d" % self._max_obsidian)

            # Initialize the state
            # ore, clay, obs, geo, oR, cR bR, gR, build
            self._states = [ [0, 0, 0, 0, 1, 0, 0, 0, 0] ]

            minute = 0
            while minute <= self._max_minutes:
                minute += 1
                if minute > self._max_minutes: break

                print("Minute: %s states: %d =============================" %
                      (minute, len(self._states)))

                self.purge_states_new(minute)

                if len(self._states) > 100000000:
                    print("too many states... aborting!!!!!!")
                    break

                self._states_new = []

                try:
                    for state in self._states:
                        self.get_new_minerals(state)
                        self.process(state)

                except ExceptionDone:
                    pass

                # De we have any duplicate states?
                # len_before = len(self._states_new)
                # len_after = len(list(set(self._states_new)))
                # print("LEN BEFORE: %s ADFTER: %d" % (len_before, len_after))

                self._states = self._states_new

            print("finished this blueprint %d" % blueprint_number)

            max_geodes = self.get_max_geodes()
            total_score += max_geodes * (blueprint_number)

            if blueprint_number == 3:
                break
#            for state in self._states:
#                self.print_state(state)

        print("TOTAL: %d" % total_score)
        print("done")


    def purge_states(self, minute):

        keep_states = []
        purge_count = 0
        minutes_remaining = self._max_minutes - minute
        if minutes_remaining < 2:
            return

        max_geodes = 0

        # First, get the maximum number of geodes if no state ever builds another geode robot
        for state in self._states:
            possible_geodes = state[GEODE] + state[ROBOT_GEODE] * minutes_remaining
            if possible_geodes > max_geodes:
                max_geodes  = possible_geodes

        # Now lets see how many geodes this state counlf build if it build a geode
        # robot in every remaining step
        remaining_geodes = sum([i for i in range(minutes_remaining)])
        for state in self._states:
            possible_geodes = state[GEODE] + state[ROBOT_GEODE] * minutes_remaining
            # possible_geodes += math.factorial(minutes_remaining-1)
            possible_geodes += remaining_geodes

            if possible_geodes < max_geodes:
                # print("can purge this path!!! %d < %d " % (possible_geodes, max_geodes ))
                purge_count += 1
            else:
                keep_states.append(state)

        print("can purge %d paths" % purge_count)
        self._states = keep_states

    def purge_states_new(self, minute):

        minutes_remaining = self._max_minutes - minute
        if minutes_remaining < 2:
            return

        if len(self._states) < 1000000:
            return

        temp = []
        for state in self._states:
            score = state[ROBOT_ORE] + state[ROBOT_CLAY] * 2 + state[ROBOT_OBSIDIAN] * 3 + state[ROBOT_GEODE] * 4
            temp.append((score, state))

        temp.sort()
        temp.reverse()

        result = []
        for i in range(100000):
            result.append(temp[i][1])

        self._states = result

    def get_max_geodes(self):

        max_geodes = 0
        for state in self._states:
            if state[GEODE] > max_geodes:
                max_geodes = state[GEODE]
                self.print_state(state)
        print("MAX GEODES: %d" % max_geodes)
        return max_geodes

    def process(self, state):

        # Can we afford a geode robot? If so that is all we should do
        if state[ORE] >= self._blueprint[3][0]:
            if state[OBSIDIAN] >= self._blueprint[3][1]:
                new = copy.deepcopy(state)
                new[ORE] -= self._blueprint[3][0]
                new[OBSIDIAN] -= self._blueprint[3][1]
                new[BUY_ROBOT] = ROBOT_GEODE
                # print("boght a geode robot")

                self._states_new.append(new)
                return

                # self._states_new = [new]
                # raise ExceptionDone

        option_count = 0

        if state[ROBOT_OBSIDIAN] < self._max_obsidian:
            if state[CLAY] >= self._blueprint[2][1]:
                if state[ORE] >= self._blueprint[2][0]:
                    new = copy.deepcopy(state)

                    new[ORE]  -= self._blueprint[2][0]
                    new[CLAY] -= self._blueprint[2][1]
                    new[BUY_ROBOT] = ROBOT_OBSIDIAN
                    self._states_new.append(new)
                    option_count += 1

        # Can we build a clay robot... do we want to?
        if state[ROBOT_CLAY] < self._max_clay:
            if state[ORE] >= self._blueprint[1]:
                # Buy a clay robot
                new = copy.deepcopy(state)
                new[ORE] -= self._blueprint[1]
                new[BUY_ROBOT] = ROBOT_CLAY
                self._states_new.append(new)
                option_count += 1

        # Can we build an ore robot? do we want to?
        if state[ROBOT_ORE] < self._max_ore:
            if state[ORE] >= self._blueprint[0]:
                # Buy a clay robot
                new = copy.deepcopy(state)
                new[ORE] -= self._blueprint[0]
                new[BUY_ROBOT] = ROBOT_ORE
                self._states_new.append(new)
                option_count += 1

        # Do nothing . add do nothing state to list of new states
        if option_count < 3:
            new = copy.deepcopy(state)
            self._states_new.append(new)


    def get_new_minerals(self, state):

        # Each robot produces one item
        state[ORE]      += state[ROBOT_ORE]
        state[CLAY]     += state[ROBOT_CLAY]
        state[OBSIDIAN] += state[ROBOT_OBSIDIAN]
        state[GEODE]    += state[ROBOT_GEODE]

        if state[BUY_ROBOT] > 0:
            state[ state[BUY_ROBOT] ] += 1
            state[BUY_ROBOT] = 0
    #             print("   new robot %d ready... now have %d" %
    #                   ((new_robot_index), state[new_robot_index]))
    #             new_robot_index = None
    #
    def print_state(self, state):

        print("ORE: %d CLAY: %d OBS: %d: GEO: %d   --- ROBOTS: ORE: %d CLAY: %d OBS: %d GEODE: %d" % \
            (state[ORE], state[CLAY], state[OBSIDIAN], state[GEODE],
             state[ROBOT_ORE], state[ROBOT_CLAY], state[ROBOT_OBSIDIAN], state[ROBOT_GEODE]))

    # def go(self, blueprint):
    #
    #     state = [0, 0, 0, 0, 1, 0, 0, 0]
    #     robots_ordered = [0, 0, 0, 0, 1, 0, 0, 0]
    #     new_robot_index = None
    #
    #     max_ore_robots = max(blueprint[1], blueprint[2][0], blueprint[3][0])
    #     max_clay_robots = blueprint[2][1]
    #     max_obsidian_robots = blueprint[3][1]
    #
    #     print("Max robots: ORE: %d CLAY: %d OBSIDIAN: %d" % \
    #           (max_ore_robots, max_clay_robots, max_obsidian_robots ))
    #
    #     minute = 0
    #     while True:
    #
    #         # Each robot produces one item
    #         state[ORE]      += state[ROBOT_ORE]
    #         state[CLAY]     += state[ROBOT_CLAY]
    #         state[OBSIDIAN] += state[ROBOT_OBSIDIAN]
    #         state[GEODE]    += state[ROBOT_GEODE]
    #
    #         minute += 1
    #         if minute > self._max_minutes: break
    #
    #         print("Minute: %d -------ORE: %d CLAY: %d OBSIDIAN: %d GEODE: %d" %
    #               (minute, state[ORE], state[CLAY], state[OBSIDIAN], state[GEODE]))
    #
    #         if new_robot_index is not None:
    #             state[new_robot_index] += 1
    #             print("   new robot %d ready... now have %d" %
    #                   ((new_robot_index), state[new_robot_index]))
    #             new_robot_index = None
    #
    #         # Can I afford a geode robot?
    #         if state[ORE] >= blueprint[3][0]:
    #             if state[OBSIDIAN] >= blueprint[3][1]:
    #                 state[ORE] -= blueprint[3][0]
    #                 state[OBSIDIAN] -= blueprint[3][1]
    #                 new_robot_index = ROBOT_GEODE
    #                 print("    bought an GEODE robot")
    #                 continue
    #
    #         if robots_ordered[ROBOT_OBSIDIAN] < max_obsidian_robots:
    #             if state[CLAY] >= blueprint[2][1]:
    #                 if state[ORE] >= blueprint[2][0]:
    #                         state[ORE] -= blueprint[2][0]
    #                         state[CLAY] -= blueprint[2][1]
    #                         robots_ordered[ROBOT_OBSIDIAN] += 1
    #                         new_robot_index = ROBOT_OBSIDIAN
    #                         print("    bought an OBSIDIAN robot")
    #                         continue
    #                 # I have enough clay, but not enough ore...
    #                 # wait a rouind to get more ore
    #                 continue
    #
    #         if robots_ordered[ROBOT_CLAY] < max_clay_robots:
    #             if state[ORE] >= blueprint[1]:
    #                 state[ORE] -= blueprint[1]
    #                 new_robot_index = ROBOT_CLAY
    #                 robots_ordered[ROBOT_CLAY] += 1
    #                 print("    bought a CLAY robot")
    #                 continue
    #
    #         if robots_ordered[ROBOT_ORE] < max_ore_robots:
    #             if state[ORE] >= blueprint[0]:
    #                 state[ORE] -= blueprint[0]
    #                 new_robot_index = ROBOT_ORE
    #                 robots_ordered[ROBOT_ORE] += 1
    #                 print("    bought an ORE robot")
    #                 continue
    #
    #
    #     print("got %d geodes" % state[GEODE])
    #
    #
    #     return state[GEODE]


        # # Reset the iterator
        # self._choices.reset()
        #
        # max_geodes = 0
        # max_path = []
        #
        #
        # while True:
        #     # Get the next path
        #     choice = self._choices.get_next()
        #     if choice is None:
        #         break
        #
        #     geodes, path = self.process_path(choice, blueprint)
        #
        #     # print("got %d geodes % geodes)
        #     # print("path: %s" % repr(path))
        #     if len(path) < self._max_minutes:
        #         self._choices.skip_branch(path)
        #
        #     if geodes > max_geodes:
        #         print("new max_geodes: %s path: %s" % (geodes, repr(path)))
        #         max_geodes = geodes
        #         max_path = path
        #
        # print("done, max_geodes:", max_geodes)
        # print("path: %s" % repr(max_path))
        #
        # return max_geodes

    # def process_path(self, choice, blueprint):
    #
    #     state = [0, 0, 0, 0, 1, 0, 0, 0]
    #
    #     # print(choice)
    #
    #     new_robot = None
    #     choice_index = 0
    #     choices_processed = []
    #     want_robot = choice[choice_index]
    #
    #     for minute in range(1, self._max_minutes + 1):
    #         # get new minerals from the robots
    #
    #         if new_robot:
    #             state[new_robot_index] += 1
    #             choice_index += 1
    #             want_robot = choice[choice_index]
    #             choices_processed.append(new_robot)
    #             new_robot = None
    #
    #         if want_robot == 'A':
    #             # print("I want to buy an ore robot, can I")
    #             if state[ORE] >= blueprint[0]:
    #                 state[ORE] -= blueprint[0]
    #                 new_robot_index = ROBOT_ORE
    #                 new_robot = want_robot
    #
    #         elif want_robot == 'B':
    #             # print("I want to buy a clay robot, can I")
    #             if state[ORE] >= blueprint[1]:
    #                 state[ORE] -= blueprint[1]
    #                 new_robot_index = ROBOT_CLAY
    #                 new_robot = want_robot
    #
    #         elif want_robot == 'C':
    #             # print("I want to buy an obsidian robot, can I")
    #             if state[ORE] >= blueprint[2][0]:
    #                 if state[CLAY] >= blueprint[2][1]:
    #                     state[ORE] -= blueprint[2][0]
    #                     state[CLAY] -= blueprint[2][1]
    #                     new_robot_index = ROBOT_OBSIDIAN
    #                     new_robot = want_robot
    #
    #         elif want_robot == 'D':
    #             # print("I want to buy an geode robot, can I")
    #             if state[ORE] >= blueprint[3][0]:
    #                 if state[OBSIDIAN] >= blueprint[3][1]:
    #                     state[ORE] -= blueprint[3][0]
    #                     state[OBSIDIAN] -= blueprint[3][1]
    #                     new_robot_index = ROBOT_GEODE
    #                     new_robot = want_robot
    #
    #
    #         # Each robot produces one item
    #         state[ORE]      += state[ROBOT_ORE]
    #         state[CLAY]     += state[ROBOT_CLAY]
    #         state[OBSIDIAN] += state[ROBOT_OBSIDIAN]
    #         state[GEODE]    += state[ROBOT_GEODE]
    #
    #         # print(minute, state)
    #
    #     # print("finished this path!!!", choices_processed)
    #     # print("got %d geodes" % state[GEODE])
    #
    #     return state[GEODE], choices_processed

    def go_OBS(self, blueprint):
        """

        """
        queue = Queue()

        queue.put_nowait(state)

        loop_count = 0
        while True:

            if queue.empty():
                print("queue is empty; loop_count: %d" % loop_count)
                break

            loop_count += 1

            state = queue.get_nowait()

            minute = state[MINUTE] + 1
            if minute == 25:

                # print("Done; state: %s" % repr(state))
                continue

            state[MINUTE] = minute

            # Each robot produces one item
            state[ORE]      += state[ROBOT_ORE]
            state[CLAY]     += state[ROBOT_CLAY]
            state[OBSIDIAN] += state[ROBOT_OBSIDIAN]
            state[GEODE]    += state[ROBOT_GEODE]

            # This is the "do nothing state"
            queue.put_nowait(state)

            # Can I buy an ore robot:
            if state[ORE] >= blueprint[0]:
                # print("buy an ore robot")
                state1 = copy.copy(state)
                state1[ROBOT_ORE] += 1
                state1[ORE] -= blueprint[0]

                queue.put_nowait(state1)

            # Can I buy an clay robot:
            if state[ORE] >= blueprint[1]:
                # print("buy an ore robot")
                state1 = copy.copy(state)
                state1[ROBOT_CLAY] += 1
                state1[ORE] -= blueprint[1]

                queue.put_nowait(state1)

    def process_line(self, line):
        print(line)
        line = line.replace(':', '')
        parts = line.split(' ')

        part_count = len((parts))
        if self._expect_parts is None:
            self._expect_parts = part_count
        elif self._expect_parts != part_count:
            raise ValueError("unexpected part count")

        #for i, part in enumerate(parts):
        #    print(i, part)

        blueprint = int(parts[1])
        ore_cost = int(parts[6])
        clay_cost = int(parts[12])
        obsidian_cost = ( int(parts[18]), int(parts[21]) )
        geode_cost =  ( int(parts[27]), int(parts[30]) )

        # print(ore_cost, clay_cost, obsidian_cost, geode_cost )

        self._blueprints[blueprint] = ( ore_cost, clay_cost, obsidian_cost, geode_cost )



def test1():

    x = [1,2,3]
    y = itertools.product(x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x)

    loop_count = 0
    for pair in y:
        loop_count += 1
        #print(pair)
    print(loop_count)

def test2():

    i = MyIterator(length = 24)

    for _ in range(20):

        val = i.get_next()
        if val is None:
            print("we are done")
            break

        print( val )

    test = ['A', 'A', 'B']
    i.skip_branch(test)
    d = i.get_next()
    print(d)

    test = ['A', 'A']
    i.skip_branch(test)
    d = i.get_next()
    print(d)

if __name__ == '__main__':
    # test1()
    #test2()
    runner = Runner()
    runner.run()
