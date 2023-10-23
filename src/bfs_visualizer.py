import pygame
import os
import sys
from collections import deque

# GAME SETUP
WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BFS")
FPS = 60
delay = 30


# DEFINE COLOR
WHITE = (255, 255, 255)


# Constants
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

# SCALE IMG
START_IMG = pygame.transform.scale(START_IMG, (CELL_WIDTH, CELL_HEIGHT))
END_IMG = pygame.transform.scale(END_IMG, (CELL_WIDTH, CELL_HEIGHT))
GIFT_IMG = pygame.transform.scale(GIFT_IMG, (CELL_WIDTH, CELL_HEIGHT))
WALL_IMG = pygame.transform.scale(WALL_IMG, (CELL_WIDTH, CELL_HEIGHT))
VISITED_IMG = pygame.transform.scale(VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
PATH_IMG = pygame.transform.scale(PATH_IMG, (CELL_WIDTH, CELL_HEIGHT))

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

def load_maze(maze_path):
    maze_data = []
    gift_data = []
    with open(maze_path, 'r') as file:
        lines = file.read().splitlines()
        # The first line is the number of rows (ignore it)

        n = int(list(lines[0])[0])
        for i in range(1, n + 1): 
            gift_data.append(list(lines[i]))

        for line in lines[n + 1:]:
            maze_data.append(list(line))

        rows = len(lines) - n - 1
        cols = len(lines[n + 1])

    return maze_data, rows, cols

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

def bfs(grid, rows, cols): 
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
                queue.append((new_x, new_y))
                visited[new_x][new_y] = True
                trace[new_x][new_y] = (x, y)

                if new_x == 0 or new_x == rows - 1 or new_y == 0 or new_y == cols - 1:
                    path = []
                    while new_x != start_x or new_y != start_y:
                        path.append((new_x, new_y))
                        new_x, new_y = trace[new_x][new_y]
                    path.append((start_x, start_y))
                    path.reverse()
                    return path
                
                draw_cell(new_x, new_y, VISITED_IMG)
 
    return []

def draw_path(grid, rows, cols):
    path = bfs(grid, rows, cols)
    path = path[1:-1]

    pygame.time.delay(1000)
    for x, y in path:
        draw_cell(x, y, PATH_IMG)

def main(maze_path):
    maze_data, rows, cols = load_maze(maze_path)
    
    global X_OFFSET, Y_OFFSET   
    X_OFFSET = (WIDTH - cols * CELL_WIDTH) // 2
    Y_OFFSET = (HEIGHT - rows * CELL_HEIGHT) // 2

    WIN.fill(WHITE)
    draw_maze(maze_data, rows, cols)
    pygame.display.update()
    pygame.time.delay(1000)

    draw_path(maze_data, rows, cols)

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
