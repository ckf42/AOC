import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=22, y=2019)

# part 1
cardCount = 10007
(a, b) = (1, 0) # x |-> a x + b
for line in inp.splitlines():
    if 'into new stack' in line:
        a *= -1
        b = cardCount - 1 - b
    elif 'cut' in line:
        b = (b - int(line.rsplit(maxsplit=1)[-1])) % cardCount
    else:
        offset = int(line.rsplit(maxsplit=-1)[-1])
        a = (a * offset) % cardCount
        b = (b * offset) % cardCount
print((2019 * a + b) % cardCount)

# part 2
cardCount = 119315717514047
iterCount = 101741582076661
(a, b) = (1, 0) # x |-> a x + b
for line in inp.splitlines()[::-1]:
    if 'into new stack' in line:
        a *= -1
        b = cardCount - 1 - b
    elif 'cut' in line:
        b = (b + int(line.rsplit(maxsplit=1)[-1])) % cardCount
    else:
        offset = pow(int(line.rsplit(maxsplit=-1)[-1]), -1, cardCount)
        a = (a * offset) % cardCount
        b = (b * offset) % cardCount
b = (b * (pow(a, iterCount, cardCount) - 1) * pow(a - 1, -1, cardCount)) % cardCount
a = pow(a, iterCount, cardCount)
print((2020 * a + b) % cardCount)
