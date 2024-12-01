import AOCInit
import util

from collections import Counter


if __name__ != '__main__':
    exit()

inp = util.getInput(d=1, y=2024)

# part 1
nums = util.transpose(util.getInts(line) for line in inp.splitlines())
print(sum(abs(a - b) for a, b in zip(sorted(nums[0]), sorted(nums[1]))))

# part 2
c = Counter(nums[1])
print(sum(x * c[x] for x in nums[0]))

