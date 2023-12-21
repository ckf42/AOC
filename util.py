import dataclasses as _dc
import functools as _ft
import heapq as _hq
import itertools as _it
import math as _math
import re as _re
import typing as _tp
import urllib.error as _ule
import urllib.request as _ulq
from pathlib import Path as _Path
# check inf and nan
from math import isinf as _isinf
from math import isnan as _isnan

from sys import version_info as _vinfo
if _vinfo.major == 3 and _vinfo.minor < 10: # for TypeAlias
    from typing_extensions import TypeAlias as _TypeAlias
else:
    from typing import TypeAlias as _TypeAlias


if __name__ == '__main__':
    exit()

_T = _tp.TypeVar('_T')
_S = _tp.TypeVar('_S')

# helper var
inf = float('Inf')
intInf = _tp.cast(int, float('inf'))

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
        Usually there is no reason to set this as True
        defaults to False

    Returns
    -----
    str
    the input for question of day `d` in year `y` fetched from the website
    the same input str will be written in cwd with filename `input{d}`.
    if this file already exists and `force` is true, will overwrite
    if `force` is false and this file already exists,
    will read from this file instead

    Note
    -----
    if needed to fetch from the website,
    it is expected to see a file named `session` in the parent dir of
    cwd that contains only the session cookie
    """
    try:
        if force:
            raise FileNotFoundError
        with _Path(f'input{d}').open('rt') as f:
            return f.read()
    except FileNotFoundError:
        pass
    with _Path('../session').open('rt') as sessKey:
        try:
            sKey = sessKey.read().strip()
            with _ulq.urlopen(
                    _ulq.Request(
                        f'https://adventofcode.com/{y}/day/{d}/input',
                        headers={'Cookie': f'session={sKey}'})
                    ) as resp:
                rt = resp.fp.read().decode()
                with _Path(f'input{d}').open('wt') as f:
                    print(rt, file=f, end='')
                return rt
        except _ule.HTTPError as e:
            detail = e.fp.read().decode()
            if 'Please log in to get your puzzle input.' in detail:
                raise RuntimeError("Not logged in. Token may be invalid or expired") \
                        from e
            else:
                raise RuntimeError(f"Failed to fetch input: {e.reason}\n"
                                   f"Detail: {detail}") from e


def firstSuchThat(
        arr: _tp.Iterable[_T],
        cond: _tp.Callable[[_T], bool]
        ) -> _tp.Union[tuple[int, _T], tuple[None, None]]:
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
    return next(
            ((idx, ele)
             for idx, ele in enumerate(arr)
             if cond(ele)),
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
    if e is None:
        e = len(arr)
    else:
        e = min(e, len(arr))
    assert e is not None
    return next(
            (idx + s
             for (idx, ele) in enumerate(arr[s:e:step])
             if cond(ele)),
            None)

def lastSuchThat(
        arr: _tp.Iterable[_T],
        cond: _tp.Callable[[_T], bool]
        ) -> _tp.Union[tuple[int, _T], tuple[None, None]]:
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
    lastTrue: _tp.Union[tuple[int, _T], tuple[None, None]] = (None, None)
    while (o := next(filter(lambda t: cond(t[1]), enumerate(arr)), None)) is not None:
        lastTrue = o
    return lastTrue


def firstAccumSuchThat(
        arr: _tp.Iterable[_T],
        func: _tp.Callable[[_T, _T], _T],
        cond: _tp.Callable[[_T], bool]
        ) -> _tp.Union[tuple[int, _T, _T], tuple[None, None, None]]:
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
    return next(
            ((idx, ele, acc)
             for (idx, ele, acc)
             in zip(_it.count(0), arr, _it.accumulate(arr, func))
             if cond(acc)),
            (None, None, None))


def lastAccumSuchThat(
        arr: _tp.Iterable[_T],
        func: _tp.Callable[[_T, _T], _T],
        cond: _tp.Callable[[_T], bool]
        ) -> _tp.Union[tuple[int, _T, _T], tuple[None, None, None]]:
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
    lastTrue: _tp.Union[tuple[int, _T, _T], tuple[None, None, None]] \
            = (None, None, None)
    while (o := next(((idx, ele, acc)
                      for (idx, ele, acc)
                      in zip(_it.count(0), arr, _it.accumulate(arr, func))
                      if cond(acc)),
                     None)) is not None:
        lastTrue = o
    return lastTrue


@_tp.overload
def flatten(arr: _T, level: _tp.Literal[0]) -> _T: ...
@_tp.overload
def flatten(arr: _tp.Iterable[_tp.Iterable[_T]],
            level: _tp.Literal[1]) -> tuple[_T]: ...
@_tp.overload
def flatten(arr: _tp.Iterable[_T], level: _tp.Literal[1]) -> tuple[_T]: ...
@_tp.overload
def flatten(arr: _tp.Any, level: int) -> _tp.Any: ...
def flatten(arr, level=1):
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
    if `arr` is iterable but contains no iterable,
        will return its items wrapped in a tuple

    Note
    -----
    will also flatten str to tuple of single-char string (as it is iterable)
    """
    if isinstance(arr, _tp.Iterable) and level != 0:
        return tuple(
                x
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


@_tp.overload
def prod(arr: _tp.Iterable[int]) -> int: ...
@_tp.overload
def prod(arr: _tp.Iterable[float]) -> float: ...
def prod(arr):
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
    return _ft.reduce(mul, arr)


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
    the second entry contains the remaining elements in `arr`,
        with the first one being `arr[index]`
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
    return tuple(
            int(match)
            for match in _re.findall((r'-?' if allowNegative else r'') + r'\d+', s))


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
    return tuple(
            float(match)
            for match in _re.findall(r'-?\d+(?:\.\d+)?', s))


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
    If `allowRemain` is False
        but `arr` is not of length of a integer multiple of `gpSize`,
        will raise `IndexError` for index out of range

    NOTE
    -----
    In 3.12, itertools has `batched`. Should switch to that if we hit 3.12
    """
    return tuple(tuple(arr[gpInit:(min(gpInit + gpSize, len(arr))
                                   if allowRemain
                                   else gpInit + gpSize)])
                 for gpInit in range(0, len(arr), gpSize))


def takeFromEvery(
        arr: _tp.Sequence[_T],
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
        determine if the last group is allowed have size smaller than `gpSize`
        defaults to True

    Return
    -----
    a tuple containing elements in `arr`
    the elements are `arr[idx]`, `arr[idx + gpSize]`, `arr[idx + 2 * gpSize]`, and so on
    if `takeFromRemain` is False, will only take `arr[idx + k * gpSize]`
        if `len(arr) >= (k + 1) * gpSize` (`[k * gpSize:(k + 1) * gpSize]` is valid)
    """
    return tuple(_it.islice(
        arr,
        idx,
        None if takeFromRemain else (len(arr) // gpSize) * gpSize,
        gpSize))


@_tp.overload
def sub(originalSym: _tp.Iterable[_T],
        targetSym: _tp.Iterable[_S],
        arr: _tp.Iterable[_T],
        discard: _tp.Literal[True]) -> tuple[_S, ...]: ...
@_tp.overload
def sub(originalSym: _tp.Iterable[_T],
        targetSym: _tp.Iterable[_S],
        arr: _tp.Iterable[_T],
        discard: _tp.Literal[False]) -> tuple[_tp.Union[_T, _S], ...]: ...
def sub(originalSym, targetSym, arr, discard=False):
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
    replacementDict = dict(zip(originalSym, targetSym))
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
    a string with characters in `originalSym` replaced
        with the corresponding one in `targetSym`

    Note
    -----
    wrapper of str.translate
    """
    return s.translate(str.maketrans(originalSym, targetSym))


def multiMap(arr: _tp.Iterable[_T],
             funcTuple: tuple[_tp.Callable[[_T], _S], ...]
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
    all sequences are truncated to the shortest one

    NOTE
    -----
    Old behavior is to truncate to `len(seq[0])`
        and raise IndexError if `seq[0]` is not the shortest
    """
    return tuple(zip(*seq))


def transpose(
        seq: _tp.Sequence[_tp.Sequence[_T]]) -> tuple[tuple[_T, ...], ...]:
    """
    alias of `takeApart`
    """
    return takeApart(seq)


@_tp.overload
def rangeBound(
        seq: _tp.Sequence[_tp.Sequence[int]]
        ) -> tuple[tuple[int, int], ...]: ...
@_tp.overload
def rangeBound(
        seq: _tp.Sequence[_tp.Sequence[float]]
        ) -> tuple[tuple[float, float], ...]: ...
def rangeBound(seq):
    """
    find the range of numbers

    Parameter
    -----
    seq: Sequence[Sequence[float or int]]
        a collection of sets of numbers

    Return
    -----
    a tuple containing 2-tuples of float numbers
    `rangeBound[i]` is the (min, max) of `seq[i]`
    """
    return tuple((min(s), max(s)) for s in seq)

@_tp.overload
def rangeBoundOnCoors(
        pts: _tp.Iterable[_tp.Sequence[int]]
        ) -> tuple[tuple[int, int], ...]: ...
@_tp.overload
def rangeBoundOnCoors(
        pts: _tp.Iterable[_tp.Sequence[float]]
        ) -> tuple[tuple[float, float], ...]: ...
def rangeBoundOnCoors(pts):
    """
    find the range of coordinates of points

    Parameter
    -----
    pts: Iterable[Sequence[float or int]]
        a collection of sets of numbers
        assumed to be of uniform length

    Return
    -----
    a tuple containing 2-tuples of float or int numbers
    `rangeBoundOnCoor[i]` is the (min, max) of `pt[i]`
        over all `pt` in `pts`

    Note
    -----
    `pts` will get consumed if it is a generator

    Almost equivalent to `rangeBound(takeApart(pts))`
    but also take non-sequence input
    """
    initPt = next(iter(pts))
    minVal = list(initPt)
    maxVal = list(initPt)
    for pt in pts:
        for i in range(len(pt)):
            minVal[i] = min(minVal[i], pt[i])
            maxVal[i] = max(maxVal[i], pt[i])
    return takeApart((minVal, maxVal))


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
    return 0 if x == 0 else (1 if x > 0 else -1)


def argmax(
        arr: _tp.Iterable[_T],
        key: _tp.Callable[[_T], float] = lambda x: _tp.cast(float, x)
        ) -> _tp.Optional[_T]:
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
    the first item in `arr` (as returned by its iterator)
        that gives the maximal `key` value
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

def argmin(
        arr: _tp.Iterable[_T],
        key: _tp.Callable[[_T], float] = lambda x: _tp.cast(float, x)
        ) -> _tp.Optional[_T]:
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
    the first item in `arr` (as returned by its iterator)
        that gives the minimum `key` value
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

    Note
    -----
    (now) a wrapper of math.gcd
    """
    if len(n) == 0:
        return 1  # back compat behavior: math.gcd() == 0
    return _math.gcd(*n)


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

    Note
    -----
    (now) a wrapper of math.lcm
    """
    return _math.lcm(*n)


class Heap(_tp.Generic[_T]):
    """
    simple wrapper for heap based on heapq

    init Parameter
    -----
    initItemList: Iterable[T] or None, optional
        the initial list of items in heap
        None is same as an empty iterable (no items)
        defaults to None

    key: Callable[[T], float] or None, optional
        the key callable used to order items
        the key value is computed when item is pushed
        if None, the items themselves will be used to compare (must be comparable)
        ignored if `runtimeKeyOnly` is True
        defaults to None

    runtimeKeyOnly: bool, optional
        determine if the key must be passed in during push
        use this if a key function may not be easily available on heap initialization
        if True, `key` will be ignored, and `key` in `push` and `extend` cannot be None
        defaults to False

    Note
    -----
    See https://stackoverflow.com/a/8875823

    Using None (or equivalently a function that returns non-float) as key
        may lead to deteriorating performance
    """

    __slots__ = ('__data', '__key', '__itemDict', '__idx', '__runtimeKeyOnly')

    def __init__(self,
                 initItemList: _tp.Optional[_tp.Iterable[_T]] = None,
                 key: _tp.Optional[_tp.Callable[[_T], float]] = None,
                 runtimeKeyOnly: bool = False):
        self.__runtimeKeyOnly: bool = runtimeKeyOnly
        if runtimeKeyOnly:
            # mypy hack
            key = lambda k: _tp.cast(float, None)
        # NOTE: If key is None, __data should have type list[tuple[_T, int]]
        self.__data: list[tuple[float, int]] | list[tuple[_T, int]] = list()
        self.__key: _tp.Callable[[_T], float] = (
                key
                if key is not None
                else (lambda k: _tp.cast(float, k)))
        self.__itemDict: dict[int, _T] = dict()
        self.__idx: int = 0
        if initItemList is not None:
            self.extend(initItemList)

    def push(self, item: _T, key: _tp.Optional[float] = None):
        """
        Push an element in the heap

        Parameters
        -----
        item: T
            the item to be pushed in

        key: float or None, optional
            the key to use
            must not be None if `runtimeKeyOnly` is set True
            if not None, will ignore `key` function provided and use this value instead
                this key will not be visible on `pop`
            defaults to None
        """
        if self.__runtimeKeyOnly:
            assert key is not None, "key is None when runtimeKeyOnly is set True"
        self.__itemDict[self.__idx] = item
        _hq.heappush(self.__data,
                     (self.__key(item) if key is None else key,
                      self.__idx))
        self.__idx += 1

    def extend(self,
               itemList: _tp.Iterable[_T],
               keyList: _tp.Optional[_tp.Iterable[_tp.Optional[float]]] = None):
        """
        Push an iterable of elements in the heap

        Parameters
        -----
        itemList: Iterable[T]
            an iterable that contains the items to be pushed in

        keyList: Iterable[T or None] or None, optional
            the keys used
            see description in `push`
            if shorter than `itemList`, all remaining items will use key `None`
            if None, will be treated as an iterable of None
        """
        if keyList is None:
            keyList = tuple()
        keyList = _it.chain(keyList, _it.repeat(None))
        for item, key in zip(itemList, keyList):
            if self.__runtimeKeyOnly:
                assert key is not None, "key is None when runtimeKeyOnly is set True"
            self.__itemDict[self.__idx] = item
            self.__data.append((self.__key(item) if key is None else key,
                                self.__idx))
            self.__idx += 1
        _hq.heapify(self.__data)

    def pop(self) -> _T:
        """
        Remove the top element in the heap and return it
        """
        return self.__itemDict.pop(_hq.heappop(self.__data)[-1])

    def top(self) -> _T:
        """
        Get the top element
        """
        return self.__itemDict[self.__data[0][-1]]

    def __len__(self) -> int:
        return len(self.__data)

    def __repr__(self) -> str:
        return f'Heap (at 0x{id(self):x}) ' \
                f'of {len(self)} item{"s" if len(self) >= 2 else ""}'

    def isEmpty(self) -> bool:
        """
        Check if the heap is empty
        """
        return len(self.__data) == 0

    def resize(self, newSize: int):
        """
        Reduce the heap to (at most) the given size
        The larger elements are more likely to get removed, but no guarantee on which
        """
        if newSize < len(self):
            for idxPair in self.__data[newSize:]:
                self.__itemDict.pop(idxPair[-1])
            self.__data[:] = self.__data[:newSize]
            _hq.heapify(self.__data)

    def clear(self):
        """
        Remove all elements in the heap
        """
        self.__data.clear()
        self.__itemDict.clear()
        self.__idx = 0

    def discard(self, item: _T) -> bool:
        """
        Remove the element in the heap if it exists, and return if any element is removed
        If multiple copies of the same item exist in the heap (possibly with different keys),
            does not guarantee which got removed
        """
        dataIdx = next((idx
                        for idx in range(len(self.__data))
                        if self.__itemDict[self.__data[idx][-1]] == item),
                       None)
        if dataIdx is None:
            return False
        self.__itemDict.pop(self.__data.pop(dataIdx)[-1])
        _hq.heapify(self.__data)
        return True


def MinHeap(initItemList: _tp.Optional[_tp.Iterable[_T]] = None,
            key: _tp.Optional[_tp.Callable[[_T], float]] = None,
            runtimeKeyOnly: bool = False
            ) -> Heap[_T]:
    """
    Wrapper function to get a min heap. See Heap.__init__ for details

    Parameter
    -----
    initItemList: Iterable[T] or None, optional
        the initial list
        defaults to None

    key: Callable[[T], float] or None, optional
        the key function
        if None, the items themselves will be used to compare (must be comparable)
        defaults to None

    runtimeKeyOnly: bool, optional
        determine if the key must be passed in during push
        use this if a key function may not be easily available on heap initialization
        if True, `key` will be ignored, and `key` in `push` and `extend` cannot be None
        defaults to False

    Return
    -----
    A min heap as defined with Heap

    Note
    -----
    Wrapper function for better readability
    """
    return Heap(initItemList=initItemList,
                key=key,
                runtimeKeyOnly=runtimeKeyOnly)


def MaxHeap(initItemList: _tp.Optional[_tp.Iterable[_T]] = None,
            key: _tp.Optional[_tp.Callable[[_T], float]] = None
            ) -> Heap[_T]:
    """
    Wrapper function to get a max heap. See Heap.__init__ for details

    Parameter
    -----
    initItemList: Iterable[T] or None, optional
        the initial list
        defaults to None

    key: Callable[[T], float] or None, optional
        the key function
        if None, the object itself will be used for comparison
        (must be comparable and can be multiplied with -1)
        defaults to None

    Return
    -----
    A max heap as defined with Heap

    Note
    -----
    Wrapper function
    MaxHeap is just MinHeap with key().__neg__
    `runtimeKeyOnly` is always set to False (so `key` must be provided)
    """
    # TODO: make MaxHeap work for tuple-val key
    if key is None:
        key = (lambda k: _tp.cast(float, k))
    assert key is not None
    return Heap(initItemList=initItemList,
                key=lambda x: -key(x),
                runtimeKeyOnly=False)


def dijkstra(
        initialNode: _T,
        costFunc: _tp.Callable[[_T, _T, float], float],
        neighbourListFunc: _tp.Callable[[_T], _tp.Iterable[_T]],
        goalCheckerFunc: _tp.Callable[[_T], bool],
        aStarHeuristicFunc: _tp.Callable[[_T], float] = (lambda _: 0)
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

    aStarHeuristicFunc: Callable[[T], float], optional
        a heuristic distance for A*
        for details, please check the theory for A* algorithm
        expected to be a callable that takes a node
            and returns the estimated cost to a goal
        defaults to the constant zero callable

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
    h: Heap[tuple[_T, float]] = MinHeap(
            initItemList=((initialNode, 0),),
            key=(lambda sc: sc[1] + aStarHeuristicFunc(sc[0])))
    visited = set()
    try:
        while not h.isEmpty():
            (currNode, currCost) = h.pop()
            if goalCheckerFunc(currNode):
                return (currNode, currCost)
            if currNode in visited:
                continue
            visited.add(currNode)
            for nextNode in neighbourListFunc(currNode):
                nodeToPush = (nextNode, costFunc(nextNode, currNode, currCost))
                if nodeToPush not in visited:
                    h.push(nodeToPush)
    except KeyboardInterrupt as e:
        print(f"Heap size={len(h)}\nVisited node count={len(visited)}\n"
              f"Killed at node {currNode} with cost {currCost}")
        raise e
    return None

def clip(x: float, lb: float = -inf, ub: float = inf) -> float:
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
    return min(ub, max(lb, x))


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
    return (1 + n.bit_length() - b_c(-n)) if n < 0 else b_c(n)


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
    return sum(1 if cond(ele) else 0 for ele in arr)


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
    compare by __eq__
    """
    return sum(ele == item for ele in arr)


def consoleChar(b: _tp.Optional[bool]) -> str:
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
    return '\u2592' if b is None else ('\u2588' if b else '\u0020')


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

    @classmethod
    def fromUnioning(cls, *intervalCollection: 'IntegerIntervals'):
        newColl = cls()
        for coll in intervalCollection:
            newColl.unionWith(coll)
        return newColl

    def __init__(self, *initIntervals: tuple[int, int]):
        # sorted list of 2-tuple components
        self.__contents: list[tuple[int, int]] = list()
        # element count in collection, None if recorded invalidated
        self.__eleCount: _tp.Optional[int] = 0
        if len(initIntervals) != 0:
            for itv in initIntervals:
                self.add(itv)

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
        """
        Behavior undefined if collection change mid iteration
        """
        assert self.isBounded(), "Cannot iterate from an unbounded collection"
        for itv in self.__contents:
            yield from range(itv[0], itv[1] + 1)

    def __repr__(self) -> str:
        if len(self.__contents) == 0:
            return "Empty Collection of Interval"
        if len(self.__contents) == 1:
            return f"Interval{self.__contents[0]}"
        return "Union(" \
                + ", ".join("Interval[" + str(comp)[1:-1] + "]"
                            for comp in self.__contents) \
                + ")"

    def __getitem__(self, idx: int) -> tuple[int, int]:
        return self.__contents[idx]

    # TODO: need testing
    def add(self, interval: tuple[int, int]):
        """
        Add an interval to the collection
        """
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

    def unionWith(self, *otherCollections: 'IntegerIntervals'):
        """
        Update self by unioning another collection
        wrapper on self.unionWith
        """
        for coll in otherCollections:
            for itv in coll.components():
                self.add(itv)

    def intersectWith(self, interval: tuple[int, int]):
        """
        Compute the intersection of the collection with the interval
        """
        assert self.__itvIsValid(interval), f"Invalid interval: {interval}"
        self.__contents[:] = list(
                map(lambda compo: self.__itvIntersectIfIntersect(compo, interval),
                    filter(lambda itv: self.__itvIsIntersect(itv, interval),
                           self.__contents)))
        self.__eleCount = None

    def components(self) -> _tp.Iterable[tuple[int, int]]:
        """
        Iterater on all components, from lowest to highest
        Behavior undefined if collection change mid iteration
        """
        yield from self.__contents

    def component(self, idx: int) -> tuple[int, int]:
        """
        Return the connection component at `idx`
        """
        return self[idx]

    def countComponents(self) -> int:
        """
        Return the number of connected components in the collection
        """
        return len(self.__contents)

    def count(self) -> int:
        """
        Return the number of integers included in the collection
        """
        return len(self)

    def isEmpty(self) -> bool:
        """
        Return whether the collection is empty set
        """
        return len(self.__contents) == 0

    def isBounded(self) -> bool:
        """
        Return whether the collection is bounded
        """
        return self.isEmpty() \
                or (self.__contents[0][0] > -float('Inf')
                    and self.__contents[-1][1] < float('Inf'))

    def isSupersetOf(self, interval: tuple[int, int]) -> bool:
        """
        Return whether the collection contains the given interval
        """
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
        """
        Remove the given interval from the collection
        """
        assert self.__itvIsValid(interval), f"Invalid interval: {interval}"
        self.__contents[:] = [newItv
                              for itv in self.__contents
                              for newItv in self.__itvSetminus(itv, interval)]
        self.__eleCount = None

    def clear(self):
        """
        Reset the whole collection
        """
        self.__contents.clear()
        self.__eleCount = 0


def allPairDistances(
        nodes: _tp.Iterable[_T],
        distFunc: _tp.Callable[[_T, _T], _tp.Optional[float]]
        ) -> dict[tuple[_T, _T], float]:
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
    minDistDict: dict[tuple[_T, _T], float] = dict()
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


@_tp.overload
def findSeqPeriod(
        seq: _tp.Sequence[_T],
        cond: _tp.Optional[_tp.Callable[[int], bool]],
        noErrorOnAperiodic: _tp.Literal[True]
        ) -> _tp.Optional[tuple[int, int]]: ...
@_tp.overload
def findSeqPeriod(
        seq: _tp.Sequence[_T],
        cond: _tp.Optional[_tp.Callable[[int], bool]],
        noErrorOnAperiodic: _tp.Literal[False]
        ) -> tuple[int, int]: ...
def findSeqPeriod(seq, cond=None, noErrorOnAperiodic=False):
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

    noErrorOnAperiodic: bool, optional
        determine if we should raise error if `seq` is found aperiodic
        if False, will raise RuntimeError
        if True, no error will be raise, and return value is None
        defaults to False

    Return
    -----
    a tuple containing 2 int
        the first int is the proposed period
        the second int is the length of irregularity
    such that `seq[irregularity : irregularity + period]` is the earliest period
    if no such period is found, will
        raise RuntimeError if `noErrorOnAperiodic` is False
        return None instead if `noErrorOnAperiodic` is True

    the period returned has the minimal length of irregularities
    if multiple periods has the shorest irregularities, the smallest period

    Note
    -----
    l^2 time complexity, 1 space complexity
    is it possible to speed up?
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
                lambda i: seq[(seqLen - (i + 1) * t):(seqLen - i * t)] \
                        != seq[seqLen - t:])
        remainLen = seqLen - t * ((rep + 1)
                                  if rep is not None
                                  else (seqLen // t))
        if currOptimal is None or remainLen < currOptimal[1]:
            currOptimal = (t, remainLen)
    assert currOptimal is not None
    if sum(currOptimal) == seqLen:
        if not noErrorOnAperiodic:
            raise RuntimeError("findSeqPeriod failed to find proper period. "
                               "seq may be aperiodic")
        else:
            currOptimal = None
    return currOptimal

def extrapolatePeriodicSeq(
        arr: _tp.Sequence[float],
        idx: int,
        inDiff: bool = False
        ) -> float:
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
        although setting True works for value-periodic sequence,
            performance deteriorates (a bit)
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
        assert periodData is not None
        d, m = divmod(idx - periodData[1], periodData[0])
        return (arr[sum(periodData)] - arr[periodData[1]]) * d + arr[periodData[1] + m]
    else:
        periodData = findSeqPeriod(arr)
        assert periodData is not None
        return arr[(idx - periodData[1]) % periodData[0] + periodData[1]]

def integerLattice(
        dim: int,
        norm: float,
        p: float = 1,
        excludeNeg: bool = False,
        excludeZero: bool = True
        ) -> _tp.Iterator[tuple[int, ...]]:
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
    Generates `dim`-tuples of integers
        that are included in a sphere of L`p` radius `norm`.
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
            remainNorm = norm \
                    if p == float('Inf') \
                    else (norm ** p - coor ** p) ** (1 / p)
            for pt in integerLattice(
                    dim - 1, remainNorm, p, excludeNeg, excludeZero=False):
                if not excludeNeg:
                    yield (-coor,) + pt
                yield (coor,) + pt


def nearby2DGridPts(
        pt: tuple[int, int],
        bd: tuple[tuple[int, int], tuple[int, int]] \
                | tuple[int, int] \
                | None \
                = None,
        isL1: bool = True
        ) -> _tp.Iterator[tuple[int, int]]:
    """
    Generates integer coordinates near a 2D point

    Parameter
    -----
    pt: tuple[int, int]
        The center point

    isL1: bool, optional
        Determine if the points generated should be L^1 neighbours
        if True, all (4) points generated would have unit L^1 dist with `pt`
        if False, all (8) points generated would have unit L^infty dist with `pt`
        defaults to True

    bd: None or tuple[int, int] or tuple[tuple[int, int], tuple[int, int]], optional
        The bounds of the grid, specified as two diagonal points
        If specified as `((minX, minY), (maxX, maxY))`,
            all points generated would satisfy
            `minX <= p[0] < maxX` and `minY <= p[1] < maxY`
        If spefified as `(maxX, maxY)`, same as `((0, 0), (maxX, maxY))`
        If None, same as `((-inf, -inf), (inf, inf))` (no bounds)
        defaults to None

    Return
    -----
    Generates 2-tuples of integers that are neighbours of `pt`
    """
    if bd is None:
        bd = ((-intInf, -intInf), (intInf, intInf))
    elif not isinstance(bd[0], tuple):
        bd = ((0, 0), bd)
    for d in integerLattice(dim=2, norm=1, p=(1 if isL1 else inf)):
        newI, newJ = pt[0] + d[0], pt[1] + d[1]
        if bd[0][0] <= newI < bd[1][0] and bd[0][1] <= newJ < bd[1][1]:
            yield (newI, newJ)


@_tp.overload
def complexToTuple(c: complex, asInt: _tp.Literal[False]) -> tuple[float, float]: ...
@_tp.overload
def complexToTuple(c: complex, asInt: _tp.Literal[True]) -> tuple[int, int]: ...
def complexToTuple(c, asInt=True):
    """
    convert the coordinates of a complex number to tuple of floats

    Parameters
    -----
    c: complex
        the complex to convert from

    asInt: bool, optional
        determine if the output should be converted to int
        does not check if each part is numerically int or not

    Returns
    -----
    a tuple of 2 floats or a tuple of 2 ints, depending on `asInt`
    """
    return (int(c.real), int(c.imag)) if asInt else (c.real, c.imag)

class Point:
    """
    A wrapper class for using tuple as points in Euclidean space
    If you only need 2D points for addition and comparison only,
        consider using complex numbers (6~10x speedup)

    TODO: rewrite for better code
    TODO: common base class with MutPoint?
    """
    # NOTE: total ordering from dataclass does not support comparison with scalars
    __slots__ = ('__coor',)

    def __init__(self, *coors: float) -> None:
        assert len(coors) != 0, "Empty coordinate"
        self.__coor: tuple[float, ...] = tuple(coors)

    @classmethod
    def fromIterable(cls, it: _tp.Iterable[float]) -> 'Point':
        """
        Construct a Point from an Iterable that contains the same value
        """
        return cls(*it)

    @classmethod
    def zero(cls, dim: int) -> 'Point':
        """
        Construct a Point of zero of given dimension
        """
        return cls.fromIterable((0,) * dim)

    @property
    def dim(self) -> int:
        """
        The dimension (number of coordinates) of the point
        """
        return len(self.__coor)

    @_tp.overload
    def __getitem__(self, key: int) -> float: ...
    @_tp.overload
    def __getitem__(self, key: slice) -> tuple[float, ...]: ...
    def __getitem__(self, key):
        if isinstance(key, int):
            assert 0 <= key < self.dim, \
                    f"Invalid dimension ({key} not in [0, {self.dim - 1}])"
            return self.__coor[key]
        if isinstance(key, slice):
            assert 0 <= key.start and (key.stop is None or key.stop <= self.dim), \
                    f"Invalid slice ({key} on dim {self.dim})"
            return self.__coor[key]
        raise NotImplementedError(f"Subscript type not recognized: {type(key)}")

    def __iter__(self) -> _tp.Iterable[float]:
        yield from self.__coor

    def __repr__(self) -> str:
        return "Point(" + ", ".join(map(str, self.__coor)) + ")"

    def __len__(self) -> int:
        return self.dim

    def __add__(self, other: _tp.Union['Point', 'MutPoint']) -> 'Point':
        assert self.dim == other.dim, f"Dimension mismatch ({self.dim} != {other.dim})"
        return type(self)(*(self.__coor[i] + other[i] for i in range(self.dim)))

    def __rmul__(self,
                 other: _tp.Union[int, float, 'Point', 'MutPoint']) -> 'Point':
        if isinstance(other, (int, float)):
            return type(self)(*(other * self.__coor[i] for i in range(self.dim)))
        else:
            assert self.dim == other.dim
            return type(self)(*(other[i] * self.__coor[i]  for i in range(self.dim)))

    def __mul__(self,
                other: _tp.Union[int, float, 'Point', 'MutPoint']) -> 'Point':
        return self.__rmul__(other)

    def __truediv__(self,
                    other: _tp.Union[int, float, 'Point', 'MutPoint']) -> 'Point':
        if isinstance(other, (int, float)):
            return type(self)(*(self.__coor[i] / other for i in range(self.dim)))
        else:
            assert self.dim == other.dim
            return type(self)(*(self.__coor[i] / other[i] for i in range(self.dim)))

    def __floordiv__(self,
                     other: _tp.Union[int, float, 'Point', 'MutPoint']) -> 'Point':
        if isinstance(other, (int, float)):
            return type(self)(*(self.__coor[i] // other for i in range(self.dim)))
        else:
            assert self.dim == other.dim
            return type(self)(*(self.__coor[i] // other[i]  for i in range(self.dim)))

    def __neg__(self) -> 'Point':
        return self.__rmul__(-1)

    def __sub__(self,
                other: _tp.Union['Point', 'MutPoint']) -> 'Point':
        assert self.dim == other.dim, f"Dimension mismatch ({self.dim} != {other.dim})"
        return type(self)(*(self.__coor[i] - other[i] for i in range(self.dim)))

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
                and all(self.__coor[i] == other[i]
                        for i in range(self.dim)))

    def __lt__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = type(self).fromIterable((other,) * self.dim)
        elif not isinstance(other, type(self)):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] < other[i]
                        for i in range(self.dim)))

    def __le__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = type(self).fromIterable((other,) * self.dim)
        elif not isinstance(other, type(self)):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] <= other[i]
                        for i in range(self.dim)))

    def __gt__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = type(self).fromIterable((other,) * self.dim)
        elif not isinstance(other, type(self)):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] > other[i]
                        for i in range(self.dim)))

    def __ge__(self, other: object) -> bool:
        if isinstance(other, (int, float)):
            other = type(self).fromIterable((other,) * self.dim)
        elif not isinstance(other, type(self)):
            return NotImplemented
        return (self.dim == other.dim
                and all(self.__coor[i] >= other[i]
                        for i in range(self.dim)))

    def __bool__(self) -> bool:
        return any(self.__coor)

    def __hash__(self) -> int:
        return hash(('Point type', self.dim,) + self.__coor)

    def norm(self, p: float = 2) -> float:
        """
        Return the L^p norm of the point

        Parameter
        -----
        p: float
            p in L^p
            Must be between 1 and float('inf') (inclusive)
            defaults to 2

        Return
        -----
        a float representing the L^p norm of the point
        """
        assert p >= 1, f"p ({p}) must be at least 1"
        if p == float('Inf'):
            return max(map(abs, self.__coor))
        elif p == 1:
            return sum(map(abs, self.__coor))
        else:
            return sum(abs(c) ** p for c in self.__coor) ** (1 / p)

    def innerProd(self, other: _tp.Union['Point', 'MutPoint']) -> float:
        assert self.dim == other.dim
        return sum(self.__coor[i] * other.__coor[i] for i in range(self.dim))

class MutPoint:
    """
    A wrapper class for using tuple as points in Euclidean space
    Point but mutable and not hashable
    If you only need 2D points for addition and comparison only,
        consider using complex numbers (6~10x speedup)
    """
    # TODO: make this and `Point` inherite from an abstract base class
    __slots__ = ('__coor',)

    def __init__(self, *coors: float) -> None:
        assert len(coors) != 0, "Empty coordinate"
        self.__coor: list[float] = list(coors)

    @classmethod
    def fromIterable(cls, it: _tp.Iterable[float]) -> 'MutPoint':
        """
        Construct a Point from an Iterable that contains the same value
        """
        return cls(*it)

    @classmethod
    def zero(cls, dim: int) -> 'MutPoint':
        """
        Construct a Point of zero of given dimension
        """
        return cls.fromIterable((0,) * dim)

    @property
    def dim(self) -> int:
        """
        The dimension (number of coordinates) of the point
        """
        return len(self.__coor)

    def asPoint(self) -> Point:
        """
        Return a copy of this point as (immutable) Point
        """
        return Point.fromIterable(self.__coor)

    @_tp.overload
    def __getitem__(self, key: int) -> float: ...
    @_tp.overload
    def __getitem__(self, key: slice) -> tuple[float, ...]: ...
    def __getitem__(self, key):
        if isinstance(key, int):
            assert 0 <= key < self.dim, \
                    f"Invalid dimension ({key} not in [0, {self.dim - 1}])"
            return self.__coor[key]
        if isinstance(key, slice):
            assert 0 <= key.start and (key.stop is None or key.stop <= self.dim), \
                    f"Invalid slice ({key} on dim {self.dim})"
            return tuple(self.__coor[key])
        raise NotImplementedError(f"Subscript type not recognized: {type(key)}")

    def __setitem__(self, key: int, val: _tp.Union[int, float]):
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

    def __rmul__(self, other: _tp.Union[int, float, Point, 'MutPoint']) -> Point:
        if isinstance(other, (int, float)):
            return Point(*(other * self.__coor[i] for i in range(self.dim)))
        else:
            return Point(*(other[i] * self.__coor[i] for i in range(self.dim)))

    def __mul__(self, other: _tp.Union[int, float, Point, 'MutPoint']) -> Point:
        return self.__rmul__(other)

    def __imul__(self, other: _tp.Union[float, int, Point, 'MutPoint']) -> 'MutPoint':
        if isinstance(other, (float, int)):
            for i in range(self.dim):
                self.__coor[i] *= other
        else:
            assert self.dim == other.dim, \
                f"Dimension mismatch ({self.dim} != {other.dim})"
            for i, v in enumerate(other):
                self.__coor[i] *= v
        return self

    def __truediv__(self,
                    other: _tp.Union[int, float, Point, 'MutPoint']) -> Point:
        if isinstance(other, (int, float)):
            return Point(*(self.__coor[i] / other for i in range(self.dim)))
        else:
            assert self.dim == other.dim
            return Point(*(self.__coor[i] / other[i] for i in range(self.dim)))

    def __itruediv__(self,
                     other: _tp.Union[int, float, Point, 'MutPoint']) -> 'MutPoint':
        if isinstance(other, (int, float)):
            for i in range(self.dim):
                self.__coor[i] /= other
        else:
            assert self.dim == other.dim
            for i, v in enumerate(other):
                self.__coor[i] /= other[i]
        return self

    def __floordiv__(self,
                     other: _tp.Union[int, float, Point, 'MutPoint']) -> Point:
        if isinstance(other, (int, float)):
            return Point(*(self.__coor[i] // other for i in range(self.dim)))
        else:
            assert self.dim == other.dim
            return Point(*(self.__coor[i] // other[i] for i in range(self.dim)))

    def __ifloordiv__(self,
                      other: _tp.Union[int, float, Point, 'MutPoint']) -> 'MutPoint':
        if isinstance(other, (int, float)):
            for i in range(self.dim):
                self.__coor[i] //= other
        else:
            assert self.dim == other.dim
            for i, v in enumerate(other):
                self.__coor[i] //= other[i]
        return self

    def __neg__(self) -> Point:
        return self.__rmul__(-1)

    def __sub__(self, other: _tp.Union['MutPoint', Point]) -> Point:
        return self.__add__(other.__neg__())

    def __isub__(self, other: _tp.Union[Point, 'MutPoint']) -> 'MutPoint':
        assert self.dim == other.dim, f"Dimension mismatch ({self.dim} != {other.dim})"
        for i, v in enumerate(other):
            self.__coor[i] -= v
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
        """
        Return the L^p norm of the point

        Parameter
        -----
        p: float
            p in L^p
            Must be between 1 and float('inf') (inclusive)
            defaults to 2

        Return
        -----
        a float representing the L^p norm of the point
        """
        return self.asPoint().norm(p)

    def innerProd(self, other: _tp.Union[Point, 'MutPoint']) -> float:
        assert self.dim == other.dim
        return sum(self.__coor[i] * other.__coor[i] for i in range(self.dim))


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
    a tuple of int, which represents the digits,
        starting from *the LEAST significant digit*
    it is to make that `sum(d * b ** i for i, d in enumerate(toBase(n, b))) == n` holds
    """
    assert b > 0
    assert n >= 0
    if n == 0:
        return (0,)
    res = list()
    while n != 0:
        (n, r) = divmod(n, b)
        res.append(r)
    return tuple(res)


@_tp.overload
def fromBase(
        digits: _tp.Sequence[int],
        b: int,
        fractionalPartLen: _tp.Literal[0]) -> int: ...
@_tp.overload
def fromBase(
        digits: _tp.Sequence[int],
        b: int,
        fractionalPartLen: int) -> _tp.Union[int, float]: ...
def fromBase(digits, b, fractionalPartLen=0):
    """
    Convert a number to given base

    Parameter
    -----
    digits: Sequence[int]
        the digits of the number,
            ordered from *MOST* significant digit to least significant digit
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
    digitLen: int = len(digits)
    x: _tp.Union[int, float] = 0
    for i in range(digitLen - fractionalPartLen):
        x *= b
        x += digits[i]
    fracPart: float = 0.0
    for i in range(digitLen - 1, digitLen - fractionalPartLen - 1, -1):
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
    MUCH SLOWER than hardcoded indices
    Only use this for (deep) array access with unknown number of layers
    """
    coorPtr = 0
    while coorPtr < len(coor):
        arr = arr[coor[coorPtr]]
        coorPtr += 1
    return arr

def matchClosingBracket(
        s: str,
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
        if True, will only match the closing bracket that is at the right level
        if False, other opening bracket are always treated as escaped
        defaults to True

    Return
    -----
    a int that indicates the matching closing bracket following the escape rule,
    or None if no such closing bracket is found
    """
    strLen = len(s)
    assert 0 <= idx < strLen
    openBracket = s[idx]
    assert openBracket != closeBracket
    depthCount = 0
    ptr = idx + 1
    isEscaped = False
    for ptr in range(idx + 1, strLen):
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

def diff(arr: _tp.Sequence[float], count: int = 1) -> tuple[float, ...]:
    """
    compute the (forward) difference of a sequence

    Parameters
    -----
    arr: Sequence[float]
        the sequence to look at
        assumed of length >= `count + 1`

    count: int
        the number of diff to apply on `seq`
        defaults to 1

    Return
    -----
    On `count == 1`,
        a tuple of floats that is of length `len(arr) - 1`
        where `diff[i] == arr[i + 1] - diff[i]`
    Otherwise `diff(diff(seq), count - 1)`
    slower than `np.diff`
    """
    assert len(arr) >= count + 1
    for _ in range(count):
        arr = tuple(arr[i + 1] - arr[i] for i in range(len(arr) - 1))
    return arr

class DisjointSet(_tp.Generic[_T]):
    """
    A simple disjoint-set structure
    """
    __slots__ = ('__parent', '__gpSize', '__isCompressed')

    def __init__(
            self,
            initItems: _tp.Union[int, _tp.Iterable[_T]] = tuple()
            ) -> None:
        if isinstance(initItems, int):
            initItems = _tp.cast(_tp.Iterable, range(initItems))
        assert not isinstance(initItems, int)
        self.__parent: dict[_T, _T] = {k: k for k in initItems}
        self.__gpSize: dict[_T, int] = {k: 1 for k in self.__parent}
        # book keeping: is struct guaranteed to be compressed?
        # this should avoid repeatedly calling __compress
        self.__isCompressed: bool = True

    def __len__(self) -> int:
        return len(self.__parent)

    def __repr__(self) -> str:
        return f"Disjoint set with {len(self.__parent)} " \
                + f"element{'s' if len(self.__parent) > 1 else ''}" \
                + f" at 0x{id(self):x}"

    def __contains__(self, item: _T) -> bool:
        return item in self.__parent

    def addItem(self, item: _T) -> None:
        """
        Add an item in the disjoint set.
        If item is already in the set, this function does nothing
        If item is not in the set, it is added in a group of itself
        """
        if item not in self.__parent:
            self.__parent[item] = item
            self.__gpSize[item] = 1

    def getRep(self, item: _T) -> _T:
        """
        Return a representative item that is in the same group
        Items in the same group will always have the same representative item
        """
        if item not in self.__parent:
            return item
        while self.__parent[item] != item:
            (item, self.__parent[item]) = \
                    (self.__parent[item], self.__parent[self.__parent[item]])
        return item

    def isSameGroup(self, item1: _T, item2: _T) -> bool:
        """
        Return whether the two items are in the same group
        """
        if any(k not in self.__parent for k in (item1, item2)):
            return item1 == item2
        return self.getRep(item1) == self.getRep(item2)

    def union(self, item1: _T, item2: _T) -> None:
        """
        Union the groups of the two items
        """
        for k in (item1, item2):
            self.addItem(k)
        item1 = self.getRep(item1)
        item2 = self.getRep(item2)
        if item1 == item2:
            return
        if self.__gpSize[item1] < self.__gpSize[item2]:
            (item1, item2) = (item2, item1)
        self.__parent[item2] = item1
        self.__gpSize[item1] += self.__gpSize[item2]
        self.__isCompressed = False

    def __compress(self):
        """
        Compress the structure
        Reassign each parent to rep
        ~O(n ItLn(n)) ~ O(n) time complexity
        """
        if self.__isCompressed:
            return
        for k in self.__parent:
            self.__parent[k] = self.getRep(k)
        self.__isCompressed = True

    def groupCount(self) -> int:
        """
        Return the number of groups
        """
        self.__compress()
        return len(frozenset(self.__parent.values()))

    def entriesInSameGroup(self, item: _T) -> frozenset[_T]:
        """
        Return the indices that are in the same group as the item
        """
        self.__compress()
        return frozenset(
                ele
                for ele in self.__parent
                if self.__parent[ele] == self.__parent[item])

    def groupSize(self, item: _T) -> int:
        """
        Return the size of the group that the item belongs to
        """
        self.__compress()
        return sum(
                1
                for par in self.__parent.values()
                if par == self.__parent[item])

class SegmentTree:
    """
    Prop-down segment tree
    Each update only affects subranges
    Can be used for hit count on a range

    NOTE: a bit too slow, not ready for use
    TODO: need more testing
    """
    __slots__ = ('__dim', '__nodeList')

    RangeType: _TypeAlias = tuple[tuple[int, int], ...]

    @_dc.dataclass
    class __Node:
        """
        Helper class for the node
        """
        # domain of node, in form prod [a, b)
        dom: 'SegmentTree.RangeType'
        # division point to determine child
        divPt: _tp.Optional[tuple[int, ...]] = _dc.field(init=False, default=None) # c
        # value of this node
        val: int
        # index of child by location mark
        # False: [a, c), True: [c, b)
        child: dict[tuple[bool, ...], int] = _dc.field(init=False, default_factory=dict)
        # vol that belongs to this node, nan = needs to recalculate
        effVol: _tp.Union[int, float] = _dc.field(init=False, default=float('nan'))

        def __post_init__(self):
            self.effVol = prod(itv[1] - itv[0] for itv in self.dom)

        @classmethod
        def __getDivVal(cls, itv: tuple[int, int], domItv: tuple[int, int]) -> int:
            """
            Helper function for new divPt
            if itv is properly contained in domItv, uses itv[0]
            else if itv is not domItc, uses the endpoint that is different
            otherwise, uses a mid point
            """
            if domItv[0] + 1 <= itv[0] and itv[1] < domItv[1] - 1:
                return itv[0]
            elif itv[0] != domItv[0]:
                return itv[0]
            elif itv[1] != domItv[1]:
                return itv[1]
            elif domItv == (-intInf, intInf):
                return 0
            elif domItv[0] == -intInf:
                return (domItv[1] * 2) \
                        if domItv[1] < 0 \
                        else (-4 if domItv[1] == 0 else 0)
            elif domItv[1] == intInf:
                return (domItv[0] * 2) \
                        if domItv[0] > 0 \
                        else (4 if domItv[0] == 0 else 0)
            else:
                return sum(domItv) // 2

        def setDivPt(self, interval: 'SegmentTree.RangeType'):
            """
            Set divPt according to interval
            Assumed interval \\subseteq self.dom
            Does not check if divPt is set
            """
            self.divPt = tuple(self.__getDivVal(interval[d], self.dom[d])
                               for d in range(len(self.dom)))

        def getChildDom(self, m: tuple[bool, ...]) -> 'SegmentTree.RangeType':
            """
            Compute what the domain of the designated location mark is
            Assumed divPt is set
            """
            assert self.divPt is not None, \
                "Attempt to get child domain on node without divPt"
            assert len(m) == len(self.dom), "Dimension mismatch"
            return tuple(((self.divPt[d], self.dom[d][1])
                          if m[d]
                          else (self.dom[d][0], self.divPt[d]))
                         for d in range(len(self.dom)))

        def recalEffVol(self):
            """
            Recalculate effVol
            Time complexity: ~2 ** dim
            """
            totalVol = 0
            for m in _it.product((False, True), repeat=len(self.dom)):
                if m not in self.child:
                    totalVol += prod(itv[1] - itv[0] for itv in self.getChildDom(m))
                if _isinf(totalVol):
                    break
            self.effVol = totalVol


    def __init__(self, dim: int):
        self.__dim: int = dim
        self.__nodeList: list['SegmentTree.__Node'] = [
            self.__Node(tuple((-intInf, intInf) for _ in range(dim)), 0)
        ]

    @property
    def dim(self) -> int:
        """
        Dimension of the tree
        """
        return self.__dim

    def __len__(self) -> int:
        return len(self.__nodeList)

    def __incre(self, ptr: int, interval: 'SegmentTree.RangeType', val: int):
        """
        increment interval by val
        interval assumed as [a, b)
        assume interval \\subseteq __nodeList[ptr].dom
        """
        if self.__nodeList[ptr].dom == interval:
            # update nodes and children therein
            stack: list[int] = [ptr]
            while len(stack) != 0:
                cPtr = stack.pop()
                self.__nodeList[cPtr].val += val
                stack.extend(self.__nodeList[cPtr].child.values())
        else:
            if self.__nodeList[ptr].divPt is None:
                # do not know how to subdivide yet
                self.__nodeList[ptr].setDivPt(interval)
            assert self.__nodeList[ptr].divPt is not None
            # child identifiers that we need propagate search
            involvedRange: frozenset[tuple[bool, ...]] = frozenset((tuple(),))
            for i in range(self.__dim):
                if len(involvedRange) == 0:
                    break
                possibleRange: tuple[bool, ...] = \
                        ((False,)
                         if interval[i][0] < self.__nodeList[ptr].divPt[i]
                         else tuple()) \
                        + ((True,)
                           if self.__nodeList[ptr].divPt[i] < interval[i][1]
                           else tuple())
                if len(possibleRange) == 0:
                    involvedRange = frozenset()
                    break
                involvedRange = frozenset(n + (choice,)
                                          for n in involvedRange
                                          for choice in possibleRange)
            for m in involvedRange:
                if m not in self.__nodeList[ptr].child:
                    # does not have this child yet, need to create new one
                    self.__nodeList[ptr].child[m] = len(self.__nodeList)
                    self.__nodeList.append(self.__Node(
                        self.__nodeList[ptr].getChildDom(m),
                        self.__nodeList[ptr].val))
                    self.__nodeList[ptr].effVol -= self.__nodeList[len(self.__nodeList) - 1].effVol
                self.__incre(
                        self.__nodeList[ptr].child[m],
                        tuple(((max(self.__nodeList[ptr].divPt[d], interval[d][0]),
                                interval[d][1])
                               if m[d]
                               else (interval[d][0],
                                     min(self.__nodeList[ptr].divPt[d], interval[d][1])))
                              for d in range(self.__dim)),
                        val)

    def add(self, interval: 'SegmentTree.RangeType', val: int = 1):
        """
        Add a new interval

        Parameter
        -----
        interval: tuple[tuple[int, int], ...]
            the range of the new interval
            Assumed of format (itv, ...) where itv = [a, b) is the slice

        val: int
            the hit count
        """
        assert len(interval) == self.__dim, "Dim mismatch"
        assert all(len(itv) == 2 and itv[0] < itv[1] for itv in interval), \
                "Not a valid range"
        self.__incre(0, interval, val)

    def getAtPoint(self, pt: tuple[int, ...]) -> int:
        """
        Get the hit count at the given point
        """
        assert len(pt) == self.__dim, "Dimension mismatch"
        if len(self.__nodeList) == 0:
            return 0
        ptr = 0
        while self.__nodeList[ptr].divPt is not None \
                and (m := tuple(self.__nodeList[ptr].divPt[d] <= pt[d]
                                for d in range(self.__dim))) in self.__nodeList[ptr].child:
            ptr = self.__nodeList[ptr].child[m]
        return self.__nodeList[ptr].val

    def maxHit(self) -> tuple[tuple['SegmentTree.RangeType', ...], int]:
        """
        Find the max hit

        Return
        -----
        a tuple that consists of
            a tuple of ranges, each represents a range that has the maximal hit count
            a integer that represents the maximal hit count
        """
        leafIdx = tuple(i for i, n in enumerate(self.__nodeList) if len(n.child) == 0)
        maxVal = max(self.__nodeList[i].val for i in leafIdx)
        return (tuple(self.__nodeList[idx].dom
                      for idx in leafIdx
                      if self.__nodeList[idx].val == maxVal),
                maxVal)

    def countVal(
            self,
            valRange: _tp.Union[int, tuple[int, int]]) -> _tp.Union[int, float]:
        """
        Count the (hyper)volume that is in the given range

        Parameter
        -----
        valRange: int or tuple[int, int]
            the range to enquiry
            if int, only count intervals that is exactly this value
            if tuple, count intervals with values in this range (read as [a, b))

        Return
        -----
        The (hyper)range of intervals with the given condition,
            which is either an integer or float('inf')
        """
        if isinstance(valRange, int):
            valRange = (valRange, valRange + 1)
        assert isinstance(valRange, tuple)
        volCount: _tp.Union[int, float] = 0
        for node in self.__nodeList:
            if valRange[0] <= node.val < valRange[1]:
                if _isnan(node.effVol):
                    node.recalEffVol()
                volCount += node.effVol
            if _isinf(volCount):
                break
        return volCount

def longestCommonPrefix(listOfStr: _tp.Sequence[str]) -> str:
    """
    Find longest common prefix of the given strings

    Parameters
    -----
    listOfStr: Sequence[str]
        the strings in question

    Returns
    -----
    the longest string that is a common prefix of all strings in `listOfStr`,
        which may be the empty string
    """
    assert len(listOfStr) != 0
    sampleStr: str = next(iter(listOfStr))
    ptr: int = len(sampleStr)
    for s in listOfStr:
        ptr = min(len(s), ptr)
        for i in range(ptr):
            if s[i] != sampleStr[i]:
                ptr = i
                break
    return sampleStr[:ptr]


def segmentIntersection(
        ps: Point, pe: Point,
        qs: Point, qe: Point
        ) -> _tp.Union[None, Point, tuple[Point, Point]]:
    """
    Check if two segments have intersection

    Parameters
    -----
    ps, pe, qs, qe: Point
        the endpoints of the segments to check
        assumed to be 2-dimenisonal
        the two segments should have endpoints (ps, pe), (qs, qe) resp.

    Returns
    -----
    Either of None, a Point, or a tuple of 2 Point
    If the two segments have no intersection,
        None
    If they have a single point intersection,
        Point that records the point
    If they have more than one intersection,
        a tuple of Point that denotes the intersection segment

    Note
    -----
    from https://stackoverflow.com/a/565282
    """
    assert all(pt.dim == 2 for pt in (ps, pe, qs, qe))
    r = pe - ps
    s = qe - qs

    def crossProd(pt1: Point, pt2: Point) -> float:
        return pt1[0] * pt2[1] - pt1[1] * pt2[0]

    rxs = crossProd(r, s)
    pqxr = crossProd(ps - qs, r)
    if rxs == 0:
        if pqxr == 0:
            # case 1
            rr = r.innerProd(r)
            t0 = (qs - ps).innerProd(r) / rr
            t1 = t0 + r.innerProd(s) / rr
            if t0 > t1:
                t0, t1 = t1, t0
            t0 = max(0, t0)
            t1 = min(1, t1)
            if t0 > t1:
                return None
            else:
                return (ps + t0 * r, ps + t1 * r)
        else:
            # case 2
            return None
    elif 0 <= (t := -crossProd(qs - ps, s) / rxs) <= 1 \
                and 0 <= -pqxr / rxs <= 1:
        # case 3
        return ps + t * r
    else:
        # case 4
        return None

def polygonArea(
        vertices: _tp.Sequence[Point]
        ) -> float:
    """
    Find the area of a 2D polygon with shoelace formula
    Assumed no self intersection of edges

    Parameters
    -----
    vertices: Sequence[Point]
        the vertices of the polygon
        assumed to be 2-dimenisonal and given in an edge order
            that is, every pair of adjacent points has an edge connecting them
            (this includes the first and the last points)

    Returns
    -----
    a float representing the area. Always nonnegative

    NOTE
    -----
    see https://en.wikipedia.org/wiki/Shoelace_formula
    """
    assert all(pt.dim == 2 for pt in vertices)
    doubleArea: float = 0.0
    for i in range(len(vertices)):
        doubleArea += vertices[i][1] * vertices[i - 1][0] \
                - vertices[i][0] * vertices[i - 1][1]
    return abs(doubleArea) / 2.0


