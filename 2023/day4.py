import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=4, y=2023).splitlines()
matches = list()
for line in inp:
    nums = line.split(': ')[1].split('|')
    matches.append(len(
        frozenset(util.getInts(nums[0]))\
                .intersection(util.getInts(nums[1]))
        ))

# part 1
print(sum(2 ** (pt - 1) for pt in matches if pt != 0))

# part 2
multiplier = list(1 for _ in matches)
for idx, pt in enumerate(matches):
    if pt != 0:
        for i in range(1, pt + 1):
            multiplier[idx + i] += multiplier[idx]
print(sum(multiplier))

