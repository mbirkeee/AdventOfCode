import math

class Monkey(object):

    def __init__(self, number, lines):

        self._number = number

        print("Make monkey: %d" % self._number)
        self._worry_list = self.init_worry( lines[0] )

        self._op_func, self._op_arg = self.init_operation( lines[1] )
        self._test_arg   = self.init_arg( lines[2], 'Test: divisible by ' )
        self._test_true  = self.init_arg( lines[3], 'If true: throw to monkey ' )
        self._test_false = self.init_arg( lines[4], 'If false: throw to monkey' )

        self._total_inspections = 0
        self._monkey_dict = {}

        self._worry_divisor = 1
        #----------------------------------------------------------------------
        # print("operation: %s" % lines[1])
        # print("test: %s" % lines[2])
        # print("true: %s" % lines[3])
        # print("false: %s" % lines[4])

        # self._min_pass = None
        #
        # i = 3
        # while True:
        #     new_val = self._op_func(i)
        #     if self.test(new_val):
        #         self._min_pass = i
        #         break
        #     i += 1

    def get_min_pass(self, arg):
        i = arg
        while True:
            new_val = self._op_func(i)
            if self.test(new_val):
                return new_val
            i += arg


    # def reduce_worry(self, factor):
    #
    #     #print("REDUCE WORRY CALLED!!!!!")
    #     new = []
    #     for worry in self._worry_list:
    #         new.append(int(worry/factor))
    #
    #     self._worry_list = new

    def get_number(self):
        return self._number

    def get_test_arg(self):
        return self._test_arg

    def set_monkey_dict(self, monkey_dict):
        self._monkey_dict = monkey_dict

        for monkey in monkey_dict.values():
            self._worry_divisor *= monkey.get_test_arg()

    def init_arg(self, line, sig):
        if not line.startswith(sig):
            raise ValueError('bad input')

        line = line[len(sig):].strip()
        return int(line)

    def get_worry_list(self):
        return self._worry_list

    def init_worry(self, line):

        # print("init_items: %s" % line)
        items = []

        if not line.startswith('Starting items:'):
            raise ValueError('bad input')

        parts = line.split(':')
        things = parts[1]
        parts = things.split(',')

        for part in parts:
            item = int(part.strip())
            items.append(item)

        return items

    def init_operation(self, line):
        # print("init_operation: %s" % line)
        sig = 'Operation: new = old'
        if not line.startswith(sig):
            raise ValueError('bad input')

        line = line[len(sig):].strip()
        parts = line.split()
        # print(parts)

        op_arg = parts[1].strip()

        if parts[0] == '*':
            return self.op_mult, op_arg
        elif parts[0] == '+':
            return self.op_add, op_arg
        else:
            raise ValueError('bad input')

    def op_add(self, worry):

        try:
            v = int(self._op_arg)
        except:
            v = worry

        result = worry + v
        # print("op_add: %d + %d -> %d" % (worry, v, result))
        return result

    def op_mult(self, worry):

        try:
            v = int(self._op_arg)
        except:
            v = worry

        result = worry * v
        # print("op_mult: %d * %d -> %d" % (worry, v, result))
        return result

    def catch(self, worry):
        # print("%d CATCH <- %d" % (self._number, worry))
        self._worry_list.append(worry)

    def test(self, worry):

        if worry % self._test_arg:
            return False
        return True

    def play(self, round):

        for worry in self._worry_list:
            # print("Monkey: %s inspect item worry: %d" % (self._number, worry ))

            self._total_inspections += 1

            value = self._op_func(worry)

            #new_value = int(value/3)
            new_value = value % self._worry_divisor

            if self.test(new_value):
                target_monkey_number = self._test_true
                # new_value = self._test_arg * round
            else:
                target_monkey_number = self._test_false

            target_monkey = self._monkey_dict[target_monkey_number]

            # Does the target monkey also like this value?
            # if target_monkey.test(new_value):
            #     new_value = target_monkey.get_min_pass(self._test_arg)
            #    # print("resetting mi value: %d" % new_value)

            target_monkey.catch(new_value)

        self._worry_list = []

    def get_total_inspections(self):
        return self._total_inspections

    def print(self):
        print("Monkey: %d total inspections: %d" % (self._number, self.get_total_inspections() ))
        # print("  WORRY: %s" % self._worry_list)
        # print("  TEST: %d  TRUE: %d FALSE: %d" % (self._test_arg, self._test_true, self._test_false ))

class Runner(object):

    def __init__(self):
        self._file_name = 'input_real.txt'
        # self._file_name = 'input_test.txt'

        self._monkey_dict = {}

    def run(self):

        lines = []
        fp = open(self._file_name, 'r')
        for line in fp:
            lines.append(line.strip())

        # Make the monkeys ----------------------------------------------------
        while True:
            if len(lines) == 0: break

            line = lines.pop(0)
            if line.startswith('Monkey'):
                line = line.strip(':')
                parts = line.split()
                monkey_number = int(parts[1])
                monkey = Monkey(monkey_number, lines[0:5])
                self._monkey_dict[monkey_number] = monkey

        # Start the game ------------------------------------------------------

        for monkey in self._monkey_dict.values():
            monkey.set_monkey_dict(self._monkey_dict)

        round = 1
        while True:
            for monkey in self._monkey_dict.values():
                monkey.play(round)
                # self.reduce_worry()

            # print("Round %d ---------------------------------------" % round)

            if round in [1,20, 30, 40, 50, 100, 1000, 2000, 3000, 4000, 5000, 10000]:
                print("Round %d ---------------------------------------" % round)
                self.print_inpections()
                self.print_items()


            round += 1
            if round > 10000: break


        inspections = []
        for monkey in self._monkey_dict.values():
            inspections.append(monkey.get_total_inspections())

        inspections.sort()
        inspections.reverse()

        result = inspections[0] * inspections[1]
        print("Part 1 result: %d" % result)
        print('done')

    def print_inpections(self):
        for monkey in self._monkey_dict.values():
            name = monkey.get_number()
            total_inspections = monkey.get_total_inspections()
            print("Monkey %d inspections: %d" % (name, total_inspections))

    def print_items(self):
        for monkey in self._monkey_dict.values():
            name = monkey.get_number()
            worry_list = monkey.get_worry_list()
            print("Monkey %d items: %s" % (name, repr(worry_list)))

    def reduce_worry(self):
        while True:
            min_worry=math.pow(2,64)
            for monkey in self._monkey_dict.values():
                worry_list = monkey.get_worry_list()
                # print(worry_list)
                for worry in worry_list:
                    if worry < min_worry:
                        min_worry = worry

            if min_worry < 10000000000: break

            for monkey in self._monkey_dict.values():
                monkey.reduce_worry(2)

        #print("min worry: %ld" % min_worry)
if __name__ == '__main__':
    runner = Runner()
    runner.run()
