class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self):
        # self._file_name = 'input_test.txt'
        self._file_name = 'input_real.txt'

        self._list_orig = []
        self._map = {}

    def run(self):

        fp = open(self._file_name, 'r')
        lines = []
        for line in fp:
            line = line.strip()
            lines.append(line)

        fp.close()

        for i, line in enumerate(lines):
            val = int(line) * 811589153
#            val = int(line)
            self._list_orig.append((i, val))

            self._map[(i, val)] = float(i)

        # print(self._map)

#        self.mix()
#        self.result()

        for _ in range(10):
            self.mix()
            self.result()

        print("done")

    def result(self):

        total = 0
        length = len(self._list_orig)

        lst = self.make_list()

        started = False
        count = 0
        index = 0
        while True:
            value = lst[index]
            # value = item[1]
            index += 1

            if index >= length:
                index = 0

            if started == False:
                if value == 0:
                    started = True
                continue

            count += 1
            if count  in [1000, 2000, 3000]:
                total += value
                print("count: %d value: %d total: %d" % (count, value, total))

            if count >= 3000:
                break

    def rebuild_map(self):

        l = [(v, k) for k, v in self._map.items()]
        # print("*"*80)
        # print(l)
        l.sort()

        map = {}
        for i, item in enumerate(l):
            map[item[1]] = i

        self._map = map

    def make_list(self):

        result = []
        l = [(v, k) for k, v in self._map.items()]
        l.sort()

        for item in l:
            thing = item[1]
            result.append(thing[1])

        return result

    def mix(self):

        length = len(self._list_orig)
        len2 = length - 1

        for item in self._list_orig:

            skip = item[1]

            if skip == 0:
                continue

            pos = self._map[item]
            pos -= 0.5

            new_pos = pos + skip


            # remove the item from the map
            del self._map[item]
            self.rebuild_map()

            new_pos = new_pos % (length -1)



            # while new_pos < 0:
            #      new_pos += len2
            #
            # while new_pos >= len2:
            #      new_pos -= len2

            # print(new_pos, test_pos)

            self._map[item] = new_pos
            self.rebuild_map()

           # l = self.make_list()
           # print("move item: %10s: %s" % (repr(item), repr(l)))

    def mix_OLD(self):

        length = len(self._list_orig)

        self.print_array()
        print(self._list)

        for item in self._list_orig:

            index = self._list.index(item)
            self._list.pop(index)

            new_index = index + item[1]

            wrapped_back = False
            while new_index < 0:
                wrapped_back = True
                new_index += length

            wrapped_fwd = False
            while new_index > length:
                wrapped_fwd = True
                new_index -= length

            if new_index == index:
                continue

            print("item %s starting index: %d add: %d new index: %d " % (repr(item), index, item[1], new_index))

            if new_index > index:
                if wrapped_back:
                    self._list.insert(new_index, item)
                    self._list.pop(index)
                else:
                    self._list.insert(new_index, item)
                    self._list.pop(index)

            else:

                if wrapped_fwd:
                    self._list.pop(index)
                    self._list.insert(new_index, item)
                else:
                    self._list.insert(new_index, item)

            if new_index < 0:
                raise ValueError("index too small")

            if new_index > length:
                raise ValueError("index too big")

            self.print_array()



    def print_array(self):
        s = ""
        for item in self._list:
            s += " %d, " % item[1]

        print(s)

if __name__ == '__main__':
    runner = Runner()
    runner.run()
