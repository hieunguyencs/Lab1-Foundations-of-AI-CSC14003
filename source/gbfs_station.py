import sys
from collections import deque
import heapq
from WriteOutput import *
import visualizer
from visualizer import frames,draw_cell, load_maze, dx, dy, WIN, LONGDELAY

pygame.display.set_caption("Stations: GBFS")

# because STATION and GIFT use a same symbol '+' in .txt
# so, I use this code to change STATION icon in pygame map
STATION_IMG = pygame.image.load(os.path.join('..', 'Assets', 'bus_stop.jpg'))
GIFT_IMG = STATION_IMG
GIFT_IMG = pygame.transform.scale(GIFT_IMG, (visualizer.CELL_WIDTH, visualizer.CELL_HEIGHT))

# --- WRITE GRAPH FUNCTION HERE ---
# You can call function draw_cell(x, y, IMG) to draw IMG at cell (x, y)

total_path = []

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

def cnt_distance(grid, rows, cols): 
    start_x, start_y = find_end(grid, rows, cols)

    visited = [[False for _ in range(cols)] for _ in range(rows)]
    trace = [[(0, 0) for _ in range(cols)] for _ in range(rows)]
    distance = [[0 for i in range(cols)] for i in range(rows)]
    queue = deque()

    queue.append((start_x, start_y))
    visited[start_x][start_y] = True

    while queue:
        x, y = queue.popleft()

        for i in range(4):
            new_x, new_y = x + dx[i], y + dy[i]

            if (
                0 <= new_x < rows
                and 0 <= new_y < cols
                and not visited[new_x][new_y]
                and grid[new_x][new_y] != 'x'
            ):
                queue.append((new_x, new_y))
                visited[new_x][new_y] = True
                trace[new_x][new_y] = (x, y)
                distance[new_x][new_y] = distance[x][y] + 1

                # draw_cell(new_x, new_y, VISITED_IMG)
 
    return distance

def GBFS(grid, num_row, num_col, start, end): 
    MAX_DIS = 1_000_000_000
    distance = [[MAX_DIS for i in range(num_col)] for i in range(num_row)]
    trace = [[[-1, -1] for i in range(num_col)] for i in range(num_row)]
    closed = [[0 for i in range(num_col)] for i in range(num_row)]

    # heuristic: manhattan distance 
    def h(x, y):
        X = abs(x - end[0])
        Y = abs(y - end[1])
        return X + Y
    
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

    return constructPath()

def find_path(grid, gift_data, rows, cols): 
    # find distance from end to all pickup cell
    distance = cnt_distance(grid, rows, cols)

    # draw maze again
    # pygame.time.delay(long_delay)
    # draw_maze(grid, rows, cols)
    pygame.time.delay(LONGDELAY)

    # save list of pick up cells and also start, end
    pick_up_list = []
    for x, y, z in gift_data: 
        pick_up_list.append([distance[x][y], [x, y]])
    pick_up_list.sort()
    pick_up_list.reverse()
    start = find_start(grid, rows, cols)
    end = find_end(grid, rows, cols)
    pick_up_list.append([0, end])
    pick_up_list.insert(0, [0, start])

    # # list includes pick up cell
    lst = []
    for x, y in pick_up_list:
        lst.append(y)

    draw_cell(start[0], start[1], visualizer.START_CHECK_IMG)
    global total_path
    cur = pick_up_list[0][1]
    for i in range(1, len(pick_up_list)): 
        en = pick_up_list[i][1]

        if en in total_path: 
            continue
        st = cur
        path = GBFS(grid, rows, cols, st, en)

        if len(path) < 2: 
            return []
        path = path[1:]

        visualizer.draw_maze(grid, rows, cols)
        for x, y in total_path: 
            if ([x, y] == end): 
                visualizer.draw_cell_no_delay(x, y, visualizer.DOOR_OPEN)
            elif [x, y] == start: 
                visualizer.draw_cell_no_delay(x, y, visualizer.START_CHECK_IMG)
            elif ([x, y] in lst): 
                visualizer.draw_cell_no_delay(x, y, visualizer.STATION_CHECK_IMG)
            else:
                visualizer.draw_cell_no_delay(x, y, visualizer.PATH_IMG)
        for x, y in path: 
            if ([x, y] == end): 
                draw_cell(x, y, visualizer.DOOR_OPEN)
            elif ([x, y] == start): 
                draw_cell(x, y, visualizer.START_CHECK_IMG)
            elif ((x, y) == path[-1]): 
                draw_cell(x, y, visualizer.STATION_CHECK_IMG)
            elif ([x, y] in lst): 
                draw_cell(x, y, visualizer.STATION_CHECK_IMG)
            else:
                draw_cell(x, y, visualizer.PATH_IMG)
        total_path = total_path + path
        cur = en

    total_path.insert(0, start)
    draw_cell(total_path[-1][0], total_path[-1][1], visualizer.DOOR_OPEN)
    return total_path

# ---------------------------------

def main(maze_path):
    maze_data, gift_data, rows, cols = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    path = find_path(maze_data, gift_data, rows, cols)

    dir_name = generate_output_path(maze_path, "GBFS_station")
    cost_file = dir_name + "/GBFS_station.txt"
    writeToFile(cost_file, path, WIN=WIN, frames=frames)

    # --------------------------------
    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python gbfs_station.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
