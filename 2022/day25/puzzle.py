import numpy as np
import math

class ExceptionDeadEnd(Exception):
    pass

class ExceptionDone(Exception):
    pass

VALUE = {
    "2" :  2,
    "1" :  1,
    "0" :  0,
    "-" : -1,
    "=" : -2
}

SUBTRACT_FIVE = {
    '3' : '=',
    '4' : '-',
    '5' : '0',
    '6' : '1',
    '7' : '2'
}

ADD_ONE = {
    '0' : '1',
    '1' : '2',
    '2' : '3',
    '3' : '4',
    '4' : '5'
}


class Number(object):

    """
    2     =    2
    1     =    1
    0     =    0
    -     =   -1
    =     =   -2
    """
    def __init__(self, snafu=None, decimal=None):

        self._snafu = snafu
        self._decimal = decimal
        self._base = 5
        self._digits = ['4', '3' ,'2', '1', '0']


    def get_snafu(self):
        if self._snafu is None:
            self._snafu = self.make_snafu()
        return self._snafu

    def get_decimal(self):

        if self._decimal is None:
            self._decimal = self.make_decimal()

        return self._decimal

    def make_decimal(self):

        value = 0
        array = [c for c in self._snafu]
        array.reverse()

        for i, c in enumerate(array):
            # print(c)
            add = VALUE[c] * math.pow(self._base, (i))
            value += add

        return value


    def make_snafu(self):

        print("---- convert %d to snafu -------" % self._decimal)

        snafu = self.decimal_to_snafu(self._decimal)
        print(snafu)
        return snafu

    def decimal_to_snafu(self, num, base=5):

        # First, convert the decimal number ot base 5
        base_five = []

        while num > 0:
            dig = int( num % base )
            if dig > 10:
                raise ValueError('value error')
            base_five.append(str(dig))
            num //= base

        print("reversed digit array: %s" % repr(base_five))

        base_five.append('0')

        for i in range(len(base_five)):

            c = base_five[i]

            if c in ['0', '1', '2']:
                continue
            else:
                base_five[i] =  SUBTRACT_FIVE[c]
                base_five[i+1] = ADD_ONE[base_five[i+1]]

        print(base_five)

        if base_five[-1] == '0':
            base_five.pop(-1)

        base_five.reverse()

        return ''.join(base_five)

class Runner(object):

    def __init__(self):
        self._file_name = 'input_test.txt'
        # self._file_name = 'input_test2.txt'
        self._file_name = 'input_real.txt'

        self._numbers = []

    def run(self):

        fp = open(self._file_name, 'r')
        lines = []
        for line in fp:
            lines.append(line.strip())
        fp.close()

        for line in lines:
            n = Number(snafu=line)
            self._numbers.append(n)

        for n in self._numbers:
            print("snafu: %20s    %20d" % (n.get_snafu(), n.get_decimal() ))

        total = 0
        for n in self._numbers:
            total += n.get_decimal()

        print("the total is: %d" % total)
        n = Number(decimal=total)
        print("SNAFU: %s" % n.get_snafu())

if __name__ == '__main__':
    runner = Runner()
    runner.run()
