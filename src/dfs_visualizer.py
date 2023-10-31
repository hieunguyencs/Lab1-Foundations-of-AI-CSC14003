import pygame
import os
import sys
from WriteOutput import *

# GAME SETUP
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.HIDDEN)
pygame.display.set_caption("DFS")
FPS = 60
delay = 20
long_delay = 1000

# DEFINE COLOR
WHITE = (255, 255, 255)

# CONSTANTS
CELL_WIDTH, CELL_HEIGHT = 50, 50
dx = [-1, 0, 0, 1]
dy = [0, 1, -1, 0]
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
    pygame_screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
    bgr_frame = cv2.cvtColor(pygame_screenshot, cv2.COLOR_RGB2BGR)
    frames.append(bgr_frame)

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

    scale_img()

    global X_OFFSET, Y_OFFSET   
    X_OFFSET = (WIDTH - cols * CELL_WIDTH) // 2
    Y_OFFSET = (HEIGHT - rows * CELL_HEIGHT) // 2

    # Draw maze
    WIN.fill(WHITE)
    draw_maze(maze_data, rows, cols)
    pygame.display.update()
    pygame.time.delay(1000)

    return maze_data, gift_data, rows, cols

# --- WRITE GRAPH FUNCTION HERE ---
# You can call function draw_cell(x, y, IMG) to draw IMG at cell (x, y)

def DFS(a, rows, cols):
    vis = [[False for j in range(cols)] for i in range(rows)]
    trace = [[[-1, -1] for j in range(cols)] for i in range(rows)]

    for i in range(rows):
        for j in range(cols):
            if a[i][j] == 'S':
                start = [i, j]
            if a[i][j] != 'x' and (i == 0 or i == rows - 1 or j == 0 or j == cols - 1):
                end = [i, j]

    found = False

    def inGrid(x, y): 
        return x >= 0 and x < rows and y >= 0 and y < cols

    def recurse(x, y):
        nonlocal found
        if found:
            return  
        vis[x][y] = True
        for i in range(4):
            new_x = x + dx[i]
            new_y = y + dy[i]

            if (found): 
                return

            if inGrid(new_x, new_y) and not vis[new_x][new_y] and a[new_x][new_y] != 'x':
                trace[new_x][new_y] = [x, y]
                if [new_x, new_y] == end:
                    found = True
                    return  

                draw_cell(new_x, new_y, VISITED_IMG)
                recurse(new_x, new_y)

    recurse(start[0], start[1])


    path = []
    if (found):
        # Trace path
        X, Y = end
        while True: 
            if [X, Y] == [-1, -1]: 
                break    
            path.append([X, Y])
            X, Y = trace[X][Y]
        path.reverse()

    return path

def draw_path(path): 
    if len(path) == 0: 
        return
    pygame.time.delay(long_delay)
    draw_cell(path[0][0], path[0][1], START_CHECK_IMG)
    end = path[-1]
    path = path[1:-1]
    for u, v in path: 
        draw_cell(u, v, PATH_IMG)
    draw_cell(end[0], end[1], DOOR_OPEN)

# ---------------------------------

def main(maze_path):
    maze_data, gift_data, rows, cols = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    path = DFS(maze_data, rows, cols)
    draw_path(path)

    dir_name = generate_output_path(maze_path, "dfs")
    cost_file = dir_name + "/dfs.txt"
    writeToFile(cost_file, path, WIN=WIN, frames=frames)

    # --------------------------------

    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python dfs_visualizer.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
