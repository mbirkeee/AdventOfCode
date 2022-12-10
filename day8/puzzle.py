import numpy as np

class Runner(object):

    def __init__(self):
        print("running")
        self._file_name = 'input_real.txt'
        # self._file_name = 'input_test.txt'


        self._part1_answer = 0
        self._part2_answer = None

    def run(self):

        fp = open(self._file_name, 'r')

        lines = []
        cols = None

        for line in fp:
            stripped = line.strip()
            # print(stripped)
            lines.append(stripped)

            if cols is None:
                cols = len(stripped)
            else:
                if len(stripped) != cols:
                    raise ValueError("bad input")
        fp.close()

        rows = len(lines)

        # print("ROWS: %d COLS: %d" % (rows, cols))

        array = np.zeros((rows, cols), dtype=np.int32)

        for row, line in enumerate(lines):
            for col, val in enumerate(line):
                array[row,col] = val

        visible_count = 0
        max_score = 0

        for row in range(rows):
            for col in range(cols):

                visible = False

                h = array[row, col]

                above = array[0:row,col]
                below = array[row+1:,col]
                left = array[row,0:col]
                right = array[row,col+1:]

                for other in [left, right, above, below]:
                    if len(other) == 0:
                        visible = True
                    elif max(other) < h:
                        visible = True

                if visible:
                    visible_count += 1

                # if row != 3 or col !=2:
                #     continue

                # print("check tree at %d,%d height: %d" % (row, col, h))

                # print("left : %s" % left)
                # print("right: %s" % right)
                # print("above: %s" % above)
                # print("below: %s" % below)

                if len(left) is 0:
                    continue

                if len(right) is 0:
                    continue

                if len(above) == 0:
                    continue

                if len(below) == 0:
                    continue

                left = np.flip(left)
                above = np.flip(above)

                # print("left : %s" % left)
                # print("right: %s" % right)
                # print("above: %s" % above)
                # print("below: %s" % below)

                distance = [0,0,0,0]

                for d, item in enumerate([left, right, above, below]):

                    for i in range(len(item)):
                        if item[i] >= h:
                            break
                    distance[d] = i+1

                # print(distance)

                score = distance[0] * distance[1] * distance[2] * distance[3]

                # print("tree: %d,%d height: %d score: %d" % (row, col, h, score))

                if score > max_score:
                    max_score = score

        print("visible count: %s" % visible_count)
        print("max score: %d" % max_score)

        print("done")



if __name__ == '__main__':
    runner = Runner()
    runner.run()
