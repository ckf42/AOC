import AOCInit
import util
import re

if __name__ != '__main__':
    exit()

inp = util.getInput(d=8, y=2015).splitlines()

# part 1
reD = re.compile(r'\\"|\\\\')
reHex = re.compile(r'\\x[0-9a-fA-F]{2}')

def parseLine(s):
    ss = s[1:-1]
    return len(reD.findall(ss)) + 3 * len(reHex.findall(ss)) + 2

print(sum(parseLine(l) for l in inp))

# part 2
print(sum(sum(util.sub(('"', '\\'), (1, 1), s, discard=True)) + 2 for s in inp))

