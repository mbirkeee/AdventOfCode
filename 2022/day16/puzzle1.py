import numpy as np
import time

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

class Node(object):

    def __init__(self, name, mgr, parent=None):

        self._skip_open = False
        if name.endswith('*'):
            # print("name: %s SKIP OPEN!!!!!" % name)
            name = name.strip('*')
            self._skip_open = True

        self._name = name
        self._mgr = mgr
        self._parent = parent
        self._next = []
        self._opened = 0

        meta = self._mgr.get_valve_meta(name)

        self._flow = meta['flow']
        self._next = meta['next']

        self._parent_list, opened, open_count = self.get_parent_list()

        done = False
        loop_flag = False

        # Break loops
        try:
            before1 = self._parent
            before2 = before1.get_parent()
            before3 = before2.get_parent()

            if before2.get_name() == self._name:
                if before3.get_name() == before1.get_name():
                    loop_flag = True
                    # print("LOOP: %s %s %s %s" % (before3.get_name(),  before2.get_name(), before1.get_name(), self._name ))
        except:
            pass

        if loop_flag:
            # outside try/except just to catch bugs
            self._mgr.inc_loop_count()
            done = True
        else:
            pass
#            self.print_path()

        if open_count == self._mgr.get_open_count():
            # print("All valves open!!")
            done = True

        if done or len(self._parent_list) >= 30:
            # print("reached end of the line")
            self.get_pressure()
            self._next = []
            self._parent = None
            self._parent_list = None
        else:
            pass

            if not self._skip_open and opened == 0 and self._flow:
                # If this is the first visit to this node and it has flow,
                # Insert into path with opened flag

                # print("Open Valve %s" % name)
                self._next = [name]
                self._opened = 1

                # We must also tell the parent to consider a path where is NOT opened
                # print("Skip %s open" % name)
                # self._parent.append_next( name + '*')

    def get_pressure(self, print_flag=False):
        total_pressure = 0
        minute = 0
        for node in self._parent_list:
            minute += 1
            if node.get_opened():
                # We sped a minute opening
                minutes_open = 30 - minute
                pressure  = node.get_flow() * minutes_open
                total_pressure += pressure
                if print_flag:
                    print("Minute: %d (%d) valve %s opened; pressure: %d" %
                          (minute, minutes_open, node.get_name(), pressure))

        if print_flag:
            self.print_path()

        if total_pressure > self._mgr.get_pressure_max():
            self._mgr.set_pressure_max(total_pressure)
            print("!!!!!!!!!!!!!!!!!! new max total pressure", total_pressure)
            self.get_pressure(print_flag = True)

        return total_pressure

    def get_flow(self):
        return self._flow

    def print_path(self):
        str = ''
        for parent in self._parent_list:
            str += " %s" % parent.get_name()
            # print("PARENT: %s" % parent.get_name())
        print(str)

    def append_next(self, name):
        if name not in self._next:
            self._next.append(name)
            print(self._next)

    def get_parent_list(self):

        parent = self._parent
        name = self._name

        parent_list = []
        open_count = 0
        opened = 0

        while True:
            if parent is None:
                break

            if parent.get_name() == name:
                if parent.get_opened():
                    opened += 1

            open_count += parent.get_opened()

            parent_list.append(parent)
            parent = parent.get_parent()

        parent_list.reverse()
        parent_list.append(self)
        parent_list = parent_list
        return parent_list, opened, open_count

    def get_next(self):
        for name in self._next:
            yield name

    def get_parent_list_old(self):

        parent = self._parent
        name = self._name

        parent_list = []
        visit_count = 0
        open_count = 0
        while True:
            if parent is None:
                break

            if parent.get_name() == name:
                parent
                visit_count += 1

            open_count += parent.get_opened()

            parent_list.append(parent)
            parent = parent.get_parent()

        parent_list.reverse()
        parent_list.append(self)
        parent_list = parent_list
        return parent_list, visit_count, open_count

    def get_opened(self):
        return self._opened

    def __del__(self):
        # print("node __del__ called; name: %s depth: %d" % (self._name, self._depth))
        pass

    def get_parent(self):
        return self._parent

    def get_name(self):
        return self._name

    def get_next(self):
        return self._next

class Runner(object):

    def __init__(self):
        self._file_name = 'input_test.txt'
        # self._file_name = 'input_test2.txt'
        # self._file_name = 'input_real.txt'
        self._valves = {}
        self._tree = {}
        self._node_count = 0
        self._path_count = 0
        self._path_count2 = 0
        self._mgr = Manager()

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

        node = Node('AA', self._mgr)
        self._node_count += 1

        self.process_node(node)

        print("Path count: %d" % self._path_count)
        print("Valves to open: %d" % self._mgr.get_open_count() )
        print("Loop count: %d" % self._mgr.get_loop_count() )

    def process_node(self, node):

        self._path_count += 1
        self._path_count2 += 1

        if self._path_count2 >= 1000000:
            print("path count: %d" % self._path_count)
            self._path_count2 = 0

        # next_names = node.get_next()
        # for name in next_names:
        for name in node.get_next():
            next_node = Node(name, self._mgr, parent=node)
            self.process_node(next_node)


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
