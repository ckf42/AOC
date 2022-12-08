import AOCInit
import util
import numpy as np

# TODO: would rewrite with seg tree save space? currently takes ~2 MB

if __name__ != '__main__':
    exit()

inp = tuple((ls[0] if ls[0] == 'toggle' else ls[1], util.getInts(l))
            for l in util.getInput(d=6, y=2015).splitlines()
            if (ls := l.split()))
dim = 1000

# part 1
lights = np.full((dim, dim), False, dtype=bool)
for inst in inp:
    (l, r, u, d) = (inst[1][0], inst[1][2] + 1, inst[1][1], inst[1][3] + 1)
    if inst[0] == 'toggle':
        np.logical_not(lights[l:r, u:d], out=lights[l:r, u:d])
    else:
        lights[l:r, u:d] = inst[0] == 'on'
print(np.sum(lights))

# part 2
lights = np.full((dim, dim), 0, dtype=np.int16)
for inst in inp:
    (l, r, u, d) = (inst[1][0], inst[1][2] + 1, inst[1][1], inst[1][3] + 1)
    lights[l:r, u:d] += {'on': 1, 'off': -1, 'toggle': 2}[inst[0]]
    if inst[0] == 'off':
        np.maximum(lights[l:r, u:d], 0, out=lights[l:r, u:d])
print(np.sum(lights))

