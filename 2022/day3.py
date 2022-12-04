import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=3, y=2022).splitlines()

def val(c):
    return ord(c) + ((1 - ord('a')) if c.islower() else (27 - ord('A')))

# part 1
rucksacks = list(util.splitAt(l, len(l) // 2) for l in inp)
print(sum(val(c) for g in rucksacks for c in set.intersection(*map(set, g))))

# part 2
elfGp = util.splitIntoGp(inp, 3)
print(sum(val(c) for g in elfGp for c in set.intersection(*map(set, g))))

