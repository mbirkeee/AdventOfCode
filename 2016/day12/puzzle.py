import sys


class ExceptionDone(Exception):
    pass

class CPU(object):

    def __init__(self):

        self._reg_a = 0
        self._reg_b = 0
        self._reg_c = 1
        self._reg_d = 0

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
        print("D:", self._reg_c)

    def get(self, item):
        if isinstance(item, int):
            return item

        if item == 'a':
            return self._reg_a
        elif item == 'b':
            return self._reg_b
        elif item == 'c':
            return self._reg_c
        elif item == 'd':
            return self._reg_d
        else:
            raise ValueError("bad")

    def put(self, reg, value):

        if not isinstance(value, int):
            raise ValueError("bad value: %s" % repr(value))

        if reg == 'a':
            self._reg_a = value
        elif reg == 'b':
            self._reg_b = value
        elif reg == 'c':
            self._reg_c = value
        elif reg == 'd':
            self._reg_d = value
        else:
            raise ValueError("bad reg")

    def inst_cpy(self, inst):
        # print("cpy")
        v = self.get(inst[1])
        self.put(inst[2], v)
        self._program_counter += 1

    def inst_jnz(self, inst):
        # print("jnz")
        v = self.get(inst[1])
        if v == 0:
            self._program_counter += 1
        else:
            self._program_counter += inst[2]

    def inst_inc(self, inst):
        # print("inc")
        v = self.get(inst[1])
        self.put(inst[1], v + 1)
        self._program_counter += 1

    def inst_dec(self, inst):
        # print("dec")
        v = self.get(inst[1])
        self.put(inst[1], v - 1)
        self._program_counter += 1

    def tick(self):

        if self._program_counter < 0 or self._program_counter >= self._program_len:
            raise ExceptionDone("done")

        instruction = self._program[self._program_counter]
        # print("pc: %d run instruction: %s" %(self._program_counter, repr(instruction)))

        opcode = instruction[0]

        if opcode == 'cpy':
            self.inst_cpy(instruction)
        elif opcode == 'jnz':
            self.inst_jnz(instruction)
        elif opcode == 'inc':
            self.inst_inc(instruction)
        elif opcode == 'dec':
            self.inst_dec(instruction)
        else:
            raise ValueError("bad inst: %s" % opcode)

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
            print(line)
            parts = line.split(' ')
            opcode = parts[0]

            a1 = parts[1].strip(',')
            try:
                arg1 = int(a1)
            except:
                arg1 = a1

            try:
                a2 = parts[2]
                try:
                    arg2 = int(a2)
                except:
                    arg2 = a2
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
