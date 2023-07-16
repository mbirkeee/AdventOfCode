"""
"""

import sys
import math
import copy
import itertools
import hashlib

from results_part1 import TRANSLATIONS
from results_part1 import TRANSLATIONS_TEST

X = 0
Y = 1
Z = 2
R = 4

class ExceptionDone(Exception):
    pass

ROT_AXIS = {
    X: (Z, Y),
    Z: (X, Y),
    Y: (X, Z),
}

""""
These must be applied in order!!!

       RED (Y)
        |
        |
        o------ Green (X)
       /
      /
    BLUE (Z)

"""
ROTATIONS = [
    [R],            # Red UP
    [Y],
    [Y],
    [Y],
    [R, Z, Z],      # Red DOWN
    [Y],
    [Y],
    [Y],
    [R, X],         # Blue UP
    [Y],
    [Y],
    [Y],
    [R, X, X, X],   # Blue DOWN
    [Y],
    [Y],
    [Y],
    [R, Z, Z, Z],   # Green UP
    [Y],
    [Y],
    [Y],
    [R, Z],         # Green DOWN
    [Y],
    [Y],
    [Y],
]

class Scanner(object):
    """
    Its too mind bending to figure out the 24 successive rotations I need.
    So, I will reset the cube to get back to a known position
    """
    def __init__(self, index):
        self._beacons = []
        self._beacons_copy = []
        self._index = index

        self._translate_x = 0
        self._translate_y = 0
        self._translate_z = 0

        self._located = False

    def set_located(self):
        self._located = True

    def get_located(self):
        return self._located

    def absorb(self, scanner):

        # Load the new beacon positions (these should be relative to the
        # initially locked scanner
        new_beacons = scanner.get_translated_beacons()
        for new_beacon in new_beacons:
            if new_beacon not in self._beacons:
                self._beacons.append(new_beacon)
                self._beacons_copy.append(new_beacon)

    def add_beacon(self, line):
        #print("scanner %s add beacon %s" % (self._index, line))
        line = line.strip()
        if len(line) == 0:
            return

        parts = line.split(',')
        beacon = [ int(parts[0]), int(parts[1]), int(parts[2]) ]

        #print(beacon)
        self._beacons.append(beacon)
        self._beacons_copy.append(beacon)

    def get_index(self):
        return self._index

    def print_beacons(self):

        for beacon in self._beacons:
            print("X: %6d Y: %6d z: %6d" % (beacon[0], beacon[1], beacon[2]))

    def reset(self):
        self._beacons = copy.deepcopy(self._beacons_copy)

    def apply_moves(self, moves):

        #print("apply moves", moves)
        for move in moves:
            self.rotate(move)

    def rotate(self, axis):

        if axis == R:
            self.reset()
            return

        # ALL rotations are exactly 90 degrees clockwise

        meta = ROT_AXIS.get(axis)
        index_x = meta[0]
        index_y = meta[1]

        for beacon in self._beacons:
            x = beacon[index_x]
            y = beacon[index_y]

            beacon[index_x] = y
            beacon[index_y] = x * -1

    def get_beacon_count(self):
        return len(self._beacons)

    def get_beacon(self, i):
        return copy.deepcopy(self._beacons[i])

    def get_beacons(self):
        return copy.deepcopy(self._beacons)

    def translate(self, beacon_src, beacon_tgt):
        # print("translate tgt", beacon_tgt)
        # print("translate src", beacon_src)

        # Translate beacon_src to beacon_tgt
        self._translate_x = beacon_tgt[0] - beacon_src[0]
        self._translate_y = beacon_tgt[1] - beacon_src[1]
        self._translate_z = beacon_tgt[2] - beacon_src[2]

        # print("translate x", self._translate_x)
        # print("translate y", self._translate_y)
        # print("translate z", self._translate_z)

    def get_translated_beacon(self, index):

        beacon = self._beacons[index]
        # print("translate start", beacon)

        return [
            beacon[0] + self._translate_x,
            beacon[1] + self._translate_y,
            beacon[2] + self._translate_z
        ]

    def get_translation(self):
        return [
            self._translate_x,
            self._translate_y,
            self._translate_z
        ]

    def get_translated_beacons(self):

        result = []
        for i in range(len(self._beacons)):
            result.append(self.get_translated_beacon(i))

        return result

class Runner(object):

    def __init__(self, filename):

        lines = []
        fp = None

        self._scanner_dict = {}

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(lines))

        scanner = None

        for line in lines:
            if line.find('scanner') > 0:
                # print("found scanner: %s" % line)
                parts = line.split()
                scanner_number = int(parts[2])
                # print(scanner_number)
                scanner = Scanner(scanner_number)

                # Add newly create scanner to the dict of scanners
                self._scanner_dict[scanner_number] = scanner
            else:
                scanner.add_beacon(line)

        for scanner_number, scanner in self._scanner_dict.items():
            print("---- SCANNER: %d beacons: %d"  % (scanner_number, scanner.get_beacon_count()))
            #scanner.print_beacons()



    def compare_beacons(self, beacons1, beacons2):

        # print("compare beacons 1", beacons1)
        # print("compare beacons 2", beacons2)
        match_list = []

        for beacon in beacons1:
            if beacon in beacons2:
                match_list.append(beacon)

        return match_list


    def compare_scanners(self, scanner1, scanner2):

        print("compare scanners %d %d" % (scanner1.get_index(), scanner2.get_index()))
        # print("scanner 1 beacons")
        # scanner1.print_beacons()

        if not scanner1.get_located():
            print("base scanner is not located!!!!")
            return

        if scanner2.get_located():
            print("*" * 80)
            print("we can skip this scanner, we know where it is!!!!")
            print("*" * 80)
            return

        target_beacons = scanner1.get_beacons()
        beacon2_count = scanner2.get_beacon_count()

        for target_beacon in target_beacons:
            # print("target beacon", target_beacon)

                # Rotate the test scanner to all 24 possible positions:
            for move_index, moves in enumerate(ROTATIONS):
                scanner2.apply_moves(moves)
                # print("scanner 2 beacons")
                # scanner2.print_beacons()

                for i in range(beacon2_count):
                    # print("check mode %d get beacon %d" % (move_index, i))
                    test_beacon = scanner2.get_beacon(i)
                    scanner2.translate(test_beacon, target_beacon)

                    translated_beacons = scanner2.get_translated_beacons()

                    match_list = self.compare_beacons(target_beacons, translated_beacons)

                    if len(match_list) > 10:
                        print("scanner1: %s scanner2: %d move index: %d beacon_index: %d matches: %d" %
                              (scanner1.get_index(), scanner2.get_index(), move_index, i, len(match_list)))
                        print("translation", scanner2.get_translation())

                        for beacon in match_list:
                            print("matching beacon", beacon)

                        scanner1.absorb(scanner2)
                        if scanner1.get_located():
                            scanner2.set_located()
                        # scanner2.reset()
                        return


    def run(self):

        scanner0 = self._scanner_dict.get(0)
        scanner0.set_located()

        # scanner2 = self._scanner_dict.get(4)
        # self.compare_scanners(scanner1, scanner2)
        # return

        index_list = [k for k in self._scanner_dict.keys()]

        loop_count = 0
        while True:

            loop_count += 1
            if loop_count > 1000:
                break

            print("START "*10)

            for i, scanner in self._scanner_dict.items():
                if i == 0: continue
                self.compare_scanners(scanner0, scanner)

            # combinations = itertools.combinations(index_list, 2)
            #
            # for combination in combinations:
            #     print("compare combo %s" % repr(combination))
            #     scanner1 = self._scanner_dict.get(combination[0])
            #     scanner2 = self._scanner_dict.get(combination[1])
            #
            #     self.compare_scanners(scanner1, scanner2)

            located_flag = True
            for scanner in self._scanner_dict.values():
                print("Scanner: %d located: %s beacons: %d translate: %s" %
                      (scanner.get_index(), scanner.get_located(),
                       scanner.get_beacon_count(), repr(scanner.get_translation())))

                if not scanner.get_located():
                    located_flag = False

            if located_flag:
                break

        print("done!!")




    def test1(self):

        print("test 1")

        scanner = Scanner(0)
        scanner.add_beacon("4,2,1")
        scanner.print_beacons()

        scanner.rotate(Z)
        scanner.print_beacons()

        scanner.rotate(Z)
        scanner.print_beacons()

        scanner.rotate(Z)
        scanner.print_beacons()

        scanner.rotate(Z)
        scanner.print_beacons()

    def test2(self):

        print("test2")

        scanner = Scanner(0)
        scanner.add_beacon("4,2,1")
        scanner.print_beacons()

        for moves in ROTATIONS:
            # print(moves)
            for move in moves:
                scanner.rotate(move)
                scanner.print_beacons()

    def distance(self, b1, b2, manhatten=False):

        d0 = b1[0] - b2[0]
        d1 = b1[1] - b2[1]
        d2 = b1[2] - b2[2]

        if manhatten:
            return abs(d0) + abs(d1) + abs(d2)

        else:
            d_sq = d0 * d0 + d1 * d1 + d2 * d2
            return math.sqrt(d_sq)


    def hash(self, beacons):

        m = hashlib.sha256()
        for beacon in beacons:
            s = "%d%d%d" % (beacon[0], beacon[1], beacon[2])
            m.update(s.encode())

        print(m.hexdigest())

    def test3(self):

        scanner = Scanner(0)
        scanner.add_beacon("1,7,5")
        scanner.add_beacon("-2,-6,4")
        scanner.add_beacon("5,3,-7")
        scanner.add_beacon("2,-4,-8")
        scanner.add_beacon("1,4,5")
        scanner.add_beacon("7,0,-6")


        for moves in ROTATIONS:
            # print(moves)
            # print("---")
            scanner.apply_moves(moves)
            # scanner.print_beacons()

            beacons = scanner.get_beacons()

            # d = self.distance(beacons[1], beacons[5])
            # print(d)
            #
            # d = self.distance(beacons[0], beacons[3])
            # print(d)
            #
            # d = self.distance(beacons[2], beacons[4])
            # print(d)

            self.hash(beacons)

    def part2(self):
        translations = TRANSLATIONS

        for translation in translations:
            print("translation", repr(translation))

        translation_count = len(translations)
        combinations = itertools.combinations(range(translation_count), 2)

        d_max = 0
        for combination in combinations:
            print("test", combination)

            d = self.distance(
                translations[combination[0]],
                translations[combination[1]], manhatten=True)

            if d > d_max:
                d_max = d

        print("mas dist", d_max)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    # runner.run()
    runner.part2()
    # runner.test3()
