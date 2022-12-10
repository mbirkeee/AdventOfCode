import os

class Directory(object):

    def __init__(self, parent, name, root=False):
        # print("make directory: %s" % name)
        self._name = name
        if parent is None:
            parent = self
        self._parent = parent
        self._root =  root
        self._files = {}
        self._directories = {}

    def add_file(self, name, size):
        print("Dir %s add file %s (size: %d)" % (self.get_name(), name, size))
        self._files[name] = size

    def get_name(self):
        return self._name

    def get_parent(self):
        return self._parent

    def add_directory(self, d):
        name = d.get_name()
        self._directories[name] = d

    def get_child(self, name):
        return self._directories[name]

    def get_directories(self):
        return [d for d in self._directories.values()]

    def is_root(self):
        return self._root

    def get_path(self):
        parts = []
        d = self
        while True:
            if d.is_root():
                parts.append('root')
                break
            parts.append(d.get_name())
            d = d.get_parent()

        parts.reverse()
        # print(parts)
        return parts

    def get_size(self):
        size = 0
        for file_name, file_size in self._files.items():
            size += file_size

        directories = self.get_directories()

        for d in directories:
            size += d.get_size()

        return size

class Runner(object):

    def __init__(self):
        print("running")
        self._file_name = 'input_real.txt'
        # self._file_name = 'input_test.txt'

        self._root = Directory(None, 'root', root=True)
        self._cwd = self._root

        self._part1_answer = 0
        self._part2_answer = None
        self._need_space = None

    def run(self):

        fp = open(self._file_name, 'r')

        for line in fp:
            stripped = line.strip()
            self.process_line(stripped)

        fp.close()

        root_size = self._root.get_size()
        free_space = 70000000 - root_size

        self._need_space = 30000000 - free_space

        print("NNED TO FREE: root: %d free: %d short: %d" % (root_size, free_space, self._need_space))


        self.print_directories(self._root)

        print("Part1: %d" % self._part1_answer)
        print("Part2: %d" % self._part2_answer)



        print("done")

    def print_directories(self, d):

        my_size = d.get_size()
        if my_size < 100000:
            self._part1_answer += my_size


        if my_size > self._need_space:
            if self._part2_answer is None or my_size < self._part2_answer:
                self._part2_answer = my_size


        print("NAME: %s (%s) (TOTAL SIZE: %d" % (d.get_name(), repr(d.get_path()), my_size ))
        children = d.get_directories()
        for child in children:
            self.print_directories(child)

    def process_line(self, line):
        # print("LINE: %s" % line)

        if line.startswith('$'):
            if line.startswith('$ cd'):
                self.change_directory(line)

            elif line == '$ ls':
                # print("list directory")
                pass

            else:
                raise ValueError("unknown command")
        else:
            # this MUST be output from an ls command
            if line.startswith('dir'):
                target_dir = line[4:].strip()
                d = Directory(self._cwd, target_dir)
                self._cwd.add_directory(d)
            else:
                # This is a file; add to current directory
                parts = line.split(' ')
                size = int(parts[0].strip())
                name = parts[1].strip()
                self._cwd.add_file(name, size)

    def change_directory(self, line):
        target_dir = line[4:].strip()

        if target_dir == '/':
            self._cwd = self._root

        elif target_dir == '..':
            self._cwd = self._cwd.get_parent()

        else:
            self._cwd = self._cwd.get_child(target_dir)




if __name__ == '__main__':
    runner = Runner()
    runner.run()
