from collections import defaultdict
import time

alphabet = 'abcdefghijklmnopqrstuvwxyzES' # 0 - 27
print(len(alphabet))

grid = {}
start = None
end = None
rows = 0
cols = 0

with open('d12_data.txt', 'r') as f:
    content = f.read().splitlines()
    rows = len(content)
    cols = len(content[0])
    for i, line in enumerate(content):
        for k, char in enumerate(line):
            grid[(i, k)] = alphabet.index(char)
            if char == 'S':
                start = (i, k)
            if char == 'E':
                end = (i, k)



def bfs_part1(grid: dict, start: tuple, end: tuple):
    """  Breath-first search
    Walk from the start to all squares keeping track of the number of steps along the way
    When we reach END, we check how many steps we needed
    """
    queue = []
    start = (start[0], start[1], 1)
    queue.append(start)

    distance = {}
    for (a, b), _ in grid.items():
        distance[(a, b)] = 99999
    distance[start] = 0

    while queue:
        si, sk, steps = queue.pop(0)
        height = grid[(si, sk)]
        #print(f'({si}, {sk}, {steps}) {alphabet[height]}')

        if si == end[0] and sk == end[1]:
            print(f'End found: {si} {sk} | distance: {distance[(si, sk)]}')
            return end

        for i in [-1, 1]:
            # Check up/down
            if (0 <= si+i < rows):
                if grid[(si+i, sk)] <= height+1 and steps < distance[(si+i, sk)]:
                    distance[(si+i, sk)] = steps
                    queue.append((si+i, sk, steps+1))
            # Check left/right
            if (0 <= sk+i < cols):
                if grid[(si, sk+i)] <= height+1 and steps < distance[(si, sk+i)]:
                    distance[(si, sk+i)] = steps
                    queue.append((si, sk+i, steps+1))


def bfs_part2(grid: dict, start: tuple, end: tuple):
    """
    Walk backwards from the END untill you find the first 'a' square in the grid
    """
    queue = []
    start = (start[0], start[1], 1)
    queue.append(start)

    distance = {}
    for (a, b), _ in grid.items():
        distance[(a, b)] = 99999
    distance[start] = 0

    while queue:
        si, sk, steps = queue.pop(0)
        height = grid[(si, sk)]
        #print(f'({si}, {sk}, {steps}) {alphabet[height]}')

        if grid[(si, sk)] == 0:
            print(f'End found: {si} {sk} | distance: {distance[(si, sk)]}')
            return distance[(si, sk)]

        for i in [-1, 1]:
            # Check up/down
            if (0 <= si+i < rows):
                if grid[(si+i, sk)] - height >= -1 and steps < distance[(si+i, sk)]:
                    distance[(si+i, sk)] = steps
                    queue.append((si+i, sk, steps+1))
            # Check left/right
            if (0 <= sk+i < cols):
                if grid[(si, sk+i)] - height >= -1 and steps < distance[(si, sk+i)]:
                    distance[(si, sk+i)] = steps
                    queue.append((si, sk+i, steps+1))


print(f'Start: {start}')
print(f'End: {end}')
ss = time.perf_counter()
bfs_part1(grid, start, end)
print(f'{(time.perf_counter() - ss):.3f}')

ss = time.perf_counter()
bfs_part2(grid, end, start)
print(f'{(time.perf_counter() - ss):.3f}')
