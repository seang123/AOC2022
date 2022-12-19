
with open('d8_data.txt', 'r') as f:
    content = f.read().splitlines()


grid = {}

for ii, row in enumerate(content):
    for kk, tree in enumerate(row):
        grid[(ii,kk)] = tree


def part1(grid, content):
    n_rows = len(content)
    n_cols = len(content[0])

    visible = 0
    for (ii, kk), height in grid.items():

        if ii == 0 or kk == 0 or ii == len(content)-1 or kk == len(content[0])-1:
            visible += 1
            continue

        # Check up to row
        is_visible = True
        for neighbour in range(0, ii):
            h2 = grid[(neighbour, kk)]
            if h2 >= height:
                is_visible = False
        if is_visible:
            visible += 1
            continue

        is_visible = True
        for n in range(ii+1, n_rows):
            h2 = grid[(n, kk)]
            if h2 >= height:
                is_visible = False
        if is_visible:
            visible += 1
            continue

        is_visible = True
        for n in range(0, kk):
            h2 = grid[(ii, n)]
            if h2 >= height:
                is_visible = False
        if is_visible:
            visible += 1
            continue

        is_visible = True
        for n in range(kk+1, n_cols):
            h2 = grid[(ii, n)]
            if h2 >= height:
                is_visible = False
        if is_visible:
            visible += 1
            continue

    return visible

def part2(grid, content):
    n_rows = len(content)
    n_cols = len(content[0])

    scores = []
    for (ii, kk), height in grid.items():
        score_r1 = 0
        score_r2 = 0
        score_c1 = 0
        score_c2 = 0


        ## Rows
        for n in range(ii+1, n_rows):
            if grid[(n, kk)] >= grid[(ii, kk)]:
                score_r1 += 1
                break
            else:
                score_r1 += 1

        for n in range(ii-1, -1, -1):
            if grid[(n, kk)] >= grid[(ii, kk)]:
                score_r2 += 1
                break
            else:
                score_r2 += 1

        ## Cols
        for n in range(kk+1, n_cols):
            if grid[(ii, n)] >= grid[(ii, kk)]:
                score_c1 += 1
                break
            else:
                score_c1 += 1

        for n in range(kk-1, -1, -1):
            if grid[(ii, n)] >= grid[(ii, kk)]:
                score_c2 += 1
                break
            else:
                score_c2 += 1

        scores.append( score_r1 * score_r2 * score_c1 * score_c2 )

    return max(scores)


print('P1:', part1(grid, content))
print('P2:', part2(grid, content))