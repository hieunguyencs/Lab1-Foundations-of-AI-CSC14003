import sys
import heapq
import math
from WriteOutput import *
import visualizer
from visualizer import frames,draw_cell, load_maze, dx, dy, WIN, LONGDELAY

pygame.display.set_caption("GBFS - Euclidean distance heuristic")

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

def GBFS(grid, num_row, num_col): 
    start = find_start(grid, num_row, num_col)
    end = find_end(grid, num_row, num_col)

    MAX_DIS = 1_000_000_000
    distance = [[MAX_DIS for i in range(num_col)] for i in range(num_row)]
    trace = [[[-1, -1] for i in range(num_col)] for i in range(num_row)]
    closed = [[0 for i in range(num_col)] for i in range(num_row)]

    # heuristic: Euclidean distance
    def h(x, y): 
        X = abs(x - end[0]) 
        Y = abs(y - end[1])
        return math.sqrt(X*X + Y*Y)
    
    def constructPath(): 
        X, Y = end
        path = []
        while [X, Y] != [-1, -1]: 
            path.append([X, Y])
            X, Y = trace[X][Y]
        path.reverse()        
        return path
    
    def inGrid(x, y): 
        return (x >= 0 and x < num_row
                and y >= 0 and y < num_col)

    heap = []
    heapq.heappush(heap, [h(start[0], start[1]), start])
    closed[start[0]][start[1]] = 1
    found = False
    while len(heap) > 0: 
        if (found): 
            break
        
        next = heapq.heappop(heap)
        picked_cell = next[1]
        value = next[0]

        # if (picked_cell == end): 
        #     break

        if (picked_cell != start): 
            draw_cell(picked_cell[0], picked_cell[1], visualizer.VISITED_IMG)

        for i in range(4): 
            next_x = picked_cell[0] + dx[i]
            next_y = picked_cell[1] + dy[i]

            if (inGrid(next_x, next_y)
                and grid[next_x][next_y] != 'x'
                and closed[next_x][next_y] == 0): 

                distance[next_x][next_y] = distance[picked_cell[0]][picked_cell[1]] + 1
                trace[next_x][next_y] = picked_cell
                closed[next_x][next_y] = 1
                heapq.heappush(heap, [h(next_x, next_y), [next_x, next_y]])

                if [next_x, next_y] == end: 
                    found = True
                    break

    path = []
    tmp = []
    if (found): 
    # draw path
        path = constructPath()
        tmp = path

        if len(path) > 0: 
            pygame.time.delay(LONGDELAY)
            draw_cell(path[0][0], path[0][1], visualizer.START_CHECK_IMG)
            end = path[-1]
            path = path[1:-1]
            for x, y in path: 
                draw_cell(x, y, visualizer.PATH_IMG)
            draw_cell(end[0], end[1], visualizer.DOOR_OPEN)

    return tmp

# ---------------------------------

def main(maze_path):
    maze_data, gift_data, rows, cols = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    path = GBFS(maze_data, rows, cols)

    dir_name = generate_output_path(maze_path, "GBFS_heuristic_2")
    cost_file = dir_name + "/GBFS_heuristic_2.txt"
    writeToFile(cost_file, path, WIN=WIN, frames=frames)

    # --------------------------------
    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python gbfs_heuristic2.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
