import random
def create_grid():
    mines=10
    size=8
    minesplaced=0
    grid=[[0 for _ in range(size)] for _ in range(size)]
    while minesplaced < mines:
        i=random.randint(0,size-1)
        j=random.randint(0,size-1)
        if grid[i][j] != 'M':
            grid[i][j]="M"
            minesplaced+=1
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "M":
                continue

            count = 0

            for ni in range(max(0, i - 1), min(size, i + 2)):
                for nj in range(max(0, j - 1), min(size, j + 2)):
                    if (ni, nj) == (i, j):
                        continue

                    if grid[ni][nj] == "M":
                        count+=1
                
            grid[i][j] = count
    return grid
