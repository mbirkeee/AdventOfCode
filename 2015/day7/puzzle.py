"""

"""
import numpy as np
import sys
import math
import itertools

NOT     = "NOT"
AND     = "AND"
OR      = "OR"
LSHIFT  = "LSHIFT"
RSHIFT  = "RSHIFT"
INPUT   = "INPUT"

class Wire(object):

    def __init__(self, runner, name):

        self._runner = runner
        self._name = name
        self._value = None
        self._op = None
        self._input1 = None
        self._input2 = None

        print("wire: '%s'" % self._name)

    def get_name(self):
        return self._name

    def set_input1(self, input):
        try:
            self._input1 = int(input)
        except:
            self._input1 = input

    def set_input2(self, input):
        try:
            self._input2 = int(input)
        except:
            self._input2 = input

    def set_op(self, op):
        self._op = op


    def get_value(self):

        if self._value is not None:
            return self._value

    def get_input1(self):
        if self._input1 is None:
            return

        if isinstance(self._input1, str):
            wire = self._runner.get_wire(self._input1)
            value = wire.get_value()

            if value is None:
                return None
            if value is not None:
                self._input1 = value
            return value
        else:
            return self._input1

    def get_input2(self):
        if self._input2 is None:
            return

        if isinstance(self._input2, str):
            wire = self._runner.get_wire(self._input2)
            value = wire.get_value()

            if value is None:
                return None
            if value is not None:
                self._input2 = value
            return value
        else:
            return self._input2

    def process(self):
        if self._value is not None:
            return

        # print("processing.... %s %s %s" % (self._op, repr(self._input1), repr(self._input2)))

        value1 = self.get_input1()
        value2 = self.get_input2()

        # print("processing.... value1: %s value2: %s" % (repr(value1), repr(value2)))

        if self._op in [AND, OR, LSHIFT, RSHIFT]:
            if value1 is None or value2 is None:
                return

            if self._op == OR:
                self._value = (value1 | value2) & 0xffff

            elif self._op == AND:
                self._value = (value1 & value2) & 0xffff

            elif self._op == RSHIFT:
                self._value = (value1 >> value2) & 0xffff

            elif self._op == LSHIFT:
                self._value = (value1 << value2) & 0xffff

            else:
                raise ValueError('bad')

            print("set value to", self._value)

        elif self._op == INPUT:
            if value1 is None:
                return
            self._value = value1
            print("set value to", self._value)

        elif self._op == NOT:
            if value1 is None:
                return

            self._value = (~value1) & 0xffff
            print("set value to", self._value)

        else:
            raise ValueError('bad')

class Runner(object):

    def __init__(self, filename):

        self._wire_dict = {}
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

        self.initialize()

    def initialize(self):

        wire_dict = {}

        for line in self._lines:
            parts = line.split(' ')
            # print(parts)
            # print(len(parts))

            wire_name = parts[-1]
            wire_dict[wire_name] = True

            wire = Wire(self, parts[-1])

            if len(parts) == 3:
                # this is a direct input
                wire.set_input1(parts[0])
                wire.set_op(INPUT)

            elif len(parts) == 4:
                # Sanity test
                wire.set_op(parts[0])
                wire.set_input1(parts[1])

            elif len(parts) == 5:
                wire.set_input1(parts[0])
                wire.set_input2(parts[2])
                wire.set_op(parts[1])

            self._wire_dict[wire.get_name()] = wire

    def get_wire(self, name):
        return self._wire_dict[name]

    def run(self):

        print("run")

        count = 0
        while True:

            not_complete = 0
            complete = 0
            for wire in self._wire_dict.values():

                wire.process()
                value = wire.get_value()
                if value is None:
                    not_complete += 1
                else:
                    complete += 1

            print("complete", complete, "not complete", not_complete)

            if not_complete == 0:
                break

            # count += 1
            # if count > 10:
            #     break


        # Example
        for wire in self._wire_dict.values():
            print("WIRE: %s value: %d" % (wire.get_name(), wire.get_value()))

        # Part1
        wire = self._wire_dict.get('a')
        print("WIRE: %s value: %d" % (wire.get_name(), wire.get_value()))

        # print(wire_dict)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
