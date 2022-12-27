class ExceptionDone(Exception):
    pass

class Node(object):

    def __init__(self, row, col, rows, cols, elevation, node_map):
        self._row = row
        self._col = col
        self._elevation = ord(elevation)

        self._destination = False

        self._key = (row, col)
        self._node_map = node_map
        self._rows = rows
        self._cols = cols
        self._from = None
        if elevation == 'E':
            self._destination = True
            self._visit_step = 0
            self._elevation = ord('z')

        elif elevation == 'S':
            self._elevation = ord('a')
            self._visit_step = 1
        else:
            self._visit_step = 0

        print("ROW: %d COL: %d (%d %d) ELEVATION %d" % (row, col, rows, cols, self._elevation))

    def set_map(self, node_map):
        self._node_map = node_map

    def key(self):
        return self._key

    def get_visit_step(self):
        return self._visit_step

    def is_destination(self):
        return self._destination

    def set_from(self, node):
        self._from = None

    def get_elevation(self):
        return self._elevation

    def set_visit_step(self, step):
        self._visit_step = step

    def move(self, step):

        up    = self._node_map.get( (self._row - 1 , self._col     ) )
        down  = self._node_map.get( (self._row + 1 , self._col     ) )
        left  = self._node_map.get( (self._row     , self._col - 1 ) )
        right = self._node_map.get( (self._row     , self._col + 1 ) )

        for node in [up, down, left, right]:
            if node is None: continue

            print("NODE: %s neighbour: %s" % (repr(self.key()), repr(node.key())))

            if node.get_visit_step() > 0:
                continue

            if ( node.get_elevation() - self.get_elevation() ) <= 1:
                print("can move")
                node.set_from(self)
                node.set_visit_step(step)
                if node.is_destination():
                    return False

        return True

class Runner(object):

    def __init__(self):
        self._file_name = 'input_real.txt'
        # self._file_name = 'input_test.txt'

        self._node_map = {}

    def run(self):

        lines = []
        fp = open(self._file_name, 'r')
        for line in fp:
            lines.append(line.strip())
        fp.close()

        rows = len(lines)
        cols = len(lines[0])

        print(rows, cols)
        # Build the map
        for row, line in enumerate(lines):
            print("LINE: %s" % line)
            for col, c in enumerate(line):
                node = Node(row, col, rows, cols, c, self._node_map)
                self._node_map[node.key()] = node

        # Start traversing the map
        step = 1
        try:
            while True:

                print("STEP: %d ----------------------" % step)
                nodes = []
                for node in self._node_map.values():
                    if node.get_visit_step() != step: continue
                    nodes.append(node)
                    # print("consider node: %s" % repr(node.key()))

                step += 1

                for node in nodes:
                    if node.move(step) is False:
                        raise ExceptionDone("found the destination")


                if step > 2000:
                    raise ExceptionDone("too many steps")

        except ExceptionDone as err:
            print(err)


        # Part 2

        # self.print_visits(rows, cols)

    def print_visits(self, rows, cols):
        print("visits")
        for row in range(rows):
            row_str = ''
            for col in range(cols):
                node = self._node_map.get((row, col))
                elev = node.get_visit_step()
                e = " %3d" % elev
                row_str += e

            print(row_str)
        #print("min worry: %ld" % min_worry)
if __name__ == '__main__':
    runner = Runner()
    runner.run()
