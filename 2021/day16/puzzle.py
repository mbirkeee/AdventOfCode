"""
Success!!! This was a fun one and was pretty easy
"""

import sys
import numpy as np

class ExceptionDone(Exception):
    pass

class Stream(object):

    def __init__(self):
        self._temp = []
        self._bit_index = 0
        self._bits = None

    def load(self, bits):
        self._bits = bits
        self._bit_index = 0

    def add_bit(self, bit):
        self._temp.append(int(bit))

    def finalize(self):
        self._bits = np.array(self._temp)

    def print(self):
        print(self._bits)

    def get_bits(self, count):
        start = self._bit_index
        stop = start + count
        self._bit_index += count
        return self._bits[start:stop]

    def make_decimal(self, bits, start=0):
        result = start
        for bit in bits:
            result *= 2
            result += bit
        return result

    def get_version(self):
        bits = self.get_bits(3)
        return self.make_decimal(bits)

    def get_pid(self):
        bits = self.get_bits(3)
        return self.make_decimal(bits)

    def get_remaining_count(self):
        return len(self._bits) - self._bit_index

class Runner(object):

    def __init__(self, filename):

        self._stream = Stream()

        self._version_sum = 0

        lines = []
        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                lines.append(line)

            if len(lines) != 1:
                raise ValueError("expect 1 line, got %d" % len(lines))

            for c in line:
                b = bin(int('0x1%c' % c, 16))
                # print("got %c --> %s" % (c, b))
                for i in [3,4,5,6]:
                    # print(b[i])
                    self._stream.add_bit(b[i])
            self._stream.finalize()

        finally:
            if fp: fp.close()

    def read_literal(self, stream):

        value = 0
        while True:
            group =  stream.get_bits(5)
            literal = group[1:]
            value =  stream.make_decimal(literal, start=value)
            # print("literal", literal)

            if group[0] == 1:
                # print("keep reading")
                pass
            else:
                # print("done reading")
                break

        print("return literal value:", value)
        return value

    def read_operator(self, stream, pid):
        """
        To indicate which subsequent binary data represents its sub-packets,
        an operator packet can use one of two modes indicated by the bit
        immediately after the packet header; this is called the length type ID:

        If the length type ID is 0, then the next 15 bits are a number that represents
        the total length in bits of the sub-packets contained by this packet.

        If the length type ID is 1, then the next 11 bits are a number that represents
        the number of sub-packets immediately contained by this packet.
        """

        # Make a list of values for the operator to work on
        values = []
        result = 0
        length_type = stream.get_bits(1)

        if length_type == 0:
            bits = stream.get_bits(15)
            bit_count = stream.make_decimal(bits)
            print("number of bits in subpackets: %d" % bit_count)
            bits = stream.get_bits(bit_count)

            # Make a new stream
            new_stream = Stream()
            new_stream.load(bits)

            try:
                while True:
                    value = self.read_packet(new_stream)
                    values.append(value)

            except ExceptionDone:
                print("done reading sub packets")

        else:
            bits = stream.get_bits(11)
            packet_count = stream.make_decimal(bits)
            print("number subpackets: %d" % packet_count)
            for _ in range(packet_count):
                value = self.read_packet(stream)
                values.append(value)

        print("OPERATOR VALUES", values)

        value_array = np.array(values)
        if pid == 0:
            # This is a sum of the sub packets
            print("OPERATOR: SUM")
            result = np.sum(value_array)

        elif pid == 1:
            print("PRODUCT")
            result = np.product(value_array)

        elif pid == 2:
            print("MIN")
            result = np.min(value_array)

        elif pid == 3:
            print("MAX")
            result = np.max(value_array)

        elif pid == 5:
            print("GREATER THAN")
            if len(value_array) != 2:
                raise ValueError("unexpected number of values!!")

            if value_array[0] > value_array[1]:
                result = 1
            else:
                result = 0

        elif pid == 6:
            print("LESS THAN")
            if len(value_array) != 2:
                raise ValueError("unexpected number of values!!")

            if value_array[0] < value_array[1]:
                result = 1
            else:
                result = 0

        elif pid == 7:

            print("EQUAL TO")

            if len(value_array) != 2:
                raise ValueError("unexpected number of values!!")
            if value_array[0] == value_array[1]:
                result = 1
            else:
                result = 0

        return result

    def read_packet(self, stream):

        if stream.get_remaining_count() < 6:
            raise ExceptionDone

        version = stream.get_version()
        pid = stream.get_pid()

        print("packet version: %d id: %d" % (version, pid))
        self._version_sum += version

        if pid == 4:
            value = self.read_literal(stream)
        else:
            value = self.read_operator(stream, pid)

        return value

    def run(self):
        print("run called")
        # self._bits.print()

        try:
            while True:
                value = self.read_packet(self._stream)
        except ExceptionDone:
            print("Done!!")

        print("Version sum", self._version_sum)
        print("Value", value)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


