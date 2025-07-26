import sys
import math
import itertools
import numpy as np


class Thing(object):

    def __init__(self, s, g):
        self._string = s
        self._groups = g
        self._bits = 0
        self._dots_have = 0

        for c in self._string:

            if c == '?':
                self._bits += 1
            if c == '.':
                self._dots_have += 1

        self._dots_want = len(self._string) - sum(self._groups)
        self._dots_need = self._dots_want - self._dots_have

    def run(self):

        match_count = 0

    #    print("bits", self._bits)
    #    print("dots (have)", self._dots_have)
    #    print("dots (want)", self._dots_want)
    #    print("groups", self._groups)

        max_value = int(math.pow(2, self._bits))

        possible_count = 0

        mask = max_value >> 1

        for x in range(max_value):

            if bin(x).count('1') == self._dots_need:
                possible_count += 1
                # print("%d number: %x (max: %x) bits set: %d" % (possible_count, x, max_value, self._dots_want))

                mask_temp = mask
                candidate = ""
                for c in self._string:
                    if c == '?':
                        add = '.' if mask_temp & x else '#'
                        candidate += add
                        # print("%s %x" % (candidate, mask_temp))
                        mask_temp = mask_temp >> 1
                    else:
                        candidate += c

    #            print(possible_count, candidate, len(candidate), len(self._string))
                parts = candidate.split('.')

                counts = []
                for part in parts:
                    l = len(part)
                    if l > 0:
                        counts.append(l)


                # sanity check
                if sum(counts) != sum(self._groups):
                    raise ValueError("something is wrong %d %d" % (sum(counts), sum(self._groups)))
                if len(counts) != len(self._groups):
                    continue

                # IF we made it to here then this was a match
 #               print("candidate:", candidate)
     #           print(counts, self._groups)
                match = True

                for i in range(len(self._groups)):
                    if counts[i] != self._groups[i]:
                        match = False
                        break

                if match:
                    match_count +=1

        return match_count



class Runner(object):

    def __init__(self, filename):

        print("init")

        lines = []
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

        print("read %d lines" % len(lines))

        self._cases = []

        for line in lines:
            parts = line.split(' ')
            row = parts[0]
            g = parts[1].split(',')
            group_list = [int(c) for c in g]

            # print("add row", row)
            self._cases.append((row, group_list))

    def run_part1(self):
        print("run")

        matches_total = 0

        for i, case in enumerate(self._cases):
            # print(case)
            # continue

            s = case[0]
            groups = case[1]
            possible = self.make_potential_strings(s, groups)

            match_count = 0

            print("-------------------")
            print(s, groups)

            for item in possible:

                if self.check_match(s, item):
                    match_count += 1
                    print(item)

            print("case %d: got %d potential matches" % (i, match_count))
            matches_total += match_count
            # input("continue...")

        print("part 1: total matches: %d" % matches_total)

    def run_part1_new(self):

        matches_total = 0

        for i, case in enumerate(self._cases):
            # print(case)
            # continue

            s = case[0]
            groups = case[1]

            thing = Thing(s, groups)

            match_count = thing.run()
            matches_total += match_count

        print("part 1: total matches: %d (new)" % matches_total)


    def run_part2(self):

        matches_total = 0

        for i, case in enumerate(self._cases):

            print(i, "---------")

            s = case[0]
            groups = case[1]
            groups2 = groups * 2

            # possible = self.make_potential_strings(s, groups)
            #
            # match_count = 0
            #
            # print("-------------------")
            # print(s, groups)
            #
            # for item in possible:
            #
            #     if self.check_match(s, item):
            #         match_count += 1
            #         #print(item)
            #
            # print("initial matches", match_count)
            # # Now double the string with a '.' separator
            # s1 = s + "." + s
            #
            # print(s1, groups)
            # possible = self.make_potential_strings(s1, groups2)
            # match_count1 = 0
            # for item in possible:
            #
            #     if self.check_match(s1, item):
            #         match_count1 += 1
            #         #print(item)

            thing = Thing(s, groups)
            match_count = thing.run()

            s2 = s + "#" + s
            thing = Thing(s2, groups2)
            match_count1 = thing.run()

            s3 = s + "." + s
            thing = Thing(s3, groups2)
            match_count2 = thing.run()
            #
            # # Now double the string with a '#' separator
            # possible = self.make_potential_strings(s2, groups2)
            # match_count2 = 0
            # for item in possible:
            #
            #     if self.check_match(s2, item):
            #         match_count2 += 1
            #         print(item)

            factor1 = match_count1 / match_count
            factor2 = match_count2 / match_count

            total_factor = int(factor1 + factor2)
            match_count = match_count * total_factor * total_factor * total_factor * total_factor

            print("match count", match_count, match_count1, match_count2)
            matches_total += match_count

        print("TOTAL:", matches_total)

    def yield_bins2(self, bins, balls):

        ball_list = [i for i in range(balls+1)]

        # print(ball_list)

        result_total = []

        x = itertools.combinations_with_replacement(ball_list, bins)
        # x = itertools.permutations(ball_list, bins)
        for thing in x:
            result = []

            if sum(thing) != balls:
                # print("no good", thing, sum(thing), balls, len(thing), bins)
                continue

            zeros = 0
            for i in range(bins):
                if thing[i] == 0:
                    zeros += 1

            if zeros > 2: continue

            print("good", thing)

            # print("get permutations", thing)
            count = 0
            bad = 0

            for item in itertools.permutations(thing, bins):
                count += 1
                #print("item....", item)
                try:
                    for j in range(1, bins-1):
                    # print("check l[%d]: %d" % (j, l[j]))
                        if item[j] == 0:
                            #print("this result is no good")
                            bad += 1
                            raise ValueError

                    # print(item)
                    result.append(item)

                except:
                    continue

            print("total", count, "bad", bad, "good", len(result))
            result = list(set(result))
            print("good unique", len(result))

            result_total.extend(result)

        for item in result_total:
            # print(item)
            yield item

    def make_potential_strings(self, s, groups):

        # max_unknown_len = 0
        # unknown_len = 0
        # for c in s:
        #     if c == '#':
        #         if unknown_len > max_unknown_len:
        #             max_unknown_len = unknown_len
        #         unknown_len = 0
        #     else:
        #         unknown_len += 1
        #
        # if unknown_len > max_unknown_len:
        #     max_unknown_len = unknown_len

        # print("max_unknown_len", max_unknown_len)

        length = len(s)
        group_count = len(groups)
        bins = group_count + 1
        balls = length - sum(groups)

        result = []

        for item in self.yield_bins2(bins, balls):
            if len(item) != bins:
                raise ValueError("what the !?!?!?", len(item), bins)

            new = ''
            for i in range(group_count):
                new = new + '.' * item[i]
                new = new + '#' * groups[i]

            new += '.' * item[group_count]
            result.append(new)
            # print("new", new)

        return result

    def check_match(self, s, p):

        # print("compare", s, p)
        if len(s) != len(p):
            raise ValueError("bad length len(s) %s len(p) %s" % (len(s), len(p)) )


        for i in range(len(s)):
            # print("compare %c to %c" % (s[i], p[i]))
            if s[i] == '?':
                continue

            if s[i] != p[i]:
                return False

        return True

    def test1(self):

        s = '??????#?.#?#.????.?'
        groups = [7, 1, 1, 2, 1]

        s = s + '#' + s
        groups = groups + groups
        # possible = self.make_potential_strings(s, groups)

        print("string", s)

        thing = Thing(s, groups)

        #for item in possible:
        #    print(item)

        # How many ways can the gaps be arranged?


if __name__ == '__main__':

    """
    25874588538826 - too low
    27586463792660 - too low
    27593372770705 - not the right answer
    8685584341198  - must be waay to low
    6768213599535
    1045075980505
    5298705311449
    5298705311449


    """
    runner = Runner(sys.argv[1])
    # runner.run_part1()
    # runner.run_part1_new()
    runner.run_part2()
    # runner.test1()
    #runner.test1()
