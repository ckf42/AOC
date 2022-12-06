import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInts(util.getInput(d=17, y=2015))
target = 150
# inp = [20, 15, 10, 5, 5]
# target = 25

# part 1
dp = {0: (1, 0, 1)} # (ways, min containers, ways with min containers)
for newItem in inp:
    vals = sorted(dp.keys(), reverse=True)
    for v in vals:
        if v + newItem <= target:
            dpv = dp[v]
            dvOld = dp.get(v + newItem, (0, float('inf'), 0))
            if dvOld[1] > dpv[1] + 1:
                dp[v + newItem] = (dvOld[0] + dpv[0],
                                   dpv[1] + 1,
                                   dpv[2])
            elif dvOld[1] < dpv[1] + 1:
                dp[v + newItem] = (dvOld[0] + dpv[0],
                                   dvOld[1],
                                   dvOld[2])
            else:
                dp[v + newItem] = (dvOld[0] + dpv[0],
                                   dvOld[1],
                                   dpv[2] + dvOld[2])
print(dp[target][0])

# part 2
print(dp[target][2])

