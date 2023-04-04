import AOCInit
import util
from collections import deque

if __name__ != '__main__':
    exit()

inp = util.getInput(d=22, y=2020)
deckList: tuple[deque[int], ...] = tuple(
    deque(util.getInts(player)[1:])
    for player in inp.split('\n\n')
)

# part 1
while not any(len(q) == 0 for q in deckList):
    deckTops = tuple(q.popleft() for q in deckList)
    if deckTops[0] > deckTops[1]:
        deckList[0].extend(deckTops)
    else:
        deckList[1].extend(deckTops[::-1])
winner = 0 if len(deckList[0]) != 0 else 1
totalDeckSize = len(deckList[winner])
print(sum(v * (totalDeckSize - i) for i, v in enumerate(deckList[winner])))

# part 2
def playRecursiveGame(deck1: deque[int],
                      deck2: deque[int]) -> bool:
    """
    return if player 1 wins this game
    modify decks
    """
    seenConfig: set[tuple[tuple[int, ...],
                          tuple[int, ...]]] = set()
    while len(deck1) != 0 and len(deck2) != 0:
        state = (tuple(deck1), tuple(deck2))
        if state in seenConfig:
            return True
        seenConfig.add(state)
        top1, top2 = deck1.popleft(), deck2.popleft()
        player1Win = top1 > top2
        if top1 <= len(deck1) and top2 <= len(deck2):
            player1Win = playRecursiveGame(deque((deck1[i] for i in range(top1))),
                                           deque((deck2[i] for i in range(top2))))
        if player1Win:
            deck1.extend((top1, top2))
        else:
            deck2.extend((top2, top1))
    return len(deck1) != 0


deckList = tuple(
    deque(util.getInts(player)[1:])
    for player in inp.split('\n\n')
)
winner = 0 if playRecursiveGame(deckList[0], deckList[1]) else 1
totalDeckSize = len(deckList[winner])
print(sum(v * (totalDeckSize - i) for i, v in enumerate(deckList[winner])))

