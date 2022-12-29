import AOCInit
import util
# from collections import deque
# from functools import cache

if __name__ != '__main__':
    exit()

inp = util.getInput(d=19, y=2016)

n = int(inp)

# https://en.wikipedia.org/wiki/Josephus_problem#k=2
def survivingPrisoner(k):
    l = k
    r = 1
    while l != 1:
        l //= 2
        r *= 2
    return (k - r) * 2 + 1

# part 1
# print(survivingPrisoner(n))

# part 2
# TODO: need to prove this. Currently done by observing pattern
# @cache
# def modified(k):
    # q = deque(range(1, k + 1))
    # while (l := len(q)) != 1:
        # q.rotate(-(l // 2))
        # q.popleft()
        # q.rotate(l // 2 - 1)
    # return q[0]

def modifiedSurvivingPrisoner(k):
    l = k
    r = 1
    while l >= 3:
        l //= 3
        r *= 3
    return r * (l - 1) + (k - l * r) * l

