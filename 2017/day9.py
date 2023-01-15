import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=9, y=2017)

charList = list(inp)
removeCount = 0
searchAtIdx = 0
while True:
    joinedStr = ''.join(charList)
    initIdx = joinedStr.find('<', searchAtIdx)
    if initIdx == -1:
        break
    endIdx = util.matchClosingBracket(joinedStr, initIdx, '>', escapeChar='!', hasNesting=False)
    if endIdx is None:
        raise RuntimeError('no matching closing bracket found')
    ptr = initIdx + 1
    while ptr != endIdx:
        if charList[ptr] == '!':
            ptr += 2
        else:
            removeCount += 1
            ptr += 1
    charList[initIdx:endIdx + 1] = []
    searchAtIdx = initIdx + 1

# part 1
counter = 0
score = 0
for c in charList:
    if c == '{':
        counter += 1
        score += counter
    elif c == '}':
        counter -= 1
print(score)

# part 2
print(removeCount)


