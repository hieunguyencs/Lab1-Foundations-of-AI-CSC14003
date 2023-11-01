import sys
import heapq
from WriteOutput import *
import visualizer
from visualizer import frames,draw_cell, load_maze, dx, dy, WIN, LONGDELAY

pygame.display.set_caption("UCS")

# --- WRITE GRAPH FUNCTION HERE ---
# You can call function draw_cell(x, y, IMG) to draw IMG at cell (x, y)

def find_start(grid, num_row, num_col): 
    for i in range(num_row):
        for j in range(num_col):
            if grid[i][j] == 'S':
                return [i, j]
            
def find_end(grid, num_row, num_col): 
    for i in range(num_row): 
        for j in range(num_col): 
            if (grid[i][j] != 'x'
                and (i == 0 or i == num_row - 1
                     or j == 0 or j == num_col - 1)): 
                return [i, j]

def ucs(grid, num_row, num_col): 
    start = find_start(grid, num_row, num_col)
    end = find_end(grid, num_row, num_col)

    visited = [[False for i in range(num_col)] for i in range(num_row)]
    trace = [[[-1, -1] for i in range(num_col)] for i in range(num_row)]
    distance = [[1_000_000_000 for i in range(num_col)] for i in range(num_row)]
    distance[start[0]][start[1]] = 0

    heap = []
    heapq.heappush(heap, [0, start])

    def inGrid(x, y): 
        return (x >= 0 and x < num_row
                and y >= 0 and y < num_col)

    while len(heap) > 0: 
        cur = heapq.heappop(heap)
        cur_dis = cur[0]
        cur_cell = cur[1]

        if (distance[cur_cell[0]][cur_cell[1]] != cur_dis): 
            continue

        for i in range(4): 
            newX = cur_cell[0] + dx[i]
            newY = cur_cell[1] + dy[i]
            if (inGrid(newX, newY) 
                and grid[newX][newY] != 'x'
                and not visited[newX][newY]): 
                if (cur_dis + 1 < distance[newX][newY]): 
                    distance[newX][newY] = cur_dis + 1
                    trace[newX][newY] = cur_cell
                    heapq.heappush(heap, [distance[newX][newY], [newX, newY]])

                    if [newX, newY] != end: 
                        draw_cell(newX, newY, visualizer.VISITED_IMG)

        visited[cur_cell[0]][cur_cell[1]] = True

    if distance[end[0]][end[1]] >= 1_000_000_000: 
        return []
    
    X, Y = end
    path = []
    while [X, Y] != [-1, -1]: 
        path.append([X, Y])
        X, Y = trace[X][Y]
    path.reverse()

    return path

def draw_path(path): 
    if (len(path) == 0): 
        return
    pygame.time.delay(LONGDELAY)
    draw_cell(path[0][0], path[0][1], visualizer.START_CHECK_IMG)
    end = path[-1]
    path = path[1:-1]
    for x, y in path: 
        draw_cell(x, y, visualizer.PATH_IMG)
    draw_cell(end[0], end[1], visualizer.DOOR_OPEN)

# ---------------------------------

def main(maze_path):
    maze_data, gift_data, num_row, num_col = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    path = ucs(maze_data, num_row, num_col)
    draw_path(path)

    dir_name = generate_output_path(maze_path, "UCS")
    cost_file = dir_name + "/UCS.txt"
    writeToFile(cost_file, path, WIN=WIN, frames=frames)

    # --------------------------------
    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python ucs.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)