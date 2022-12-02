import AOCInit
import util
import hashlib

inp = 'abcdef'

def computeMD5(s):
    return hashlib.md5(s.encode()).hexdigest()

# part 1
counter = 1
while True:
    if computeMD5(inp + str(counter))[:5] == '00000':
        break
    counter += 1
print(counter)

# part 2
while True:
    if computeMD5(inp + str(counter))[:6] == '000000':
        break
    counter += 1
print(counter)
