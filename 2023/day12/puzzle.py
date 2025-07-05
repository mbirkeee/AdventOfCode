import sys
import math
import itertools
import numpy as np

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

        # print("read %d lines" % len(lines))

        self._cases = []

        for line in lines:
            parts = line.split(' ')
            row = parts[0]
            g = parts[1].split(',')
            group_list = [int(c) for c in g]

            # print("add row", row)
            self._cases.append((row, group_list))

        self._balls = 0
        self._bins = 0

    def run(self):
        print("run")

        matches_total = 0

        for i, case in enumerate(self._cases):
            # print(case)
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

    def run4(self):
        print('run4')

        all = 0
        for i, case in enumerate(self._cases):
            sin = case[0]
            groups = case[1]

            match_count1 = 0
            match_count2 = 0

            s = sin
            possible = self.make_potential_strings(s, groups)
            for item in possible:
                if self.check_match(s, item):
                    print(item)
                    match_count1 += 1

            if sin.endswith('#'):
                s2 = sin
                s2 = sin + '?'
            # groups = groups * 2
            possible = self.make_potential_strings(s2, groups)
            for item in possible:
                if self.check_match(s2, item):
                    match_count2 += 1

            extra = match_count2 / match_count1
            total = match_count1 * math.pow(extra, 4)

            print("case: %d, match_count1: %d match_count2: %d extra: %f total: %d" %
                  (i, match_count1, match_count2, extra, int(total)))
            all += total

        print("final", all)

    def run2(self):
        print("run2")

        matches_total = 0

        for i, case in enumerate(self._cases):

            print("-------------------")
            print(case[0],      case[1])

            sin = case[0]
            groups = case[1]

            match_count1 = 0
            match_count2 = 0
            match_count3 = 0
            match_count4 = 0

            s = sin
            # for j in range(len(sin)):
            #     if sin[j] == '?':
            #         s = s + '?'
            #     else:
            #         break

            possible = self.make_potential_strings(s, groups)
            for item in possible:
                if self.check_match(s, item):
                    match_count1 += 1
                    # print(item)

            # Consider adding to front only
            if sin.endswith('#'):
                s = '.' + sin
            else:
                s = '?' + sin

            possible = self.make_potential_strings(s, groups)
            for item in possible:
                if self.check_match(s, item):
                    match_count2 += 1
                    # print(item)

            # consider adding to end only
            if sin.startswith('#'):
                s = sin + '.'
            else:
                s = sin + '?'

            possible = self.make_potential_strings(s, groups)
            for item in possible:

                if self.check_match(s, item):
                    match_count3 += 1
                    # print(item)

            # Consider adding to front only
            if sin.endswith('#'):
                s = '.' + sin
            else:
                s = '?' + sin

            if sin.startswith('#'):
                s = s + '.'
            else:
                s = s + '?'

            possible = self.make_potential_strings(s, groups)
            for item in possible:

                if self.check_match(s, item):
                    match_count4 += 1


            match_count_A = math.pow(match_count2, 4) * match_count1
            match_count_B = math.pow(match_count3, 4) * match_count1
            match_count_C = math.pow(match_count4, 2) * math.pow(match_count1, 3)
            match_count_D = math.pow(match_count1, 2) * match_count2 * match_count3 * match_count4
            match_count_E = math.pow(match_count2, 2) * math.pow(match_count3, 2) * match_count1
            print(match_count_A, match_count_B, match_count_C, match_count_D, match_count_E)
            # print("case %d: "got %d potential matches (%d %d %d)" % (i, match_count, match_count1, match_count2, match_count3))
            matches_total += max(match_count_A, match_count_B, match_count_C, match_count_D, match_count_E)
            # input("continue...")

        print("part 2: total matches: %d" % matches_total)

    def run3(self):
        print("run3")

        matches_total = 0

        for i, case in enumerate(self._cases):

            if i != 5: continue

            s = case[0]
            groups = case[1]

            min_length = sum(groups)
            # min_length = len(s) + 1
            # bins = len(groups) + 1
            start_pos = 0
            end_pos = start_pos +  min_length

            s5 = s + '?' + s + '?' + s + '?' + s + '?' + s
            print("-------------------------------------------")
            print(s5, groups)

            final_pos = len(s5)
            matches = 0
            last_matches = 0

            match_count_list = []
            while True:
                consider = s5[start_pos:end_pos]
                print("consider", consider)

                possible = self.make_potential_strings(consider, groups)

                # print("possible_count", len(possible))
                if len(possible) == 0:
                    end_pos += 1
                else:

                    for item in possible:
                        # print(item)
                        if self.check_match(consider, item):
                            matches += 1
                            print(item)

                    input("continue (%d matches)" % matches)

                    if matches:
                        print("there were some matches", matches, last_matches)
                        # if True:
                        if matches <= last_matches:
                            # advanve to next string segment
                            # if matches != 15:
                            #
                            #     print("---- GOT %d matches!!!!" % last_matches)
                            #     match_count_list.append(last_matches)
                            #     start_pos = end_pos - 2
                            #     end_pos = start_pos + min_length
                            # else:
                            #     print("---- GOT %d matches!!!!" % matches)

                            match_count_list.append(matches)
                            start_pos = end_pos - 1
                            end_pos = start_pos + min_length

                            print("start_pos", start_pos, "end_pos", end_pos)
                            last_matches = 0
                            matches = 0
                        else:
                            print("matches", matches, "last_matches", last_matches)
                            last_matches = matches
                            matches = 0
                            end_pos += 1
                    else:
                        #print("matches", matches, "last_matches", last_matches)
                        # There were zero matches.. tye again with a longer string
                        end_pos += 1

                if end_pos >= final_pos:
                    print("end_pos", end_pos, "matches", matches, "last_matches", last_matches)
                    if matches:
                        match_count_list.append(matches)
                    break

            print(match_count_list)
            c = 1
            for item in match_count_list:
                c = c * item

            print("MATCHES FOR STRING", c)
            matches_total += c

        print("part 2: total matches: %d" % matches_total)

    def test1(self):

        print(4, 6)
        for item in self.yield_bins(4, 6):
            print(item)

        print(5, 5)
        for item in self.yield_bins(5, 5):
            print(item)

        print(6, 4)
        for item in self.yield_bins(6, 4):
            print(item)


    def yield_bins2(self, bins, balls):

        ball_list = [i for i in range(balls+1)]

        # print(ball_list)

        result = []

        x = itertools.combinations_with_replacement(ball_list, bins)
        #x = itertools.permutations(ball_list, bins)
        for thing in x:
            # print(thing)
            if sum(thing) != balls:
                # print("no good")
                continue

            # print("get permutations", thing)
            for item in itertools.permutations(thing, bins):
                # print(item)
                try:
                    for j in range(1, bins-1):
                    # print("check l[%d]: %d" % (j, l[j]))
                        if item[j] == 0:
                            # print("this result is no good")
                            raise ValueError

                    # print(item)
                    result.append(item)

                except:
                    continue

        result = list(set(result))
        for item in result:
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
                raise ValueError("what the !?!?!? ")

            new = ''
            for i in range(group_count):
                new = new + '.' * item[i]
                new = new + '#' * groups[i]

            new += '.' * item[group_count]
            result.append(new)

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

    def test2(self):
        """
        ???.???..?.?#.?..?? [1, 1]
        :return:
        """
        s = "?###????????"
        groups = [3,2,1]

        # s = '.??..??...?##.'
        # s = '.??..??...?##.'
        # groups = [1, 1, 3]

        # s = s +'?' + s + '?' + s + '?' + s + '?' + s
        # groups *= 5

        s = s + '?' + s
        groups *= 2

        match_count = 0
        print(s)
        print("-------------")

        possible = self.make_potential_strings(s, groups)
        for item in possible:

            if self.check_match(s, item):
                match_count += 1
                print(item)

        print("Got %d potential matches" % match_count)

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
    # runner.run()
    #runner.run4()
    # runner.run2()
    runner.test2()
