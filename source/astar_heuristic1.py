import sys
import heapq
from WriteOutput import *
import visualizer
from visualizer import frames,draw_cell, load_maze, dx, dy, WIN, LONGDELAY

pygame.display.set_caption("A* - Manhattan distance heuristic")

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

def aStar(grid, num_row, num_col): 
    start = find_start(grid, num_row, num_col)
    end = find_end(grid, num_row, num_col)
    
    MAX_DIS = 1_000_000_000
    distance = [[MAX_DIS for i in range(num_col)] for i in range(num_row)]
    trace = [[[-1, -1] for i in range(num_col)] for i in range(num_row)]
    open = [[0 for i in range(num_col)] for i in range(num_row)]
    heap = [] # this is for getting min f = g + h

    # heuristic: manhattan distance 
    def h(x, y):
        X = abs(x - end[0])
        Y = abs(y - end[1])
        return X + Y
    
    # trace path
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

    distance[start[0]][start[1]] = 0
    heapq.heappush(heap, [h(start[0], start[1]), start])
    open[start[0]][start[1]] = True

    while len(heap) > 0: 
        cur = heapq.heappop(heap)
        cur_cell = cur[1]

        if (cur_cell == end): 
            return constructPath()
        
        if cur_cell != start:
            draw_cell(cur_cell[0], cur_cell[1], visualizer.VISITED_IMG)

        open[cur_cell[0]][cur_cell[1]] = False
        for i in range(4): 
            newX = cur_cell[0] + dx[i]
            newY = cur_cell[1] + dy[i]

            if not inGrid(newX, newY) or grid[newX][newY] == 'x':
                continue

            proposal_gScore = distance[cur_cell[0]][cur_cell[1]] + 1
            if (proposal_gScore < distance[newX][newY]):
                distance[newX][newY] = proposal_gScore
                fScore = proposal_gScore + h(newX, newY)
                trace[newX][newY] = cur_cell
                if not open[newX][newY]:
                    heapq.heappush(heap, [fScore, [newX, newY]])

    return []

def draw_path(path): 
    if len(path) == 0: 
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
    maze_data, gift_data, rows, cols = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    path = aStar(maze_data, rows, cols)
    draw_path(path)


    dir_name = generate_output_path(maze_path, "astar_heuristic_1")
    cost_file = dir_name + "/astar_heuristic_1.txt"
    writeToFile(cost_file, path, WIN=WIN, frames=frames)

    # --------------------------------


    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python astar_heuristic1.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
