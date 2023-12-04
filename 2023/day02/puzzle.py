import sys

class ExceptionDone(Exception):
    pass

class ExceptionNotPossible(Exception):
    pass

class Runner(object):

    def __init__(self, filename):

        self._max_green = 0
        self._max_blue = 0
        self._max_red = 0

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

        self._program = []
        print("read %d lines" % len(self._lines))
        self.initialize()


    def initialize(self):

        self._max_green = 13
        self._max_blue = 14
        self._max_red = 12

        print("initialize")

        total = 0
        total_power = 0

        for line in self._lines:
            parts = line.split(':')

            game = parts[0]
            game_id = game.split(' ')
            game_id = int(game_id[1])

            print("game id: %d" % game_id)

            all_games = parts[1]
            game_list = all_games.split(';')

            saw_red = 0
            saw_green = 0
            saw_blue = 0

            fail_count = 0

            try:
                for game in game_list:
                    game = game.strip()

                    # print(game)
                    draws = game.split(',')
                    # print(draws)
                    for draw in draws:
                        draw = draw.strip()
                        # print("draw:", draw)
                        draw_parts = draw.split(' ')
                        count = int(draw_parts[0].strip())
                        color = draw_parts[1].strip()
                        print("game_id: %d -> draw %d %s" % (game_id, count, color))

                        if color == 'red':
                            if count > saw_red:
                                saw_red = count

                            if count > self._max_red:
                                fail_count += 1
                                #saw_red = self._max_red
                                # raise ExceptionNotPossible()

                        elif color == 'green':
                            if count > saw_green:
                                saw_green = count

                            if count > self._max_green:
                                fail_count += 1
                                #saw_green = self._max_green
                                # raise ExceptionNotPossible()

                        elif color == 'blue':
                            if count > saw_blue:
                                saw_blue = count

                            if count > self._max_blue:
                                fail_count += 1
                                #saw_blue = self._max_blue
                                # raise ExceptionNotPossible()

                if fail_count == 0:
                    print("game %d is possible!!" % game_id)
                    total += game_id

                power = saw_red * saw_green * saw_blue
                total_power += power
                print("power: %d" % power)

            except ExceptionNotPossible:
                print("game_id %d not possible" % game_id)

            print("total", total)
            print("total power", total_power)

    def run(self):

        print("run")

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
