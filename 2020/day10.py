import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=10, y=2020)
adapterRatings = [0] + sorted(util.getInts(inp))
adapterRatings.append(adapterRatings[-1] + 3)

# part 1
jumpCount = [0 for i in range(4)]
for i in range(1, len(adapterRatings)):
    jumpCount[adapterRatings[i] - adapterRatings[i - 1]] += 1
print(jumpCount[1] * jumpCount[3])

# part 2
methodCount: list[int] = [0, 1]
for e in range(2, len(adapterRatings)):
    count = 0
    for i in range(e - 2, -1, -1):
        if adapterRatings[e - 1] - adapterRatings[i] > 3:
            break
        count += methodCount[i + 1]
    methodCount.append(count)
print(methodCount[-1])

