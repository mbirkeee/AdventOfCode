import json

class ExceptionDone(Exception):
    pass

class ExceptionOrderBad(Exception):
    pass

class ExceptionOrderGood(Exception):
    pass


class Runner(object):

    def __init__(self):
        self._file_name = 'input_real.txt'
        # self._file_name = 'input_test.txt'

        self._node_map = {}

    def run(self):

        pair_count = 0
        pairs = []
        first = None

        part2 = []

        fp = open(self._file_name, 'r')



        for line in fp:
            line = line.strip()


            if len(line) == 0:
                if pair_count != 2:
                    raise ValueError("bad input")
                pair_count = 0
                continue

            item = json.loads(line)
            # print(item)
            part2.append(item)

            if pair_count == 0:
                first = item
                pair_count += 1

            elif pair_count == 1:
                pair = [first, item]
                pairs.append(pair)
                pair_count += 1

            else:
                raise ValueError("bad input")

        fp.close()

        # # Part 1
        # good_indexes = []
        # for index, pair in enumerate(pairs):
        #     result = self.process_pair(pair)
        #
        #     print("PAIR INDEX %d  result %s" % (index + 1, repr(result)))
        #     if result:
        #         good_indexes.append(index+1)
        #
        # print("good indexes: %s" % repr(good_indexes))
        # print("PART 1 result: %d" % sum(good_indexes))

        part2.append([[2]])
        part2.append([[6]])

        packet_count = len(part2)

        while True:
            again = False
            for i in range(packet_count-1):
                result = self.process_pair((part2[i], part2[i+1]))
                if not result:
                    temp = part2[i+1]
                    part2[i+1] = part2[i]
                    part2[i] = temp
                    print("*"*80)
                    print("AGAIN  i: %d" % i)
                    print("*"*80)
                    again = True
                    break

            print("At the end of the list ................................................ run again: %s" % repr(again))
            if again is False:
                break

        for index, item in enumerate(part2):
            print("PART2 %d ITEM: %s" % ((index+ 1), repr(item)))

    def process_pair(self, pair):
    #    print("---------------------")
    #    print("LINE 0: %s" % pair[0] )
    #    print("LINE 1: %s" % pair[1] )

        try:
            self.compare(pair[0], pair[1])

        except ExceptionOrderBad as err:
     #       print("ORDER BAD")
            return False

        except ExceptionOrderGood as err:
     #       print("ORDER GOOD")
            return True

        raise ValueError("no result determined")

    def compare(self, left, right):

     #   print("compare %s (%s) <-> %s (%s)" % (repr(left), type(left), repr(right), type(right) ))

        if isinstance(left, int) and isinstance(right, int):

            if left == right:
      #          print("%d == %d returing false" % (left, right))
                return False

            if left < right:
       #         print("%d < %d ... ORDER IS GOOD" % (left, right))
                raise ExceptionOrderGood("order good")

            raise ExceptionOrderBad("wrong order")

        elif isinstance(left, list) and isinstance(right, list):

            index = 0
            max_index = max(len(left), len(right))
            for index in range(max_index):
            #while True:
                try:
                    item_left = left[index]
                except:
                    # Left side out of items, order id OK
                    # return True
                    raise ExceptionOrderGood("left list empty")
                try:
                    item_right = right[index]
                except:
                    # Left side out of items, order id OK
                    raise ExceptionOrderBad("out of order")

                # print("list index: %d index left: %s right: %s" % (index, repr(item_left), repr(item_right)))

                result = self.compare(item_left, item_right)
                #index += 1

            return False

        elif isinstance(left, int):
            return self.compare([left], right)

        elif isinstance(right, int):
            return self.compare(left, [right])

        else:
            print(type(left))
            print(type(right))

            raise ValueError("should not be here")

if __name__ == '__main__':
    runner = Runner()
    runner.run()
