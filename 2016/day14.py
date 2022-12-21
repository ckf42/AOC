import AOCInit
import util
from hashlib import md5
import re
from collections import deque

if __name__ != '__main__':
    exit()

salt = util.getInput(d=14, y=2016).strip()
repeat3Re = re.compile(r'(.)\1\1')
repeat5Re = re.compile(r'(.)\1\1\1\1')

def md5Hash(s, repCount):
    for _ in range(repCount):
        s = md5(s.encode()).hexdigest()
    return s

def getRepChar(index, repCount):
    if index not in repCharDict:
        h = md5Hash(salt + str(index), repCount)
        repCharDict[index] = (gp.group(1)
                              if (gp := repeat3Re.search(h)) is not None
                              else None,
                              frozenset(repeat5Re.findall(h)))
    return repCharDict[index]

# part 1
keyCount = 0
idx = 0
repCharDict = dict()
while True:
    if (repChar := getRepChar(idx, 1)[0]) is not None:
        if any(repChar in getRepChar(idx + inc, 1)[1]
               for inc in range(1, 1001)):
            keyCount += 1
            if keyCount == 64:
                break
    idx += 1
print(idx)

# part 2
keyCount = 0
idx = 0
repCharDict = dict()
while True:
    if (repChar := getRepChar(idx, 2017)[0]) is not None:
        if any(repChar in getRepChar(idx + inc, 2017)[1]
               for inc in range(1, 1001)):
            keyCount += 1
            if keyCount == 64:
                break
    idx += 1
print(idx)

