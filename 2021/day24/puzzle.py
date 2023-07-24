"""

"""
import numpy as np
import sys
import math

# from programs import PROGRAM_1
# from programs import PROGRAM_2
# from programs import PROGRAM_3
# from programs import PROGRAM_4
# from programs import PROGRAM_5
# from programs import PROGRAM_6
#
# from programs import PROGRAM_11
# from programs import PROGRAM_12
#
# from programs import PROGRAM_13
# from programs import PROGRAM_14


class ExceptionDone(Exception):
    pass

class ALU(object):
    """
    inp a - Read an input value and write it to variable a.
    add a b - Add the value of a to the value of b, then store the result in variable a.
    mul a b - Multiply the value of a by the value of b, then store the result in variable a.
    div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
    mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
    eql a b - If the value of a and b are equal, then store the value 1 in variabl
    """
    def __init__(self, get_next_input):

        self._get_next_input = get_next_input
        self._w = 0
        self._x = 0
        self._y = 0
        self._z = 0

        self._print_flag = False

    def print_enable(self, value):
        self._print_flag = value

    def status(self):
        print("------------------------")
        print("W: %10d" % self._w)
        print("X: %10d" % self._x)
        print("Y: %10d" % self._y)
        print("Z: %10d" % self._z)

    def print(self):

        if not self._print_flag:
            return

        print("------------------------")
        print("W: %10d" % self._w)
        print("X: %10d" % self._x)
        print("Y: %10d" % self._y)
        print("Z: %10d" % self._z)

    def execute(self, line):

        # print("execute line: %s" % line)

        parts = line.split(' ')
        inst = parts[0]
        arg1 = parts[1]
        if len(parts) > 2:
            arg2 = parts[2]

        if inst == 'inp':
            self.inp(arg1)

        elif inst == 'add':
            self.add(arg1, arg2)

        elif inst == 'mul':
            self.mul(arg1, arg2)

        elif inst == 'div':
            self.div(arg1, arg2)

        elif inst == 'mod':
            self.mod(arg1, arg2)

        elif inst == 'eql':
            self.eql(arg1, arg2)
        else:
            raise ValueError(" invalid instruction")

        if self._print_flag:
            self.print()
            input("continue...")

    def get(self, reg):

        if reg == 'w':
            return self._w

        if reg == 'x':
            return self._x

        if reg == 'y':
            return self._y

        if reg == 'z':
            return self._z

        return int(reg)


    def put(self, reg, value):

        if reg == 'w':
            self._w = value
        elif reg == 'x':
            self._x = value
        elif reg == 'y':
            self._y = value
        elif reg == 'z':
            self._z = value

        else:
            raise ValueError("invalid register")

    def inp(self, reg):

        value = int(self._get_next_input())
        if self._print_flag: print("INP: %s %d" % (reg, value) )
        self.put(reg, value)

    def add(self, reg, arg):
        if self._print_flag: print("ADD: %s %s" % (reg, arg) )

        val1 = self.get(reg)
        val2 = self.get(arg)

        self.put(reg, val1 + val2)

    def mul(self, reg, arg ):
        if self._print_flag: print("MUL: %s %s" % (reg, arg) )

        val1 = self.get(reg)
        val2 = self.get(arg)

        self.put(reg, val1 * val2)

    def div(self, reg, arg ):
        if self._print_flag: print("DIV: %s %s" % (reg, arg) )

        val1 = self.get(reg)
        val2 = self.get(arg)

        self.put(reg, int(math.floor(val1 // val2 )) )

    def mod(self, reg, arg):
        if self._print_flag: print("MOD: %s %s" % (reg, arg) )

        val1 = self.get(reg)
        val2 = self.get(arg)

        self.put(reg, val1 % val2)

    def eql(self, reg, arg):
        if self._print_flag: print("EQL: %s %s" % (reg, arg) )

        val1 = self.get(reg)
        val2 = self.get(arg)

        if val1 == val2:
            self.put(reg, 1)
        else:
            self.put(reg, 0)

    def reset(self):
        self._w = 0
        self._x = 0
        self._y = 0
        self._z = 0

class Runner(object):

    def __init__(self, filename):

        self._alu = ALU(self.get_next_input)

        self._input_data = []
        self._input_data_index = 0
        self._programs = {}

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

        self._monad = self._lines

        print("read %d lines" % len(self._lines))

    def get_next_input(self):

        r = self._input_data[self._input_data_index]
        self._input_data_index += 1

        # print("get next input called; returning %s" % repr(r))
        return r

    def get_program(self, index):

        program = self._programs.get(index)
        if program is not None:
            return program

        program = []

        inp_count = 0
        in_program = False

        for line in self._lines:
            if line == 'inp w':
                if not in_program:
                    if inp_count == index:
                        in_program = True
                        program.append(line)
                else:
                    break
                inp_count += 1
            else:
                if in_program:
                    program.append(line)

        if len(program) > 0:
            self._programs[index] = program
            return program

    def run_program(self, program, input_data, reset_alu=True):


        if isinstance(input_data, int):
            if input_data > 9:
                raise ValueError("input > 9 not yet implemented")
            self._input_data = [input_data]
        else:
            self._input_data = [c for c in input_data]

        self._input_data_index = 0

        if reset_alu:
            self._alu.reset()

        for line in program:
            self._alu.execute(line)

    def run_monad(self, input_data):

        self._input_data = [c for c in input_data]
        self._input_data_index = 0

        self._alu.reset()
        for line in self._monad:
            self._alu.execute(line)

        result = self._alu.get('z')
        print("MONAD RESULT: %d" % result)

    def run(self):
        print("run")

        z_dict = {0 : 0}

        for digit in range(14):

            program = self.get_program(digit)
            # print(program)

            z_dict_new = {}
            print("digit %d checking %d z value " % (digit, len(z_dict)))

            for z, val in z_dict.items():

                val_base = val * 10

                for d in range(1,10):
                    val_new = val_base + d
                    self._alu.reset()
                    self._alu.put('z', z)

                    self.run_program(program, d, reset_alu=False)
                    z_new = self._alu.get('z')

                    # Find Biggest
                 #   val_old = z_dict_new.get(z_new, 0)
                 #   if val_new > val_old:
                 #       z_dict_new[z_new] = val_new

                    # Find smallest
                    val_old = z_dict_new.get(z_new)
                    if val_old is None or val_new < val_old:
                        z_dict_new[z_new] = val_new


            z_dict = z_dict_new

            # if digit == 6:
            #     break

            for z in range(10000):
                result = z_dict.get(z)
                if result is not None:
                    print("Z: %d max val: %d" % (z, result))
                    break


        max_z_ever = 0

        for z, v in z_dict.items():
            # print("Z: %d max: %d" % (z, v))

            if z > max_z_ever:
                max_z_ever = z

        print("max_z_ever", max_z_ever)

        for z in range(10000):
            result = z_dict.get(z)
            if result is not None:
                print("Z: %d max val: %d" % (z, result))
                break


        print("done")
        # print(z_values)

    def run_backwards(self):

        loop_count = 0

        want_dict = {0:0}

        for digit in range(13, 5, -1):
            loop_count += 1
            program = self.get_program(digit)

            z_limit = int(10 * math.pow(9, loop_count))
            print("digit: %d zlimit: %d" % (digit, z_limit))


            temp = {}
            # print("want dict: %s" % repr(want_dict))

            for d in range(1, 10):

                # print("test digit value", d)

                for z in range(0, z_limit):

                    self._alu.reset()
                    self._alu.put('z', z)
                    self.run_program(program, d, reset_alu=False)

                    result = self._alu.get('z')

                    if result in want_dict.keys():
                        # print("val %d input z %d produces result %d" % (d, z, result))
                        temp[z] = d

            print("targets: %d" % len(temp))
            want_dict = temp
            if digit == 8:
                break

    def print_enable(self, value):
        self._alu.print_enable(value)


    def test_programs(self):

        for i in range(15):
            program = self.get_program(i)
            if program is None:
                print("%d: no program" % i)
            else:
                print("program %d" % i)
                for line in program:
                    print("  %s" % line)

    def test_program_5(self):

        program = self.get_program(5)

        print(program)

        for z in range(100):
            self._alu.reset()
            self._alu.put('z', z)
            self.run_program(program, 2, reset_alu=False)
            result = self._alu.get('z')
            print("Z: %d result: %d" % (z, result))

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
#    runner.run_backwards()

#    runner.test2()
#    runner.test3()
#    runner.test4()
#    runner.test_stage_14()

#    runner.test_stage_11()

#    runner.print_enable(True)

 #   runner.run_monad("13579246899999")
 #   runner.run_monad("99999999999999")
#    runner.run_monad("99299513899971")

    # runner.run()
