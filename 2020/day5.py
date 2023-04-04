import AOCInit
import util

if __name__ != '__main__':
    exit()

inp = util.getInput(d=5, y=2020)

def toSeatId(seat: str) -> int:
    return int(seat.replace('F', '0')\
            .replace('B', '1')\
            .replace('L', '0')\
            .replace('R', '1'), base=2)

seatIds = tuple(map(toSeatId, inp.splitlines()))

# part 1
maxSeat = max(seatIds)
print(maxSeat)

# part 2
minSeat = min(seatIds)
print((minSeat + maxSeat) * (maxSeat - minSeat + 1) // 2 - sum(seatIds))

