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
    for i, item in enumerate(items):
        for rg, offset in mapping.items():
            if rg[0] <= item <= rg[1]:
                items[i] = offset + item
                break
print(min(items))


# part 2
# admittedly this can be further modularized
# by extending the existing util.IntegerIntervals
# to support piecewise functions (constant shifting)
# and various operations
# and rewrite some inplace operations to return values
seedItvs = list(
        (pr[0], pr[0] + pr[1] - 1)
        for pr in util.splitIntoGp(seedNums, 2))
for mapping in mappings:
    newItvs = list()
    while len(seedItvs) != 0:
        itv = seedItvs.pop()
        hasApply = False
        for rg, offset in mapping.items():
            if (rg[0] <= itv[0] <= rg[1]) or (rg[0] <= itv[1] <= rg[1]):
                intersect = (max(rg[0], itv[0]), min(rg[1], itv[1]))
                newItvs.append((intersect[0] + offset, intersect[1] + offset))
                if itv[0] < intersect[0]:
                    seedItvs.append((itv[0], intersect[0] - 1))
                if intersect[1] < itv[1]:
                    seedItvs.append((intersect[1] + 1, itv[1]))
                hasApply = True
                break
        if not hasApply:
            newItvs.append(itv)
    seedItvs = newItvs
print(min(itv[0] for itv in seedItvs))


