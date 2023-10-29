from collections import deque

import pygame
import os
import sys

# GAME SETUP
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Teleport")
FPS = 60
delay = 30
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
WALL_IMG = pygame.image.load(os.path.join('..', 'Assets', 'wall.jpg'))
VISITED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'visited.jpg'))
TELEPORT_IN_IMG = pygame.image.load(os.path.join('..', 'Assets', 'teleport_in.png'))
TELEPORT_OUT_IMG = pygame.image.load(os.path.join('..', 'Assets', 'teleport_out.png'))
PATH_IMG = pygame.image.load(os.path.join('..', 'Assets', 'path.jpg'))
TELEPORT_IN_VISITED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'teleport_in_visited.png'))
TELEPORT_OUT_VISITED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'teleport_out_visited.png'))
START_CHECK_IMG = pygame.image.load(os.path.join('..', 'Assets', 'start_checked.png'))

# SCALE IMAGE
def scale_img():
    global START_IMG, END_IMG, WALL_IMG, VISITED_IMG, PATH_IMG, TELEPORT_IN_IMG, TELEPORT_OUT_IMG, TELEPORT_IN_VISITED_IMG, TELEPORT_OUT_VISITED_IMG, START_CHECK_IMG
    START_IMG = pygame.transform.scale(START_IMG, (CELL_WIDTH, CELL_HEIGHT))
    END_IMG = pygame.transform.scale(END_IMG, (CELL_WIDTH, CELL_HEIGHT))
    WALL_IMG = pygame.transform.scale(WALL_IMG, (CELL_WIDTH, CELL_HEIGHT))
    VISITED_IMG = pygame.transform.scale(VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_IN_IMG = pygame.transform.scale(TELEPORT_IN_IMG,(CELL_WIDTH,CELL_HEIGHT))
    TELEPORT_IN_VISITED_IMG = pygame.transform.scale(TELEPORT_IN_VISITED_IMG,(CELL_WIDTH,CELL_HEIGHT))
    TELEPORT_OUT_IMG = pygame.transform.scale(TELEPORT_OUT_IMG,(CELL_WIDTH,CELL_HEIGHT))
    TELEPORT_OUT_VISITED_IMG = pygame.transform.scale(TELEPORT_OUT_VISITED_IMG,(CELL_WIDTH,CELL_HEIGHT))
    PATH_IMG = pygame.transform.scale(PATH_IMG, (CELL_WIDTH, CELL_HEIGHT))
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
    for row in range(rows):
        for col in range(cols):
            cell = maze_data[row][col]
            if cell == 'x':
                draw_cell_no_delay(row, col, WALL_IMG)
            elif cell == 'S':
                draw_cell_no_delay(row, col, START_IMG)
            elif row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                draw_cell_no_delay(row, col, END_IMG)
            elif cell == 'o':
                draw_cell_no_delay(row, col, TELEPORT_IN_IMG)
            elif cell == 'O':
                draw_cell_no_delay(row, col, TELEPORT_OUT_IMG)

# LOAD MAZE GIVEN PATH
def load_maze(maze_path):
    # Set caption
    map_number = int(maze_path.split('/')[-1].replace('input', '').split('.')[0])
    cur_caption = pygame.display.get_caption()[0]
    new_caption = f"{cur_caption} - Map {map_number}"
    pygame.display.set_caption(new_caption)

    # Read maze
    maze_data = []
    teleport_data = []
    with open(maze_path, 'r') as file:
        lines = file.read().splitlines()

        n = list(map(int, lines[0].split()))[0]
        for i in range(1, n + 1):
            teleport_data.append(list(map(int, lines[i].split())))

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

    return maze_data, teleport_data, rows, cols

# --- WRITE GRAPH FUNCTION HERE ---
# You can call function draw_cell(x, y, IMG) to draw IMG at cell (x, y)

def bfs(grid, teleport_data, rows, cols):
    start_x, start_y = None, None
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 'S':
                start_x, start_y = i, j
                break
        if start_x is not None:
            break
    if start_x is None:
        return []

    visited = [[False for _ in range(cols)] for _ in range(rows)]
    trace = [[(0, 0) for _ in range(cols)] for _ in range(rows)]
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
                #queue.append((new_x, new_y))
                visited[new_x][new_y] = True
                trace[new_x][new_y] = (x, y)

                if grid[new_x][new_y] == 'o':
                    for teleport in teleport_data:
                        x1, y1, x2, y2 = teleport
                        if (new_x, new_y) == (x1, y1):
                            queue.append((x2, y2))
                            visited[x2][y2] = True
                            trace[x2][y2] = (new_x, new_y)
                    continue
                queue.append((new_x, new_y))

                if new_x == 0 or new_x == rows - 1 or new_y == 0 or new_y == cols - 1:
                    path = []
                    while new_x != start_x or new_y != start_y:
                        path.append((new_x, new_y))
                        new_x, new_y = trace[new_x][new_y]
                    path.append((start_x, start_y))
                    path.reverse()
                    return path
                if grid[new_x][new_y] != 'o' and grid[new_x][new_y] != 'O':
                    draw_cell(new_x, new_y, VISITED_IMG)

    return []

def draw_path(path, teleport_data):
    pygame.time.delay(1000)
    draw_cell(path[0][0], path[0][1], START_CHECK_IMG)
    path = path[1:-1]
    for x, y in path:
        is_teleport = False
        for teleport in teleport_data:
            x1, y1, x2, y2 = teleport
            if (x, y) == (x1, y1):
                is_teleport = True
                draw_cell(x, y, TELEPORT_IN_VISITED_IMG)
                break
            if (x, y) == (x2, y2):
                is_teleport = True
                draw_cell(x, y, TELEPORT_OUT_VISITED_IMG)
                break
        if not is_teleport:
            draw_cell(x, y, PATH_IMG)
# ---------------------------------

def main(maze_path):
    maze_data, teleport_data, rows, cols = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    # draw_path(maze_path, teleport_data, rows, cols)
    path = bfs(maze_data, teleport_data, rows, cols)
    draw_path(path, teleport_data)

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
    print("Usage: python teleport_visualizer.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)