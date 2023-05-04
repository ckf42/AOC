import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=1, y=2021)
numb = util.getInts(inp)

# part 1
print(util.count(range(len(numb) - 1),
                 lambda idx: numb[idx] < numb[idx + 1]))


# part 2
windowSum = list(0 for _ in range(len(numb) - 2))
windowSum[0] = sum(numb[:3])
for i in range(1, len(windowSum)):
    windowSum[i] = windowSum[i - 1] - numb[i - 1] + numb[i + 2]
print(util.count(range(len(windowSum) - 1),
                 lambda idx: windowSum[idx] < windowSum[idx + 1]))

