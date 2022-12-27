
class Stack():

    def __init__(self, name):
        print("creating stack %s" % name)
        self._name = name
        self._crates = []

    def add(self, crate):
        print("called: %s" % crate)
        if len(crate) != 1:
            raise ValueError('bad crate')
        self._crates.append(crate)

    def remove(self):
        crate = self._crates.pop(-1)
        if len(crate) != 1:
            raise ValueError('bad crate')
        return crate

    def display(self):
        d = "Name: %s: " % self._name

        for crate in self._crates:
            d += ' [%s]' % crate

        print(d)


class Runner(object):

    def __init__(self):
        print("running")
        self._file_name = 'input_real.txt'
#        self._file_name = 'input_test.txt'
        self._stacks = {}

    def run(self):

        instructions = []
        init = []
        stack_count = None

        fp = open(self._file_name, 'r')

        for line in fp:

            stripped = line.strip()
            if len(stripped) == 0:
                continue

            if stripped.startswith('1'):
                stack_count = line

            elif stripped.startswith('move'):
                instructions.append(line)

            elif stripped.startswith('['):
                init.append(line)

            else:
                raise ValueError("init error")

        fp.close()

        stack_names = stack_count.split()

        # make the stacks
        for name in stack_names:
            self._stacks[name] = Stack(name)

        # Initialize the stacks
        init.reverse()
        for line in init:
            print(line)
            print("*"*80)
            for i, name in enumerate(stack_names):
                try:
                    start = i*4
                    end = start + 3
                    crate = line[start:end]
                    crate = crate.strip(' []')
                    if(len(crate) != 1):
                        print("no crate")
                        continue

                    stack = self._stacks[name]
                    stack.add(crate)

                except:
                    print("end of the line")

        # build the stacks
        # print(init)

        self.display_stacks()

        # Move the crates
        for instruction in instructions:
            # print("instruction: %s" % instruction)
            parts = instruction.split()
            count = int(parts[1])
            from_stack_name = parts[3]
            to_stack_name = parts[5]

            print("Move %s from '%s' to '%s'" % (count, from_stack_name, to_stack_name))
            from_stack = self._stacks[from_stack_name]
            to_stack = self._stacks[to_stack_name]

            crates = []
            for _ in range(count):
                crates.append(from_stack.remove())

            crates.reverse()
            for crate in crates:
                to_stack.add(crate)

        self.display_stacks()

        print("done")

    def display_stacks(self):
        for name, stack in self._stacks.items():
            stack.display()

if __name__ == '__main__':
    runner = Runner()
    runner.run()
