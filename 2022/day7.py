import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = tuple(map(lambda l: l.splitlines(),
                util.getInput(d=7, y=2022).strip('$ ').split('\n$ ')))

# part 1
sizeLimit = 100000
dirStructure = {'/': list()}
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
                    dirStructure[dd] = list()
            else:
                # is file
                dirStructure[cwd].append(int(ll[0]))

totalSize = dict()

def findSize(p):
    if p not in totalSize:
        totalSize[p] = 0
        for s in dirStructure[p]:
            if isinstance(s, str):
                totalSize[p] += findSize(s)
            else:
                totalSize[p] += s
    return totalSize[p]

findSize('/')
tVs = totalSize.values()
print(sum(filter(lambda x: x <= sizeLimit, tVs)))

# part 2
atLeastThisLarge = totalSize['/'] - (70000000 - 30000000)
print(util.firstSuchThat(sorted(tVs, reverse=False), lambda x: x >= atLeastThisLarge)[1])

