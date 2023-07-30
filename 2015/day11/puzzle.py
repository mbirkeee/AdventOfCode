import sys
import itertools

ALPHAS = 'abcdefghjkmnpqrstuvwxyz'

class Runner(object):

    def __init__(self, line):

        self._line = line
        self._password = []
        self._password_length = None

    def get_index(self, input):

        for i, c in enumerate(ALPHAS):
            if c == input:
                return i

    def run(self):

        print(self._line)

        print("digit count", len(ALPHAS))

        for c in self._line:
            self._password.append(self.get_index(c))

        print(self._password)
        self._password.reverse()
        print(self._password)

        self._password_length = len(self._password)
        print("password length", self._password_length)

        for _ in range(5000000):
            self.iterate()
            if self.check_password() is True:
                break

    def check_password(self):

        # First, look for three decreasing numbers (recall password is reversed!!
        met = False
        for i in range(self._password_length - 2):
            if self._password[i+1] == self._password[i] - 1:
                if self._password[i+2] == self._password[i] - 2:
                    # print("meets 3 sequential")
                    met = True
                    break

        if not met:
            return False

        met = False
        met_char = None

        # Look for two chars in a row - first pair
        for i in range(self._password_length - 1):
            if self._password[i+1] == self._password[i]:
                # print("meets pair 1")
                met = True
                met_char = self._password[i]
                break

        if not met:
            return False

        # Look for two chars in a row - second pair
        for i in range(self._password_length - 1):
            if self._password[i] == met_char:
                continue

            if self._password[i+1] == self._password[i]:
                return True

        return False


    def print_password(self):
        p = ''
        for i in range(self._password_length -1 , -1, -1):
            p += ALPHAS[self._password[i]]

        print(p)

    def iterate(self):

        for p in range(self._password_length):

            digit = self._password[p]
            digit += 1
            if digit < len(ALPHAS):
                # We are done
                self._password[p] = digit
                break
            self._password[p] = 0

        # print(self._password)
        self.print_password()

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()
