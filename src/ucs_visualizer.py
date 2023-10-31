import pygame
import os
import sys
import heapq
from WriteOutput import *

# GAME SETUP
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UCS")
FPS = 60
delay = 30

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
GIFT_IMG = pygame.image.load(os.path.join('..', 'Assets', 'gift.jpg'))
WALL_IMG = pygame.image.load(os.path.join('..', 'Assets', 'wall.jpg'))
VISITED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'visited.jpg'))
PATH_IMG = pygame.image.load(os.path.join('..', 'Assets', 'path.jpg'))
START_CHECK_IMG = pygame.image.load(os.path.join('..', 'Assets', 'start_checked.png'))
DOOR_OPEN = pygame.image.load(os.path.join('..','Assets', 'door_checked.png'))


# SCALE IMAGE
def scale_img():
    global START_IMG, END_IMG, GIFT_IMG, WALL_IMG, VISITED_IMG, PATH_IMG, START_CHECK_IMG, DOOR_OPEN
    START_IMG = pygame.transform.scale(START_IMG, (CELL_WIDTH, CELL_HEIGHT))
    END_IMG = pygame.transform.scale(END_IMG, (CELL_WIDTH, CELL_HEIGHT))
    GIFT_IMG = pygame.transform.scale(GIFT_IMG, (CELL_WIDTH, CELL_HEIGHT))
    WALL_IMG = pygame.transform.scale(WALL_IMG, (CELL_WIDTH, CELL_HEIGHT))
    VISITED_IMG = pygame.transform.scale(VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    PATH_IMG = pygame.transform.scale(PATH_IMG, (CELL_WIDTH, CELL_HEIGHT))
    START_CHECK_IMG = pygame.transform.scale(START_CHECK_IMG, (CELL_WIDTH, CELL_HEIGHT))
    DOOR_OPEN = pygame.transform.scale(DOOR_OPEN, (CELL_WIDTH, CELL_HEIGHT))

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
    WIN.fill(WHITE)
    draw_maze(maze_data, rows, cols)
    pygame.display.update()
    pygame.time.delay(1000)

    return maze_data, gift_data, rows, cols

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
                        draw_cell(newX, newY, VISITED_IMG)

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
    pygame.time.delay(1000)
    draw_cell(path[0][0], path[0][1], START_CHECK_IMG)
    end = path[-1]
    path = path[1:-1]
    for x, y in path: 
        draw_cell(x, y, PATH_IMG)
    draw_cell(end[0], end[1], DOOR_OPEN)

# ---------------------------------

def main(maze_path):
    maze_data, gift_data, num_row, num_col = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    path = ucs(maze_data, num_row, num_col)
    draw_path(path)

    dir_name = generate_output_path(maze_path, "UCS")
    cost_file = dir_name + "/UCS.txt"
    writeToFile(cost_file, path, WIN=WIN)

    # --------------------------------
    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python ucs_visualizer.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)