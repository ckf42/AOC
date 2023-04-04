import AOCInit
import util
from sympy.ntheory import discrete_log

if __name__ != '__main__':
    exit()

inp = util.getInput(d=25, y=2020)

nums = util.getInts(inp)

# part 1
m = 20201227
b = 7
print(pow(nums[1], discrete_log(m, nums[0], b), m))

# part 2
# no part 2

