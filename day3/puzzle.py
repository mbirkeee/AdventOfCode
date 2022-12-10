

class Runner(object):

    def __init__(self):
        print("running")

        items = "abcdefghijklmnopqrstuvwxyz"
        self._items = items + items.upper()

        print((self._items))
        print(len(self._items))

    def run(self):

        fp = open('input.txt', 'r')

        total = 0
        group = []

        for line in fp:
            line = line.strip()
            # print(line)

            group.append(line)
            if len(group) == 3:
                common_item = self.check_group(group)

                value = self.get_value(common_item)
                total += value
                print("common item: %s" % common_item)

                group = []
#            contents1, contents2 = self.get_contents(line)
#            duplicates = self.check_duplicates(contents1, contents2)
            # print(duplicates)

 #           total += self.get_total(duplicates)

        print("TOTAL: %d" % total)

        fp.close()

    def check_group(self, group):

        common = []

        if len(group) != 3:
            raise ValueError("dont have 3 items")

        for item in self._items:
            have = 0
            for elf in group:
                if item in elf:
                    have += 1

            if have == len(group):
                common.append(item)

            # print("item: %s have: %d" % (item, have))

        if len(common) != 1:
            raise ValueError("did not find one common item")

        return common[0]

    def get_value(self, item):

        v = ord(item)
        if v >= ord('a') and v <= ord('z'):
            value = v - ord('a') + 1

        elif v >= ord('A') and v <= ord('Z'):
            value = v - ord('A') + 27

        else:
            raise ValueError("value error")

        print("item: %s value: %d" % (item, value))
        return value

    def get_total(self, items):

        total = 0
        for item in items:
            value = self.get_value(item)
            total += value

        return total

    def check_duplicates(self, contents1, contents2):
        # print(contents1, contents2)

        duplicates = []
        for item in contents1:
            # print(item)
            if item in contents2:
                # print("found duplicate %s" % item)
                duplicates.append(item)

        result = list(set(duplicates))

        if len(result) != 1:
            raise ValueError("got %d duplicates" % len(result))

        return result

    def get_contents(self, all):
        total = len(all)

        # Check number is positive
        if total % 2:
            raise ValueError("odd number of items")

        half = int(total/2)

        first = all[0:half]
        second = all[half:]

        if len(first) != len(second):
            raise ValueError("not the same")

        if not all.startswith(first):
            raise ValueError("first wrong")

        if not all.endswith(second):
            raise ValueError("second wrong")

        return first, second

if __name__ == '__main__':
    runner = Runner()
    runner.run()
