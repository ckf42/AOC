import AOCInit
import util
from typing import Optional

if __name__ != '__main__':
    exit()

inp = util.getInput(d=16, y=2021)

hexSignal = inp.strip()
binDict: dict[str, str] = {
    hex(i)[2:].upper(): bin(i)[2:].zfill(4)
    for i in range(16)
}
packageList: list[dict] = list()

def getBits(s: int, e: Optional[int] = None) -> str:
    if e is None:
        e = s + 1
    return ''.join(binDict[hexSignal[dm[0]]][dm[1]]
                   for i in range(s, e)
                   if (dm := divmod(i, 4)))

def parsePackage(sptr: int) -> tuple[int, int]:
    """
    return start of next package, this package id
    """
    version = int(getBits(sptr, sptr + 3), base=2)
    typeId = int(getBits(sptr + 3, sptr + 6), base=2)
    thisPackIdx = len(packageList)
    packageList.append({'v': version, 't': typeId})
    lenId = getBits(sptr + 6)  # only useful when typeId != 4
    if typeId == 4:
        numBuff = list()
        ptr = sptr + 6
        while True:
            pack = getBits(ptr, ptr + 5)
            numBuff.append(pack[1:])
            ptr += 5
            if pack[0] == '0':
                break
        packageList[thisPackIdx]['val'] = int(''.join(numBuff), base=2)
        return (ptr, thisPackIdx)
    elif lenId == '0':
        subPackBitLen = int(getBits(sptr + 7, sptr + 7 + 15), base=2)
        ptr = sptr + 7 + 15
        subPid = list()
        while ptr < sptr + 7 + 15 + subPackBitLen:
            (ptr, pid) = parsePackage(ptr)
            subPid.append(pid)
        packageList[thisPackIdx]['sub'] = tuple(subPid)
        return (ptr, thisPackIdx)
    elif lenId == '1':
        subPackCount = int(getBits(sptr + 7, sptr + 7 + 11), base=2)
        ptr = sptr + 7 + 11
        subPid = list()
        for _ in range(subPackCount):
            (ptr, pid) = parsePackage(ptr)
            subPid.append(pid)
        packageList[thisPackIdx]['sub'] = tuple(subPid)
        return (ptr, thisPackIdx)
    else:
        raise RuntimeError(f"Unsupported length id: {lenId}")


_, rootIdx = parsePackage(0)

# part 1
print(sum(p['v'] for p in packageList))


# part 2
def evalPack(idx: int) -> int:
    typeId = packageList[idx]['t']
    if typeId == 4:
        return packageList[idx]['val']
    elif typeId == 0:
        return sum(evalPack(subIdx) for subIdx in packageList[idx]['sub'])
    elif typeId == 1:
        return util.prod(evalPack(subIdx) for subIdx in packageList[idx]['sub'])
    elif typeId == 2:
        return min(evalPack(subIdx) for subIdx in packageList[idx]['sub'])
    elif typeId == 3:
        return max(evalPack(subIdx) for subIdx in packageList[idx]['sub'])
    elif typeId == 5:
        return 1 \
                if evalPack(packageList[idx]['sub'][0]) \
                    > evalPack(packageList[idx]['sub'][1]) \
                else 0
    elif typeId == 6:
        return 1 \
                if evalPack(packageList[idx]['sub'][0]) \
                    < evalPack(packageList[idx]['sub'][1]) \
                else 0
    elif typeId == 7:
        return 1 \
                if evalPack(packageList[idx]['sub'][0]) \
                    == evalPack(packageList[idx]['sub'][1]) \
                else 0
    else:
        raise RuntimeError(f"Unsupported type id: {typeId}")


print(evalPack(rootIdx))

