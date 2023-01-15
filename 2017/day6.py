import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=6, y=2017)

memBanks = list(util.getInts(inp))
l = len(memBanks)

# part 1
visited = dict()
count = 0
while (tm := tuple(memBanks)) not in visited:
    visited[tm] = count
    count += 1
    idx = memBanks.index(max(memBanks))
    (q, r) = divmod(memBanks[idx], l)
    memBanks[idx] = 0
    for i in range(1, r + 1):
        memBanks[(idx + i) % l] += q + 1
    for i in range(r + 1, l + 1):
        memBanks[(idx + i) % l] += q
print(count)

# part 2
print(count - visited[tuple(memBanks)])

