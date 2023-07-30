import sys
import json

class Runner(object):

    def __init__(self, filename):

        fp = None

        try:

            fp = open(filename, 'r')

            data = json.load(fp)

        finally:
            if fp: fp.close()

        self._data = data
        self._total = 0

    def process(self, data):

        if isinstance(data, dict):

            for value in data.values():
                if isinstance(value, str):
                    if value == "red":
                        # Dont consider this dict
                        return

            for key, value in data.items():
                # print( "KEY: %s %s" % (type(key), repr(key)))
                if not isinstance(key, str):
                    raise ValueError("key not handled")

                self.process(value)

        elif isinstance(data, list):

            for item in data:
                self.process(item)

        elif isinstance(data, str):
            print("ignoring string %s" % data)

        elif isinstance(data, int):
            print("got a number: %d" % data)
            self._total += data

        else:
            print(type(data))
            raise ValueError("type %s not handled" % type(data))

        print("total", self._total)


    def run(self):

        self.process(self._data)




if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
