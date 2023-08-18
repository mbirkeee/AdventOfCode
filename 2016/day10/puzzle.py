import sys
import copy
import itertools
from collections import Counter
import numpy as np

class ExceptionDone(Exception):
    pass

class Bot(object):

    def __init__(self, number, bot_map, bin_map):
        self._num = number

        self._bot_map = bot_map
        self._bin_map = bin_map

        self._value1 = None
        self._value2 = None

        self._low_to_bot = None
        self._low_to_output = None
        self._high_to_bot = None
        self._high_to_output = None

    def push(self, value):
        if self._value1 is None:
            self._value1 = value
        elif self._value2 is None:
            self._value2 = value
        else:
            raise ValueError("cant push... full!")

    def set_operation_low(self, kind, value):
        if kind == 'bot':
            self._low_to_bot = value
        elif kind == 'output':
            self._low_to_output = value

    def set_operation_high(self, kind, value):
        if kind == 'bot':
            self._high_to_bot = value
        elif kind == 'output':
            self._high_to_output_to_output = value

    def run(self):
        if self._value1 is None or self._value2 is None:
            # print("BOT: %3d: can't run" % self._num)
            pass
        else:
            print("BOT: %3d: can run -----------------!!" % self._num)


            if self._value1 > self._value2:
                print("swap")
                self._value1, self._value2 = self._value2, self._value1

        #    if self._value1 == 17 and self._value2 == 61:
        #        raise ValueError("bot %d compared 17 to 61" % self._num)

            if self._low_to_output is not None:
                print("low", self._value1, "to output", self._low_to_output)
                bin_list = self._bin_map.get(self._low_to_output, [])
                bin_list.append(self._value1)
                self._bin_map[self._low_to_output] = bin_list
                print(self._bin_map)

            elif self._low_to_bot is not None:
                print("low", self._value1, "to bot", self._low_to_bot)
                bot = self._bot_map.get(self._low_to_bot)
                bot.push(self._value1)

            self._value1 = None

            if self._high_to_output is not None:
                print("high", self._value2, "to output", self._high_to_output)
                bin_list = self._bin_map.get(self._high_to_output, [])
                bin_list.append(self._value2)
                self._bin_map[self._high_to_output] = bin_list
                print(self._bin_map)

            elif self._high_to_bot is not None:
                print("high", self._value2, "to bot", self._high_to_bot)
                bot = self._bot_map.get(self._high_to_bot)
                bot.push(self._value2)

            self._value2 = None

class Runner(object):

    def __init__(self, filename):

        self._lines = []

        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                if len(line) == 0:
                    continue
                self._lines.append(line)

        finally:
            if fp: fp.close()

        print("read %d lines" % len(self._lines))

        self._bot_map = {}
        self._bin_map = {}

        self.initialize()

    def get_bot(self, bot_num):

        bot = self._bot_map.get(bot_num)

        if bot is None:
            bot = Bot(bot_num, self._bot_map, self._bin_map)
            self._bot_map[bot_num] = bot

        return bot

    def init_value(self, line):

        parts = line.split(' ')
        if len(parts) != 6:
            raise ValueError("bad input")

        v = int(parts[1])
        bot_num = int(parts[5])
        bot = self.get_bot(bot_num)
        bot.push(v)

    def init_bot(self, line):

        parts = line.split(' ')
        if len(parts) != 12:
            raise ValueError("bad input")

        bot_num = int(parts[1])
        bot = self.get_bot(bot_num)

        low_val = int(parts[6])
        high_val = int(parts[11])
        print(low_val, high_val)

        bot.set_operation_low(parts[5], low_val)
        bot.set_operation_high(parts[10], high_val)

    def initialize(self):

        print("initialize")

        for line in self._lines:

            if line.startswith('value'):
                self.init_value(line)

            elif line.startswith('bot'):
                self.init_bot(line)

            else:
                raise ValueError("bad input")

    def run(self):
        print("called")

        while True:
            for bot_num, bot in self._bot_map.items():
                bot.run()
                # input("continue...")

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
