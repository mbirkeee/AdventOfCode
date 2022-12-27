import itertools
import copy
from queue import Queue

ORE             = 0
CLAY            = 1
OBSIDIAN        = 2
GEODE           = 3
ROBOT_ORE       = 4
ROBOT_CLAY      = 5
ROBOT_OBSIDIAN  = 6
ROBOT_GEODE     = 7

class ExceptionDone(Exception):
    pass


class MyIterator(object):

    def __init__(self, length=4):

        self._x = -1
        self._digits = ['A', 'B' ,'C', 'D']
        self._values = {'A': 0, 'B': 1, 'C':2, 'D':3}
        self._base = 4
        self._length = length

    def int2base(self, x, base=3):

        digits = []

        while x:
            digits.append(self._digits[x % self._base])
            x = x // self._base

        add = self._length - len(digits)
        for _ in range(add):
            digits.append(self._digits[0])
        digits.reverse()

        return digits

    def base2int(self, digits):

        answer = 0
        for d in digits:
            answer = answer * self._base
            answer += self._values[d]

        # print("current index", answer)
        return answer

    def reset(self):
        self._x = -1

    def get_next(self):

        self._x += 1

        result = self.int2base(self._x)
        if len(result) > self._length:
            return None

        return self.int2base(self._x)

    def skip_branch(self, digits):
        # print("skip branch called")
        add = self._length - len(digits)
        for _ in range(add):
            digits.append(self._digits[-1])

        # print(digits)
        x = self.base2int(digits)
        self._x = x

class Runner(object):

    def __init__(self):
        self._file_name = 'input_test.txt'
        #self._file_name = 'input_real.txt'

        self._expect_parts = None
        self._blueprints = {}

        self._max_minutes = 32
        self._choices = MyIterator(length=self._max_minutes)

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

        # self.process_path(['B', 'B', 'B', 'C', 'B', 'C', 'D', 'D', 'D', 'A', 'C'], self._blueprints[2] )
        # raise ValueError('temp stop')

        total_score = 0
        for item, value in self._blueprints.items():
            print("blueprint: %d: %s" % (item, repr(value)))
            geodes = self.go(value)
            total_score += (item * geodes)
            print("total_score: %d" % total_score)

        print("done")

    def go(self, blueprint):

        # Reset the iterator
        self._choices.reset()

        max_geodes = 0
        max_path = []

        while True:
            # Get the next path
            choice = self._choices.get_next()
            if choice is None:
                break

            geodes, path = self.process_path(choice, blueprint)

            # print("got %d geodes % geodes)
            # print("path: %s" % repr(path))
            if len(path) < self._max_minutes:
                self._choices.skip_branch(path)

            if geodes > max_geodes:
                print("new max_geodes: %s path: %s" % (geodes, repr(path)))
                max_geodes = geodes
                max_path = path

        print("done, max_geodes:", max_geodes)
        print("path: %s" % repr(max_path))

        return max_geodes

    def process_path(self, choice, blueprint):

        state = [0, 0, 0, 0, 1, 0, 0, 0]

        # print(choice)

        new_robot = None
        choice_index = 0
        choices_processed = []
        want_robot = choice[choice_index]

        for minute in range(1, self._max_minutes + 1):
            # get new minerals from the robots

            if new_robot:
                state[new_robot_index] += 1
                choice_index += 1
                want_robot = choice[choice_index]
                choices_processed.append(new_robot)
                new_robot = None

            if want_robot == 'A':
                # print("I want to buy an ore robot, can I")
                if state[ORE] >= blueprint[0]:
                    state[ORE] -= blueprint[0]
                    new_robot_index = ROBOT_ORE
                    new_robot = want_robot

            elif want_robot == 'B':
                # print("I want to buy a clay robot, can I")
                if state[ORE] >= blueprint[1]:
                    state[ORE] -= blueprint[1]
                    new_robot_index = ROBOT_CLAY
                    new_robot = want_robot

            elif want_robot == 'C':
                # print("I want to buy an obsidian robot, can I")
                if state[ORE] >= blueprint[2][0]:
                    if state[CLAY] >= blueprint[2][1]:
                        state[ORE] -= blueprint[2][0]
                        state[CLAY] -= blueprint[2][1]
                        new_robot_index = ROBOT_OBSIDIAN
                        new_robot = want_robot

            elif want_robot == 'D':
                # print("I want to buy an geode robot, can I")
                if state[ORE] >= blueprint[3][0]:
                    if state[OBSIDIAN] >= blueprint[3][1]:
                        state[ORE] -= blueprint[3][0]
                        state[OBSIDIAN] -= blueprint[3][1]
                        new_robot_index = ROBOT_GEODE
                        new_robot = want_robot


            # Each robot produces one item
            state[ORE]      += state[ROBOT_ORE]
            state[CLAY]     += state[ROBOT_CLAY]
            state[OBSIDIAN] += state[ROBOT_OBSIDIAN]
            state[GEODE]    += state[ROBOT_GEODE]

            # print(minute, state)

        # print("finished this path!!!", choices_processed)
        # print("got %d geodes" % state[GEODE])

        return state[GEODE], choices_processed

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
