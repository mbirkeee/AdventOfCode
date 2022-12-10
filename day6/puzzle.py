

class Runner(object):

    def __init__(self):
        print("running")
        self._file_name = 'input_real.txt'
        # self._file_name = 'input_test.txt'
        self._stacks = {}

    def run(self):

        instructions = []
        init = []
        stack_count = None

        fp = open(self._file_name, 'r')

        for line in fp:

            stripped = line.strip()
            self.process_message(stripped)

        fp.close()



        print("done")

    def process_message(self, data):

        print(data)
        unique_count = 14
        array = [c for c in data]

        for i in range(len(array) - unique_count):
            chunk = array[i:i+unique_count]
            # print(chunk)
            if len(chunk) == len(set(chunk)):
                pos = i + unique_count
                print("found marker at position: %d" % pos)
                break




if __name__ == '__main__':
    runner = Runner()
    runner.run()
