import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = 'dabAcCaCBAcCcaDA'
inp = util.getInput(d=5, y=2018).strip()

delta = ord('A') - ord('a')
nextLetter = {chr(k): chr(v)
              for i in range(ord('a'), ord('z') + 1)
              for (k, v) in ((i, i + delta), (i + delta, i))}

def polymerReact(polyStr):
    ptr = 0
    polymer = list(polyStr)
    while ptr + 1 < len(polymer):
        while 0 <= ptr \
                and ptr + 1 < len(polymer) \
                and polymer[ptr + 1] == nextLetter[polymer[ptr]]:
            polymer[ptr:ptr + 2] = []
            ptr -= 1
        # if ptr + 1 == len(polymer):
            # break
        ptr += 1
    return ''.join(polymer)

# part 1
minLen = len(polymerReact(inp))
print(minLen)

# part 2
for i in range(ord('a'), ord('z') + 1):
    if chr(i) in inp or chr(i).upper() in inp:
        minLen = min(minLen,
                     len(polymerReact(''.join(c for c in inp
                                              if c not in (chr(i), chr(i).upper())))))
print(minLen)


