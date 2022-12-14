import AOCInit
import util
from collections import Counter

if __name__ != '__main__':
    exit()

inp = util.getInput(d=4, y=2016).splitlines()
# TODO: find ways to count without sorting
roomList = tuple((Counter(sorted(nt[0].replace('-', ''))),
                  nt[0],
                  util.getInts(nt[1])[0],
                  l[-6:-1])
                 for l in inp
                 if (nt := l.rsplit('-', maxsplit=1)))

# part 1
realRoomList = tuple(filter(lambda r: ''.join(c[0] for c in r[0].most_common(5)) == r[3],
                            roomList))
print(sum(r[2] for r in realRoomList))

# part 2
alphabet = ''.join(chr(i) for i in util.inclusiveRange(ord('a'), ord('z')))
rooms = list((r[2],
              ' '.join(''.join(util.cycInd(alphabet,
                                           ord(c) - ord('a') + r[2] % 26)
                               for c in w)
                       for w in r[1].split('-')))
             for r in realRoomList)
rooms.sort(key=lambda x: x[1])
for r in rooms:
    if 'north' in r[1].lower():
        print(r)

