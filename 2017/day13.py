import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=13, y=2017)

layerDepth = {il[0]: il[1]
              for l in inp.splitlines()
              if (il := util.getInts(l))}
modM = {k: 2 * v - 2 for (k, v) in layerDepth.items()}
layerCount = max(layerDepth.keys())

# part 1
severity = 0
for i in range(layerCount + 1):
    if i in layerDepth and i % modM[i] == 0:
        severity += i * layerDepth[i]
print(severity)


# part 2
# TODO: find formula?
basicOffset = {k: k % modM[k] for k in layerDepth}
layerIdxList = sorted(layerDepth, key=lambda k: modM[k]) # marginally faster
delayCount = 1
while any((delayCount + basicOffset[k]) % modM[k] == 0 for k in layerIdxList):
    delayCount += 1
print(delayCount)

