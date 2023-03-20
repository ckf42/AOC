# modified from day 9 version
import typing as _tp
from collections import deque as _deque
from collections import defaultdict as _defaultdict
from enum import Enum as _Enum

if __name__ == '__main__':
    exit()


class IntCodeState(_Enum):
    HALTED = 0 # dead
    RUNNING = 1
    WAITING = 2 # need (more) input


class IntCode:
    argCountDict: dict[int, int] = {
        1: 3, 2: 3,
        3: 1, 4: 1,
        5: 2, 6: 2,
        7: 3, 8: 3,
        9: 1,
    }

    def __init__(self,
                 sourceCode: _tp.Sequence[int],
                 initInput: _tp.Iterable[int] = tuple()):
        self.prog: _defaultdict[int, int] = _defaultdict(int, enumerate(sourceCode))
        self.inputBuffer: _deque[int] = _deque(initInput)
        self.outputBuffer: _deque[int] = _deque()
        self.relativeBase: int = 0
        self.state: IntCodeState = IntCodeState.RUNNING
        self.ptr: int = 0

    @property
    def isRunning(self) -> bool:
        return self.state == IntCodeState.RUNNING

    @property
    def isWaiting(self) -> bool:
        return self.state == IntCodeState.WAITING

    @property
    def isHalted(self) -> bool:
        return self.state == IntCodeState.HALTED

    def _getLoc(self, arg: int, mode: str) -> int:
        assert mode in '02', f"Unsupported mode for getLoc: {mode}"
        locIdx = arg + (0 if mode == '0' else self.relativeBase)
        assert locIdx >= 0, f"Negative index: {locIdx}"
        return locIdx

    def _getMem(self, arg: int, mode: str) -> int:
        return arg if mode == '1' else self.prog[self._getLoc(arg, mode)]

    def send(self, *args: int):
        """
        send in numbers
        args: int
        """
        assert len(args) != 0, "Nothing to send"
        assert self.state != IntCodeState.HALTED, "Prog halted already"
        self.inputBuffer.extend(args)
        self.state = IntCodeState.RUNNING

    def get(self) -> int:
        """
        Get the oldest output
        """
        if len(self.outputBuffer) == 0 and self.state != IntCodeState.HALTED:
            if self.state == IntCodeState.WAITING:
                assert len(self.inputBuffer) != 0, "Prog waiting for input"
            self.run(pauseOnOutput=True, pauseOnInput=False)
        if len(self.outputBuffer) == 0 and self.state == IntCodeState.HALTED:
            raise StopIteration("Prog halted already")
        return self.outputBuffer.popleft()

    def getAllOutput(self) -> tuple[int, ...]:
        """
        Run the prog and get all outputs
        Will die if need input, and die after running
        """
        self.run(pauseOnOutput=False, pauseOnInput=False)
        return tuple(self.outputBuffer)

    @_tp.overload
    def pump(self, decode: _tp.Literal[False] = ...) -> tuple[int, ...]: ...
    @_tp.overload
    def pump(self, decode: _tp.Literal[True]) -> str: ...
    def pump(self, decode=False):
        """
        Get all output until need to input or die
        decode: bool, parse output as ascii if True, as int if False
        """
        self.run(pauseOnOutput=False, pauseOnInput=True)
        if decode:
            return ''.join(map(chr, self.outputBuffer))
        else:
            return tuple(self.outputBuffer)

    def purge(self):
        """
        Purge output buffer
        """
        self.outputBuffer.clear()

    def dump(self) -> dict[str, _tp.Any]:
        """
        Dump internal state
        """
        return {'c': self.prog.copy(),
                'ip': self.inputBuffer.copy(),
                'r': self.relativeBase,
                's': self.state,
                'p': self.ptr}

    def load(self, **dump):
        """
        Load internal state from dump
        """
        self.prog.clear()
        self.prog.update(dump['c'])
        self.inputBuffer = _deque(dump['ip'])
        self.relativeBase = dump['r']
        self.state = dump['s']
        self.ptr = dump['p']

    def run(self,
            pauseOnOutput: bool = True,
            pauseOnInput: bool = False):
        """
        Run the program
        pauseOnOutput: bool
        pauseOnInput: bool
        """
        assert self.isRunning, f"Cannot run prog: {self.state}"
        keepRunning = True
        while keepRunning:
            thisOpCode = self.prog[self.ptr] % 100
            if thisOpCode == 99:
                self.state = IntCodeState.HALTED
                keepRunning = False
                return
            assert thisOpCode in self.argCountDict, f"Unknown opcode: {thisOpCode}"
            argCount = self.argCountDict[thisOpCode]
            newPtr = self.ptr + argCount + 1
            paras = tuple(self.prog[self.ptr + i]
                          for i in range(1, argCount + 1))
            modes = str(self.prog[self.ptr] // 100).zfill(argCount)[::-1]
            if thisOpCode == 1:
                # sum
                self.prog[self._getLoc(paras[2], modes[2])] = \
                        self._getMem(paras[0], modes[0]) \
                        + self._getMem(paras[1], modes[1])
            elif thisOpCode == 2:
                # prod
                self.prog[self._getLoc(paras[2], modes[2])] = \
                        self._getMem(paras[0], modes[0]) \
                        * self._getMem(paras[1], modes[1])
            elif thisOpCode == 3:
                # input
                if not pauseOnInput:
                    assert len(self.inputBuffer) != 0, "No input provided"
                elif len(self.inputBuffer) == 0:
                    self.state = IntCodeState.WAITING
                    return
                self.prog[self._getLoc(paras[0], modes[0])] = self.inputBuffer.popleft()
            elif thisOpCode == 4:
                # output
                self.outputBuffer.append(self._getMem(paras[0], modes[0]))
                if pauseOnOutput:
                    keepRunning = False
            elif thisOpCode == 5:
                # jump if not zero
                if self._getMem(paras[0], modes[0]) != 0:
                    newPtr = self._getMem(paras[1], modes[1])
            elif thisOpCode == 6:
                # jump if zero
                if self._getMem(paras[0], modes[0]) == 0:
                    newPtr = self._getMem(paras[1], modes[1])
            elif thisOpCode == 7:
                # if is less
                self.prog[self._getLoc(paras[2], modes[2])] = (
                        1
                        if self._getMem(paras[0], modes[0]) < self._getMem(paras[1], modes[1])
                        else 0)
            elif thisOpCode == 8:
                # if is equal
                self.prog[self._getLoc(paras[2], modes[2])] = (
                        1
                        if self._getMem(paras[0], modes[0]) == self._getMem(paras[1], modes[1])
                        else 0)
            elif thisOpCode == 9:
                # change relative base
                self.relativeBase += self._getMem(paras[0], modes[0])
            self.ptr = newPtr

