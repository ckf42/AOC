import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=16, y=2016).strip()
subTuple = tuple(map(tuple, ('00', '11', '10', '01')))

def step(s):
    return s + '0' + util.subChar('01', '10', s[::-1])

def checksum(s):
    while not (len(s) & 1):
        s = ''.join(util.sub(subTuple, '1100', util.splitIntoGp(s, 2)))
    return s

# part 1
targetLen = 272
s = inp
while len(s) < targetLen:
    s = step(s)
print(checksum(s[:targetLen]))


# part 2
targetLen = 35651584


