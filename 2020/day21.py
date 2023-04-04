import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=21, y=2020)

foodList = tuple(
    (set(partSplit[0].split()), set(partSplit[1].split(', ')))
    for line in inp.splitlines()
    if (partSplit := line.rstrip(')').split(' (contains '))
)
allergenToFoodIdx: defaultdict[str, set[int]] = defaultdict(set)
for idx, foodLine in enumerate(foodList):
    for allergen in foodLine[1]:
        allergenToFoodIdx[allergen].add(idx)
possibleAllergenOrigin: dict[str, set[str]] = {
    allergen: set.intersection(*(foodList[idx][0] for idx in idxSet))
    for allergen, idxSet in allergenToFoodIdx.items()
}
confirmedAllergenOrigin: dict[str, str] = dict()
newOriginFound = True
while newOriginFound:
    newOriginFound = False
    for allergen in possibleAllergenOrigin:
        if len(possibleAllergenOrigin[allergen]) == 1:
            newOriginFound = True
            origin = possibleAllergenOrigin.pop(allergen).pop()
            confirmedAllergenOrigin[allergen] = origin
            for otherFoodSets in possibleAllergenOrigin.values():
                otherFoodSets.discard(origin)
            break
unmarkedFood = set.union(*(foodLine[0] for foodLine in foodList))\
        .difference(confirmedAllergenOrigin.values())

# part 1
print(sum(len(foodLine[0].intersection(unmarkedFood)) for foodLine in foodList))

# part 2
print(','.join(confirmedAllergenOrigin[allergen]
               for allergen in sorted(confirmedAllergenOrigin.keys())))

