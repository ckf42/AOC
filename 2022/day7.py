import AOCInit
import util

if __name__ != '__main__':
    exit()
inp = util.getInput(d=7, y=2022)
inp = tuple(map(lambda l: l.splitlines(), inp.strip('$ ').split('\n$ ')))
import sys
sys.setrecursionlimit(2000)

# part 1
sizeLimit = 100000
dirStructure = {'/': []}
pwd = ['']
for block in inp:
    if block[0] != 'ls':
        # cd
        addr = block[0].split()[-1]
        if addr == '/':
            pwd = ['']
        elif addr == '..':
            pwd.pop()
        else:
            cwd = '/' + '/'.join(pwd)
            dirStructure[cwd].append(cwd + '/' + addr)
            pwd.append(addr)
    else:
        # ls
        cwd = '/' + '/'.join(pwd)
        for l in block[1:]:
            # content
            ll = l.split()
            if ll[0] == 'dir':
                if (dd := cwd + '/' + ll[1]) not in dirStructure:
                    dirStructure[dd] = []
            else:
                # is file
                dirStructure[cwd].append(int(ll[0]))

totalSize = {}

def findSize(p):
    if p in totalSize:
        return totalSize[p]
    else:
        for s in dirStructure[p]:
            if isinstance(s, str):
                totalSize[p] = totalSize.get(p, 0) + findSize(s)
            else:
                totalSize[p] = totalSize.get(p, 0) + s
        return totalSize[p]

findSize('/')

print(sum(filter(lambda x: x <= sizeLimit, totalSize.values())))

# part 2
atLeastThisLarge = totalSize['/'] - (70000000 - 30000000)
kvPair = sorted(tuple(totalSize.items()), reverse=False, key=lambda x: x[1])
print(util.firstSuchThat(kvPair, lambda x: x[1] >= atLeastThisLarge)[1][1])

