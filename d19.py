import re

with open('d19_data.txt', 'r') as f:
    content = f.read().splitlines()

regex = r'\d+'
bp = [list(map(int,re.findall(regex, line))) for line in content]

time_steps = 32 #24

o = [(t-1) * t // 2 for t in range(time_steps + 1)]  # Triangular series

max_ = 0

def part1(blueprints):
    total = 0
    totals = []
    for n, a, b, c, d, e, f in blueprints:
        global max_
        max_ = 0
        mi, mj, mk = max(a, b, c, e), d, f
        def dfs(time, robot, ore_r, clay_r, obsidian_r, geode_r, ore_a, clay_a, obsidian_a, geode_a):
            global max_
            if(
                robot == 0 and ore_r >= mi or
                robot == 1 and clay_r >= mj or
                robot == 2 and (obsidian_r >= mk or clay_r == 0) or
                robot == 3 and obsidian_r == 0 or
                geode_a + geode_r * time + o[time] <= max_
            ): # Prune
                return

            while time:
                if robot == 0 and ore_a >= a: # create ORE robot
                    for r in range(4):
                        dfs(time-1, r, ore_r + 1, clay_r, obsidian_r, geode_r, ore_a - a + ore_r, clay_a + clay_r, obsidian_a + obsidian_r, geode_a + geode_r )
                    return
                elif robot == 1 and ore_a >= b: # create CLAY roboto
                    for r in range(4):
                        dfs(time-1, r, ore_r, clay_r + 1, obsidian_r, geode_r, ore_a - b + ore_r, clay_a + clay_r, obsidian_a + obsidian_r, geode_a + geode_r)
                    return
                elif robot == 2 and ore_a >= c and clay_a >= d: # create OBSIDIAN robot
                    for r in range(4):
                        dfs(time-1, r, ore_r, clay_r, obsidian_r + 1, geode_r, ore_a - c + ore_r, clay_a - d + clay_r, obsidian_a + obsidian_r, geode_a + geode_r)
                    return
                elif robot == 3 and ore_a >= e and obsidian_a >= f: # create GEODE robot
                    for r in range(4):
                        dfs(time-1, r, ore_r, clay_r, obsidian_r, geode_r + 1, ore_a - e + ore_r, clay_a + clay_r, obsidian_a - f + obsidian_r, geode_a + geode_r)
                    return
                # Cannot create robot
                time, ore_a, clay_a, obsidian_a, geode_a = time-1, ore_a + ore_r, clay_a + clay_r, obsidian_a + obsidian_r, geode_a + geode_r
            # How much did we collect after 24 minutes
            max_ = max( max_, geode_a )

        # Try every starting robot for every blueprint
        for r in range(4):
            dfs(time_steps, r, 1, 0, 0, 0, 0, 0, 0, 0)
        total += max_ * n
        totals.append(max_)
        if n == 3:  # For part 2 only compute first 3 blue prints
            break

    print('Part 1: ', total)

    out = 1
    for t in totals:
        out *= t
    print('Part 2: ', out)




if __name__ == '__main__':
    part1(bp)