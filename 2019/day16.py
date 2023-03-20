import AOCInit
import util
import numpy as np
from itertools import repeat, chain, cycle

if __name__ != '__main__':
    exit()

inp = util.getInput(d=16, y=2019).strip()

sig = np.asarray(tuple(map(int, inp)), dtype=np.int16)
sigLen = sig.size
basePatt = (1, 0, -1, 0)
m = np.zeros((sigLen, sigLen), np.int16)

for i in range(sigLen):
    g = cycle(chain(*(repeat(v, i + 1) for v in basePatt)))
    for j in range(i, sigLen):
        m[i, j] = next(g)

# part 1
phaseCount = 100
for _ in range(phaseCount):
    np.matmul(m, sig, out=sig)
    np.abs(sig, out=sig)
    np.mod(sig, 10, out=sig)
print(''.join(map(str, sig[:8])))


# part 2
digitsToSkip = int(inp[:7])
repeatCount = 10000
assert 2 * digitsToSkip + 1 >= sigLen * repeatCount
# this implies that m is just upper trig one matrix
sig = np.asarray(tuple(int(inp[i % sigLen])
                       for i in range(sigLen * repeatCount - 1,
                                      digitsToSkip - 1,
                                      -1)),
                 dtype=np.uint32)
for _ in range(phaseCount):
    np.cumsum(sig, out=sig)
    np.mod(sig, 10, out=sig)
print(''.join(map(str, sig[-1:-(8 + 1):-1])))
