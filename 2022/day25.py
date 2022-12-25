import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=25, y=2022)

numbers = inp.splitlines()

def toSNAFU(n):
    res = list()
    while n:
        res.append(n % 5)
        n //= 5
    res.append(0)
    for i in range(len(res)):
        if res[i] == 5:
            res[i] = '0'
            res[i + 1] += 1
        elif res[i] in (3, 4):
            res[i] = {3: '=', 4: '-'}[res[i]]
            res[i + 1] += 1
        else:
            res[i] = str(res[i])
    if res[-1] == '0':
        res.pop()
    return ''.join(res[::-1])


replaceDict = {'-': -1, '=': -2, '1': 1, '2': 2, '0': 0}
def toBase10(s):
    return sum(5 ** i * v
               for i, v in enumerate(tuple(replaceDict[c] for c in s)[::-1]))

# part 1
print(toSNAFU(sum(toBase10(s) for s in numbers)))

# part 2
# no part 2

