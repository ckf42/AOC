import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=5, y=2023)

inpl = inp.split('\n\n')
seedNums = util.getInts(inpl[0])
mappings = list()
for part in inpl[1:]:
    mapping = dict()
    lines = part.splitlines()
    for line in lines[1:]:
        nums = util.getInts(line)
        mapping[(nums[1], nums[1] + nums[2] - 1)] = nums[0] - nums[1]
    mappings.append(mapping)

# part 1
items = list(seedNums)
for mapping in mappings:
    newItems = items.copy()
    for i, item in enumerate(items):
        for rg, offset in mapping.items():
            if rg[0] <= item <= rg[1]:
                newItems[i] = offset + item
                break
    items = newItems
print(min(items))


# part 2
seedIntervals = list(
        (pr[0], pr[0] + pr[1] - 1)
        for pr in util.splitIntoGp(seedNums, 2))
for mapping in mappings:
    newIntervals = list()
    while len(seedIntervals) != 0:
        itv = seedIntervals.pop()
        hasApply = False
        for rg, offset in mapping.items():
            if (rg[0] <= itv[0] <= rg[1]) or (rg[0] <= itv[1] <= rg[1]):
                intersect = (max(rg[0], itv[0]), min(rg[1], itv[1]))
                newIntervals.append((intersect[0] + offset, intersect[1] + offset))
                if itv[0] < intersect[0]:
                    seedIntervals.append((itv[0], intersect[0] - 1))
                if intersect[1] < itv[1]:
                    seedIntervals.append((intersect[1] + 1, itv[1]))
                hasApply = True
                break
        if not hasApply:
            newIntervals.append(itv)
    seedIntervals = newIntervals
print(min(seedIntervals)[0])


