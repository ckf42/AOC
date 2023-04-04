import AOCInit
import util
import numpy as np
from scipy.signal import convolve

if __name__ != '__main__':
    exit()

inp = util.getInput(d=17, y=2020)

# part 1
stateMap = np.asarray((tuple(tuple(x == '#' for x in l)
                             for l in inp.splitlines()),),
                      dtype=bool)
stencil = np.ones((3, 3, 3), dtype=np.int8)
stencil[1, 1, 1] = 0
for _ in range(6):
    nei = convolve(stateMap, stencil)
    paddedStateMap = np.pad(stateMap, 1)
    np.logical_or(nei == 3,
                  np.logical_and(nei == 2, paddedStateMap),
                  out=paddedStateMap)
    # trim zero boundaries
    # from https://stackoverflow.com/a/65547931
    # and https://stackoverflow.com/a/72832102
    stateMap = paddedStateMap[tuple(np.s_[arr.min():arr.max() + 1]
                                    for arr in paddedStateMap.nonzero())]
print(stateMap.sum())

# part 2
stateMap = np.asarray(((tuple(tuple(x == '#' for x in l)
                             for l in inp.splitlines()),),),
                      dtype=bool)
stencil = np.ones((3, 3, 3, 3), dtype=np.int8)
stencil[1, 1, 1, 1] = 0
for _ in range(6):
    nei = convolve(stateMap, stencil)
    paddedStateMap = np.pad(stateMap, 1)
    np.logical_or(nei == 3,
                  np.logical_and(nei == 2, paddedStateMap),
                  out=paddedStateMap)
    # trim zero boundaries
    # from https://stackoverflow.com/a/65547931
    # and https://stackoverflow.com/a/72832102
    stateMap = paddedStateMap[tuple(np.s_[arr.min():arr.max() + 1]
                                    for arr in paddedStateMap.nonzero())]
print(stateMap.sum())


