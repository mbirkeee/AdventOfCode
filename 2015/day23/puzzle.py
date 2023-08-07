import sys


class ExceptionDone(Exception):
    pass

class CPU(object):

    def __init__(self):

        self._reg_a = 1
        self._reg_b = 0
        self._reg_c = 0

        self._program = None
        self._program_counter = 0
        self._program_len = 0

    def load(self, program):
        self._program = program
        self._program_len = len(program)

    def print_reg(self):
        print("A:", self._reg_a)
        print("B:", self._reg_b)
        print("C:", self._reg_c)

    def inst_hlf(self, inst):
        reg = inst[1]
        if reg == 'a':
            self._reg_a //= 2
        elif reg == 'b':
            self._reg_b //= 2
        elif reg == 'c':
            self._reg_c //= 2
        else:
            raise ValueError("bad input")

        self._program_counter += 1

    def inst_tpl(self, inst):
        reg = inst[1]
        if reg == 'a':
            self._reg_a *= 3
        elif reg == 'b':
            self._reg_b *= 3
        elif reg == 'c':
            self._reg_c *= 3
        else:
            raise ValueError("bad input")

        self._program_counter += 1

    def inst_inc(self, inst):

        reg = inst[1]
        if reg == 'a':
            self._reg_a += 1
        elif reg == 'b':
            self._reg_b += 1
        elif reg == 'c':
            self._reg_c += 1
        else:
            raise ValueError("bad input")

        self._program_counter += 1

    def inst_jmp(self, inst):

        self._program_counter += inst[1]

    def inst_jio(self, inst):
        """
        Jump if register even
        """
        reg = inst[1]
        jump = False
        if reg == 'a':
            if self._reg_a == 1:
                jump = True
        elif reg == 'b':
            if self._reg_b  == 1:
                jump = True
        elif reg == 'c':
            if self._reg_c  == 1:
                jump = True
        else:
            raise ValueError("bad input")

        if jump:
            self._program_counter += inst[2]
        else:
            self._program_counter += 1

    def inst_jie(self, inst):
        """
        Junp if register odd
        """
        reg = inst[1]
        jump = False
        if reg == 'a':
            if self._reg_a % 2 == 0:
                jump = True
        elif reg == 'b':
            if self._reg_b % 2 == 0:
                jump = True
        elif reg == 'c':
            if self._reg_c % 2 == 0:
                jump = True
        else:
            raise ValueError("bad input")

        if jump:
            self._program_counter += inst[2]
        else:
            self._program_counter += 1

    def tick(self):

        if self._program_counter < 0 or self._program_counter >= self._program_len:
            raise ExceptionDone("done")

        instruction = self._program[self._program_counter]
        print("pc: %d run instruction: %s" %(self._program_counter, repr(instruction)))

        opcode = instruction[0]

        if opcode == 'hlf':
            self.inst_hlf(instruction)
        elif opcode == 'tpl':
            self.inst_tpl(instruction)
        elif opcode == 'inc':
            self.inst_inc(instruction)
        elif opcode == 'jmp':
            self.inst_jmp(instruction)
        elif opcode == 'jie':
            self.inst_jie(instruction)
        elif opcode == 'jio':
            self.inst_jio(instruction)
        else:
            raise ValueError("bad inst")



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

        self._program = []
        print("read %d lines" % len(self._lines))
        self.initialize()


    def initialize(self):

        print("initialize")


        for index, line in enumerate(self._lines):
            # print(line)
            parts = line.split(' ')
            opcode = parts[0]

            try:
                arg1 = parts[1].strip(',')
                arg1 = int(arg1)
            except:
                pass

            try:
                arg2 = int(parts[2])
            except:
                arg2 = None

            self._program.append((opcode, arg1, arg2))

            # parts = line.split(' ')
            # print(len(parts))
            # parts = [part.strip(',') for part in parts]
            # parts = [part.strip(':') for part in parts]

    def run(self):

        print("run")

        cpu = CPU()
        cpu.load(self._program)

        while True:
            try:
                cpu.tick()
            except ExceptionDone as err:
                print(err)
                break

        cpu.print_reg()

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
