from collections import defaultdict
import re
import time


with open('d15_data.txt', 'r') as f:
    content = f.read().splitlines()

regex = re.compile(r'[-]?\d+')
coords = []
for line in content:
    x = list(map(int,regex.findall(line)))
    coords.append(x)

def manhattten(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])

class Signal:
    def __init__(self, coord):
        self.coord: tuple = coord
        self.nearest: tuple = None
        self.nearest_distance: int = 9999999999

    def add_nearest(self, x):
        self.nearest = x

    def __repr__(self):
        return f'S: ({self.coord[0]}, {self.coord[1]})'

def init_grid(coords):
    grid = defaultdict(str)
    signals = defaultdict(Signal)
    beacons = defaultdict(int)

    for coord in coords:
        grid[coord[0], coord[1]] = 'S'
        grid[coord[2], coord[3]] = 'B'
        signals[coord[0], coord[1]] = Signal((coord[0], coord[1]))
        beacons[coord[2], coord[3]] = 'B'

    for (x1, y1), s in signals.items():
        for (x2, y2), _ in beacons.items():
            md = manhattten((x1,y1), (x2,y2))
            if md < s.nearest_distance:
                s.nearest_distance = md
                s.add_nearest((x2, y2))

    return grid, signals, beacons

def print_grid(grid):
    min_x = min([i[0] for i in grid.keys()])
    min_y = min([i[1] for i in grid.keys()])
    max_x = max([i[0] for i in grid.keys()])
    max_y = max([i[1] for i in grid.keys()])
    print(min_x, min_y)
    print(max_x, max_y)

    for x in range(min_x, max_x):
        ss = ""
        #ss += str(x)
        for y in range(min_y, max_y):
            c = grid[y, x]
            if c == '':
                ss += '.'
            else:
                ss += c
        print(ss)

def insert(coord, symb):
    if grid[coord] == '':
        grid[coord] = symb

def fill(coord, d, chng=-1):
    if d == 0:
        #grid[coord] = '#'
        insert(coord, '#')
        return
    x, y = coord
    new_coord = (x, y+chng)
    #grid[x, y] = '#'
    insert((x, y), '#')
    for i in range(1, d+1):
        #grid[x+i, y] = '#'
        insert((x+i, y), '#')
        #grid[x-i, y] = '#'
        insert((x-i, y), '#')
    fill(new_coord, d-1, chng)

def part1():
    for (x1, y1), s in signals.items():
        d = s.nearest_distance
        print('>', x1, y1, d)
        for i in range(1, d+1):
            #grid[(x1-i, y1)] = '#'
            insert((x1-i, y1), '#')
            #grid[(x1+i, y1)] = '#'
            insert((x1+i, y1), '#')
        fill((x1,y1-1), d-1, -1)
        fill((x1, y1+1), d-1, 1)


def part1_attempt3():
    min_x = min([i[0] for i in grid.keys()])
    max_x = max([i[0] for i in grid.keys()])
    roi = []
    for i in range(min_x*2, max_x*2):
        cell = Signal((i, 2_000_000))
        for (x, y), s in signals.items():
            md = manhattten((x,y), (i, 2_000_000))
            if md < cell.nearest_distance:
                cell.nearest_distance = md
                cell.nearest = s
        roi.append(cell)

    for cell in roi:
        if cell.nearest_distance <= cell.nearest.nearest_distance:
            grid[cell.coord] = '#'

    count = 0
    for i in range(min_x*2, max_x*2):
        if grid[(i,2_000_000)] == '#':
            count += 1
    print(count)


def part1_attempt2():
    # 4531484 -- to low
    # 4531485 -- to low

    min_x = min([i[0] for i in grid.keys()])
    min_y = min([i[1] for i in grid.keys()])
    max_x = max([i[0] for i in grid.keys()])
    max_y = max([i[1] for i in grid.keys()])
    print(min_x, max_x)
    for i in range(min_x * 2, max_x * 2):

        for (x, y), s in signals.items():
            md = manhattten((i, 2_000_000), (x, y))
            if md <= s.nearest_distance:
                grid[(i, 2_000_000)] = '#'

    count = 0
    for i in range(min_x * 2, max_x * 2):
        if grid[i,2_000_000] == '#':
            count += 1
    print(count)

    return

ss = time.perf_counter()
grid, signals, beacons = init_grid(coords)
part1_attempt2()
print(f">> {(time.perf_counter()-ss):.3f}")
ss = time.perf_counter()
grid, signals, beacons = init_grid(coords)
part1_attempt3()
print(f">> {(time.perf_counter()-ss):.3f}")
#print_grid(grid)
