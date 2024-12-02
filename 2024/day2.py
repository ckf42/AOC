import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=2, y=2024)

nums = tuple(util.getInts(line) for line in inp.splitlines())

# part 1
def isSafeRow(row):
    n = len(row)
    incFail = False
    decFail = False
    for i in range(1, n):
        if row[i] - row[i - 1] not in range(1, 4):
            incFail = True
        if row[i - 1] - row[i] not in range(1, 4):
            decFail = True
        if incFail and decFail:
            return False
    return True

states = []
for row in nums:
    states.append(isSafeRow(row))
print(sum(states))


# part 2
count = 0
for i, row in enumerate(nums):
    if not states[i]:
        n = len(row)
        for j in range(n):
            if isSafeRow(row[:j] + row[j + 1:]):
                states[i] = True
                break
print(sum(states))

