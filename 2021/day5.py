import AOCInit
import util
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=5, y=2021)

segments = tuple(map(util.getInts, inp.splitlines()))
hvIdx = tuple(i
              for i, l in enumerate(segments)
              if l[0] == l[2] or l[1] == l[3])

# part 1
ptCount: defaultdict[complex, int] = defaultdict(int)
for idx in hvIdx:
    seg = segments[idx]
    if seg[0] == seg[2]:
        for k in util.inclusiveRange(seg[1], seg[3], None):
            ptCount[complex(seg[0], k)] += 1
    else:
        for k in util.inclusiveRange(seg[0], seg[2], None):
            ptCount[complex(k, seg[1])] += 1
print(sum(v >= 2 for v in ptCount.values()))

# part 2
ptCount.clear()
for seg in segments:
    if seg[0] == seg[2]:
        for k in util.inclusiveRange(seg[1], seg[3], None):
            ptCount[complex(seg[0], k)] += 1
    elif seg[1] == seg[3]:
        for k in util.inclusiveRange(seg[0], seg[2], None):
            ptCount[complex(k, seg[1])] += 1
    else:
        inc = 1 if seg[3] > seg[1] else -1
        for k in util.inclusiveRange(0, seg[2] - seg[0], None):
            ptCount[complex(seg[0] + k, seg[1] + inc * abs(k))] += 1
print(sum(v >= 2 for v in ptCount.values()))

