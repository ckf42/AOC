import AOCInit
import util
from collections import Counter

if __name__ != '__main__':
    exit()

inp = """\
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz\
"""
inp = util.getInput(d=2, y=2018)

idList = inp.splitlines()

# part 1
hasTwoCount = 0
hasThreeCount = 0
for line in idList:
    c = Counter(line)
    if 2 in c.values():
        hasTwoCount += 1
    if 3 in c.values():
        hasThreeCount += 1
print(hasTwoCount * hasThreeCount)

# part 2
strLen = len(idList[0])
def hammingDist(s1, s2):
    return len(tuple(i for i in range(strLen) if s1[i] != s2[i]))

l = len(idList)
isFound = False
for i in range(l - 1):
    for j in range(i + 1, l):
        if hammingDist(idList[i], idList[j]) == 1:
            print(''.join(idList[i][k] for k in range(strLen) if idList[i][k] == idList[j][k]))
            isFound = True
    if isFound:
        break


