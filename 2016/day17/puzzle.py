import sys
import numpy as np
import copy
import hashlib

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self, filename):

        self._rows = 4
        self._cols = 4

        self._row_tgt = 3
        self._col_tgt = 3

        self._path_list = []

        if filename.startswith('t'):
            # this is test mode
            # self._passcode = 'ihgpwlah'
            self._passcode = 'ulqzkmiv'

        elif filename.startswith('p'):
            self._passcode = 'pslxynzg'



    def move(self, state):

        # Check if we are done
        row = state['r']
        col = state['c']

        if row == self._row_tgt and col == self._col_tgt:
            # print("made it to the destination")
            # print(state)
            self._path_list.append(state['p'])
            return

        # We must move.  First, determine which doors are available to us
        s = '%s%s' % (self._passcode, state['p'])
        # print("compute hash of", s)
        h = hashlib.md5(s.encode('utf-8')).hexdigest()
        # print("compute hash of:", s, h[0], h[1], h[2], h[3])

        # UP:
        if row > 0:
            if h[0] in ['b', 'c', 'd', 'e', 'f']:
                state_new = copy.deepcopy(state)
                state_new['r'] = row - 1
                state_new['p'] = state_new['p'] + 'U'
                self.move(state_new)

        # Down:
        if row < (self._rows - 1):
            if h[1] in ['b', 'c', 'd', 'e', 'f']:
                state_new = copy.deepcopy(state)
                state_new['r'] = row + 1
                state_new['p'] = state_new['p'] + 'D'
                self.move(state_new)

        # Left:
        if col > 0:
            if h[2] in ['b', 'c', 'd', 'e', 'f']:
                state_new = copy.deepcopy(state)
                state_new['c'] = col - 1
                state_new['p'] = state_new['p'] + 'L'
                self.move(state_new)

        # Right:
        if col < (self._cols - 1):
            if h[3] in ['b', 'c', 'd', 'e', 'f']:
                state_new = copy.deepcopy(state)
                state_new['c'] = col + 1
                state_new['p'] = state_new['p'] + 'R'
                self.move(state_new)

        return

    def run(self):

        print("running, passcode:", self._passcode)

        state = {
            'r': 0,
            'c': 0,
            'p' : ''
        }

        self.move(state)

        min_length = None
        for i, path in enumerate(self._path_list):
            # print("path: %d len: %d %s" % (i, len(path), path))
            l = len(path)
            if min_length is None or l < min_length:
                min_length = l
                print("min", path)

        max_length = None
        for i, path in enumerate(self._path_list):
            # print("path: %d len: %d %s" % (i, len(path), path))
            l = len(path)
            if max_length is None or l > max_length:
                max_length = l
                print("%d max %s" % (len(path), path))


if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
