import AOCInit
import util
import ast
from functools import cmp_to_key

if __name__ != '__main__':
    exit()

# TODO: find way without parsing inp with ast

packageGroup = util.getInput(d=13, y=2022).split('\n\n')
packageList = tuple(tuple(ast.parse(ps, mode='eval').body
                          for ps in l.splitlines())
                    for l in packageGroup)

def isInOrder(a, b):
    if isinstance(a, ast.Constant) and isinstance(b, ast.Constant):
        return (0 if a.value == b.value else (-1 if a.value < b.value else 1))
    elif isinstance(a, ast.Constant):
        return isInOrder(ast.parse('[' + ast.unparse(a) + ']', mode='eval').body, b)
    elif isinstance(b, ast.Constant):
        return -isInOrder(b, a)
    else:
        la = len(a.elts)
        lb = len(b.elts)
        for idx in range(min(la, lb)):
            c = isInOrder(a.elts[idx], b.elts[idx])
            if c != 0:
                return c
        return 0 if la == lb else (-1 if la < lb else 1)

# part 1
print(sum(i + 1
          for i in range(len(packageList))
          if isInOrder(*packageList[i]) == -1))

# part 2
packageStream = list((pl, False) for gp in packageList for pl in gp) \
        + list(zip(tuple(ast.parse(s, mode='eval').body
                         for s in ('[[2]]', '[[6]]')),
                   (True, True)))
packageStream.sort(key=lambda pv: cmp_to_key(isInOrder)(pv[0]))
print(util.prod(i + 1 for i, pv in enumerate(packageStream) if pv[1]))

