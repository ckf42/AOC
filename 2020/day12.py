import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=12, y=2020)
instructions = tuple(
    (line[0], int(line[1:]))
    for line in inp.splitlines()
)

# part 1
loc: complex = complex(0, 0)
faceDir: complex = complex(1, 0)
for cmd, arg in instructions:
    if cmd == 'N':
        loc += complex(0, arg)
    elif cmd == 'S':
        loc -= complex(0, arg)
    elif cmd == 'E':
        loc += complex(arg, 0)
    elif cmd == 'W':
        loc -= complex(arg, 0)
    elif cmd == 'L':
        faceDir *= complex(0, 1) ** (arg // 90)
    elif cmd == 'R':
        faceDir *= complex(0, -1) ** (arg // 90)
    elif cmd == 'F':
        loc += arg * faceDir
    else:
        raise RuntimeError(f"Unknown inst: {(cmd, arg)}")
print(sum(map(abs, util.complexToTuple(loc))))

# part 2
loc = complex(0, 0)
wayPt: complex = complex(10, 1)
for cmd, arg in instructions:
    if cmd == 'N':
        wayPt += complex(0, arg)
    elif cmd == 'S':
        wayPt -= complex(0, arg)
    elif cmd == 'E':
        wayPt += complex(arg, 0)
    elif cmd == 'W':
        wayPt -= complex(arg, 0)
    elif cmd == 'L':
        wayPt = loc + (wayPt - loc) * complex(0, 1) ** (arg // 90)
    elif cmd == 'R':
        wayPt = loc + (wayPt - loc) * complex(0, -1) ** (arg // 90)
    elif cmd == 'F':
        d = wayPt - loc
        loc += arg * d
        wayPt = loc + d
    else:
        raise RuntimeError(f"Unknown inst: {(cmd, arg)}")
print(sum(map(abs, util.complexToTuple(loc))))

