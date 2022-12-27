class Runner(object):
    """
    For part 2, work backwards and find the starting position if the card
    """
    def __init__(self):
        self._file_name = 'input_real.txt'
        # self._file_name = 'input_test.txt'
        # self._file_name = 'input_test_2.txt'

        self._length = 119315717514047
        position = 4096
        self._shuffles_total = 101741582076661

        repeat_shuffles = self._length // 2
        self._shuffles = self._shuffles_total - repeat_shuffles

    def run(self):

        deals = []
        fp = open(self._file_name, 'r')
        for line in fp:
            deals.append(line)
        fp.close()

        deals.reverse()

        loop_count = 0
        loop_count_2 = 0

        while True:
            for deal in deals:
                # self.process_line(deal)
                repeat_shuffles = self._length // 2
                x = self._shuffles_total - repeat_shuffles
            loop_count += 1
            loop_count_2 += 1

            if loop_count_2 >= 100000:

                fraction = loop_count / self._shuffles
                print("Total Loops: %d (frac: %f)" % (loop_count, fraction))
                loop_count_2 = 0



    def process_line(self, line):
        print(line)

        if line.startswith('deal into new'):
            pass

        elif line.startswith('cut '):
            parts = line.split()
            x = int(parts[1].strip())

        elif line.startswith('deal with inc'):
            parts = line.split()
            x = int(parts[3])

        else:
            raise ValueError('bad deal')


if __name__ == '__main__':
    runner = Runner()
    runner.run()
