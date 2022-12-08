import AOCInit
import util
import re
import heapq as hq

if __name__ != '__main__':
    exit()

(rules, og) = util.getInput(d=19, y=2015).split('\n\n')
ruleList = tuple((ls[0], ls[1], re.compile(ls[0]), re.compile(ls[1]))
                 for l in rules.splitlines()
                 if (ls :=  l.split(' => ')))
og = og.strip()

# part 1
createdParticles = set()
for r in ruleList:
    for m in r[2].finditer(og):
        sp = m.span()
        createdParticles.add(og[:sp[0]] + r[1] + og[sp[1]:])
print(len(createdParticles))

# part 2
pq = []
hq.heappush(pq, (len(og), og, 0))
top = None
while len(pq) != 0:
    top = hq.heappop(pq)
    if top[1] == 'e':
        break
    for r in ruleList:
        for m in r[3].finditer(top[1]):
            sp = m.span()
            res = top[1][:sp[0]] + r[0] + top[1][sp[1]:]
            hq.heappush(pq, (len(res), res, top[2] + 1))
print(top[2])

