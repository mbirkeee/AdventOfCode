import numpy as np
import time
import itertools


class ExceptionDone(Exception):
    pass

class Manager(object):

    def __init__(self):
        self._valves = None
        self._open_count = 0
        self._pressure_max = 0
        self._loop_count = 0

    def get_next(self, valve):
        meta = self._valves[valve]
        return meta['next']

    def get_flow(self, valve):
        meta = self._valves[valve]
        return meta['flow']

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



class ValveOrder(object):

    def __init__(self, valve_list):

        self._map_valves = {}
        self._valve_count = len(valve_list)
        for i, valve in enumerate(valve_list):
            print("valve: %s" % valve_list)
            self._map_valves[i] = valve

        print(self._map_valves)

class Runner(object):

    def __init__(self):
        # self._file_name = 'input_test.txt'
        # self._file_name = 'input_test2.txt'
        self._file_name = 'input_real.txt'
        self._valves = {}
        self._tree = {}
        self._node_count = 0
        self._path_count = 0
        self._path_count2 = 0
        self._mgr = Manager()
        self._dist_queue = {}
        self._vman = None

    def get_distance(self, start, stop):
        # print("get distance from '%s' to '%s'" % (start, stop))

        key = start+stop
        distance = self._dist_queue.get(key)
        if distance is not None:
            return distance


        data = {1: [start]}
        step = 1

        while True:
            # print(data)
            valves = data.get(step)

            next_step = []
            for valve in valves:
                next = self._mgr.get_next(valve)
                # print("next: %s" % repr(next))
                if stop in next:
                    self._dist_queue[key] = distance
                    return step

                next_step.extend(next)

            # print(next_step)
            step += 1
            data[step] = list(set(next_step))

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

        count = 0
        flow_valves = []
        for valve, meta in self._valves.items():
            flow = meta['flow']
            if flow:
                count += 1
                print("%d Valve %s can add flow %d" % (count, valve, flow))
                flow_valves.append(valve)

        # self._vman = ValveOrder(flow_valves)
        # pressure = self.process_path(('DD', 'BB',  'JJ', 'HH', 'EE',  'CC' ))
        # print("pressure", pressure)
        # raise ValueError("temp stop")


        max_pressure = 0
        paths = itertools.permutations(flow_valves, r=8)

        t = time.time()
        for i, path in enumerate(paths):

            self._path_count2 += 1
            if self._path_count2 >= 100000:
                n = time.time()
                elapsed_time = n - t
                t = n
                print("paths checked: %d (sec: %d)" % ((i + 1), int(elapsed_time)))
                self._path_count2 = 0

            pressure = self.process_path(path, i)
            if pressure > max_pressure:
                print("new max pressure: %d" % pressure)
                max_pressure = pressure

        print("Max pressure: %d" % max_pressure)

    def process_path(self, path, path_count):
        # print(path, type(path))
        path_list = ['AA'] + list(path)
        # print(path_list)

        t = 30
        elapsed_time = 0
        total_pressure = 0

        for i in range(len(path_list) - 1):
            start = path_list[i]
            stop = path_list[i+1]
            distance = self.get_distance(start, stop)
            # print("Start: %s stop: %s distance: %d" % (start, stop, distance))

            elapsed_time += (distance + 1)
            if elapsed_time > 30:
                # print("%d node: %d TAKES TOO LONG %d !!!!!!" % (path_count, i, elapsed_time))
                return total_pressure
                # raise ValueError("takes too long")

            pressure = self._mgr.get_flow(stop) * (t-elapsed_time)
            total_pressure += pressure

        print("elapsed time: %d path %s" % (elapsed_time, repr(path)))
        # print("total pressure: %d" % total_pressure)
        return total_pressure


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
