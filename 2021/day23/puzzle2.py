"""

"""
import queue
import copy
from my_logger import MyLogger

log = MyLogger(debug_level=0)

A = 2
B = 4
C = 6
D = 8

class KEY(object):
    KIND    = 'k'
    COL     = 'c'
    ROW     = 'r'
    HALL    = 'h'
    MOVE    = 'm'

    COST   = 's'
    MAP    = 'a'

KIND = { A:'A', B:'B', C:'C', D:'D'}

ALLOWABLE_HALL_SPOTS_RIGHT = [3, 5, 7, 9, 10]
ALLOWABLE_HALL_SPOTS_LEFT = [7, 5, 3, 1, 0]

COST = {A: 1, B:10, C:100, D:1000}

SYSTEM = {
    KEY.COST: 0,
    KEY.MAP : {
        0   : { KEY.KIND: B, KEY.COL : A, KEY.ROW : 0, KEY.HALL : None, KEY.MOVE : 0},
        1   : { KEY.KIND: D, KEY.COL : A, KEY.ROW : 1, KEY.HALL : None, KEY.MOVE : 0},
        2   : { KEY.KIND: D, KEY.COL : A, KEY.ROW : 2, KEY.HALL : None, KEY.MOVE : 0},
        3   : { KEY.KIND: B, KEY.COL : A, KEY.ROW : 3, KEY.HALL : None, KEY.MOVE : 0},
        4   : { KEY.KIND: C, KEY.COL : B, KEY.ROW : 0, KEY.HALL : None, KEY.MOVE : 0},
        5   : { KEY.KIND: C, KEY.COL : B, KEY.ROW : 1, KEY.HALL : None, KEY.MOVE : 0},
        6   : { KEY.KIND: B, KEY.COL : B, KEY.ROW : 2, KEY.HALL : None, KEY.MOVE : 0},
        7   : { KEY.KIND: C, KEY.COL : B, KEY.ROW : 3, KEY.HALL : None, KEY.MOVE : 0},
        8   : { KEY.KIND: A, KEY.COL : C, KEY.ROW : 0, KEY.HALL : None, KEY.MOVE : 0},
        9   : { KEY.KIND: B, KEY.COL : C, KEY.ROW : 1, KEY.HALL : None, KEY.MOVE : 0},
        10  : { KEY.KIND: A, KEY.COL : C, KEY.ROW : 2, KEY.HALL : None, KEY.MOVE : 0},
        11  : { KEY.KIND: D, KEY.COL : C, KEY.ROW : 3, KEY.HALL : None, KEY.MOVE : 0},
        12  : { KEY.KIND: D, KEY.COL : D, KEY.ROW : 0, KEY.HALL : None, KEY.MOVE : 0},
        13  : { KEY.KIND: A, KEY.COL : D, KEY.ROW : 1, KEY.HALL : None, KEY.MOVE : 0},
        14  : { KEY.KIND: C, KEY.COL : D, KEY.ROW : 2, KEY.HALL : None, KEY.MOVE : 0},
        15  : { KEY.KIND: A, KEY.COL : D, KEY.ROW : 3, KEY.HALL : None, KEY.MOVE : 0},
    }
}

SYSTEM_EXAMPLE = {
    KEY.COST: 0,
    KEY.MAP : {
        0   : { KEY.KIND: B, KEY.COL : A, KEY.ROW : 0, KEY.HALL : None, KEY.MOVE : 0},
        1   : { KEY.KIND: D, KEY.COL : A, KEY.ROW : 1, KEY.HALL : None, KEY.MOVE : 0},
        2   : { KEY.KIND: D, KEY.COL : A, KEY.ROW : 2, KEY.HALL : None, KEY.MOVE : 0},
        3   : { KEY.KIND: A, KEY.COL : A, KEY.ROW : 3, KEY.HALL : None, KEY.MOVE : 0},
        4   : { KEY.KIND: C, KEY.COL : B, KEY.ROW : 0, KEY.HALL : None, KEY.MOVE : 0},
        5   : { KEY.KIND: C, KEY.COL : B, KEY.ROW : 1, KEY.HALL : None, KEY.MOVE : 0},
        6   : { KEY.KIND: B, KEY.COL : B, KEY.ROW : 2, KEY.HALL : None, KEY.MOVE : 0},
        7   : { KEY.KIND: D, KEY.COL : B, KEY.ROW : 3, KEY.HALL : None, KEY.MOVE : 0},
        8   : { KEY.KIND: B, KEY.COL : C, KEY.ROW : 0, KEY.HALL : None, KEY.MOVE : 0},
        9   : { KEY.KIND: B, KEY.COL : C, KEY.ROW : 1, KEY.HALL : None, KEY.MOVE : 0},
        10  : { KEY.KIND: A, KEY.COL : C, KEY.ROW : 2, KEY.HALL : None, KEY.MOVE : 0},
        11  : { KEY.KIND: C, KEY.COL : C, KEY.ROW : 3, KEY.HALL : None, KEY.MOVE : 0},
        12  : { KEY.KIND: D, KEY.COL : D, KEY.ROW : 0, KEY.HALL : None, KEY.MOVE : 0},
        13  : { KEY.KIND: A, KEY.COL : D, KEY.ROW : 1, KEY.HALL : None, KEY.MOVE : 0},
        14  : { KEY.KIND: C, KEY.COL : D, KEY.ROW : 2, KEY.HALL : None, KEY.MOVE : 0},
        15  : { KEY.KIND: A, KEY.COL : D, KEY.ROW : 3, KEY.HALL : None, KEY.MOVE : 0},
    }
}

SYSTEM_TEST = {
    KEY.COST: 0,
    KEY.MAP : {
        8   : { KEY.KIND: B, KEY.COL : None, KEY.ROW : None, KEY.HALL : 0,    KEY.MOVE : 0},
        0   : { KEY.KIND: D, KEY.COL : A, KEY.ROW : 1, KEY.HALL : None, KEY.MOVE : 0},
        1   : { KEY.KIND: D, KEY.COL : A, KEY.ROW : 2, KEY.HALL : None, KEY.MOVE : 0},
        9   : { KEY.KIND: B, KEY.COL : A, KEY.ROW : 3, KEY.HALL : None, KEY.MOVE : 0},
        4   : { KEY.KIND: C, KEY.COL : B, KEY.ROW : 0, KEY.HALL : None, KEY.MOVE : 0},
        5   : { KEY.KIND: C, KEY.COL : B, KEY.ROW : 1, KEY.HALL : None, KEY.MOVE : 0},
        10  : { KEY.KIND: B, KEY.COL : B, KEY.ROW : 2, KEY.HALL : None, KEY.MOVE : 0},
        6   : { KEY.KIND: C, KEY.COL : B, KEY.ROW : 3, KEY.HALL : None, KEY.MOVE : 0},
        12  : { KEY.KIND: A, KEY.COL : C, KEY.ROW : 0, KEY.HALL : None, KEY.MOVE : 0},
        11  : { KEY.KIND: B, KEY.COL : C, KEY.ROW : 1, KEY.HALL : None, KEY.MOVE : 0},
        13  : { KEY.KIND: A, KEY.COL : C, KEY.ROW : 2, KEY.HALL : None, KEY.MOVE : 0},
        2   : { KEY.KIND: D, KEY.COL : C, KEY.ROW : 3, KEY.HALL : None, KEY.MOVE : 0},
        3   : { KEY.KIND: D, KEY.COL : D, KEY.ROW : 0, KEY.HALL : None, KEY.MOVE : 0},
        14  : { KEY.KIND: A, KEY.COL : D, KEY.ROW : 1, KEY.HALL : None, KEY.MOVE : 0},
        7   : { KEY.KIND: C, KEY.COL : D, KEY.ROW : 2, KEY.HALL : None, KEY.MOVE : 0},
        15  : { KEY.KIND: A, KEY.COL : D, KEY.ROW : 3, KEY.HALL : None, KEY.MOVE : 0},
    }
}


class Runner(object):

    def __init__(self):

        # self._queue = queue.Queue()
        # self._queue.put_nowait(SYSTEM_EXAMPLE)
        self._count = 0
        self._total_count = 0
        self._min_cost = 999999999
        self._abort_count = 0
        self._finished_count = 0

    def run(self):

        self.print(SYSTEM_EXAMPLE)
        self.process(SYSTEM_EXAMPLE)

        print("done; total: %d min cost: %d" % (self._total_count, self._min_cost))

    def none_in_hall(self, system):

        map = system[KEY.MAP]

        for i, v in map.items():
            if v[KEY.HALL] is not None:
                return False

        return True

    def process(self, system):

        if system[KEY.COST] > self._min_cost:
            # print("abort branch!!")
            self._abort_count += 1
            return

        print_flag = False
        self._count += 1
        self._total_count += 1
        if self._count >= 10000:
            print_flag = True
            self._count = 0

        if self._total_count > 1:
            if self.none_in_hall(system):
                self._finished_count += 1

                # print("CHECK  " * 10)
                cost = system[KEY.COST]
                if cost < self._min_cost:
                    self._min_cost = cost

                # No need to look for subsequent branches
                return

                # print_flag = True

        if print_flag:
            self.print(system)

        # Here, I must iterate over the all the playes and queue every possible move
        map = system[KEY.MAP]

        for i, v in map.items():
            move_list = self.get_move_list(map, i, v)

            if move_list is None:
                continue

            for move in move_list:
                new_system = copy.deepcopy(system)
                # new_map = new_system[KEY.MAP]

                if isinstance(move, tuple):
                    #print("got a tuple, must be a move to a tunnel")
                    self.move_to_tunnel(new_system, i, move[0], move[1])

                elif isinstance(move, int):
                    # print("this must be a move to a hall position")
                    self.move_to_hall(new_system, i, move)
                else:
                    raise ValueError("bad move!!", repr(move), type(move))

                # self._queue.put_nowait(new_system)
                self.process(new_system)
        # msg = "queue length: %d. continue... " % self._queue.qsize()
        # input(msg)

    def move_to_tunnel(self, system, i, row, col):

        map = system[KEY.MAP]
        v = map[i]

        # Lets call hallway row -1
        cost =  COST[v[KEY.KIND]] * (abs(v[KEY.HALL] - col) + abs(-1 - row)) 
        system[KEY.COST] = system[KEY.COST] + cost

        v[KEY.HALL] = None
        v[KEY.ROW] = row
        v[KEY.COL] = col
        v[KEY.MOVE] = 2
        # TODO: add cost

    def move_to_hall(self, system, i, move):

        map = system[KEY.MAP]
        v = map[i]

        # Lets call hallway row -1
        cost =  COST[v[KEY.KIND]] * (abs(move - v[KEY.COL]) + abs(-1 - v[KEY.ROW]))
        system[KEY.COST] = system[KEY.COST] + cost

        v[KEY.HALL] = move
        v[KEY.ROW] = None
        v[KEY.COL] = None
        v[KEY.MOVE] = 1
        # TODO: add cost


    def get_move_to_hall(self, map, i, v):

        spot_list = []
        # Move from the tunnel to the hallway

        #print("I must move to the hall")
        # First, am I blocked?
        row = v[KEY.ROW]
        col = v[KEY.COL]

        #print("I am in row", row, "col", col)
        for r in range(0, row):
            if self.get_at_spot(map, r, col) is not None:
                #print("I am blocked, I cannot move")
                return

        #print("I can move!!!")

        # OK what hall stops can I get to?
        # Work up
        for spot in ALLOWABLE_HALL_SPOTS_RIGHT:
            if spot > col:
                if self.get_in_hall(map, spot) is not None:
                    break

                #print("I could move to hall spot", spot)
                spot_list.append(spot)

        for spot in ALLOWABLE_HALL_SPOTS_LEFT:
            if spot < col:
                if self.get_in_hall(map, spot) is not None:
                    break

                #print("I could move to hall spot", spot)
                spot_list.append(spot)

        return spot_list

    def my_range(self, start, stop):

        if start > stop:
            return range(start-1, stop-1, -1)
        else:
            return range(start+1, stop+1)

    def get_move_to_tunnel(self, map, i, v):

        # There are 2 conditions.... the path to the tunnel must be clear, and the
        # and the tunnel must only have the right kinds in it

        current_hall_spot = v[KEY.HALL]
        target_hall_spot = v[KEY.KIND] # My kind corresponds to the target column (tunnel)

        for spot in self.my_range(current_hall_spot, target_hall_spot):
            if self.get_in_hall(map, spot):
                # log.dbg(0, "I am blocked in the hall")
                return

        # Check the tunnel from the bottom up
        for row in [3,2,1,0]:
            index = self.get_at_spot(map, row, target_hall_spot)
            if index is None:
                # log.dbg(0, "%d: can move to this spot row: %d col: %s!!!" % (i, row, target_hall_spot))
                return[(row, target_hall_spot)]

            else:
                meta = map[index]
                if meta[KEY.KIND] != target_hall_spot:
                    return

    def get_move_list(self, map, i, v):

        # print("get move list for %s" % self.get_kind_str(map, i))
        move = v[KEY.MOVE]

        if move == 0:
            # This is a move out of the tunnel and into the hall
            return self.get_move_to_hall(map, i, v)

        elif move == 1:
            # This is a move out of the hall back into the tunnel
            return self.get_move_to_tunnel(map, i, v)

        elif move == 2:
            # This one is in final position!!
            return

        else:
            raise ValueError("bad move number")

    def get_in_hall(self, map, spot):

        for i, v in map.items():
            h = v[KEY.HALL]
            if h is not None:

                # Sanity test
                if v[KEY.COL] is not None:
                    raise ValueError("unexpected col with hall defined")

                if v[KEY.ROW] is not None:
                    raise ValueError("unexpected row with hall defined")

                if h == spot:
                    return i
            else:
                # Sanity test
                if v[KEY.COL] is None:
                    raise ValueError("no col with hall undefined")

                if v[KEY.ROW] is None:
                    raise ValueError("no row with hall undefined")

        return None

    def get_kind_str(self, map, i):
        v = map[i]
        return KIND[v[KEY.KIND]]

    def get_at_spot(self, map, row, col):

        for i, v in map.items():
            if v[KEY.COL] == col and v[KEY.ROW] == row:
                return i
        return None

    def print_row(self, map ,row):

        row_str = '  '
        for col in [A, B, C, D]:
            i = self.get_at_spot(map, row, col)
            if i is None:
                row_str += '. '
            else:
                row_str += '%s ' % self.get_kind_str(map, i)

        print(row_str)

    def print(self, system):

        map = system[KEY.MAP]
        cost = system[KEY.COST]
        self.print_map(map, cost)

    def print_map(self, map, cost):

        print("******* processed: %d abort: %d finished: %d cur cost: %d min_cost: %d" %
              (self._total_count, self._abort_count, self._finished_count, cost, self._min_cost))

        hall_string = ''
        for hall_index in range(0, 11):
            i = self.get_in_hall(map, hall_index)
            if i is None:
                hall_string += '.'
            else:
                hall_string += '%s' % self.get_kind_str(map, i)
        print(hall_string)

        for row in [0,1,2,3]:
            self.print_row((map), row)

if __name__ == '__main__':

    runner = Runner()
    runner.run()
