import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=6, y=2020)
groups = tuple(
        gp.splitlines()
        for gp in inp.split('\n\n')
)

# part 1
print(sum(map(lambda gp: len(frozenset(''.join(gp))), groups)))

# part 2
print(sum(map(lambda gp: len(frozenset.intersection(*map(frozenset, gp))), groups)))


