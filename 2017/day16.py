import AOCInit
import util
from collections import deque

if __name__ != '__main__':
    exit()

inp = util.getInput(d=16, y=2017)

danceSeq = tuple((('p', l[1], l[3])
                  if l[0] == 'p'
                  else (l[0],) + util.getInts(l))
                 for l in inp.split(','))

q = deque(chr(ord('a') + i) for i in range(16))
history = {''.join(q): 0}
targetTime = 1000000000
timeFinished = 0
pattern = None
while timeFinished < targetTime:
    for inst in danceSeq:
        if inst[0] == 's':
            q.rotate(inst[1])
        else:
            swpIdx = inst[1:] if inst[0] == 'x' else tuple(q.index(c) for c in inst[1:])
            q[swpIdx[0]], q[swpIdx[1]] = q[swpIdx[1]], q[swpIdx[0]]
    timeFinished += 1
    pattern = ''.join(q)
    if timeFinished == 1:
        print(pattern)
    if pattern in history:
        break
    else:
        history[pattern] = timeFinished

if timeFinished == targetTime:
    print(pattern)
else:
    periodStart = history[pattern]
    period = timeFinished - periodStart
    historyByTime = {v: k for k, v in history.items()}
    print(historyByTime[periodStart + (targetTime - periodStart) % period])


