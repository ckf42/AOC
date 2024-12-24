import AOCInit
import util

from functools import cache
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=24, y=2024)

gates = {
        parts[4]: (parts[1], parts[0], parts[2])
        for line in inp.split('\n\n')[1].splitlines()
        if (parts := line.split()) or True
}
outputs = {
    (v[0], *tuple(sorted(v[1:]))): k
    for k, v in gates.items()
}

initRegVals = {
        line.split(': ')[0]: line.split(': ')[1] == '1'
        for line in inp.split('\n\n')[0].splitlines()
}

zGates = sorted(
        (x for x in tuple(gates.keys()) + tuple(initRegVals) if x[0] == 'z'),
        reverse=True
)

def comp(regVals):
    @cache
    def getVal(regName):
        if regName in regVals:
            return regVals[regName]
        if gates[regName][0] == 'OR':
            return getVal(gates[regName][1]) or getVal(gates[regName][2])
        elif gates[regName][0] == 'AND':
            return getVal(gates[regName][1]) and getVal(gates[regName][2])
        elif gates[regName][0] == 'XOR':
            return getVal(gates[regName][1]) ^ getVal(gates[regName][2])
        raise AssertionError(f"bad op {gates[regName]=}")

    return ''.join('1' if getVal(g) else '0' for g in zGates)


# part 1
print(int(comp(initRegVals), base=2))

# part 2

# TBH there is no code
# I generate the graph of the circuit with GraphViz (using default layout) with
print("digraph {")
print(
    '\n'.join(f' {v[1]} -> {k} [label="{v[0]}"] ;\n {v[2]} -> {k} [label="{v[0]}"] ;'
              for k, v in gates.items())
)
print("}")

# then inspect the output graph with the following code to detect error
# on each error,
#     check where the error occur
#     compare with graph if anything does not match
#     manually increase bitCount and alter whb
#     rinse and repeat until all 4 pairs are found
bitCount = 0
whb = outputs[('AND', 'x00', 'y00')]

while True:
    bitCount += 1
    inx = 'x' + str(bitCount).zfill(2)
    iny = 'y' + str(bitCount).zfill(2)
    jjd = outputs[('XOR', inx, iny)]
    out = outputs[('XOR', *sorted((whb, jjd)))]
    bdf = outputs[('AND', inx, iny)]
    wbw = outputs[('AND', *sorted((whb, jjd)))]
    whb = outputs[('OR', *sorted((bdf, wbw)))]

