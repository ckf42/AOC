import AOCInit
import util
import re
from collections import defaultdict

if __name__ != '__main__':
    exit()

inp = util.getInput(d=2, y=2023)

games = dict()
patt = re.compile(r'(\d+) (red|green|blue)')
for line in inp.splitlines():
    desc = line.split(': ')
    gameId = util.getInts(desc[0])[0]
    balls: defaultdict[str, int] = defaultdict(int)
    for match in patt.findall(desc[1]):
        balls[match[1]] = max(balls[match[1]], int(match[0]))
    games[gameId] = balls

# part 1
req = {'red': 12, 'green': 13, 'blue': 14}
print(sum(gameId
          for gameId, balls in games.items()
          if all(balls[color] <= num
                 for color, num in req.items())))

# part 2
print(sum(util.prod(balls.values()) for balls in games.values()))

