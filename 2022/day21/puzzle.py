class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self):
        # self._file_name = 'input_test.txt'
        self._file_name = 'input_real.txt'

        self._monkeys = {}
        self._yelled = {}

    def run(self):

        fp = open(self._file_name, 'r')
        lines = []
        for line in fp:
            line = line.strip()
            lines.append(line)

        fp.close()

        for line in lines:
            self.process_line(line)


        self.compute(lines, humn=3678125408017)

        # try:
        #     while True:
        #         changed = self.work_backwards()
        #         if changed is 0:
        #             break
        # except:
        #     pass

        # self.print_monkeys()

    def compute(self, lines,  humn=5):

        self._monkeys = {}
        self._yelled = {}

        for line in lines:
            self.process_line(line)

        state = self._monkeys['humn']
        state[0] = humn

        try:
            while True:

                self.yell()
                self.operate()

        except ExceptionDone:
             pass

    def work_backwards(self):

        change_count = 0
        for monkey, state in self._monkeys.items():
            if state[0] is not None:
                continue

            if state[1] == 'humn' or state[2] == 'humn':
                continue

            monkey1 = self._monkeys[state[1]]


            val1 = monkey1[0]
            if val1 is None:
                continue

            monkey2 = self._monkeys[state[2]]
            val2 = monkey2[0]
            if val2 is None:
                continue

            change_count += 1
            oper = state[3]
            if oper == '+':
                state[0] = val1 + val2

            elif oper == '*':
                state[0] = val1 * val2

            elif oper == '/':
                state[0] = val1 / val2

            elif oper == '-':
                state[0] = val1 - val2

        print("chnaged: %d" % change_count)
        return change_count

    def print_monkeys(self):

        for monkey, state in self._monkeys.items():
            if state[0] is not None:
                print("%s: %d" % (monkey, state[0]))
            else:
                print("%s: %s %s %s" % (monkey, state[1], state[3], state[2]) )

    def operate(self):
        for monkey, state in self._monkeys.items():
            val1 = self._yelled.get(state[1])

            if val1 is None:
                continue
            val2 = self._yelled.get(state[2])

            if val2 is None:
                continue

            oper = state[3]
            if oper == '+':
                state[0] = val1 + val2

            elif oper == '*':
                state[0] = val1 * val2

            elif oper == '/':
                state[0] = val1 / val2

            elif oper == '-':
                state[0] = val1 - val2

            elif oper == '=':
                print("ROOT got val1 %s val2: %d diff: %f" % (val1, val2, val2-val1))
                raise ExceptionDone

    def yell(self):

        yelled = {}
        for monkey, state in self._monkeys.items():

            if state[0] is not None:
                yelled[monkey] = state[0]

        for name, number in yelled.items():
            del self._monkeys[name]
            self._yelled[name] = number

            # print( '%s yelled: %f' % (name, number))

            if name == 'root':
                raise ExceptionDone(name)

    def process_line(self, line):

        parts = line.split(':')

        name = parts[0]
        # print("monkey: '%s'" % name)

        task = parts[1].split()
        # print("task", task)

        number = None
        monkey1 = None
        monkey2 = None
        oper = None

        if len(task) == 1:
            number = int(task[0])
        else:
            monkey1 = task[0]
            monkey2 = task[2]
            oper = task[1]

            if name == 'root':
                oper = '='

        #             0        1        2     3
        state = [number, monkey1, monkey2, oper]
        self._monkeys[name] = state


if __name__ == '__main__':
    runner = Runner()
    runner.run()
