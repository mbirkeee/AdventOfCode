import pathlib

with pathlib.Path("input_real.txt").open('r') as f:
    L = [l.rstrip() for l in f.readlines()]
    w, h = len(L[0]) - 2, len(L) - 2
    Bn = {(i, j, L[i+1][j+1]) for i in range(h) for j in range(w) if L[i+1][j+1] not in ('#', '.')}

M = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0), 0: (0, 0)}
T = 0
B = None

def traverse(start, end):
    global T, B, Bn
    pos = [(start[0], start[1], T)]
    v = set()
    while pos:
        i, j, t = pos.pop(0)
        if B is None or t > T: # evolve
            B = Bn
            Bn = {((i+M[c][0])%h, (j+M[c][1])%w, c)  for i, j, c in B}
            T = t

        for X, Y in ((i+x, j+y) for x, y in M.values()):
            if X == end[0] and Y == end[1]: return
            if ((X, Y) != start) and (X < 0 or Y < 0 or X >= h or Y >= w): continue
            if any(1 for d in M.keys() if d and (X, Y, d) in Bn): continue

            n = (X, Y, t+1)
            if n not in v:
                pos.append(n)
                v.add(n)

print("height: %d width: %d" % (h, w))

traverse((-1, 0), (h, w-1))
print(T+1)
traverse((h, w-1), (-1, 0))
traverse((-1, 0), (h, w-1))

print(T+1)
