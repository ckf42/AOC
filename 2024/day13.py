import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=13, y=2024)

machineSpecs = inp.split('\n\n')
machines = tuple(
        util.getInts(machine)
        for machine in machineSpecs
)

# part 1
res = 0
for machine in machines:
    a, b, c, d, e, f = machine
    det = a * d - b * c
    assert det != 0
    x = d * e - c * f
    y = -b * e + a * f
    if det < 0:
        det = -det
        x = -x
        y = -y
    if x >= 0 and y >= 0 and x % det == 0 and y % det == 0:
        res += (3 * x + y) // det
print(res)


# part 2
offset = 10000000000000
res = 0
for machine in machines:
    a, b, c, d, e, f = machine
    e += offset
    f += offset
    det = a * d - b * c
    assert det != 0
    x = d * e - c * f
    y = -b * e + a * f
    if det < 0:
        det = -det
        x = -x
        y = -y
    if x >= 0 and y >= 0 and x % det == 0 and y % det == 0:
        res += (3 * x + y) // det
print(res)
