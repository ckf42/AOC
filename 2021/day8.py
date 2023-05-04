import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=8, y=2021)

signals = tuple(
    (ls[0].split(), ls[1].split())
    for line in inp.splitlines()
    if (ls := line.split(' | '))
)

# part 1
print(sum(sum(len(p) in (2, 3, 4, 7) for p in digits)
          for _, digits in signals))

# part 2
digitDisplay: dict[frozenset[str], str] = {
    frozenset('abcefg'): '0',
    frozenset('cf'): '1',
    frozenset('acdeg'): '2',
    frozenset('acdfg'): '3',
    frozenset('bcdf'): '4',
    frozenset('abdfg'): '5',
    frozenset('abdefg'): '6',
    frozenset('acf'): '7',
    frozenset('abcdefg'): '8',
    frozenset('abcdfg'): '9',
}
letterStr = 'abcdefg'
digitSums = 0
for patts, digits in signals:
    corresp = {
        c: set(letterStr)
        for c in letterStr
    }
    sigList = patts + digits
    stoke5 = list()
    stoke6 = list()
    for sig in sigList:
        if len(sig) == 2:
            # 2
            for c in letterStr:
                if c in sig:
                    corresp[c].intersection_update('cf')
                else:
                    corresp[c].difference_update('cf')
        elif len(sig) == 3:
            # 7
            for c in letterStr:
                if c in sig:
                    corresp[c].intersection_update('acf')
                else:
                    corresp[c].difference_update('acf')
        elif len(sig) == 4:
            # 4
            for c in letterStr:
                if c in sig:
                    corresp[c].intersection_update('bcdf')
                else:
                    corresp[c].difference_update('bcdf')
        elif len(sig) == 7:
            # 8
            pass
        elif len(sig) == 5:
            # 2, 3, 5
            stoke5.append(sig)
        elif len(sig) == 6:
            # 0, 6, 9
            stoke6.append(sig)
    adg = frozenset.intersection(*(frozenset(sig) for sig in stoke5))
    for c in letterStr:
        if c in adg:
            corresp[c].intersection_update('adg')
        else:
            corresp[c].difference_update('adg')
    abfg = frozenset.intersection(*(frozenset(sig) for sig in stoke6))
    for c in letterStr:
        if c in abfg:
            corresp[c].intersection_update('abfg')
        else:
            corresp[c].difference_update('abfg')
    assert all(len(v) == 1 for v in corresp.values())
    letterMap = {
        k: next(iter(v))
        for k, v in corresp.items()
    }
    digitSums += int(''.join(
        digitDisplay.get(frozenset(map(lambda x: letterMap[x], d)))
                             for d in digits))
print(digitSums)


