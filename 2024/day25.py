import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=25, y=2024)

pins = tuple(
        pin.splitlines()
        for pin in inp.split('\n\n')
)

locks: list[tuple[int, ...]] = []
keys: list[tuple[int, ...]] = []

for pin in pins:
    (locks if pin[0][0] == '#' else keys)\
            .append(tuple(r.count('#') - 1 for r in util.transpose(pin)))

# part 1
print(sum(
    all(a + b <= 5 for a, b in zip(k, l))
    for k in keys
    for l in locks
))


# part 2
# no part 2

