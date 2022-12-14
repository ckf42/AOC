import AOCInit
import util
import re

if __name__ != '__main__':
    exit()

inp = util.getInput(d=7, y=2016).splitlines()
spliterRe = re.compile(r'\[[^\[\]]+\]')
addrList = tuple((tuple(p[1:-1] for p in spliterRe.findall(s)),
                  tuple(spliterRe.split(s)))
                 for s in inp)

# part 1
abbaRe = re.compile(r'(?=(\w)(\w)\2\1)')

def isABBA(s):
    return any(gp[0] != gp[1] for gp in abbaRe.findall(s))

def isTLS(hs):
    return any(isABBA(p) for p in hs[1]) and not any(isABBA(p) for p in hs[0])

print(util.count(addrList, isTLS))

# part 2
babRe = re.compile(r'(?=(.)(.)\1)')

def isSSL(hs):
    abaList = tuple(gp[1] + gp[0] + gp[1]
                    for h in hs[0]
                    for gp in babRe.findall(h)
                    if gp[0] != gp[1])
    return any((aba in s) for aba in abaList for s in hs[1])

print(util.count(addrList, isSSL))

