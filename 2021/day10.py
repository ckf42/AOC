import AOCInit
import util
from statistics import median

if __name__ != '__main__':
    exit()

inp = util.getInput(d=10, y=2021)

codeLines = inp.splitlines()

matchingOpen = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}
bracketErrorScore = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
errorScore = 0
completionScores = list()
for line in codeLines:
    stack = list()
    isCorrupted = False
    for c in line:
        if c in '([{<':
            stack.append(c)
        else:
            if matchingOpen[c] != stack[-1]:
                errorScore += bracketErrorScore[c]
                isCorrupted = True
                break
            else:
                stack.pop()
    if not isCorrupted:
        completionScores.append(
                util.fromBase(util.sub('([{<', tuple(range(1, 5)), stack[::-1]),
                              5)
        )

# part 1
print(errorScore)

# part 2
print(median(completionScores))


