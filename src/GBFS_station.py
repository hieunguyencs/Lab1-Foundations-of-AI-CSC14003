import pygame
import os
import sys
from collections import deque
import heapq

# GAME SETUP
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BFS")
FPS = 60
delay = 20
long_delay = 1000

# DEFINE COLOR
WHITE = (255, 255, 255)

# CONSTANTS
CELL_WIDTH, CELL_HEIGHT = 50, 50
dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]
ROW, COL = 0, 0
X_OFFSET, Y_OFFSET = 0, 0

# INCLUDE IMAGE
START_IMG = pygame.image.load(os.path.join('..', 'Assets', 'start.jpg'))
END_IMG = pygame.image.load(os.path.join('..', 'Assets', 'door.jpg'))
GIFT_IMG = pygame.image.load(os.path.join('..', 'Assets', 'bus_stop.jpg'))
WALL_IMG = pygame.image.load(os.path.join('..', 'Assets', 'wall.jpg'))
VISITED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'visited.jpg'))
PATH_IMG = pygame.image.load(os.path.join('..', 'Assets', 'path.jpg'))
BUS_STOP_CHECK_IMG = pygame.image.load(os.path.join('..', 'Assets', 'bus_stop_checked.png'))
START_CHECK_IMG = pygame.image.load(os.path.join('..', 'Assets', 'start_checked.png'))

# SCALE IMAGE
def scale_img():
    global START_IMG, END_IMG, GIFT_IMG, WALL_IMG, VISITED_IMG, PATH_IMG, BUS_STOP_CHECK_IMG, START_CHECK_IMG
    START_IMG = pygame.transform.scale(START_IMG, (CELL_WIDTH, CELL_HEIGHT))
    END_IMG = pygame.transform.scale(END_IMG, (CELL_WIDTH, CELL_HEIGHT))
    GIFT_IMG = pygame.transform.scale(GIFT_IMG, (CELL_WIDTH, CELL_HEIGHT))
    WALL_IMG = pygame.transform.scale(WALL_IMG, (CELL_WIDTH, CELL_HEIGHT))
    VISITED_IMG = pygame.transform.scale(VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    PATH_IMG = pygame.transform.scale(PATH_IMG, (CELL_WIDTH, CELL_HEIGHT))
    BUS_STOP_CHECK_IMG = pygame.transform.scale(BUS_STOP_CHECK_IMG, (CELL_WIDTH, CELL_HEIGHT))
    START_CHECK_IMG = pygame.transform.scale(START_CHECK_IMG, (CELL_WIDTH, CELL_HEIGHT))

# DRAW METHOD
def draw_cell_no_delay(x, y, IMG): 
    drawX = X_OFFSET + y * CELL_WIDTH
    drawY = Y_OFFSET + x * CELL_HEIGHT
    WIN.blit(IMG, (drawX, drawY))

def draw_cell(x, y, IMG): 
    drawX = X_OFFSET + y * CELL_WIDTH
    drawY = Y_OFFSET + x * CELL_HEIGHT
    WIN.blit(IMG, (drawX, drawY))
    pygame.display.update()
    pygame.time.delay(delay)

def draw_maze(maze_data, rows, cols):
    WIN.fill(WHITE)
    for row in range(rows):
        for col in range(cols):
            cell = maze_data[row][col]
            if cell == 'x':
                draw_cell_no_delay(row, col, WALL_IMG)
            elif cell == 'S':
                draw_cell_no_delay(row, col, START_IMG)
            elif row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                draw_cell_no_delay(row, col, END_IMG)
            elif cell == '+': 
                draw_cell_no_delay(row, col, GIFT_IMG)
    pygame.display.update()

# LOAD MAZE GIVEN PATH
def load_maze(maze_path):
    # Set caption
    map_number = int(maze_path.split('/')[-1].replace('input', '').split('.')[0])
    cur_caption = pygame.display.get_caption()[0]
    new_caption = f"{cur_caption} - Map {map_number}"
    pygame.display.set_caption(new_caption)

    # Read maze
    maze_data = []
    gift_data = []
    with open(maze_path, 'r') as file:
        lines = file.read().splitlines()

        n = list(map(int, lines[0].split()))[0]
        for i in range(1, n + 1): 
            gift_data.append(list(map(int, lines[i].split())))

        for line in lines[n + 1:]:
            maze_data.append(list(line))

        rows = len(lines) - n - 1
        cols = len(lines[n + 1])

    # Set up sizes and position
    global CELL_WIDTH, CELL_HEIGHT
    if WIDTH / cols < HEIGHT / rows: 
        CELL_WIDTH = CELL_HEIGHT = (WIDTH) / (cols + 2)
    else: 
        CELL_WIDTH = CELL_HEIGHT = (HEIGHT) / (rows + 2)

    global X_OFFSET, Y_OFFSET   
    X_OFFSET = (WIDTH - cols * CELL_WIDTH) // 2
    Y_OFFSET = (HEIGHT - rows * CELL_HEIGHT) // 2

    scale_img()

    # Draw maze
    draw_maze(maze_data, rows, cols)
    pygame.time.delay(long_delay)

    return maze_data, gift_data, rows, cols

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

    while len(heap) > 0: 
        next = heapq.heappop(heap)
        picked_cell = next[1]
        value = next[0]

        if (picked_cell == end): 
            break

        closed[picked_cell[0]][picked_cell[1]] = 1

        if (picked_cell != start) and picked_cell not in total_path: 
            draw_cell(picked_cell[0], picked_cell[1], VISITED_IMG)

        for i in range(4): 
            next_x = picked_cell[0] + dx[i]
            next_y = picked_cell[1] + dy[i]

            if (inGrid(next_x, next_y)
                and grid[next_x][next_y] != 'x'
                and closed[next_x][next_y] == 0): 
                distance[next_x][next_y] = distance[picked_cell[0]][picked_cell[1]] + 1
                trace[next_x][next_y] = picked_cell
                heapq.heappush(heap, [h(next_x, next_y), [next_x, next_y]])

    return constructPath()

def find_path(grid, gift_data, rows, cols): 
    # find distance from end to all pickup cell
    distance = cnt_distance(grid, rows, cols)

    # draw maze again
    # pygame.time.delay(long_delay)
    # draw_maze(grid, rows, cols)
    # pygame.time.delay(long_delay)

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

    draw_cell(start[0], start[1], START_CHECK_IMG)
    global total_path
    cur = pick_up_list[0][1]
    for i in range(1, len(pick_up_list)): 
        en = pick_up_list[i][1]

        if en in total_path: 
            continue
        st = cur
        path = GBFS(grid, rows, cols, st, en)

        path = path[1:]

        draw_maze(grid, rows, cols)
        for x, y in total_path: 
            if ([x, y] == end): 
                draw_cell_no_delay(x, y, END_IMG)
            # elif [x, y] == start: 
            #     draw_cell_no_delay(x, y, START_CHECK_IMG)
            elif ([x, y] in lst): 
                draw_cell_no_delay(x, y, BUS_STOP_CHECK_IMG)
            else:
                draw_cell_no_delay(x, y, PATH_IMG)
        for x, y in path: 
            if ([x, y] == end): 
                draw_cell(x, y, END_IMG)
            elif ([x, y] in lst): 
                draw_cell(x, y, START_CHECK_IMG)
            elif ((x, y) == path[-1]): 
                draw_cell(x, y, BUS_STOP_CHECK_IMG)
            else:
                draw_cell(x, y, PATH_IMG)
        total_path = total_path + path

        cur = en

    return len(total_path)

# ---------------------------------

def main(maze_path):
    maze_data, gift_data, rows, cols = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    cost = find_path(maze_data, gift_data, rows, cols)

    # --------------------------------

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python bfs_visualizer.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
