import AOCInit
import util

inp = util.getInput(d=3, y=2022).splitlines()

def val(c):
    return ord(c) + ((1 - ord('a')) if c.islower() else (27 - ord('A')))

# part 1
rucksacks = list((l[:len(l) // 2], l[len(l) // 2:]) for l in inp)
print(sum(val(c) for g in rucksacks for c in set.intersection(*(set(r) for r in g))))

# part 2
elfGp = list((inp[i], inp[i + 1], inp[i + 2]) for i in range(0, len(inp), 3))
print(sum(val(c) for g in elfGp for c in set.intersection(*(set(r) for r in g))))

