import typing as _tp
import collections.abc as _abc
import pathlib as _pathlib
import requests as _rq
import re as _re
import functools as _ft
import itertools as _it
import heapq as _hq

if __name__ == '__main__':
    exit()

_T = _tp.TypeVar('T')
_S = _tp.TypeVar('S')

# helper functions
add = (lambda x, y: x + y) # helper for *SuchThat
mul = (lambda x, y: x * y) # helper for *SuchThat
identity = (lambda x: x) # helper for argmax


def getInput(d: int,
             y: int,
             force: bool = False) -> str:
    """
    fetch input file from AOC website and cache for later use

    Parameters
    -----
    d: int
        an integer representing the day

    y: int
        an integer representing the year

    force: bool, optional
        determine if the cached input should be ignored
        defaults to False

    Returns
    -----
    str
    the input for question of day `d` in year `y` fetched from the website
    the same input str will be written in cwd with filename `input{d}`
    if this file already exists, will overwrite
    if `force` is false and this file already exists, will read frm this file instead

    Note
    -----
    if needed to fetch from the website,
    it is expected to see a file named `session` in the parent dir of
    cwd that contains only the session cookie
    """
    if force or not _pathlib.Path('input').is_file():
        with open('../session', 'rt') as sessKey:
            r = _rq.get(f'https://adventofcode.com/{y}/day/{d}/input',
                        cookies={'session': sessKey.read().strip()}).text
        with open(f'input{d}', 'wt') as f:
            print(r, file=f, end='')
        return r
    else:
        with open(f'input{d}', 'rt') as f:
            return f.read()

def firstSuchThat(arr: _tp.Iterable[_T],
                  cond: _tp.Callable[_T, bool]) -> tuple[_tp.Optional[int], _tp.Optional[_T]]:
    """
    find the first element that the condition holds

    Parameters
    -----
    arr: Iterable[T]
        the input array search. If a generator, will be consumed

    cond: Callable[T, bool]
        a function that takes an element in `arr` and return a boolean denoting
        whether the value should be accepted

    Returns
    -----
    a tuple of type tuple[int, T] where
        the first entry is the index of the first element which `cond` returns true
        the second entry is the value of that element
    or (None, None) if no such element exists in `arr`

    Note
    -----
    If `arr` is a generator, it will be consumed after the returned element,
    or the whole `arr` will be consumed if no such element is found
    """
    return next(filter(lambda t: cond(t[1]), enumerate(arr)), (None, None))

def firstIdxSuchThat(arr: _tp.Iterable[_T],
                     cond: _tp.Callable[_T, bool],
                     s: int = 0,
                     e: _tp.Optional[int] = None,
                     step: int = 1) -> _tp.Optional[_T]:
    """
    find the index of the first element that the condition holds

    Parameters
    -----
    arr: Iterable[T]
        the input array search. If a generator, will be consumed

    cond: Callable[T, bool]
        a function that takes an element in `arr` and return a boolean denoting
        whether the value should be accepted

    s: int, optional
        the index to start the search at, inclusive
        defaults to 0

    e: int or None, optional
        the index to end the search at, exclusive
        if None, will search till the end of `arr`
        defaults to None

    step: int, optional
        the step size to traversal the array
        defaults to 1

    Returns
    -----
    an int that denotes the index of the first element which `cond` returns true
    or None if no such element exists in `arr`

    Note
    -----
    Wrapper of `firstSuchThat`

    If `arr` is a generator, it will be consumed after the returned element,
    or the whole `arr` will be consumed if no such element is found
    """
    return firstSuchThat(range(s, e, step), lambda idx: cond(arr[idx]))[0]

def lastSuchThat(arr: _tp.Iterable[_T],
                 cond: _tp.Callable[_T, bool]) -> tuple[_tp.Optional[int], _tp.Optional[_T]]:
    """
    find the last element that the condition holds. similar to `firstSuchThat`

    Parameters
    -----
    arr: Iterable[T]
        the input array search. If a generator, will be consumed

    cond: Callable[T, bool]
        a function that takes an element in `arr` and return a boolean denoting
        whether the value should be accepted

    Returns
    -----
    a tuple of type tuple[int, T] where
        the first entry is the index of the last element which `cond` returns true
        the second entry is the value of that element
    or (None, None) if no such element exists in `arr`

    Note
    -----
    If `arr` is a generator, it will be consumed after the returned element,
    or the whole `arr` will be consumed if no such element is found

    Slower than firstSuchThat on [::-1] as it always go through whole arr
    Only use if you cannot reverse arr (e.g. arr is generator)
    """
    lastTrue = (None, None)
    filterObj = filter(lambda t: cond(t[1]), enumerate(arr))
    while (o := next(filterObj, None)) is not None:
        lastTrue = o
    return lastTrue

def firstAccumSuchThat(
        arr: _tp.Iterable[_T],
        func: _tp.Callable[[_T, _T], _T],
        cond: _tp.Callable[_T, bool]
        ) -> tuple[_tp.Optional[int], _tp.Optional[_T], _tp.Optional[_T]]:
    """
    find the first element that the condition holds cumulatively

    Parameters
    -----
    arr: Iterable[T]
        the input array search. If a generator, will be consumed

    func: Callable[[T, T], T]
        a function that two elements from `arr` and return a element of the same type
        usually a lambda
        common choice may be addition `lambda x, y: x + y`
            or multiplication `lambda x, y: x * y`

    cond: Callable[T, bool]
        a function that takes an element in `arr` and return a boolean denoting
        whether the value should be accepted

    Returns
    -----
    a tuple of type tuple[int, T, T] where
        the first entry is the index of the first element until which `cond` returns true
            on the cumulative operation via `func`
        the second entry is the value of that element
        the third entry is the result of cumulative operation
    or (None, None, None) if no such element exists in `arr`

    Note
    -----
    If `arr` is a generator, it will be consumed after the returned element,
    or the whole `arr` will be consumed if no such element is found
    """
    return next(filter(lambda t: cond(t[2]),
                       zip(_it.count(0), arr, _it.accumulate(arr, func))),
                (None, None, None))

def lastAccumSuchThat(
        arr: _tp.Iterable[_T],
        func: _tp.Callable[[_T, _T], _T],
        cond: _tp.Callable[_T, bool]
        ) -> tuple[_tp.Optional[int], _tp.Optional[_T], _tp.Optional[_T]]:
    """
    find the last element that the condition holds cumulativly.
    similar to firstAccumSuch that

    Parameters
    -----
    arr: Iterable[T]
        the input array search. If a generator, will be consumed

    func: Callable[[T, T], T]
        a function that two elements from `arr` and return a element of the same type
        usually a lambda
        common choice may be addition `lambda x, y: x + y`
            or multiplication `lambda x, y: x * y`

    cond: Callable[T, bool]
        a function that takes an element in `arr` and return a boolean denoting
        whether the value should be accepted

    Returns
    -----
    a tuple of type tuple[int, T, T] where
        the first entry is the index of the last element until which `cond` returns true
            on the cumulative operation via `func`
        the second entry is the value of that element
        the third entry is the result of cumulative operation
    or (None, None, None) if no such element exists in `arr`

    Note
    -----
    If `arr` is a generator, it will be consumed after the returned element,
    or the whole `arr` will be consumed if no such element is found
    """
    lastTrue = (None, None, None)
    filterObj = filter(lambda t: cond(t[2]),
                       zip(_it.count(0), arr, _it.accumulate(arr, func)))
    while (o := next(filterObj, None)) is not None:
        lastTrue = o
    return lastTrue

def flatten(arr: _tp.Any, completely: bool = False):
    """
    flatten an iterable of iterables

    Parameter
    -----
    arr: Any
        an item to be flatten

    completely: bool, optional
        determine if all iterables somehow contained in `arr` should be flatten too
        if False, only flatten the first level
        if True, will flatten all levels nested into one
        defaults to False

    Return
    -----
    a tuple containing the flattened result
    if `arr` is not iterable, will return `arr` itself
    if `arr` is iterable but contains no iterable, will return its items wrapped in a tuple
    """
    if isinstance(arr, _abc.Iterable):
        return tuple(x
                     for itab in ((flatten(item, completely)
                                if isinstance(item, _abc.Iterable)
                                else (item,))
                               for item in arr)
                     for x in itab)
    else:
        return arr

def cycInd(arr: _abc.Sequence[_T], index: int) -> _T:
    """
    access a sequence with arbitrary index

    Parameters
    -----
    arr: Sequence[T]
        the sequence to access

    index: int
        the index of the target element

    Returns
    -----
    T, an element in `arr` with the index `index`
    this function extends the usual indexing such that
        `index` larger than `len(arr)` will loop around from the start
        and `index` smaller than `-len(arr)` will loop around from the end
    """
    return arr[index % len(arr)]

def prod(arr: _tp.Iterable[float]) -> float:
    """
    compute the product of elements. similar to the builtin `sum`

    Parameters
    -----
    arr: Iterable[float]
        an iterable that contains the numbers in question

    Returns
    -----
    a float that denotes the product of elements in `arr`

    Note
    -----
    `arr` will be consumed if it is a generator
    Does not seem compatible with `ortools`
    """
    return _ft.reduce(lambda x, y: x * y, arr)

def takeExcept(arr: _abc.Sequence[_T], index: int) -> _abc.Sequence[_T]:
    """
    copy the whole arr with a certain element removed

    Parameters
    -----
    arr: Sequence[T]
        the sequence in question

    index: int
        the index of the element to be removed

    Returns
    -----
    a copy of the original `arr` with the element at `index` removed
    """
    return arr[:index] + arr[index + 1:]

def splitAt(arr: _abc.Sequence[_T],
            index: int) -> tuple[_abc.Sequence[_T], _abc.Sequence[_T]]:
    """
    split a sequence at the given location

    Parameters
    -----
    arr: Sequence[T]
        the sequence in question

    index: int
        the index to cutoff

    Returns
    -----
    a tuple of two sequence of the same type as `arr`
    the first entry contains elements of `arr` up until index `arr`, with length `index`
    the second entry contains the remaining elements in `arr`, with the first one being `arr[index]`
    both sequences retain the original order
    """
    return (arr[:index], arr[index:])

def getInts(s: str) -> tuple[int]:
    """
    get only the integers in a string

    Parameters
    -----
    s: str
        the string to look at

    Returns
    -----
    a tuple of int that contains all (possibly negative) integers that appear in `s`
    """
    return tuple(map(int, _re.findall(r'-?\d+', s)))

def getFloats(s: str) -> tuple[float]:
    """
    get only the floats in a string

    Parameters
    -----
    s: str
        the string to look at

    Returns
    -----
    a tuple of float that contains all (possibly negative) floats that appear in `s`
    """
    return tuple(map(float, _re.findall(r'-?\d+(?:\.\d+)', s)))

def splitIntoGp(arr: _abc.Sequence[_T],
                gpSize: int,
                allowRemain: bool = True) ->tuple[tuple[_T]]:
    """
    grouping elements in a sequence by their order

    Parameter
    -----
    arr: Sequence[T]
        a sequence that contains the elements in question

    gpSize: int
        the size of a group

    allowRemain: bool, optional
        determine if the last group may have size smaller than `gpSize`
        defaults to True

    Return
    -----
    a tuple of tuples that contains elements in `arr`
    the tuples will be `arr[0:gpSize]`, `arr[gpSize:2 * gpSize]`, and so on
    each tuple will have `gpSize` elements
    (except possibly the last one, if `allowRemain` is True)

    Error
    -----
    If `allowRemain` is False but `arr` is not of length of a integer multiple of `gpSize`,
        will raise `IndexError` for index out of range
    """
    lArr = len(arr)
    return tuple(tuple(arr[gpInit:(min(gpInit + gpSize, lArr)
                                   if allowRemain
                                   else gpInit + gpSize)])
                 for gpInit in range(0, lArr, gpSize))

def takeFromEvery(arr: _abc.Sequence[_T],
                  gpSize: int,
                  idx: int = 0,
                  takeFromRemain: bool = True) -> tuple[_T]:
    """
    take an element in a sequence once every given amount

    Parameters
    -----
    arr: Sequence[T]
        a sequence that contains the elements in question

    gpSize: int
        the size of a group

    idx: int
        the index to take from each group

    takeFromRemain: bool, optional
        determine if the last group may have size smaller than `gpSize`
        defaults to True

    Return
    -----
    a tuple containing elements in `arr`
    the elements are `arr[idx]`, `arr[idx + gpSize]`, `arr[idx + 2 * gpSize]`, and so on
    if `takeFromRemain` is False, will only take `arr[idx + k * gpSize]`
        if `len(arr) >= (k + 1) * gpSize` (`[k * gpSize:(k + 1) * gpSize]` is valid)
    """
    lArr = len(arr)
    return tuple(arr[gpInit + idx]
                 for gpInit in range(0, lArr, gpSize)
                 if takeFromRemain or gpInit + gpSize <= lArr)

def sub(originalSym: _abc.Iterable[_T],
        targetSym: _abc.Iterable[_S],
        arr: _abc.Iterable[_T],
        discard: bool = False) -> tuple[_tp.Union[_T, _S]]:
    """
    create a copy of the collection with its entry replaced

    Parameter
    -----
    originalSym: Iterable[T]
        the symbols to look up in `arr`
        if the symbol appears in `originalSym` multiple times,
            only the last appearance is considered

    targetSym: Iterable[S]
        the symbols to replace with in `arr`
        should have the same length as `originalSym`
        the longer one of the two will be truncated (with `zip`)

    arr: Iterable[T]
        the collection to look at

    discard: bool, optional
        determine whether symbols not in `originalSym` should be discarded
        defaults to False

    Returns
    -----
    a tuple containing the entries in `arr` with symbols in `originalSym`
        replaced with the corresponding one in `targetSym`
    if `discard` is True, symbols in `arr` but not in `originalSym` are discarded
    """
    replacementDict = {k: v for k, v in zip(originalSym, targetSym)}
    return tuple(replacementDict.get(c, c)
                 for c in arr
                 if not discard or c in replacementDict)

def subChar(originalSym: str, targetSym: str, s: str) -> str:
    """
    substitute characters in a string

    Parameters
    -----
    originalSym: str
        the characters to look up in `s`

    targetSym: str
        the symbols to replace with in `s`
        must be equal length with `originalSym`

    s: str
        the str to look at

    Return
    -----
    a string with characters in `originalSym` replaced with the corresponding one in `targetSym`

    Note
    -----
    wrapper of str.translate
    """
    return s.translate(str.maketrans(originalSym, targetSym))

def multiMap(arr: _tp.Iterable[_T], funcTuple: tuple[_tp.Callable[_T, _tp.Any]]) -> tuple[tuple]:
    """
    `map` with multiple functions

    Parameters
    -----
    arr: Iterable[T]
        the sequence in question

    funcTuple: tuple[Callable[T, Any]]
        a tuple of callables that maps elements in `arr` to something

    Return
    -----
    a tuple of tuples each containing the images of a function in `funcTuple`
    `multiMap[i]` contains the image of `funcTuple[i]`
    """
    return tuple(tuple(map(f, arr)) for f in funcTuple)

def takeApart(seq: _abc.Iterable[_abc.Sequence]) -> tuple[tuple]:
    """
    splitting sequences of sequences

    Parameter
    -----
    seq: Iterable[Sequence]
        a sequence of sequences. At least contain one sequence

    Return
    -----
    a tuple of tuples of elements from `seq`
    `takeApart[i]` contains the `i`th element in every sequence with order preserved
    `len(takeApart) == len(seq[0])` and `len(takeApart[i]) == len(seq)`
    if `seq[i]` has length less than `seq[0]`, will raise `IndexError`
    if `seq[i]` has length larger than `seq[0]`, the sequence will be truncated
    """
    l = len(seq[0])
    return multiMap(seq, tuple((lambda x, idx=i: x[idx]) for i in range(l)))

def transpose(seq: _abc.Iterable[_abc.Sequence]) -> tuple[tuple]:
    """
    alias of `takeApart`
    """
    return takeApart(seq)

def sgn(x: float) -> int:
    """
    compute the signum of a float

    Parameters
    -----
    x: float
        the number in question

    Returns
    -----
    a int that represents the signum of `x`
    if x == 0, returns 0
    if x > 0, returns 1
    if x < 0, returns -1
    """
    if x == 0:
        return 0
    else:
        return 1 if x > 0 else -1

def argmax(arr: _abc.Iterable[_tp.Any],
           key: _tp.Callable[_tp.Any, float]) -> _tp.Optional[_tp.Any]:
    """
    find where maximum occurs

    Parameter
    -----
    arr: Iterable
        the collection of elements to look at

    key: Callable[Any, float]
        a callable that computes the (float) key for comparison

    Return
    -----
    the first item in `arr` (as returned by its iterator) that gives the maximal `key` value
    if there is no element in `arr`, returns None

    Note
    -----
    Only enumerate whole `arr` once
    """
    currMaxItem = None
    currMaxKey = -float('Inf')
    for item in arr:
        if (k := key(item)) > currMaxKey:
            currMaxItem = item
            currMaxKey = k
    return item

def gcd(*n: int) -> int:
    """
    Compute gcd of integers

    Parameter
    -----
    *n: int
        the integers to compute gcd for

    Return
    -----
    the gcd of the given integers
    if no integer is given, return 1
    """
    if len(n) == 0:
        return 1
    elif len(n) == 1:
        return n[0]
    elif len(n) == 2:
        return n[0] if n[1] == 0 else gcd(n[1], n[0] % n[1])
    else:
        return gcd(gcd(*n[:2]), *n[2:])

def lcm(*n: int) -> int:
    """
    Compute lcm of integers

    Parameter
    -----
    *n: int
        the integers to compute gcd for

    Return
    -----
    the lcm of the given integers
    if no integer is given, return 1
    """
    if len(n) == 0:
        return 1
    elif len(n) == 1:
        return n[0]
    elif len(n) == 2:
        return n[0] // gcd(*n) * n[1]
    else:
        return lcm(lcm(*n[:2]), *n[2:])

class MinHeap:
    """
    simple wrapper for heap based on heapq

    Note
    -----
    See https://stackoverflow.com/a/8875823
    """
    def __init__(self, initItemList=None, key=lambda k: k):
        self.__data = list()
        self.__key = key
        if initItemList is not None:
            self.__data.extend((self.__key(item), item) for item in initItemList)
            _hq.heapify(self.__data)

    def push(self, item):
        _hq.heappush(self.__data, (self.__key(item), item))

    def pop(self):
        return _hq.heappop(self.__data)[-1]

    def top(self):
        return self.__data[0][-1]

    def __len__(self):
        return len(self.__data)

    def isEmpty(self):
        return len(self.__data) == 0


def dijkstra(initialNode: _T,
             costFunc: _tp.Callable[[_T, _T, float], float],
             neighbourListFunc: _tp.Callable[_T, _abc.Iterable[_T]],
             goalCheckerFunc: _tp.Callable[_T, bool],
             aStarHeuristicFunc: _tp.Optional[_tp.Callable[_T, float]] = None
             ) -> _tp.Optional[tuple[_T, float]]:
    """
    search for minimal cost path via Dijkstra / A*

    Parameter
    -----
    initialNode: T
        the initial node to start searching

    costFunc: Callable[[T, T, float], float]
        a function to compute cost to a certain node from `initialNode`
        expected to take 3 positional arguments:
            newNode: T, tbe node to transfer to
            oldNode: T, the original node
            oldCost: float, the original cost to get to `oldNode`
        expected to return a float representing the cost to `newNode`

    neighbourListFunc: Callable[T, Iterable[T]]
        a function to get what a node can transfer to
        expected to take 1 positional argument (`node`, the original node)
        expected to return a collection of nodes, which `node` can transfer to

    goalCheckerFunc: Callable[T, bool]
        a function that checks whether a node is accepted as the goal node
        expected to take 1 positional argument (`node`, the node in question)
        expected to return a bool denoting whether `node` is accepted as a goal

    aStarHeuristicFunc: Callable[T, float] or None, optional
        a heuristic distance for A*
        for details, please check the theory for A* algorithm
        expected to be a callable that takes a node and returns the estimated cost to a goal
        if None, the heuristic cost is constant zero
        defaults to None

    Return
    -----
    a tuple of [node, cost] where
        `goalCheckerFunc(node)` is True
        `cost` is minimal (assuming the heuristic, if given, is suitable)
    or None, if no such node is found
    """
    if aStarHeuristicFunc is None:
        aStarHeuristicFunc = (lambda state: 0)
    h = MinHeap(initItemList=((initialNode, 0), ),
                key=(lambda sc: sc[1] + aStarHeuristicFunc(sc[0])))
    visited = set()
    while not h.isEmpty():
        (currNode, currCost) = h.pop()
        if goalCheckerFunc(currNode):
            return (currNode, currCost)
        if currNode in visited:
            continue
        visited.add(currNode)
        for nextNode in neighbourListFunc(currNode):
            h.push((nextNode, costFunc(nextNode, currNode, currCost)))
    return None

def clip(x: float, lb: _tp.Optional[float] = None, ub: _tp.Optional[float] = None) -> float:
    """
    clipping a value

    Parameter
    -----
    x: float
        the number to clip

    lb: float or None, optional
        the lower bound (inclusive)
        if None, no lower bounding clipping will be done

    ub: float or None, optional
        the upper bound (inclusive)
        if None, no upper bounding clipping will be done

    Return
    -----
    the clipped value
    if `ub < lb`, will return `lb`
    """
    return min(ub if ub is not None else float('Inf'),
               max(lb if lb is not None else -float('Inf'),
                   x))

def countOnes(n: int) -> int:
    """
    count ones in the binary representation of a (signed) integer

    Parameter
    -----
    n: int
        the integer to count

    Return
    -----
    an integer counting the number of ones in the signed binary representation of `n`
    Different from int.bit_count, this takes in account of the sign of `n`
    If `n` is non-negative, the result is the same as `n.bit_count()`

    Example
    -----
    >>> (127).bit_count()
    7
    >>> countOnes(127)
    7
    >>> (-127).bit_count()
    7
    >>> countOnes(-127)
    1 
    """
    if n == 0:
        return 0
    elif n < 0:
        return 1 + n.bit_length() - (-n).bit_count()
    else:
        return n.bit_count()

