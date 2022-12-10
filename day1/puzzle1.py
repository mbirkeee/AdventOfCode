class Runner(object):

    def __init__(self):
        print("running")


    def run(self):

        fp = open('advent_1_input.txt', 'r')

        result = {}
        calories_total = 0
        calories_max = 0
        elf = 1

        for line in fp:
            line.strip()

            try:
                calories = int(line)
                calories_total += calories
            except:

                print("ELF: %d calories: %d" % (elf, calories_total))

                result[elf] = calories_total

                elf += 1

                if calories_total > calories_max:
                    calories_max = calories_total
                    print("got new max calories: %d" % calories_max)
                calories_total = 0

            # print("calories: %d" % calories)

        fp.close()


        print(result)

        list = [(v, k) for k, v in result.items()]
        list.sort()
        list.reverse()
        print(list)

        top_three_total = 0
        for i in range(3):
            item = list[i]
            print(item)
            top_three_total += item[0]

        print(top_three_total)

if __name__ == '__main__':
    runner = Runner()
    runner.run()
