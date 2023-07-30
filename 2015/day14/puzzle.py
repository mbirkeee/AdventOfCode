import sys
import itertools

class Deer(object):

    def __init__(self, name, speed, duration, rest):

        self._name = name
        self._speed = speed
        self._duration = duration
        self._rest = rest
        self._points = 0

    def wins(self):
        self._points += 1

    def get_points(self):
        return self._points

    def get_distance(self, t):

        cycle_time = self._duration + self._rest

        cycles = int(t // cycle_time )
        distance = cycles * self._speed * self._duration

        remainder = t % cycle_time

        if remainder > self._duration:
            remainder = self._duration

        distance +=  self._speed * remainder

        return distance

    def get_name(self):
        return self._name

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

        self._deer_list = []

        self.initialize()


    def initialize(self):
        print("initialize")

        for line in self._lines:
            parts = line.split(' ')
            # print(parts)
            # print(len(parts))

            if len(parts) != 15:
                raise ValueError("bad number of parts")

            name = parts[0]
            speed = int(parts[3])
            duration = int(parts[6])
            rest = int(parts[13])

            print(name, speed, duration, rest)
            deer = Deer(name, speed, duration, rest)
            self._deer_list.append(deer)

    def run(self):

        print("run")

        for t in range(1, 2504):

            result = {}
            max_postion = 0

            for deer in self._deer_list:
                name = deer.get_name()
                position = deer.get_distance(t)
                # print("t: %d name: %s position: %d" % (t, name, position))
                result[deer] = position
                if position > max_postion:
                    max_postion = position

            for deer, position in result.items():
                if position == max_postion:
                    deer.wins()

        for deer in self._deer_list:
            print("%s points %d" % ( deer.get_name(), deer.get_points() ))

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


