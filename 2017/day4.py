import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=4, y=2017)

passphases = tuple(l.split() for l in inp.splitlines())

# part 1
print(util.count(passphases, lambda p: len(p) == len(set(p))))

# part 2
passphases = tuple(tuple(''.join(sorted(w))
                         for w in l.split())
                   for l in inp.splitlines())
print(util.count(passphases, lambda p: len(p) == len(set(p))))

