import AOCInit
import util

# TODO: simpler code?

if __name__ != '__main__':
    exit()

inp = util.getInput(d=19, y=2023)

workflowInp, ratingInp = inp.split('\n\n')
workflowDict = dict()
for line in workflowInp.splitlines():
    wfStart = line.index('{')
    wfName = line[:wfStart]
    wfList: list[tuple[None | tuple[str, str, int], str]] = list()
    for wfCmd in line[wfStart + 1:-1].split(','):
        if ':' in wfCmd:
            clause, dest = wfCmd.split(':')
            if '<' in clause:
                v, val = clause.split('<')
                wfList.append(((v, '<', int(val)), dest))
            else:
                v, val = clause.split('>')
                wfList.append(((v, '>', int(val)), dest))
        else:
            wfList.append((None, wfCmd))
    workflowDict[wfName] = wfList

ratingList = list()
for line in ratingInp.splitlines():
    ratingList.append({
        ps[0]: int(ps[1])
        for part in line[1:-1].split(',')
        if (ps := part.split('=')) is not None})

# part 1
totalRating = 0
for rating in ratingList:
    currWf = 'in'
    clausePtr = 0
    while currWf != 'A' and currWf != 'R':
        clause, dest = workflowDict[currWf][clausePtr]
        if clause is None:
            currWf = dest
            clausePtr = 0
        else:
            val = rating[clause[0]]
            if (val > clause[2] if clause[1] == '>' else val < clause[2]):
                currWf = dest
                clausePtr = 0
            else:
                clausePtr += 1
    if currWf == 'A':
        totalRating += sum(rating.values())
print(totalRating)

# part 2
stack: list[tuple[tuple[str, int],
                  dict[str, tuple[int, int]]]] \
                          = [(('in', 0), {k: (1, 4000) for k in 'xmas'})]
accCount = 0
while len(stack) != 0:
    (currWf, clausePtr), ratingRg = stack.pop()
    if currWf == 'A' or currWf == 'R':
        if currWf == 'A':
            accCount += util.prod(valRg[1] - valRg[0] + 1
                                  for valRg in ratingRg.values())
        continue
    clause, dest = workflowDict[currWf][clausePtr]
    if clause is None:
        currWf = dest
        clausePtr = 0
        stack.append(((currWf, clausePtr), ratingRg))
    else:
        valRg = ratingRg[clause[0]]
        if clause[1] == '>':
            if clause[2] + 1 <= valRg[0]:
                stack.append(((dest, 0), ratingRg))
            elif clause[2] + 1 <= valRg[1]:
                ratingRg[clause[0]] = (clause[2] + 1, valRg[1])
                stack.append(((dest, 0), ratingRg.copy()))
                ratingRg[clause[0]] = (valRg[0], clause[2])
                stack.append(((currWf, clausePtr + 1), ratingRg.copy()))
            else:
                stack.append(((currWf, clausePtr + 1), ratingRg))
        else:
            if valRg[1] <= clause[2] - 1:
                stack.append(((dest, 0), ratingRg))
            elif valRg[0] <= clause[2] - 1:
                ratingRg[clause[0]] = (valRg[0], clause[2] - 1)
                stack.append(((dest, 0), ratingRg.copy()))
                ratingRg[clause[0]] = (clause[2], valRg[1])
                stack.append(((currWf, clausePtr + 1), ratingRg.copy()))
            else:
                stack.append(((currWf, clausePtr + 1), ratingRg))
print(accCount)


