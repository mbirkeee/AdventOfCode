
class CPU(object):

    def __init__(self):
        self._queue = []
        self._cycle = 0
        self._register_x = 1

    def add_instruction(self, instruction):
        # print("add instruction: %s" % instruction)
        self._queue.append(instruction)

    def tick(self):

        self._cycle += 1
        if self._cycle == 1:
            return 1

        try:
            instruction = self._queue.pop(0)
        except:
            return None

        # print("run: %s" % instruction)

        parts = instruction.split()
        cmd = parts[0].strip()
        if len(parts) > 1:
            arg = parts[1].strip()
        else:
            arg = None


        if cmd == 'noop':
            # print("CMD NOOP")
            pass

        elif cmd == 'addx':
            # print("CMD: addx")
            internal_command = 'addx_done ' + arg
            self._queue.insert(0, internal_command)

        elif cmd == 'addx_done':
            value = int(arg)
            # print("cycle: %d regx: %d CMD: ADD %d" % (self._cycle, self._register_x, value))
            self._register_x += value

        else:
            raise ValueError('unsupported command: %s' % cmd)

        return self._cycle

    def get_register_x(self):
        return self._register_x

class Runner(object):

    def __init__(self):
        self._file_name = 'input_real.txt'
        # self._file_name = 'input_test.txt'
        # self._file_name = 'input_test2.txt'
        self._cpu = CPU()

    def run(self):

        fp = open(self._file_name, 'r')
        for line in fp:
            self._cpu.add_instruction(line.strip())

        fp.close()
        self.execute()

        print('done')

    def execute(self):

        for row in range(6):
            s = ''
            for col in range(40):
                self._cpu.tick()
                center_pos = self._cpu.get_register_x()

                if abs(center_pos - col) <= 1:
                    s += '#'
                else:
                    s += ' '

            print(s)

    def execute1(self):

        part1 = 0

        check_at_cycle = [20, 60, 100, 140, 180, 220]

        while True:
            cycle = self._cpu.tick()

            if cycle is None:
                break

            if cycle in check_at_cycle:
                value = self._cpu.get_register_x()
                print("CYCLE: %d REG X: %d" % (cycle, value))
                part1 += (value * cycle)


        print("PART 1: %d" % part1)

if __name__ == '__main__':
    runner = Runner()
    runner.run()
