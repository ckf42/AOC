import AOCInit
import util
from hashlib import md5
from random import choice

if __name__ != '__main__':
    exit()

inp = '123'
doAnimation = True
animationRate = 36000

# part 1
counter = 0
outputBuffer = list()
while len(outputBuffer) != 8:
    h = md5((inp + str(counter)).encode()).hexdigest()
    if h[:5] == '00000':
        outputBuffer.append(h[5])
    counter += 1
print(''.join(outputBuffer))


# part 2
letters = '0123456789abcdef'
counter = 0
filledPlaces = 0
outputBuffer = [None] * 8
while filledPlaces != 8:
    digitFound = False
    h = md5((inp + str(counter)).encode()).hexdigest()
    if h[:5] == '00000' and (p := int(h[5], base=16)) < 8 and outputBuffer[p] is None:
        outputBuffer[p] = h[6]
        filledPlaces += 1
        digitFound = True
    counter += 1
    if doAnimation and (digitFound or counter % animationRate == 0):
        print(''.join((c if c is not None else choice(letters))
                      for c in outputBuffer))
print(''.join(outputBuffer))

