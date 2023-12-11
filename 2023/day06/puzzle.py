import sys


class Runner(object):

    def __init__(self, filename):

        if filename == 'test':
            self._races = [
                ( 7,   9),
                (15,  40),
                (30, 200),
            ]
        else:
            self._races = [
                (51,  222),
                (92, 2031),
                (68, 1126),
                (90, 1225),
            ]

    def ways_to_beat_record(self, race):

        duration = race[0]
        record = race[1]
        beat_count = 0

        for hold in range(duration):

            speed = hold
            distance = (duration - hold ) * speed

            if distance > record:
                beat_count += 1

        return beat_count


    def run1(self):

        result = 1
        for race in self._races:
            beat_count = self.ways_to_beat_record(race)

            print('Race: %s beat_count: %d' % (race, beat_count))
            result *= beat_count

        print("part 1 result:", result)

    def run2_test(self):

        self._races = [
            (71530, 940200)
        ]

        self.run1()

    def run2_prod(self):
        self._races = [
            (51926890, 222203111261225)
        ]

        self.run1()

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run1()
    runner.run2_test()
    runner.run2_prod()
