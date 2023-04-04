import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=9, y=2020)
preambleLen = 25
cipher = util.getInts(inp)

# part 1
invalidVal = None
preamble = set(cipher[:preambleLen])
for i in range(preambleLen, len(cipher)):
    if not any(cipher[i] - v in preamble for v in preamble):
        invalidVal = cipher[i]
        print(invalidVal)
        break
    preamble.discard(cipher[i - preambleLen])
    preamble.add(cipher[i])

# part 2
assert invalidVal is not None
s, e = (0, 2)
windowSum = sum(cipher[s:e])
while True:
    if windowSum == invalidVal:
        print(min(cipher[s:e]) + max(cipher[s:e]))
        break
    if windowSum > invalidVal:
        windowSum -= cipher[s]
        s += 1
    else:
        windowSum += cipher[e]
        e += 1

