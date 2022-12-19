import re
from collections import defaultdict
from functools import cache, lru_cache
import time
import sys

sys.setrecursionlimit(1000000)


with open('d16_data.txt', 'r') as f:
    content = f.read().splitlines()

class Valve:
    def __init__(self, name, flow_rate, other):
        self.name = name
        self.flow_rate = flow_rate
        self.other = other
        self.open = False

    def __repr__(self):
        return f'{self.name} @ {self.flow_rate} -> {self.other}'

def init(content):
    valves = []

    regex = r'\d+'
    for line in content:
        fr = int(re.findall(regex, line)[0])
        valve = line.split(' ')[1]
        try:
            other = line.split('valves ')[1].split(', ')
        except IndexError as e:
            other = line.split('valve ')[1].split(', ')
        v = Valve(valve, fr, other)
        valves.append(v)
    return valves

valves = init(content)
valves = sorted(valves, key=lambda x: x.name)
valves_dict = {v.name: v for v in valves}

def bfs(valve: Valve, other: Valve):
    queue = []
    queue.append((valve.name, 0))
    visited = []
    visited.append(valve.name)

    while queue:
        v, dist = queue.pop(0)
        v: Valve = valves_dict[v]

        visited.append(v.name)

        if v.name == other.name:
            return dist
        else:
            for i in v.other:
                if i not in visited:
                    queue.append((i, dist+1))

def create_dist_matrix(valves):
    """ Create a matrix of how long it takes to get from each valve to each other valve """
    valve_distM = defaultdict(int)  # {(AB): 5}  A to B in 5 minutes
    for v1 in valves:
        for v2 in valves:
            #if valve_distM[v1.name, v2.name] == 0 and valve_distM[v2.name, v1.name] == 0:
            #    x = bfs(v1, v2)
            valve_distM[v1.name, v2.name] = bfs(v1, v2)
            #    valve_distM[v2.name, v1.name] = x #bfs(v1, v2)


    return valve_distM

ss = time.perf_counter()
valve_distM = create_dist_matrix(valves)
print(f'> {(time.perf_counter() - ss):.3f}')
non_zero_valves = [v for v in valves if v.flow_rate > 0]

for v in non_zero_valves:
    print(v)
#for v in valves:
#    print(v)
print('----------------------------')


@cache
def loop_1_fast(current: Valve, minute: int, opened: set):
    if minute <= 0:
        return 0

    best = 0
    #for valve in current.other:
    for valve in non_zero_valves:
        dist = valve_distM[current.name, valve.name]
        if dist > 0:
            best = max(best, loop_1_fast(valve, minute-dist, opened))

    if current.name not in opened and current.flow_rate > 0 and minute > 0:
        opened = set(opened)
        opened.add(current.name)
        minute -= 1
        new_sum = minute * current.flow_rate
        #for valve in current.other:
        for valve in non_zero_valves:
            dist = valve_distM[current.name, valve.name]
            if dist > 0:
                best = max(best, new_sum + loop_1_fast(valve, minute - dist, frozenset(opened)))

    return best

@cache
def loop(current: Valve, minute: int, opened: set):
    #print(current)

    if minute <= 0:
        return 0

    best = 0
    for valve in current.other:
        best = max(best, loop(valves_dict[valve], minute-1, opened))

    if current.name not in opened and current.flow_rate > 0 and minute > 0:
        opened = set(opened)
        opened.add(current.name)
        minute -= 1
        new_sum = minute * current.flow_rate
        for valve in current.other:
            best = max(best, new_sum + loop(valves_dict[valve], minute - 1, frozenset(opened)))

    return best

@cache
def loop_2(current: Valve, minute: int, opened: set):
    #print(current)

    if minute <= 0:
        return loop(valves_dict['AA'], 26, opened)

    best = 0
    for valve in current.other:
        best = max(best, loop_2(valves_dict[valve], minute-1, opened))

    if current.name not in opened and current.flow_rate > 0 and minute > 0:
        opened = set(opened)
        opened.add(current.name)
        minute -= 1
        new_sum = minute * current.flow_rate
        for valve in current.other:
            best = max(best, new_sum + loop_2(valves_dict[valve], minute - 1, frozenset(opened)))

    return best


def part1(valves):
    aa = valves[0]

    ss = time.perf_counter()
    trip = loop_1_fast(aa, 30, frozenset())  # Part1: 2080
    print(f'Total release (Part1): {trip}')
    print(f'> {(time.perf_counter() - ss):.3f}')

    ss = time.perf_counter()
    trip = loop(aa, 30, frozenset())  # Part1: 2080
    print(f'Total release (Part1): {trip}')
    print(f'> {(time.perf_counter() - ss):.3f}')

    ss = time.perf_counter()
    trip = loop_2(aa, 26, frozenset())  # Part2:
    print(f'Total release (Part2): {trip}')
    print(f'> {(time.perf_counter() - ss):.3f}')

    return


part1(valves)