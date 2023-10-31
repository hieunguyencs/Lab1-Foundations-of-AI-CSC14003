import pygame
import os
import sys
import heapq
import math
from WriteOutput import *

# GAME SETUP
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.HIDDEN)
pygame.display.set_caption("GBFS - Euclidean distance heuristic")
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
GIFT_IMG = pygame.image.load(os.path.join('..', 'Assets', 'gift.jpg'))
WALL_IMG = pygame.image.load(os.path.join('..', 'Assets', 'wall.jpg'))
VISITED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'visited.jpg'))
PATH_IMG = pygame.image.load(os.path.join('..', 'Assets', 'path.jpg'))
START_CHECK_IMG = pygame.image.load(os.path.join('..', 'Assets', 'start_checked.png'))
DOOR_OPEN = pygame.image.load(os.path.join('..','Assets', 'door_checked.png'))

frames = []
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
    pygame_screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
    bgr_frame = cv2.cvtColor(pygame_screenshot, cv2.COLOR_RGB2BGR)
    frames.append(bgr_frame)

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
    pygame_screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
    bgr_frame = cv2.cvtColor(pygame_screenshot, cv2.COLOR_RGB2BGR)
    frames.append(bgr_frame)

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
    pygame.time.delay(long_delay)

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
            draw_cell(picked_cell[0], picked_cell[1], VISITED_IMG)

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
            pygame.time.delay(long_delay)
            draw_cell(path[0][0], path[0][1], START_CHECK_IMG)
            end = path[-1]
            path = path[1:-1]
            for x, y in path: 
                draw_cell(x, y, PATH_IMG)
            draw_cell(end[0], end[1], DOOR_OPEN)

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
    print("Usage: python GBFS_heuristic2_visualizer.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
