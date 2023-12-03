
class Runner(object):

    def __init__(self):
        print("running")

    def run(self):

        fp = open('input.txt', 'r')

        contained_count = 0
        overlap_count = 0

        for line in fp:
            line = line.strip()
            parts = line.split(',')

            elf1 = parts[0]
            elf2 = parts[1]
            #
            # if self.contained(elf1, elf2):
            #     contained_count += 1
            # elif self.contained(elf2, elf1):
            #     contained_count += 1

            if self.overlap(elf1, elf2):
                overlap_count += 1

        fp.close()

        # print(contained_count)
        print(overlap_count)

    def contained(self, elf1, elf2):

        elf1_parts = elf1.split('-')
        elf2_parts = elf2.split('-')

        elf1_start = int(elf1_parts[0])
        elf1_end = int(elf1_parts[1])

        elf2_start = int(elf2_parts[0])
        elf2_end = int(elf2_parts[1])

        if elf2_start >= elf1_start and elf2_end <= elf1_end:
            return True

        return False

    def overlap(self, elf1, elf2):

        elf1_parts = elf1.split('-')
        elf2_parts = elf2.split('-')

        elf1_start = int(elf1_parts[0])
        elf1_end = int(elf1_parts[1])

        elf2_start = int(elf2_parts[0])
        elf2_end = int(elf2_parts[1])

        elf1_list = [i for i in range(elf1_start, elf1_end+1)]
        elf2_list = [i for i in range(elf2_start, elf2_end+1)]

        # print(elf1_list)
        # print(elf2_list)

        elf1_list.extend(elf2_list)
        # print(elf1_list)

        if len(elf1_list) == len(set(elf1_list)):
            return False


        return True

if __name__ == '__main__':
    runner = Runner()
    runner.run()
