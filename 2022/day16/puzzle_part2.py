import copy
import itertools
class ExceptionDone(Exception):
    pass

class Manager(object):

    def __init__(self):
        self._valves = None
        self._open_count = 0
        self._pressure_max = 0
        self._loop_count = 0

    def inc_loop_count(self):
        self._loop_count += 1

    def get_loop_count(self):
        return self._loop_count

    def set_valves(self, valves):
        self._valves = valves

        for valve in self._valves.values():
            if valve['flow'] > 0:
                self._open_count += 1

    def get_valve_meta(self, name):
        return self._valves[name]

    def get_open_count(self):
        return self._open_count

    def get_pressure_max(self):
        return self._pressure_max

    def set_pressure_max(self, value):
        self._pressure_max = value

    def get_next_valves(self, valve):
        # print(self._valves)
        meta = self._valves[valve]
        return meta['next']

    def get_flow(self, valve):
        meta = self._valves[valve]
        return meta['flow']

class Runner(object):

    def __init__(self):
        #self._file_name = 'input_test.txt'
        # self._file_name = 'input_test2.txt'
        self._file_name = 'input_real.txt'
        self._valves = {}
        self._tree = {}
        self._node_count = 0
        self._path_count = 0
        self._path_count2 = 0
        self._mgr = Manager()
        self._max_minutes = 26

        self._paths = []
        self._paths_new = []


    def run(self):

        fp = open(self._file_name, 'r')
        lines = []
        for line in fp:
            line = line.strip()
            lines.append(line)

        fp.close()

        # build the map
        for line in lines:
            self.process_line(line)

        self._mgr.set_valves(self._valves)

        # Note: there are two srarting paths!!!
        self._paths = [[( 'AA', 'AA' )]]

        minute = 0

        while True:

            print("Minute: %d ----- paths : %d" % (minute, len(self._paths)))

            self._paths_new = []

            self.purge_paths()

            for path in self._paths:
                self.process_path(path)

            self._paths = self._paths_new

            minute += 1
            if minute > self._max_minutes: break

   #         self.print_paths()

            print("total paths: %d" % len(self._paths))
 #           self.top_score()
 #           input("continue...")

        self.top_score()

    def top_score(self):

        if len(self._paths) < 1000: return

        temp = []
        for path in self._paths:
            score = self.path_score(path)
            temp.append((score, path))

        temp.sort()
        temp.reverse()

        for i in range(100):
            item = temp[i]
            score = item[0]
            path = item[1]

            print("SCORE: %d path: %s" % (score, repr(path)))


    def purge_paths(self):

        if len(self._paths) < 1000000:
            return

        temp = []
        for path in self._paths:
            score = self.path_score(path)
            temp.append((score, path))

        temp.sort()
        temp.reverse()

        keep = []
        for i in range(100000):
            keep.append(temp[i][1])

        self._paths = keep


    def process_path(self, path):

        # The path should be a list of lists
        # print(path)

        # Get last location pair in the path
        location = path[-1]

        location_0 = location[0]
        location_1 = location[1]

        if location_0.endswith('*'):
            next_0 = [location_0[:-1]]
        else:
            next_0 = copy.deepcopy(self._mgr.get_next_valves(location_0))

        if location_1.endswith('*'):
            next_1 = [location_1[:-1]]
        else:
            next_1 = copy.deepcopy(self._mgr.get_next_valves(location_1))

        # Can we open any valves?
        path1 = [item[0] for item in path]
        path2 = [item[1] for item in path]
        path1.extend(path2)
        combined_path = list(set(path1))
        # print("combined path", combined_path)

    #    print(next_0)
    #    print(next_1)

        add_0 = []
        for item in next_0:
            if self._mgr.get_flow(item):
                opened = item + '*'
                if opened not in combined_path:
                    add_0.append(opened)

        next_0.extend(add_0)

        add_1 = []
        for item in next_1:
            # print('check', item)
            if self._mgr.get_flow(item):
                opened = item + '*'
                if opened not in combined_path:
                    add_1.append(opened)

        next_1.extend(add_1)


        for item_0 in next_0:
            for item_1 in next_1:
                if item_1 == item_0:
                    if item_0.endswith('*'):
                        # print("skip", item_0, item_1)
                        continue

                location = (item_0, item_1)
                new = copy.deepcopy(path)
                new.append(location)
                self._paths_new.append(new)



    def path_score(self, path):

        score_0 = 0
        score_1 = 0

        for i in range(self._max_minutes):
            try:
                pair = path[i]
                # print("v:", pair)

                valve = pair[0]
                if valve.endswith('*'):
                    flow = self._mgr.get_flow(valve[:-1])
                    score_0 += flow * (self._max_minutes - i - 1)

                valve = pair[1]
                if valve.endswith('*'):
                    flow = self._mgr.get_flow(valve[:-1])
                    score_1 += flow * (self._max_minutes - i - 1)

            except Exception as err:
                # print(err)
                # print("done")
                break

        return score_0 + score_1


    def print_paths(self):
        for path in self._paths:
            self.print_path(path)
            # print("score: %d" % self.path_score(path))

    def print_path(self, path):
        print(path)
        # p = ",".join(path)
        # print(p)

    def get_flow(self, input):
        # print(input)
        parts = input.split('=')
        return int(parts[1].strip())

    def process_line(self, line):
        line = line.replace("valves", "valve")
        line = line.replace("leads", "lead")
        line = line.replace(";", "")

        print("------------------ LINE %s" % line)
        halves = line.split('lead to valve')
        parts = halves[0].split()

        # print(parts)
        name = parts[1].strip()
        flow = self.get_flow(parts[4])
        # print('NAME: "%s" flow: %d' % (name, flow))

        # print(halves)
        next = halves[1].split(',')
        next = [item.strip() for item in next]
        # print(next)


        self._valves[name] = {
            'flow' : flow,
            'next' : next
        }

if __name__ == '__main__':
    runner = Runner()
    runner.run()
