import AOCInit
import util
from collections import deque

if __name__ != '__main__':
    exit()

inp = util.getInput(d=9, y=2018)

(playerCount, maxMarble) = util.getInts(inp)

# part 1
score = [0 for _ in range(playerCount)]
q = deque((0,))
for m in range(1, maxMarble + 1):
    if m % 23 == 0:
        q.rotate(7)
        score[m % playerCount] += m + q.popleft()
    else:
        q.rotate(-2)
        q.appendleft(m)
print(max(score))

# part 2
maxMarble *= 100
score = [0 for _ in range(playerCount)]
q = deque((0,))
for m in range(1, maxMarble + 1):
    if m % 23 == 0:
        q.rotate(7)
        score[m % playerCount] += m + q.popleft()
    else:
        q.rotate(-2)
        q.appendleft(m)
print(max(score))


