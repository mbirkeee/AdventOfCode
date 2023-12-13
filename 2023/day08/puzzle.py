import sys

class Runner(object):

    def __init__(self, filename):

        lines = []
        self._map = {}
        self._turns = []
        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                line = line.strip('.')
                if len(line) == 0:
                    continue
                lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(lines))

        for i, line in enumerate(lines):
            if i == 0:
                print("this is the route", line)
                for c in line:
                    if c == 'L':
                        self._turns.append(0)
                    else:
                        self._turns.append(1)

                self._turns_len = len(self._turns)

            else:
                line = line.replace(' ','')
                line = line.replace('(','')
                line = line.replace(')','')

                # print("MAP: %s" % line)
                parts = line.split('=')

                # print(parts)
                key = parts[0]
                items = parts[1].split(',')

                # print items
                self._map[key] = items

    def run1(self):

        position = 'AAA'
        turn_index = 0
        turn_count = 0

        while True:

            turn = self._turns[turn_index]
            turn_index += 1
            if turn_index >= self._turns_len: turn_index = 0

            turn_count += 1
            options = self._map[position]
            position = options[turn]

            if position == 'ZZZ':
                break

        print("arrived at ZZZ after %d turns" % turn_count)


    def run2(self):

        """
        0 16897
        1 16343
        2 21883
        3 13019
        4 14681
        5 20221

:return:
"""
        path_list = []

        for k, v in self._map.items():

            if k.endswith('A'):
                path_list.append(k)

        print(path_list)

        turn_index = 0
        turn_count = 0
        last_hit = 0
        diff = 0

        while True:
            turn = self._turns[turn_index]
            turn_count += 1
            turn_index += 1

            if turn_index >= self._turns_len: turn_index = 0

            for i, position in enumerate(path_list):
                options = self._map[position]
                position = options[turn]
                path_list[i] = position


                if i == 2:
                    if position.endswith('Z'):
                        if last_hit is not None:
                            diff = turn_count - last_hit
                        last_hit = turn_count

                        print("position", position, turn_index, turn_count, diff)

            # print("turns: %s positions: %s" % (turn_count, path_list))
            done = True
            for position in path_list:
                if not position.endswith('Z'):
                    done = False
                    break

            if done:
                break

        print("arrived at all Zs after %d turns" % turn_count)

    def run3(self):
        """
        23355229540361858900885867 is too high
        loops = [
            16897, 61, 277
            16343, 59, 277
            21883, 79, 277
            13019, 47, 277
            14681, 53 277
            20221, 73, 277
        ]

        I noticed that each path looped with a certain frequency and then I got the
        prime factors of each loop period and then found the lowest common multiple
        which was the answer
        """

        loops = [
            16897,
            16343,
            21883,
            13019,
            14681,
            20221,
        ]
        x = 0
        while True:

            x = x + 20221

            good = True

            for v in loops:
                if x % v:
                    # not a factor:
                    good = False
                    break
                else:
                    print("found a factor")

            if good:
                break

            print(x)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run2()
    # runner.run3()
