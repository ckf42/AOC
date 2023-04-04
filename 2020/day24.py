import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=24, y=2020)

def parseInst(inst: str) -> tuple[str, ...]:
    ptr = 0
    instList: list[str] = list()
    while ptr < len(inst):
        if inst[ptr] in 'ew':
            instList.append(inst[ptr])
            ptr += 1
        else:
            instList.append(inst[ptr:ptr + 2])
            ptr += 2
    return tuple(instList)

instructions = tuple(map(parseInst, inp.splitlines()))
nbDict: dict[str, complex] = {
    'e': complex(2, 0),
    'w': complex(-2, 0),
    'ne': complex(1, 1), # (1 + 1 * sq3) / 2
    'se': complex(1, -1), # (1 - 1 * sq3) / 2
    'nw': complex(-1, 1), # (-1 + 1 * sq3) / 2
    'sw': complex(-1, -1), # (-1 - 1 * sq3) / 2
}

# part 1
blackTiles: set[complex] = set()
for inst in instructions:
    pt = complex(0, 0)
    for cmd in inst:
        pt += nbDict[cmd]
    if pt not in blackTiles:
        blackTiles.add(pt)
    else:
        blackTiles.remove(pt)
print(len(blackTiles))


# part 2
# ~1s
neiCount: defaultdict[complex, int] = defaultdict(int)
for _ in range(100):
    neiCount.clear()
    for pt in blackTiles:
        for d in nbDict.values():
            neiCount[pt + d] += 1
    blackTiles = set((pt
                      for pt, c in neiCount.items()
                      if c == 2 or (c == 1 and pt in blackTiles)))
print(len(blackTiles))


