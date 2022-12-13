import AOCInit
import util
from collections import namedtuple

if __name__ != '__main__':
    exit()

(bossHp, bossDamage) = util.getInts(util.getInput(d=22, y=2015))

State = namedtuple('State',
                   ['hp', 'mp', 'manaSpent', 'bossHp',
                    'defence', 'shieldRemain', 'poisonRemain', 'rechargeRemain'])
Magic = namedtuple('Magic',
                   ['cost', 'damage', 'heal',
                    'defBuff', 'mpRefill', 'linger'])
magicDict = {
    'missile': Magic(cost=53, damage=4, heal=0, defBuff=0, mpRefill=0, linger=0),
    'drain': Magic(cost=73, damage=2, heal=2, defBuff=0, mpRefill=0, linger=0),
    'shield': Magic(cost=113, damage=0, heal=0, defBuff=7, mpRefill=0, linger=6),
    'poison': Magic(cost=173, damage=3, heal=0, defBuff=0, mpRefill=0, linger=6),
    'recharge': Magic(cost=229, damage=0, heal=0, defBuff=0, mpRefill=101, linger=5),
}

def applyEffect(st: State, regHarmVal: int = 0) -> State:
    return State(hp=st.hp - regHarmVal,
                 mp=st.mp + (magicDict['recharge'].mpRefill if st.rechargeRemain > 0 else 0),
                 manaSpent=st.manaSpent,
                 bossHp=st.bossHp - (magicDict['poison'].damage if st.poisonRemain > 0 else 0),
                 defence=(magicDict['shield'].defBuff if st.shieldRemain > 0 else 0),
                 shieldRemain=max(0, st.shieldRemain - 1),
                 poisonRemain=max(0, st.poisonRemain - 1),
                 rechargeRemain=max(0, st.rechargeRemain - 1))

def moveState(st: State, regHarmVal: int = 0) -> list[State]:
    st = applyEffect(st, regHarmVal)
    if st.hp <= 0:
        return list()
    elif st.bossHp <= 0:
        return [st]
    moveList = list()
    # player turn
    for n, m in magicDict.items():
        if st.mp >= m.cost:
            if m.linger == 0:
                # instant
                moveList.append(
                    State(hp=st.hp + m.heal,
                          mp=st.mp - m.cost,
                          manaSpent=st.manaSpent + m.cost,
                          bossHp=st.bossHp - m.damage,
                          defence=st.defence,
                          shieldRemain=st.shieldRemain,
                          poisonRemain=st.poisonRemain,
                          rechargeRemain=st.rechargeRemain)
                )
            elif getattr(st, n + 'Remain') == 0:
                # activate effect
                moveList.append(
                    State(hp=st.hp,
                          mp=st.mp - m.cost,
                          manaSpent=st.manaSpent + m.cost,
                          bossHp=st.bossHp,
                          defence=st.defence,
                          shieldRemain=(m.linger if n == 'shield' else st.shieldRemain),
                          poisonRemain=(m.linger if n == 'poison' else st.poisonRemain),
                          rechargeRemain=(m.linger if n == 'recharge' else st.rechargeRemain))
                )
    # boss turn
    moveList = tuple(applyEffect(s, regHarmVal=0) for s in moveList)
    moveList = tuple(
        (
            State(hp=s.hp - max(1, bossDamage - s.defence),
                    mp=s.mp,
                    manaSpent=s.manaSpent,
                    bossHp=s.bossHp,
                    defence=s.defence,
                    shieldRemain=s.shieldRemain,
                    poisonRemain=s.poisonRemain,
                    rechargeRemain=s.rechargeRemain)
            if s.bossHp > 0
            else s # boss died, keep state
        )
        for s in moveList
        if s.hp > 0
    )
    return list(filter(lambda s: s.hp > 0, moveList))

# part 1
print(util.dijkstra(State(hp=50, mp=500, manaSpent=0, bossHp=bossHp, defence=0,
                          shieldRemain=0, poisonRemain=0, rechargeRemain=0),
                    costFunc=lambda s, ost, oc: s.manaSpent,
                    neighbourListFunc=lambda s: moveState(s, 0),
                    goalCheckerFunc=lambda s: s.bossHp <= 0)[1])

# part 2
print(util.dijkstra(State(hp=50, mp=500, manaSpent=0, bossHp=bossHp, defence=0,
                          shieldRemain=0, poisonRemain=0, rechargeRemain=0),
                    costFunc=lambda s, ost, oc: s.manaSpent,
                    neighbourListFunc=lambda s: moveState(s, 1),
                    goalCheckerFunc=lambda s: s.bossHp <= 0)[1])


