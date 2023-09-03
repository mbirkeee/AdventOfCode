import sys
import numpy as np
import copy
import hashlib

class ExceptionDone(Exception):
    pass

class Runner(object):

    def __init__(self, filename):

        if filename.startswith('t'):
            # this is test mode
            self._disk_length = 20
            self._initial_state = '10000'

        elif filename.startswith('p'):
            self._initial_state = '10111100110001111'
            # self._disk_length = 272
            self._disk_length = 35651584

    def run(self):

        length = len(self._initial_state)
        array = np.zeros((length), dtype=np.int)

        for i, c in enumerate(self._initial_state):
            if c == '1':
                array[i] = 1

        while True:

            len_cur = len(array)

            if len_cur >= self._disk_length:
                print("need: %d have: %d" % (self._disk_length, len_cur))
                array = array[:self._disk_length]
                break

            # print("must implement the dragon curve")

            len_new = 2 * len_cur + 1
            array_new = np.zeros((len_new))

            array_new[0:len_cur] = array

            # print("*"*80)
            # print(array)

            flipped = np.flip(array)
            flipped *= -1
            flipped += 1

            array_new[len_cur + 1:] = np.flip(array)
            # print(array_new)

            array = array_new

            # input("continue...")

        print("now compute checksum")
        have_len = len(array)
        print("have data len", have_len)

        while True:
            l = len(array)
            if l % 2:
                print("length is odd; we are done")
                break

            i_in = 0
            i_out = 0

            array_new = np.zeros((l//2))
            while True:
                if i_in >= l:
                    break
                pair_0 = array[i_in]
                pair_1 = array[i_in+1]

                if pair_0 == pair_1:
                    array_new[i_out] = 1
                i_in += 2
                i_out += 1

            array = array_new

        print("done")
        print("cksum", array)

        cksum = ''
        for i in range(len(array)):
            if array[i]:
                cksum += '1'
            else:
                cksum += '0'
        print(cksum)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
