import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=4, y=2018)

records = tuple(sorted(
        tuple((' '.join(ls[:2])[1:-1], ls[-1])
              for l in inp.splitlines()
              if (ls := l.split(maxsplit=2))),
        key=lambda tp: tp[0]))

sleepRecord = dict()
currGuard = None
startSleep = None
for rec in records:
    if 'begins shift' in rec[1]:
        currGuard = int(rec[1].split(maxsplit=2)[1][1:])
    elif 'falls asleep' in rec[1]:
        startSleep = int(rec[0].rsplit(':', maxsplit=1)[1])
    elif 'wakes up' in rec[1]:
        assert startSleep is not None
        currTime = int(rec[0].rsplit(':', maxsplit=1)[1])
        if currGuard not in sleepRecord:
            sleepRecord[currGuard] = [0 for _ in range(60)]
        for t in range(startSleep, currTime):
            sleepRecord[currGuard][t] += 1
        startSleep = None

# part 1
mostSleepGuard = util.argmax(sleepRecord, lambda g: sum(sleepRecord[g]))
mostSleetTime = util.argmax(range(60), lambda t: sleepRecord[mostSleepGuard][t])
print(mostSleepGuard * mostSleetTime)

# part 2
mostFreqGuard = util.argmax(sleepRecord, lambda g: max(sleepRecord[g]))
mostFreqTime = util.argmax(range(60), lambda t: sleepRecord[mostFreqGuard][t])
print(mostFreqGuard * mostFreqTime)

