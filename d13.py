from itertools import zip_longest
import functools
from ast import literal_eval
from enum import Enum

with open('d13_data.txt', 'r') as f:
    content = [i.splitlines() for i in f.read().split('\n\n')]

npairs = []
for pair in content:
    npair = []
    for p in pair:
        npair.append(literal_eval(p))
    npairs.append(npair)

#for pairs in npairs:
#    print(pairs)


class State(Enum):
    Left = -1
    Right = +1
    Cont = 0

def compare(x, y):

    if isinstance(x, int) and isinstance(y, int):
        if x < y:
            return -1
        elif x == y:
            return 0
        else:
            return 1

    if type(x) is int:
        x = [x]
    if type(y) is int:
        y = [y]

    if x == [] and y != []: return -1
    if x != [] and y == []: return 1
    if x == [] and y == []: return 0

    tf = compare(x[0], y[0])
    if tf:
        return tf
    else:
        return compare(x[1:], y[1:])



def part1(pairs):
    pair_idxs = []
    for ii, pair in enumerate(pairs, start=1):
        p0 = pair[0]
        p1 = pair[1]
        state = compare(p0, p1)
        if state == -1:
            pair_idxs.append(ii)

    print('>', pair_idxs)
    return pair_idxs

def part2(pairs):
    data = pairs + [[[2]]] + [[[6]]]
    data.sort(key=functools.cmp_to_key(compare))
    print(f"Part 2: Decoder key: {1 + data.index( [[2]] ) * (1 + data.index( [[6]] ))}")


print('Sum pair idxs:', sum(part1(npairs)))

data = [literal_eval(t) for t in open("d13_data.txt").read().split()] + [[[2]]] + [[[6]]]
data.sort(key=functools.cmp_to_key(compare))
print("PART 2: Decoder key: ", (1 + data.index([[2]])) * (1 + data.index([[6]])))