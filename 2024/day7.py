import AOCInit
import util

if __name__ != '__main__':
    exit()

# NOTE:
#     from discussion thread, people seem to be doing DFS / backtracking
#     would it be faster?
#         this would depend if there are many dup intermediate val

inp = util.getInput(d=7, y=2024)

nums = tuple(
        util.getInts(line)
        for line in inp.splitlines()
)

# part 1
evalState = [False] * len(nums)
total = 0
for i, rec in enumerate(nums):
    target = rec[0]
    buff = set((rec[1],))
    for x in rec[2:]:
        buff = set(
            res
            for ele in buff
            for res in (ele + x, ele * x)
            if res <= target
        )
    if target in buff:
        total += target
        evalState[i] = True
print(total)


# part 2
for i, rec in enumerate(nums):
    if evalState[i]:
        continue
    target = rec[0]
    buff = set((rec[1],))
    for x in rec[2:]:
        buff = set(
            res
            for ele in buff
            for res in (ele + x, ele * x, int(str(ele) + str(x)))
            if res <= target
        )
    if target in buff:
        total += target
print(total)


