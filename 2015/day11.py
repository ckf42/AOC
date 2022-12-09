import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = list(ord(c) - ord('a') for c in 'abcdefgh')
l = 8

skipLet = (ord('i'), ord('o'), ord('l'))
consect = (lambda lt, i: lt[i - 1] + 1 == lt[i] == lt[i + 1] - 1)
rep = (lambda lt, i: lt[i] == lt[i + 1])

def checkerFunc(lst):
    idx = next(filter(lambda i: rep(lst, i), range(0, l - 1)), None)
    if idx is None:
        return False
    return next(filter(lambda i: consect(lst, i),
                       range(1, l - 1)), None) is not None \
        and next(filter(lambda i: rep(lst, i), range(idx + 2, l - 1)), None) is not None

def incre(lst):
    while True:
        inp[l - 1] += 1
        for i in range(l - 1, 0, -1):
            if inp[i] == 26:
                inp[i] = 0
                inp[i - 1] += 1
        if (m := util.firstSuchThat(lst,
                                    lambda i: i in skipLet)[0]) is not None:
            lst[m] += 1
            for i in range(m + 1, l):
                lst[i] = 0
        if checkerFunc(lst):
            yield ''.join(map(lambda i: chr(i + ord('a')), lst))

# part 1
pwGen = incre(inp)
print(next(pwGen))

# part 2
print(next(pwGen))

