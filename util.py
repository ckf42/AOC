import typing as _tp
# import collections.abc as _abc
import urllib.request as _ulq
import urllib.error as _ule
import re as _re
import functools as _ft
import itertools as _it
import heapq as _hq


if __name__ == '__main__':
    exit()

_T = _tp.TypeVar('_T')
_S = _tp.TypeVar('_S')

# helper var
inf = float('Inf')

# helper functions
add = (lambda x, y: x + y)
mul = (lambda x, y: x * y)
identity = (lambda x: x)


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
    if `force` is false and this file already exists,
    will read frm this file instead

    Note
    -----
    if needed to fetch from the website,
    it is expected to see a file named `session` in the parent dir of
    cwd that contains only the session cookie
    """
    try:
        if force:
            raise FileNotFoundError
        with open(f'input{d}', 'rt') as f:
            return f.read()
    except FileNotFoundError:
        pass
    with open('../session', 'rt') as sessKey:
        try:
            sKey = sessKey.read().strip()
            with _ulq.urlopen(
                    _ulq.Request(
                        f'https://adventofcode.com/{y}/day/{d}/input',
                        headers={'Cookie': f'session={sKey}'})
                    ) as resp:
                rt = resp.fp.read().decode()
                with open(f'input{d}', 'wt') as f:
                    print(rt, file=f, end='')
                return rt
        except _ule.HTTPError as e:
            detail = e.fp.read().decode()
            if 'Please log in to get your puzzle input.' in detail:
                raise RuntimeError("Not logged in. Token may be invalid or expired") from e
            else:
                raise RuntimeError(f"Failed to fetch input: {e.reason}\n"
                                   f"Detail: {detail}") from e


def firstSuchThat(
        arr: _tp.Iterable[_T],
        cond: _tp.Callable[[_T], bool]
        ) -> tuple[_tp.Optional[int], _tp.Optional[_T]]:
    """
    find the first element that the condition holds

    Parameters
    -----
    arr: Iterable[T]
        the input array search. If a generator, will be consumed

    cond: Callable[[T], bool]
        a function that takes an element in `arr` and return a boolean denoting
        whether the value should be accepted

    Returns
    -----
    a tuple of type tuple[int, T] where the entries are
        the index of the first element which `cond` returns true
        and the value of that element
    or (None, None) if no such element exists in `arr`

    Note
    -----
    If `arr` is a generator, it will be consumed after the returned element,
    or the whole `arr` will be consumed if no such element is found
    """
    return next(filter(lambda t: cond(t[1]),
                       enumerate(arr)),
                (None, None))


def firstIdxSuchThat(arr: _tp.Sequence[_T],
                     cond: _tp.Callable[[_T], bool],
                     s: int = 0,
                     e: _tp.Optional[int] = None,
                     step: int = 1) -> _tp.Optional[int]:
    """
    find the index of the first element that the condition holds

    Parameters
    -----
    arr: Sequence[T]
        the input array search. If a generator, will be consumed

    cond: Callable[[T], bool]
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
    int that denotes the index of the first element which `cond` returns true
    or None if no such element exists in `arr`

    Note
    -----
    Wrapper of `firstSuchThat`

    If `arr` is a generator, it will be consumed after the returned element,
    or the whole `arr` will be consumed if no such element is found
    """
    return firstSuchThat(range(s, e if e is not None else len(arr), step),
                         lambda idx: cond(arr[idx]))[0]

def lastSuchThat(
        arr: _tp.Iterable[_T],
        cond: _tp.Callable[[_T], bool]
        ) -> tuple[_tp.Optional[int], _tp.Optional[_T]]:
    """
    find the last element that the condition holds. similar to `firstSuchThat`

    Parameters
    -----
    arr: Iterable[T]
        the input array search. If a generator, will be consumed

    cond: Callable[[T], bool]
        a function that takes an element in `arr` and return a boolean denoting
        whether the value should be accepted

    Returns
    -----
    a tuple of type tuple[int, T] where the entries are
        the index of the last element which `cond` returns true
        and the value of that element
    or (None, None) if no such element exists in `arr`

    Note
    -----
    If `arr` is a generator, it will be consumed after the returned element,
    or the whole `arr` will be consumed if no such element is found

    Slower than firstSuchThat on [::-1] as it always go through whole arr
    Only use if you cannot reverse arr (e.g. arr is generator)
    """
    lastTrue: tuple[_tp.Optional[int], _tp.Optional[_T]] = (None, None)
    filterObj = filter(lambda t: cond(t[1]), enumerate(arr))
    while (o := next(filterObj, None)) is not None:
        lastTrue = o
    return lastTrue


def firstAccumSuchThat(
        arr: _tp.Iterable[_T],
        func: _tp.Callable[[_T, _T], _T],
        cond: _tp.Callable[[_T], bool]
        ) -> tuple[_tp.Optional[int], _tp.Optional[_T], _tp.Optional[_T]]:
    """
    find the first element that the condition holds cumulatively

    Parameters
    -----
    arr: Iterable[T]
        the input array search. If a generator, will be consumed

    func: Callable[[T, T], T]
        a function on two elements from `arr` and return one of the same type
        common choice may be addition `lambda x, y: x + y` (see `add`)
            or multiplication `lambda x, y: x * y` (see `mul`)

    cond: Callable[[T], bool]
        a function that takes an element in `arr` and return a boolean denoting
        whether the value should be accepted

    Returns
    -----
    a tuple of type tuple[int, T, T] where the entries are
        the index of the first element until which `cond` returns true
            on the cumulative operation via `func`
        and the value of that element
        and the result of cumulative operation
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
        cond: _tp.Callable[[_T], bool]
        ) -> tuple[_tp.Optional[int], _tp.Optional[_T], _tp.Optional[_T]]:
    """
    find the last element that the condition holds cumulativly.
    similar to firstAccumSuch that

    Parameters
    -----
    arr: Iterable[T]
        the input array search. If a generator, will be consumed

    func: Callable[[T, T], T]
        a function on two elements from `arr` and return one of the same type
        usually a lambda
        common choice may be addition `lambda x, y: x + y`
            or multiplication `lambda x, y: x * y`

    cond: Callable[[T], bool]
        a function that takes an element in `arr` and return a boolean denoting
        whether the value should be accepted

    Returns
    -----
    a tuple of type tuple[int, T, T] where the entries are
        the index of the last element until which `cond` returns true
            on the cumulative operation via `func`
        and the value of that element
        and the result of cumulative operation
    or (None, None, None) if no such element exists in `arr`

    Note
    -----
    If `arr` is a generator, it will be consumed after the returned element,
    or the whole `arr` will be consumed if no such element is found
    """
    lastTrue: tuple[_tp.Optional[int], _tp.Optional[_T], _tp.Optional[_T]] = (None, None, None)
    filterObj = filter(lambda t: cond(t[2]),
                       zip(_it.count(0), arr, _it.accumulate(arr, func)))
    while (o := next(filterObj, None)) is not None:
        lastTrue = o
    return lastTrue


def flatten(arr: _tp.Any, level: int = 1):
    """
    flatten an iterable of iterables

    Parameter
    -----
    arr: Any
        an item to be flatten

    level: int, optional
        the number of levels to flatten
        if 0, nothing will be flatten
        if negative (e.g. -1), will try to flatten every nested objects
        defaults to 1 (only flatten the first level)

    Return
    -----
    a tuple containing the flattened result
    if `arr` is not iterable, will return `arr` itself
    if `arr` is iterable but contains no iterable, will return its items wrapped in a tuple

    Note
    -----
    will also flatten str to tuple of single-char string (as it is iterable)
    """
    if isinstance(arr, _tp.Iterable) and level != 0:
        return tuple(x
                     for itab in ((flatten(item, max(level - 1, -1))
                                   if isinstance(item, _tp.Iterable)
                                   else (item,))
                                  for item in arr)
                     for x in itab)
    else:
        return arr


def cycInd(arr: _tp.Sequence[_T], index: int) -> _T:
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

    Note
    -----
    Vanilla python syntax only accepts indices in [-len, len)
    this function allows arbitrary index (but not for slicing)
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
    """
    return _ft.reduce(lambda x, y: x * y, arr)


def splitAt(arr: _tp.Sequence[_T],
            index: int) -> tuple[_tp.Sequence[_T], _tp.Sequence[_T]]:
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

    Note
    -----
    syntax sugar
    """
    return (arr[:index], arr[index:])


def splitBy(
        arr: _tp.Iterable[_T],
        cond: _tp.Callable[[_T], bool]
        ) -> tuple[tuple[_T, ...], tuple[_T, ...]]:
    """
    split elements according to given condition

    Parameters
    -----
    arr: Iterable[T]
        the iterable to be split

    cond: Callable[[T], bool]
        a callable to determine how the splitting is done

    Return
    -----
    a tuple containing two tuples of elements from `arr`
    the first tuple contains elements such that `cond` gives True
    the second tuple contains elements such that `cond` gives False
    """
    trueBucket = list()
    falseBucket = list()
    for item in arr:
        if cond(item):
            trueBucket.append(item)
        else:
            falseBucket.append(item)
    return (tuple(trueBucket), tuple(falseBucket))


def getInts(s: str, allowNegative: bool = True) -> tuple[int, ...]:
    """
    get only the integers in a string

    Parameters
    -----
    s: str
        the string to look at

    allowNegative: bool, optional
        determine if the negative sign should be included
        defaults to True

    Returns
    -----
    a tuple of int that contains all (signed, if `allowNegative` is True) integers
        that appear in `s`
    """
    intRegex = (r'-?' if allowNegative else r'') + r'\d+'
    return tuple(map(int,
                     _re.findall(intRegex, s)))


def getFloats(s: str) -> tuple[float, ...]:
    """
    get only the floats in a string

    Parameters
    -----
    s: str
        the string to look at

    Returns
    -----
    a tuple of float that contains all (signed) floats that appear in `s`
    """
    return tuple(map(float, _re.findall(r'-?\d+(?:\.\d+)?', s)))


def splitIntoGp(
        arr: _tp.Sequence[_T],
        gpSize: int,
        allowRemain: bool = True) -> tuple[tuple[_T, ...], ...]:
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
    (except possibly the last tuple, if `allowRemain` is True)

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


def takeFromEvery(arr: _tp.Sequence[_T],
                  gpSize: int,
                  idx: int,
                  takeFromRemain: bool = True) -> tuple[_T, ...]:
    """
    take an element in a sequence once every given amount

    Parameters
    -----
    arr: Sequence[T]
        a sequence that contains the elements in question

    gpSize: int
        the size of each group

    idx: int
        the index to take from each group, start counting from 0

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


def sub(originalSym: _tp.Iterable[_T],
        targetSym: _tp.Iterable[_S],
        arr: _tp.Iterable[_T],
        discard: bool = False) -> tuple[_tp.Union[_T, _S], ...]:
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


def multiMap(arr: _tp.Iterable[_T],
             funcTuple: tuple[_tp.Callable[[_T], _S]]
             ) -> tuple[tuple[_S, ...], ...]:
    """
    `map` with multiple functions

    Parameters
    -----
    arr: Iterable[T]
        the sequence in question

    funcTuple: tuple[Callable[[T], Any]]
        a tuple of callables that maps elements in `arr` to something

    Return
    -----
    a tuple of tuples each containing the images of a function in `funcTuple`
    `multiMap[i]` is the image of `funcTuple[i]` on `arr`
    """
    return tuple(tuple(map(f, arr)) for f in funcTuple)


def takeApart(
        seq: _tp.Sequence[_tp.Sequence[_T]]) -> tuple[tuple[_T, ...], ...]:
    """
    splitting sequences of sequences

    Parameter
    -----
    seq: Sequence[Sequence]
        a sequence of sequences. At least contain one sequence

    Return
    -----
    a tuple of tuples of elements from `seq`
    `takeApart[i]` contains the `i`th element in every sequence with order preserved
    `len(takeApart) == len(seq[0])` and `len(takeApart[i]) == len(seq)`
    if `seq[i]` has length less than `seq[0]`, will raise `IndexError`
    if `seq[i]` has length larger than `seq[0]`, the sequence will be truncated
    """
    return multiMap(seq,
                    tuple((lambda x, idx=i: x[idx])
                          for i in range(len(seq[0]))))

def transpose(
        seq: _tp.Sequence[_tp.Sequence[_T]]) -> tuple[tuple[_T, ...], ...]:
    """
    alias of `takeApart`
    """
    return takeApart(seq)


def rangeBound(
        seq: _tp.Sequence[_tp.Sequence[float]]
        ) -> tuple[tuple[float, float], ...]:
    """
    find the range of numbers

    Parameter
    -----
    seq: Sequence[Sequence[float]]
        a collection of sets of numbers

    Return
    -----
    a tuple containing 2-tuples of float numbers
    `rangeBound[i]` is the (min, max) of `seq[i]`
    """
    return takeApart(multiMap(seq, (min, max)))


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


def argmax(arr: _tp.Iterable[_tp.Any],
           key: _tp.Callable[[_tp.Any], float]=lambda x: x) -> _tp.Optional[_tp.Any]:
    """
    find where maximum occurs

    Parameter
    -----
    arr: Iterable
        the collection of elements to look at

    key: Callable[[Any], float], optional
        a callable that computes the (float) key for comparison
        defaults to the identity map

    Return
    -----
    the first item in `arr` (as returned by its iterator) that gives the maximal `key` value
    if there is no element in `arr`, returns None

    Note
    -----
    Only enumerate whole `arr` once
    Will consume `arr` if it is a generator
    """
    currMaxItem = None
    currMaxKey = -float('Inf')
    for item in arr:
        if (k := key(item)) > currMaxKey:
            currMaxItem = item
            currMaxKey = k
    return currMaxItem

def argmin(arr: _tp.Iterable[_tp.Any],
           key: _tp.Callable[[_tp.Any], float]=lambda x: x) -> _tp.Optional[_tp.Any]:
    """
    find where minimum occurs

    Parameter
    -----
    arr: Iterable
        the collection of elements to look at

    key: Callable[[Any], float], optional
        a callable that computes the (float) key for comparison
        defaults to the identity map

    Return
    -----
    the first item in `arr` (as returned by its iterator) that gives the minimum `key` value
    if there is no element in `arr`, returns None

    Note
    -----
    Only enumerate whole `arr` once
    Will consume `arr` if it is a generator
    wrapper of argmax
    """
    return argmax(arr, lambda x: -key(x))


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


class Heap(_tp.Generic[_T]):
    """
    simple wrapper for heap based on heapq

    Note
    -----
    See https://stackoverflow.com/a/8875823
    """

    __slots__ = ('__data', '__key')

    def __init__(self,
                 initItemList: _tp.Optional[_tp.Iterable[_T]] = None,
                 key: _tp.Optional[_tp.Callable[[_T], float]] = (lambda k: _tp.cast(float, k)),
                 isMinHeap: bool = True):
        self.__data: list[tuple[float, _T]] = list()
        self.__key: _tp.Callable[[_T], float] = (
                (key if isMinHeap else (lambda k: -key(k)))
                if key is not None
                else (lambda k: 0))
        if initItemList is not None:
            self.extend(initItemList)

    def push(self, item: _T):
        """
        Push an element in the heap
        """
        _hq.heappush(self.__data, (self.__key(item), item))

    def extend(self, itemList: _tp.Iterable[_T]):
        """
        Push an iterable of elements in the heap
        """
        self.__data.extend((self.__key(item), item)
                           for item in itemList)
        _hq.heapify(self.__data)

    def pop(self) -> _T:
        """
        Remove the top element in the heap and return it
        """
        return _hq.heappop(self.__data)[-1]

    def top(self) -> _T:
        """
        Get the top element
        """
        return self.__data[0][-1]

    def __len__(self) -> int:
        return len(self.__data)

    def __repr__(self) -> str:
        return 'Heap' + self.__data.__str__()

    def isEmpty(self) -> bool:
        """
        Check if the heap is empty
        """
        return len(self.__data) == 0

    def resize(self, newSize: int):
        """
        Reduce the heap to at most the given size
        The larger elements are more likely to get removed, but no guarantee on which
        """
        if newSize < len(self):
            self.__data = self.__data[:newSize]
            _hq.heapify(self.__data)

    def clear(self):
        """
        Remove all elements in the heap
        """
        self.__data.clear()

    def discard(self, item: _T) -> bool:
        """
        Remove the element in the heap if it exists, and return if any element is removed
        If multiple copies of the same item exist in the heap with different keys,
            does not guarantee which got removed
        """
        idx = next((idx
                    for idx in range(len(self))
                    if self.__data[idx][-1] == item),
                   None)
        if idx is not None:
            self.__data[idx:idx + 1] = []
            _hq.heapify(self.__data)
            return True
        return False


def MinHeap(initItemList: _tp.Optional[_tp.Iterable[_T]] = None,
            key: _tp.Optional[_tp.Callable[[_T], float]] = (lambda k: _tp.cast(float, k))
            ) -> Heap[_T]:
    """
    Wrapper function to get a min heap. See Heap.__init__ for details

    Parameter
    -----
    initItemList: Iterable[T] or None, optional
        the initial list
        defaults to None

    key: Callable[[T], float] or None, optional
        the key functoin
        defaults to identity

    Return
    -----
    A min heap as defined with Heap

    Note
    -----
    Wrapper function
    """
    return Heap(initItemList=initItemList, key=key, isMinHeap=True)


def MaxHeap(initItemList: _tp.Optional[_tp.Iterable[_T]] = None,
            key: _tp.Optional[_tp.Callable[[_T], float]] = (lambda k: _tp.cast(float, k))
            ) -> Heap[_T]:
    """
    Wrapper function to get a max heap. See Heap.__init__ for details

    Parameter
    -----
    initItemList: Iterable[T] or None, optional
        the initial list
        defaults to None

    key: Callable[[T], float] or None, optional
        the key functoin
        defaults to identity

    Return
    -----
    A max heap as defined with Heap

    Note
    -----
    Wrapper function
    """
    return Heap(initItemList=initItemList, key=key, isMinHeap=False)


def dijkstra(initialNode: _T,
             costFunc: _tp.Callable[[_T, _T, float], float],
             neighbourListFunc: _tp.Callable[[_T], _tp.Iterable[_T]],
             goalCheckerFunc: _tp.Callable[[_T], bool],
             aStarHeuristicFunc: _tp.Optional[_tp.Callable[[_T], float]] = None
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

    neighbourListFunc: Callable[[T], Iterable[T]]
        a function to get what a node can transfer to
        expected to take 1 positional argument (`node`, the original node)
        expected to return a collection of nodes, which `node` can transfer to

    goalCheckerFunc: Callable[[T], bool]
        a function that checks whether a node is accepted as the goal node
        expected to take 1 positional argument (`node`, the node in question)
        expected to return a bool denoting whether `node` is accepted as a goal

    aStarHeuristicFunc: Callable[[T], float] or None, optional
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

    Note
    -----
    only for simple cost-minimizing problems
    if you need something more complicated (e.g. getting all goal states, callback),
        just implement the algorithm yourself
    """
    if aStarHeuristicFunc is None:
        aStarHeuristicFunc = (lambda state: 0)
    h: Heap[tuple[_T, float]] = MinHeap(
            initItemList=((initialNode, 0),),
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

def clip(x: float,
         lb: _tp.Optional[float] = None,
         ub: _tp.Optional[float] = None) -> float:
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
        in 2-complement format
    Different from int.bit_count, this takes in account of the sign of `n`
    If `n` is non-negative, the result is the same as `n.bit_count()`

    Note
    -----
    uses int.bit_count, which is only available after 3.10
    if int has not bit_count method, will use the equivalent method as noted in
        the official documentation:
        https://docs.python.org/3/library/stdtypes.html#int.bit_count

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
    b_c = getattr(int, 'bit_count', lambda x: bin(x).count('1'))
    if n < 0:
        return 1 + n.bit_length() - b_c(-n)
    else:
        return b_c(n)


def inclusiveRange(s: int, e: int, step: _tp.Optional[int] = 1) -> range:
    """
    range, but inclusive and auto step

    Parameter
    -----
    s: int
        the starting value to generate

    e: int
        the ending value to generate

    step: int or None, optional
        the step size
        if None, will use 1 if `s <= e`, -1 if `s > e`
        defaults to 1

    Return
    -----
    a range object that produces {s, s + step, ..., e},
    (with appropriate `step` if given None)
    """
    if step is None:
        step = sgn(e - s)
    return range(s, e + step, step)


def count(arr: _tp.Iterable[_T], cond: _tp.Callable[[_T], bool] = bool) -> int:
    """
    count elements in an iterable that satisfies some condition

    Parameter
    -----
    arr: Iterable[T]
        an iterable that contains the elements to count

    cond: Callable[[T], bool], optional
        a callable that checks whether if an element should be counted
        defaults to the bool constructor (check truthfulness)

    Return
    -----
    an int representing the number of elements in `arr` that satisfies `cond`

    NOTE
    -----
    wrapper of `sum` and `map`
    """
    return sum(map(cond, arr))


def countItem(arr: _tp.Iterable[_T], item: _T) -> int:
    """
    count elements in an iterable that satisfies some condition

    Parameter
    -----
    arr: Iterable[T]
        an iterable that contains the elements to count

    item: T
        the item to count in `arr`

    Return
    -----
    an int representing the number of times `item` appears in `arr`

    NOTE
    -----
    wrapper of `count`
    compare by __eq__
    """
    return count(arr, lambda x: x == item)


def consoleChar(b: _tp.Union[bool, None]) -> str:
    """
    helper function for displaying boolean array on console

    Parameter
    -----
    b: bool or None
        the boolean to determine if the pixel should be colored

    Return
    -----
    a str consisting of a single character, which is
        U+2588 (FULL BLOCK) if `b` is True
        U+0020 (SPACE) if False
        U+2592 (MEDIUM SHADE) if is None
    """
    return u'\u2592' if b is None else (u'\u2588' if b else u'\u0020')


def rangeLen(arr: _tp.Sequence) -> range:
    """
    get a range to enumerate a sequence

    Parameter
    -----
    arr: Sequence
        the sequence to enumerate

    Return
    -----
    a range object that enumerates from 0 to `len(arr)`

    Note
    -----
    wrapper of `range` and `len`, with fewer parentheses
    """
    return range(len(arr))


class IntegerIntervals:
    __slots__ = ('__contents', '__eleCount')

    @classmethod
    def __itvIsValid(cls, itv: tuple[int, int]) -> bool:
        return len(itv) == 2 \
                and itv[0] <= itv[1] \
                and itv[0] != float('Inf') \
                and itv[1] != -float('Inf')

    @classmethod
    def __itvLen(cls, itv: tuple[int, int]) -> int:
        return itv[1] - itv[0] + 1

    @classmethod
    def __itvContains(cls, n: int, itv: tuple[int, int]) -> bool:
        return itv[0] <= n <= itv[1]

    @classmethod
    def __itvIsIntersect(cls,
                         itv1: tuple[int, int],
                         itv2: tuple[int, int]) -> bool:
        return any(cls.__itvContains(c, itv2) for c in itv1) \
                or any(cls.__itvContains(c, itv1) for c in itv2)

    @classmethod
    def __itvIntersectIfIntersect(cls,
                                  itv1: tuple[int, int],
                                  itv2: tuple[int, int]) -> tuple[int, int]:
        # assumes itv1 and itv2 intersects
        return (max(itv1[0], itv2[0]), min(itv1[1], itv2[1]))

    @classmethod
    def __itvSetminus(cls,
                      itv1: tuple[int, int],
                      itv2: tuple[int, int]
                      ) -> tuple[tuple[int, int], ...]:
        if not cls.__itvIsIntersect(itv1, itv2):
            return (itv1,)
        elif itv2[0] <= itv1[0] and itv1[1] <= itv2[1]:
            return tuple()
        elif itv1[0] < itv2[0] and itv2[1] < itv1[1]:
            return ((itv1[0], itv2[0] - 1), (itv2[1] + 1, itv1[1]))
        elif itv2[0] <= itv1[0]:
            return ((itv2[1] + 1, itv1[1]),)
        elif itv1[1] <= itv2[1]:
            return ((itv1[0], itv2[0] - 1),)
        else:
            # this should not happen
            raise RuntimeError(f"Case not considered: {itv1}, {itv2}")

    def __init__(self, *initIntervals: tuple[int, int]):
        # sorted list of 2-tuple components
        self.__contents: list[tuple[int, int]] = list()
        # element count in collection, None if recorded invalidated
        self.__eleCount: _tp.Optional[int] = 0
        if len(initIntervals) != 0:
            for itv in initIntervals:
                self.unionWith(itv)

    def __len__(self) -> int:
        if self.__eleCount is None:
            self.__eleCount = sum(map(self.__itvLen, self.__contents))
        return self.__eleCount

    def __contains__(self, n: int) -> bool:
        compoCount = len(self.__contents)
        if compoCount == 0 \
                or n < self.__contents[0][0] \
                or n > self.__contents[compoCount - 1][1]:
            return False
        # TODO: need testing
        s, e = 0, compoCount
        while e != s:
            m = (s + e) // 2
            if self.__contents[m][0] > n:
                e = m
            else:
                s = m + 1
        return self.__itvContains(n, self.__contents[s - 1])

    def __iter__(self) -> _tp.Iterable[int]:
        assert self.isBounded(), "Cannot iterate from an unbounded collection"
        for itv in self.__contents:
            yield from range(itv[0], itv[1] + 1)

    def __repr__(self) -> str:
        if len(self.__contents) == 0:
            return "Empty Collection"
        if len(self.__contents) == 1:
            return f"Interval{self.__contents[0]}"
        return "Union(" \
                + ", ".join("Interval[" + str(comp)[1:-1] + "]"
                            for comp in self.__contents) \
                + ")"

    def __getitem__(self, idx: int) -> tuple[int, int]:
        return self.__contents[idx]

    # TODO: need testing
    def unionWith(self, interval: tuple[int, int]):
        assert self.__itvIsValid(interval), f"Invalid interval: {interval}"
        compoCount = len(self.__contents)
        if compoCount == 0:
            self.__contents.append(interval)
            self.__eleCount = self.__itvLen(interval)
            return
        # find first itv in contents that itv[1] >= interval[0] - 1
        # if not exists, append interval at end
        s, e = 0, compoCount
        while e != s:
            m = (s + e) // 2
            if self.__contents[m][1] < interval[0] - 1:
                s = m + 1
            else:
                e = m
        fIdx = s
        if fIdx == compoCount:
            self.__contents.append(interval)
            if self.__eleCount is not None:
                self.__eleCount += self.__itvLen(interval)
            return
        # find last itv in contents that itv[0] <= interval[1] + 1
        # if not exists, insert interval at begin
        s, e = 0, compoCount
        while e != s:
            m = (s + e) // 2
            if self.__contents[m][0] > interval[1] + 1:
                e = m
            else:
                s = m + 1
        eIdx = s - 1
        if eIdx == -1:
            self.__contents.insert(0, interval)
            if self.__eleCount is not None:
                self.__eleCount += self.__itvLen(interval)
            return
        # if firstIdx > lastIdx, insert after firstIdx
        # else, merge and replace with [firstIdx, lastIdx]
        if fIdx > eIdx:
            self.__contents.insert(fIdx, interval)
            if self.__eleCount is not None:
                self.__eleCount += self.__itvLen(interval)
        elif fIdx != eIdx \
                or not (self.__contents[fIdx][0] <= interval[0]
                        <= interval[1] <= self.__contents[fIdx][1]):
            self.__contents[fIdx:eIdx + 1] = [
                (min(interval[0], self.__contents[fIdx][0]),
                 max(interval[1], self.__contents[eIdx][1]))
            ]
            self.__eleCount = None

    def intersectWith(self, interval: tuple[int, int]):
        assert self.__itvIsValid(interval), f"Invalid interval: {interval}"
        self.__contents = list(
                map(lambda compo: self.__itvIntersectIfIntersect(compo,
                                                                 interval),
                    filter(lambda itv: self.__itvIsIntersect(itv, interval),
                           self.__contents))
                )
        self.__eleCount = None

    def component(self, idx: int) -> tuple[int, int]:
        return self[idx]

    def countComponents(self) -> int:
        return len(self.__contents)

    def count(self) -> int:
        return len(self)

    def isEmpty(self) -> bool:
        return len(self.__contents) == 0

    def isBounded(self) -> bool:
        return self.isEmpty() \
                or (self.__contents[0][0] > -float('Inf')
                    and self.__contents[-1][1] < float('Inf'))

    def isSupersetOf(self, interval: tuple[int, int]) -> bool:
        assert self.__itvIsValid(interval), f"Invalid interval: {interval}"
        compoCount = len(self.__contents)
        if compoCount == 0:
            return False
        # TODO: need testing
        s, e = 0, compoCount
        while e != s:
            m = (s + e) // 2
            if self.__contents[m][0] > interval[0]:
                e = m
            else:
                s = m + 1
        return (s != 0
                and self.__contents[s - 1][0] <= interval[0]
                and interval[1] <= self.__contents[s - 1][1])

    def setMinus(self, interval: tuple[int, int]):
        assert self.__itvIsValid(interval), f"Invalid interval: {interval}"
        self.__contents = [newItv
                           for itv in self.__contents
                           for newItv in self.__itvSetminus(itv, interval)]
        self.__eleCount = None

    def clear(self):
        self.__contents.clear()
        self.__eleCount = 0


def allPairDistances(nodes: _tp.Iterable[int],
                     distFunc: _tp.Callable[[int, int], _tp.Optional[float]]
                     ) -> dict[tuple[int, int], float]:
    """
    compute pairwise distance with Floyd-Warshall

    Parameter
    -----
    nodes: Iterable[int]
        collection of nodes to compute, represented as integers
        will only compute distances involving paths among these nodes

    distFunc: Callable[[int, int], Optional[int]]
        a callable that gives the distance between nodes
        expected to take two arguments:
            source: int, the starting node
            terminal: int, the ending
        expected to return a float representing the edge length,
        or None if no such edge exists

    Return
    -----
    a dict that takes a tuple of 2 int (from `nodes`)
    and return the minimal (directed) distance between them
    (or float('Inf') if unreachable)

    Note
    -----
    n^3 time complexity, n^2 space complexity
    """
    nodeSeq = tuple(nodes)
    minDistDict: dict[tuple[int, int], float] = dict()
    for i in nodeSeq:
        for j in nodeSeq:
            if i == j:
                minDistDict[(i, i)] = 0
            elif (d := distFunc(i, j)) is not None:
                minDistDict[(i, j)] = d
            else:
                minDistDict[(i, j)] = float('Inf')
    for k in nodeSeq:
        for i in nodeSeq:
            for j in nodeSeq:
                minDistDict[(i, j)] = min(
                        minDistDict[(i, j)],
                        minDistDict[(i, k)] + minDistDict[(k, j)])
    return minDistDict


def findSeqPeriod(seq: _tp.Sequence[_T],
                  cond: _tp.Optional[_tp.Callable[[int], bool]] = None
                  ) -> _tp.Optional[tuple[int, int]]:
    """
    find period of (eventually) periodic sequence

    Parameter
    -----
    seq: Sequence[T]
        the sequence in question
        should be long enough to contain at least two period

    cond: Callable[[int], bool] or None, optional
        a callable that hints the possible period
        will only search the periods that `cond` returns True on
        if None, will use every possible period
        defaults to None

    Return
    -----
    a tuple containing 2 int
        the first int is the proposed period
        the second int is the length of irregularity
    such that `seq[irregularity : irregularity + period]` is the earliest period
    or None, if none that satisfies `cond` is found

    the period returned has the minimal length of irregularities and if tie, shortest period

    Note
    -----
    l^2 time complexity, 1 space complexity
    should speed up if we test multiple of gcd of suffix item counter,
        but somehow it is slower than naive search
        (AoC 2022 d17 whole sol took ~6s/~2s)
    """
    seqLen = len(seq)
    if seqLen <= 1:
        return (seqLen, 0)
    currOptimal: _tp.Optional[tuple[int, int]] = None
    for t in inclusiveRange(1, seqLen // 2, None):
        if cond is not None and not cond(t):
            continue
        rep = firstIdxSuchThat(
                range(1, seqLen // t),
                lambda i: seq[(seqLen - (i + 1) * t):(seqLen - i * t)] != seq[seqLen - t:])
        remainLen = seqLen - t * ((rep + 1)
                                  if rep is not None
                                  else (seqLen // t))
        if currOptimal is None or remainLen < currOptimal[1]:
            currOptimal = (t, remainLen)
    assert currOptimal is not None
    if sum(currOptimal) == seqLen:
        raise RuntimeWarning("findSeqPeriod failed to find proper period. seq may be aperiodic")
    return currOptimal

def extrapolatePeriodicSeq(arr: _tp.Sequence[float], idx: int, inDiff: bool = False) -> float:
    """
    extrapolate a periodic sequence

    Parameter
    -----
    arr: Sequence[float]
        the sequence to extrapolate from
        should be eventually periodic and long enough to contain 2 periods
        (but longer sequence takes longer time to compute)

    idx: int
        the target index to extrapolate at
        assumed nonnegative
        if smaller than length of `arr`, will return the value in `arr` instead

    inDiff: bool, optional
        indicate whether the periodicity is in the difference (increment)
        if True, will treat the difference as periodic
        if False, will treat the value as periodic
        defaults to False

    Return
    -----
    a float of the extrapolated value
    """
    if idx < len(arr):
        return arr[idx]
    if inDiff:
        periodData = findSeqPeriod(diff(arr))
        d, m = divmod(idx - periodData[1], periodData[0])
        return (arr[sum(periodData)] - arr[periodData[1]]) * d + arr[periodData[1] + m]
    else:
        periodData = findSeqPeriod(arr)
        return arr[(idx - periodData[1]) % periodData[0] + periodData[1]]

def integerLattice(dim: int,
                   norm: float,
                   p: float = 1,
                   excludeNeg: bool = False,
                   excludeZero: bool = True) -> _tp.Iterator[tuple[int, ...]]:
    """
    Generates integer coordinates in some sphere

    Parameter
    -----
    dim: int
        The dimension of the coordinate generated

    norm: int
        The radius of the sphere

    p: float, optional
        the index used to measure radius (p in L^p)
        must be at least 1
        defaults to 1

    excludeNeg: bool, optional
        Determine if points with negative coordinates should be omitted
        Defaults to False

    excludeZero: bool, optional
        Determine if the origin point should be omitted
        defaults to True

    Return
    -----
    Return `dim`-tuples of integers that are included in a sphere of L`p` radius `norm`.
    If excludeNeg or excludeZero is True, the corresponding tuples will be omitted.
    """
    assert p >= 1
    if dim <= 0 or norm < 0:
        return
    if dim == 1:
        if not excludeZero:
            yield (0,)
        for coor in range(1, int(norm) + 1):
            if not excludeNeg:
                yield (-coor,)
            yield (coor,)
    else:
        for pt in integerLattice(dim - 1, norm, p, excludeNeg, excludeZero):
            yield (0,) + pt
        for coor in range(1, int(norm) + 1):
            remainNorm = (norm
                          if p == float('Inf')
                          else (norm ** p - coor ** p) ** (1 / p))
            for pt in integerLattice(dim - 1, remainNorm, p,
                                     excludeNeg, excludeZero=False):
                if not excludeNeg:
                    yield (-coor,) + pt
                yield (coor,) + pt


class Point:
    """
    A wrapper class for using tuple as points in Euclidean space
    If you only need 2D points for addition and comparison only, consider using complex numbers
    (~10x speedup for addition-intensive cases, e.g. AOC 2017 day 22)
    """
    __slots__ = ('__coor',)

    def __init__(self, *coors: float) -> None:
        assert len(coors) != 0, "Empty coordinate"
        self.__coor: tuple[float, ...] = tuple(coors)

    @classmethod
    def fromIterable(cls, it: _tp.Iterable[float]) -> 'Point':
        return cls(*it)

    @classmethod
    def zero(cls, dim: int) -> 'Point':
        return cls.fromIterable((0,) * dim)

    @property
    def dim(self) -> int:
        return len(self.__coor)

    def __getitem__(self,
                    dim: _tp.Union[int, slice]
                    ) -> _tp.Union[float, tuple[float, ...]]:
        if isinstance(dim, int):
            assert 0 <= dim < self.dim, f"Invalid dimension ({dim} not in [0, {self.dim - 1}])"
            return self.__coor[dim]
        if isinstance(dim, slice):
            assert 0 <= dim.start and (dim.stop is None or dim.stop <= self.dim), \
                    f"Invalid slice ({dim} on dim {self.dim})"
            return self.__coor[dim]
        raise NotImplementedError(f"Subscript type not recognized: {type(dim)}")

    def __iter__(self) -> _tp.Iterable[float]:
        yield from self.__coor

    def __repr__(self) -> str:
        return "Point(" + ", ".join(map(str, self.__coor)) + ")"

    def __len__(self) -> int:
        return self.dim

    def __add__(self, other: 'Point') -> 'Point':
        assert self.dim == other.dim, f"Dimension mismatch ({self.dim} != {other.dim})"
        return type(self)(*(self.__coor[i] + other.__coor[i] for i in range(self.dim)))

    def __rmul__(self, scalar: float) -> 'Point':
        return type(self)(*(scalar * self.__coor[i] for i in range(self.dim)))

    def __mul__(self, scalar: float) -> 'Point':
        return self.__rmul__(scalar)

    def __neg__(self) -> 'Point':
        return self.__rmul__(-1)

    def __sub__(self, other: 'Point') -> 'Point':
        return self.__add__(other.__neg__())

    def __pos__(self) -> 'Point':
        return self

    def __abs__(self) -> 'Point':
        return type(self).fromIterable(map(abs, self.__coor))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = type(self).fromIterable((other,) * self.dim)
        elif not isinstance(other, type(self)):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] == other.__coor[i]
                        for i in range(self.dim)))

    def __lt__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = type(self).fromIterable((other,) * self.dim)
        elif not isinstance(other, type(self)):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] < other.__coor[i]
                        for i in range(self.dim)))

    def __le__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = type(self).fromIterable((other,) * self.dim)
        elif not isinstance(other, type(self)):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] <= other.__coor[i]
                        for i in range(self.dim)))

    def __gt__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = type(self).fromIterable((other,) * self.dim)
        elif not isinstance(other, type(self)):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] > other.__coor[i]
                        for i in range(self.dim)))

    def __ge__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = type(self).fromIterable((other,) * self.dim)
        elif not isinstance(other, type(self)):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] >= other.__coor[i]
                        for i in range(self.dim)))

    def __bool__(self) -> bool:
        return any(self.__coor)

    def __hash__(self) -> int:
        return hash(('Point type', self.dim,) + self.__coor)

    def norm(self, p: float = 2) -> float:
        assert p >= 1, f"p ({p}) must be at least 1"
        if p == float('Inf'):
            return max(map(abs, self.__coor))
        elif p == 1:
            return sum(map(abs, self.__coor))
        else:
            return sum(abs(c) ** p for c in self.__coor) ** (1 / p)

class MutPoint:
    """
    A wrapper class for using tuple as points in Euclidean space
    Point but mutable and not hashable
    If you only need 2D points for addition and comparison only, consider using complex numbers
    (~10x speedup for addition-intensive cases, e.g. AOC 2017 day 22)
    """
    __slots__ = ('__coor',)

    def __init__(self, *coors: float) -> None:
        assert len(coors) != 0, "Empty coordinate"
        self.__coor: list[float] = list(coors)

    @classmethod
    def fromIterable(cls, it: _tp.Iterable[float]) -> 'MutPoint':
        return cls(*it)

    @classmethod
    def zero(cls, dim: int) -> 'MutPoint':
        return cls.fromIterable((0,) * dim)

    @property
    def dim(self) -> int:
        return len(self.__coor)

    def __getitem__(self,
                    key: _tp.Union[int, slice]
                    ) -> _tp.Union[float, tuple[float, ...]]:
        if isinstance(key, int):
            assert 0 <= key < self.dim, f"Invalid dimension ({key} not in [0, {self.dim - 1}])"
            return self.__coor[key]
        if isinstance(key, slice):
            assert 0 <= key.start and (key.stop is None or key.stop <= self.dim), \
                    f"Invalid slice ({key} on dim {self.dim})"
            return tuple(self.__coor[key])
        raise NotImplementedError(f"Subscript type not recognized: {type(key)}")

    def __setitem__(self,
                    key: int,
                    val: _tp.Union[int, float]):
        assert isinstance(val, (int, float))
        self.__coor[key] = val

    def __iter__(self) -> _tp.Iterable[float]:
        yield from self.__coor

    def __repr__(self) -> str:
        return "MutPoint(" + ", ".join(map(str, self.__coor)) + ")"

    def __len__(self) -> int:
        return self.dim

    def __add__(self, other: _tp.Union[Point, 'MutPoint']) -> Point:
        assert self.dim == other.dim, f"Dimension mismatch ({self.dim} != {other.dim})"
        return Point(*(self.__coor[i] + other[i] for i in range(self.dim)))

    def __iadd__(self, other: _tp.Union[Point, 'MutPoint']) -> 'MutPoint':
        assert self.dim == other.dim, f"Dimension mismatch ({self.dim} != {other.dim})"
        for i in range(self.dim):
            self.__coor[i] += other[i]
        return self

    def __rmul__(self, scalar: float) -> Point:
        return Point(*(scalar * self.__coor[i] for i in range(self.dim)))

    def __mul__(self, scalar: float) -> Point:
        return self.__rmul__(scalar)

    def __imul__(self, other: _tp.Union[float, int, Point, 'MutPoint']) -> 'MutPoint':
        if isinstance(other, (float, int)):
            for i in range(self.dim):
                self.__coor[i] *= other
        else:
            assert self.dim == other.dim, f"Dimension mismatch ({self.dim} != {other.dim})"
            for i in range(len(other)):
                self.__coor[i] *= other[i]
        return self

    def __neg__(self) -> Point:
        return self.__rmul__(-1)

    def __sub__(self, other: _tp.Union['MutPoint', Point]) -> Point:
        return self.__add__(other.__neg__())

    def __isub__(self, other: _tp.Union[Point, 'MutPoint']) -> 'MutPoint':
        assert self.dim == other.dim, f"Dimension mismatch ({self.dim} != {other.dim})"
        for i in range(len(other)):
            self.__coor[i] -= other[i]
        return self

    def __pos__(self) -> Point:
        return Point(*self.__coor)

    def __abs__(self) -> Point:
        return Point.fromIterable(map(abs, self.__coor))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = Point.fromIterable((other,) * self.dim)
        elif not isinstance(other, (Point, type(self))):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] == other[i]
                        for i in range(self.dim)))

    def __lt__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = Point.fromIterable((other,) * self.dim)
        elif not isinstance(other, (Point, type(self))):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] < other[i]
                        for i in range(self.dim)))

    def __le__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = Point.fromIterable((other,) * self.dim)
        elif not isinstance(other, (Point, type(self))):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] <= other[i]
                        for i in range(self.dim)))

    def __gt__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = Point.fromIterable((other,) * self.dim)
        elif not isinstance(other, (Point, type(self))):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] > other[i]
                        for i in range(self.dim)))

    def __ge__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = Point.fromIterable((other,) * self.dim)
        elif not isinstance(other, (Point, type(self))):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] >= other[i]
                        for i in range(self.dim)))

    def __bool__(self) -> bool:
        return any(self.__coor)

    def norm(self, p: float = 2) -> float:
        return Point(*self.__coor).norm(p)


def toBase(n: int, b: int) -> tuple[int, ...]:
    """
    Convert a number to given base

    Parameter
    -----
    n: int
        the number to convert. Must be non-negative

    b: int
        the target base

    Return
    -----
    a tuple of int, which represents the digits, starting from *the LEAST significant digit*
    it is to make that `sum(d * b ** i for i, d in enumerate(toBase(n, b))) == n` holds
    """
    assert b > 0
    assert n >= 0
    if n == 0:
        return (0,)
    res: list[int] = list()
    while n != 0:
        (n, r) = divmod(n, b)
        res.append(r)
    return tuple(res)


def fromBase(digits: _tp.Sequence[int],
             b: int,
             fractionalPartLen: int = 0) -> _tp.Union[int, float]:
    """
    Convert a number to given base

    Parameter
    -----
    digits: Sequence[int]
        the digits of the number, ordered from *MOST* significant digit to least significant digit
        (just like in usual writing)
        does not check if the digits are nonnegative or within [0, `b`)

    b: int
        the base of the number

    fractionalPartLen: int, optional
        the length of the fractional parts in `digits`
        the fractional part must be put at the end of `digits`
        defaults to 0 (no fractional)

    Return
    -----
    a int or a float (in base 10) that represents the number

    Note
    -----
    suffer from floating point error if has fractional part

    Example
    -----
    >>> fromBase([1, 2], 10)
    12
    >>> fromBase([1, 2], 10, 1)
    1.2
    """
    assert b > 0
    assert 0 <= fractionalPartLen <= len(digits)
    l: int = len(digits)
    x: _tp.Union[int, float] = 0
    for i in range(l - fractionalPartLen):
        x *= b
        x += digits[i]
    fracPart: float = 0.0
    for i in range(l - 1, l - fractionalPartLen - 1, -1):
        fracPart += digits[i]
        fracPart /= b
    if fracPart != 0:
        x += fracPart
    return x


def arrayAccess(arr: _tp.Sequence, coor: _tp.Sequence[int]) -> _tp.Any:
    """
    Access multi-dimensional array with a point

    Parameter
    -----
    arr: Sequence
        the array to access

    coor: Sequence[int]
        the coordinate to access

    Return
    -----
    whatever is in the corresponding location of `coor`

    Note
    -----
    MUCH SLOWER than hardcode indices
    Only use this for (deep) array access with unknown number of layers
    """
    if len(coor) == 0:
        return arr
    return arrayAccess(arr[coor[0]], coor[1:])

def matchClosingBracket(s: str,
                        idx: int,
                        closeBracket: str,
                        escapeChar: _tp.Optional[str] = '\\',
                        hasNesting: bool = True) -> _tp.Optional[int]:
    """
    Find the matching closing bracket

    Parameter
    -----
    s: str
        the string to look at

    idx: int
        the index of the opening bracket
        also defines the character for the opening bracket
        must not be escaped

    closeBracket: str
        a string of a single character that defines the closing bracket
        must not be the same as the opening bracket

    escapeChar: str or None, optional
        a string of a single character that defines the escape character
        must be different from the two brackets
        a closing bracket that comes after an escape character is not counted
        an escape character that comes after another escape character is not counted
        if None, no escaping is done
        defaults to '\\' (a single backslash)

    hasNesting: bool, optional
        determine if bracket pairs can be nested
        if True, other opening bracket are always treated as escaped
        if False, opening brackets appearing before a closing one are ignored0
        defaults to True

    Return
    -----
    a int that indicates the matching closing bracket following the escape rule,
    or None if no such closing bracket is found
    """
    l = len(s)
    assert 0 <= idx < l
    openBracket = s[idx]
    assert openBracket != closeBracket
    depthCount = 0
    ptr = idx + 1
    isEscaped = False
    for ptr in range(idx + 1, l):
        if s[ptr] == escapeChar:
            isEscaped = not isEscaped
        else:
            if s[ptr] == closeBracket and not isEscaped:
                depthCount -= 1
                if depthCount == -1:
                    return ptr
            elif s[ptr] == openBracket and not (not hasNesting or isEscaped):
                depthCount += 1
            isEscaped = False
    return None

def diff(arr: _tp.Sequence[float]) -> tuple[float, ...]:
    """
    compute the (forward) difference of a sequence

    Parameters
    -----
    arr: Sequence[float]
        the sequence to look at
        assumed of length >= 2

    Return
    -----
    A tuple of floats that is of length `len(arr) - 1`
    where `diff[i] == arr[i + 1] - diff[i]`
    """
    assert len(arr) >= 2
    return tuple(arr[i + 1] - arr[i] for i in range(len(arr) - 1))

