import AOCInit
import util
from itertools import combinations

if __name__ != '__main__':
    exit()

inp = util.getInput(d=14, y=2020)

# part 1
msk: str = 'X' * 36
mskSetOn: int = 0
mskSetOff: int = (1 << 37) - 1
mem: dict[int, int] = dict()
for line in inp.splitlines():
    if line.startswith('mask'):
        msk = line.rsplit(maxsplit=1)[1]
        mskSetOn = int(msk.replace('X', '0'), base=2)
        mskSetOff = int(msk.replace('X', '1'), base=2)
    else:
        inst = util.getInts(line)
        mem[inst[0]] = (inst[1] | mskSetOn) & mskSetOff
print(sum(mem.values()))

# part 2
mskFloatPart: tuple[int, ...] = tuple()
mskSetOn = 0
mskSetOff = (1 << 37) - 1
mem.clear()
for line in inp.splitlines():
    if line.startswith('mask'):
        msk = line.rsplit(maxsplit=1)[1]
        mskSetOn = int(msk.replace('X', '0'), base=2)
        mskSetOff = int(msk.replace('0', '1').replace('X', '0'), base=2)
        floatUnits = tuple(1 << (35 - i) for i, c in enumerate(msk) if c == 'X')
        mskFloatPart = tuple(sum(p)
                             for r in range(len(floatUnits) + 1)
                             for p in combinations(floatUnits, r))
    else:
        inst = util.getInts(line)
        addr = (inst[0] | mskSetOn) & mskSetOff
        for fp in mskFloatPart:
            mem[addr + fp] = inst[1]
print(sum(mem.values()))

