"""
"""

import sys
import numpy as np

class ExceptionDone(Exception):
    pass



class Runner(object):

    def __init__(self, filename):

        lines = []
        fp = None

        try:
            fp = open(filename, 'r')
            for line in fp:
                line = line.strip()
                lines.append(line)

            if len(lines) != 1:
                raise ValueError("expect 1 line, got %d" % len(lines))


        finally:
            if fp: fp.close()

        inp = lines[0]
        print(inp)

        # Extract the run parameters from the input
        parts = inp.split()

        x_parts = parts[2].split("..")

        self._x_left = int(x_parts[0][2:])
        self._x_right = int(x_parts[1].strip(','))

        y_parts = parts[3].split('..')

        self._y_top = int(y_parts[0][2:])
        self._y_bottom  = int(y_parts[1])

        if self._y_top < self._y_bottom:
            self._y_bottom, self._y_top = self._y_top, self._y_bottom

        print("y_top", self._y_top)
        print("y_bottom", self._y_bottom)

    def run(self):



        # We know that on the ay up and the way down, the ball will hit the zero
        # line. So any velocity at the sero linne greater that y_bottom can
        # never hit the target.  This gives us an upper bound on the y
        # velocities

        height_dict = {}

        y_vel_dict = {}
        for y_vel in range( abs(self._y_bottom)+1, self._y_bottom-1, -1):
            # print("test Y vel %d" % y_vel)

            hit, steps, max_height = self.check_y_velocities(y_vel)
            if hit:
                print("Y vel %d hits, height: %d (steps %s)" % (y_vel, max_height, repr(steps)))
                height_dict[max_height] = steps
                y_vel_dict[y_vel] = steps
            else:
                print("Y vel %d misses" % y_vel)

        # Because we started with the highest Y velocity, the resulting dict will
        # be sorted by max height. So, first successful x hit will result in
        # highest height

        print("----------- part 1")
        print(height_dict)

        try:
            for max_height, steps_list in height_dict.items():
                for steps in steps_list:
                    # print("Check for X hit in %d steps" % steps)

                    for x_vel in range(self._x_right + 1, 0, -1):
                        hit, hit_steps, hit_after_step = self.check_x_velocities(x_vel)
                        if hit:
                            print("X vel %d hits, steps: %s hit_after_step: %d" % (x_vel, repr(hit_steps), hit_after_step))
                            if steps in hit_steps or steps >= hit_after_step and hit_after_step > 0:
                                raise ExceptionDone("Found a hit!!")
                        else:
                            print("X vel %d misses" % x_vel)

        except ExceptionDone:
            print("done; max_height: %d" % max_height)

        print("----------- part 2")
        print(y_vel_dict)

        combo_list = []
        for y_vel, steps_list in y_vel_dict.items():
            for steps in steps_list:

                for x_vel in range(self._x_right + 1, 0, -1):

                    hit, hit_steps, hit_after_step = self.check_x_velocities(x_vel)
                    if hit:
                         if steps in hit_steps or steps >= hit_after_step and hit_after_step > 0:
                            combo_list.append((x_vel, y_vel))

        print(combo_list)
        print(len(combo_list))
        print(len(list(set(combo_list))))

    def check_y_velocities(self, velocity):
        hit = False
        hit_steps = []
        steps = 0

        max_height = 0
        position = 0

        while True:
            steps += 1
            position += velocity

            if position > max_height:
                max_height = position

            if position >= self._y_bottom and position <= self._y_top:
                # print("Y hit on step %d position %d" % (steps, position))
                hit = True
                hit_steps.append(steps)

            if position < self._y_bottom:
                # No point in going farther
                break

            velocity -= 1

        return hit, hit_steps, max_height

    def check_x_velocities(self, velocity):

        hit = False
        hit_steps = []
        steps = 0
        position = 0
        hit_after_step = -1

        while True:
            steps += 1
            position += velocity

            if position >= self._x_left and position <= self._x_right:
                # print("X hit on step %d" % steps)
                hit = True
                hit_steps.append(steps)

            if position > self._x_right:
                # We have gone past the maximum distance
                break

            velocity -= 1
            if velocity == 0:
                # We are never ging to move again, stp searching
                if position >= self._x_left and position <= self._x_right:
                    # special case: motion stopped withing target range
                    print("X motion stopped withing target range!")
                    hit_after_step = steps
                break

        return hit, hit_steps, hit_after_step

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


