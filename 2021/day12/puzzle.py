import copy
import numpy as np
import math

import sys

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

class Cave(object):

    def __init__(self, name):
        print('Cave created: %s' % name)

        self._name = name
        self._paths = []

    def add_path(self, name):

        if name == 'start':
            print("no caves link to start")
            return

        if self._name == 'end':
            print('path end has no links')
            return

        # print("add link: %s" % name)
        self._paths.append(name)

    def get_paths(self):
        return self._paths

class Runner(object):

    def __init__(self, filename):

        self._lines = []
        self._map = {}

        self._routes = []
        f = open(filename, 'r')
        for line in f:
            self._lines.append(line.strip())
        f.close()

    def run(self):
        print("run")

        for line in self._lines:
            self.process_line(line)

        self._path_list = [['start']]

        self.explore(self._path_list[0])

        # self.print_map()
        self.print_routes()

    def print_routes(self):

        for i, route in enumerate(self._routes):
            print("ROUTE %d: %s" % (i+1, route))

    def can_visit(self, caves, path):

        temp = {}
        for cave in caves:
            if cave == 'start':
                continue

            if not cave.islower():
                continue

            count = temp.get(cave, 0)
            count += 1
            temp[cave] = count

        max_count = 0
        for cave, count in temp.items():
            if count > max_count:
                max_count = count

        if max_count < 2:
            # We can visit this node
            return True

        # we have visited a node twice but can still visit if first time:
        if path not in caves:
            return True

        return False

    def explore(self, caves):
        # print("called, caves: %s" % repr(caves))

        last_cave = caves[-1]
        c = self._map[last_cave]
        paths = c.get_paths()

        for path in paths:
            # print("consider next cave: %s" % path)
            if path == 'end':
                new_path = copy.deepcopy(caves)
                new_path.append('end')
                self._routes.append(new_path)
                print("made it to the end!!! %s" % repr(caves))
                continue

            elif path.islower():
                if not self.can_visit(caves, path):
                # This is a lower case node, can only be visited once
                # if path in caves:
                    print("alreeady visited", path)
                    continue

            new_path = copy.deepcopy(caves)
            new_path.append(path)
            self.explore(new_path)





    def print_map(self):

        for name, cave in self._map.items():
            print("CAVE: %s" % name)
            paths = cave.get_paths()
            for path in paths:
                print("  path: %s" % path)

    def process_line(self, line):

        parts = line.split('-')
        name1 = parts[0].strip()
        name2 = parts[1].strip()

        if name1 not in self._map:
            self._map[name1] = Cave(name1)

        self._map[name1].add_path(name2)

        if name2 not in self._map:
            self._map[name2] = Cave(name2)

        self._map[name2].add_path(name1)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()

