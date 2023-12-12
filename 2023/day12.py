import AOCInit
import util
from functools import cache

if __name__ != '__main__':
    exit()

inp = util.getInput(d=12, y=2023)
records = tuple(
        (ls[0], util.getInts(ls[1]))
        for line in inp.splitlines()
        if (ls := line.split()))

# part 1
# DP, still too slow
def countArrange(rec, hints):
    rec = rec + '.'  # to flush last currCombo
    @cache
    def dp(recPtr, hintPtr, currCombo):
        # can we tail recur? may repeat code too many times
        res = 0
        if recPtr == len(rec):  # if no more space
            return hintPtr == len(hints)  # no more hints
        if hintPtr == len(hints):  # if no more hints
            return all(c != '#' for c in rec[recPtr:])  # no block
        if rec[recPtr] in '.?':
            # proceed as .
            newHintPtr = hintPtr
            newCombo = currCombo
            if currCombo != 0 and hints[hintPtr] == currCombo:
                # flush currCombo
                newHintPtr = hintPtr + 1
                newCombo = 0
            if newCombo == 0:
                # flush succeed / nothing to flush
                res += dp(recPtr + 1, newHintPtr, 0)
        if rec[recPtr] in '#?':
            # proceed as #
            newCombo = currCombo + 1
            if newCombo <= hints[hintPtr]:
                # still not violate hint
                res += dp(recPtr + 1, hintPtr, newCombo)
        return res
    return dp(0, 0, 0)

print(sum(countArrange(*rec) for rec in records))

# part 2
print(sum(countArrange('?'.join(rec for _ in range(5)), hints * 5)
          for (rec, hints) in records))


