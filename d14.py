from collections import defaultdict
from enum import Enum
import time

with open('d14_data.txt', 'r') as f:
    content = f.read().splitlines()


class Cave:
    Sand = -1
    Free = 0
    Wall = 1

def create_grid(content) -> defaultdict(int):
    grid = defaultdict(int)

    for line in content:
        coords = line.split(' -> ')
        for i in range(len(coords)-1):
            x1, y1 = [int(i) for i in coords[i].split(',')]
            x2, y2 = [int(i) for i in coords[i+1].split(',')]

            if x1 == x2:
                if y1 < y2:
                    for i in range(y1, y2+1):
                        grid[(x1, i)] = Cave.Wall
                elif y1 > y2:
                    for i in range(y2, y1+1):
                        grid[(x1, i)] = Cave.Wall
                else:
                    raise Exception('')
            elif y1 == y2:
                if x1 < x2:
                    for i in range(x1, x2+1):
                        grid[(i, y1)] = Cave.Wall
                elif x1 > x2:
                    for i in range(x2, x1+1):
                        grid[(i, y1)] = Cave.Wall
                else:
                    raise Exception('')
            else:
                raise Exception('')
    return grid

# As sand falls its X component (X, Y) stays the same and Y component increases



def falling(grain, grid, max_depth):

    x, y = grain
    if y >= max_depth:
        return False
    # IF next square down is blocked
    elif grid[(x, y+1)] == Cave.Sand or grid[(x, y+1)] == Cave.Wall:
        # Falling to the left
        if grid[(x-1, y+1)] != Cave.Sand and grid[(x-1, y+1)] != Cave.Wall:
            return falling((x-1, y+1), grid, max_depth)
        # Falling to the right
        elif grid[(x+1, y+1)] != Cave.Sand and grid[(x+1, y+1)] != Cave.Wall:
            return falling((x+1, y+1), grid, max_depth)
        # Both left and right are covered
        else:
            grid[(x, y)] = Cave.Sand
            return True

    # Next square is free, keep falling
    return falling((x, y+1), grid, max_depth)


def part1(content):
    grid = create_grid(content)
    max_depth = max([i[1] for i in grid.keys()])  # lowest platform at this depth - anything deeper is the void

    in_void = False
    grain_count = 0
    while not in_void:
        landed = falling((500, 0), grid, max_depth)
        if not landed:
            in_void = True
        else:
            grain_count += 1

    print(f'{grain_count} grains landed')


def part2(content):
    grid = create_grid(content)
    max_depth = max([i[1] for i in grid.keys()]) + 2

    for i in range(-1000, 1000):
        grid[(i, max_depth)] = Cave.Wall

    blocked = False
    grain_count = 0
    while not blocked:
        if grid[(500, 0)] == Cave.Sand:
            blocked = True
        else:
            landed = falling((500, 0), grid, max_depth)
            if not landed:
                blocked = True
            else:
                grain_count += 1

    print(f'{grain_count} grains landed')


ss = time.perf_counter()
part1(content)
print(f'> {(time.perf_counter() - ss):.3f}')
ss = time.perf_counter()
part2(content)
print(f'> {(time.perf_counter() - ss):.3f}')
