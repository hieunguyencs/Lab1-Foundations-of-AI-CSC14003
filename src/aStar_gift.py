import pygame
import os
import sys
import heapq
import math

# GAME SETUP
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A*")
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
START_IMG = pygame.image.load(os.path.join('..','Assets', 'start.jpg'))
END_IMG = pygame.image.load(os.path.join('..','Assets', 'door.jpg'))
WALL_IMG = pygame.image.load(os.path.join('..','Assets', 'wall.jpg'))
VISITED_IMG = pygame.image.load(os.path.join('..','Assets', 'visited.jpg'))
TELEPORT_IN_IMG = pygame.image.load(os.path.join('..','Assets', 'teleport_in.png'))
TELEPORT_OUT_IMG = pygame.image.load(os.path.join('..','Assets', 'teleport_out.png'))
PATH_IMG = pygame.image.load(os.path.join('..','Assets', 'path.jpg'))
TELEPORT_IN_VISITED_IMG = pygame.image.load(os.path.join('..','Assets', 'teleport_in_visited.png'))
TELEPORT_OUT_VISITED_IMG = pygame.image.load(os.path.join('..','Assets', 'teleport_out_visited.png'))
START_IMG = pygame.image.load(os.path.join('..','Assets', 'start.jpg'))
GIFT_CHECKED_IMG = pygame.image.load(os.path.join('..','Assets', 'gift_checked.png'))
GIFT_IMG = pygame.image.load(os.path.join('..','Assets', 'gift.jpg'))
START_CHECKED_IMG = pygame.image.load(os.path.join('..','Assets', 'start_checked.png'))
BUS_STOP_CHECK_IMG = pygame.image.load(os.path.join('..','Assets', 'bus_stop_checked.png'))
DOOR_OPEN = pygame.image.load(os.path.join('..','Assets', 'door_checked.png'))

# SCALE IMAGE
def scale_img():
    global START_IMG, END_IMG, WALL_IMG, VISITED_IMG, PATH_IMG, TELEPORT_IN_IMG, TELEPORT_OUT_IMG, TELEPORT_IN_VISITED_IMG, TELEPORT_OUT_VISITED_IMG, GIFT_CHECKED_IMG, START_CHECKED_IMG, GIFT_IMG, BUS_STOP_CHECK_IMG, DOOR_OPEN
    START_IMG = pygame.transform.scale(START_IMG, (CELL_WIDTH, CELL_HEIGHT))
    END_IMG = pygame.transform.scale(END_IMG, (CELL_WIDTH, CELL_HEIGHT))
    WALL_IMG = pygame.transform.scale(WALL_IMG, (CELL_WIDTH, CELL_HEIGHT))
    VISITED_IMG = pygame.transform.scale(VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_IN_IMG = pygame.transform.scale(TELEPORT_IN_IMG, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_IN_VISITED_IMG = pygame.transform.scale(TELEPORT_IN_VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_OUT_IMG = pygame.transform.scale(TELEPORT_OUT_IMG, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_OUT_VISITED_IMG = pygame.transform.scale(TELEPORT_OUT_VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    PATH_IMG = pygame.transform.scale(PATH_IMG, (CELL_WIDTH, CELL_HEIGHT))
    GIFT_CHECKED_IMG = pygame.transform.scale(GIFT_CHECKED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    START_CHECKED_IMG = pygame.transform.scale(START_CHECKED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    GIFT_IMG = pygame.transform.scale(GIFT_IMG, (CELL_WIDTH, CELL_HEIGHT))
    BUS_STOP_CHECK_IMG = pygame.transform.scale(BUS_STOP_CHECK_IMG, (CELL_WIDTH, CELL_HEIGHT))
    DOOR_OPEN = pygame.transform.scale(DOOR_OPEN, (CELL_WIDTH, CELL_HEIGHT))
# SCALE IMAGE


# DRAW METHOD
def draw_cell_no_delay(x, y, IMG):
    drawX = X_OFFSET + y * CELL_WIDTH
    drawY = Y_OFFSET + x * CELL_HEIGHT
    WIN.blit(IMG, (drawX, drawY))


def draw_cell(x, y, IMG, start=None, gifts=None, stops=None, tele_in=None, tele_out=None, door=None):
    drawX = X_OFFSET + y * CELL_WIDTH
    drawY = Y_OFFSET + x * CELL_HEIGHT
    if tele_in!= None and x == tele_in[0] and y == tele_in[1]:
        IMG = TELEPORT_IN_IMG
    if tele_out!= None and x == tele_out[0] and y == tele_out[1]:
        IMG = TELEPORT_OUT_IMG
    if gifts != None:
        for gift in gifts:
            if x == gift[0] and y == gift[1]:
                IMG = GIFT_CHECKED_IMG
                break
    if stops != None:
        for stop in stops:
            if x == stop[0] and y == stop[1]:
                IMG = BUS_STOP_CHECK_IMG
                break
    if start!= None and x == start[0] and y == start[1]:
        IMG = START_CHECKED_IMG
    if door!= None and x == door[0] and y == door[1]:
        IMG = DOOR_OPEN

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


def aStarForGiftProb(grid, num_row, num_col, begin, start, end, gifts):
    MAX_DIS = 1_000_000_000
    distance = [[MAX_DIS for i in range(num_col)] for i in range(num_row)]
    trace = [[[-1, -1] for i in range(num_col)] for i in range(num_row)]
    open = [[0 for i in range(num_col)] for i in range(num_row)]
    heap = []  # this is for getting min f = g + h

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

    distance[begin[0]][begin[1]] = 0
    heapq.heappush(heap, [h(begin[0], begin[1]), begin])
    open[begin[0]][begin[1]] = True

    while len(heap) > 0:
        cur = heapq.heappop(heap)
        cur_cell = cur[1]

        if (cur_cell == end):
            return constructPath()

        #if cur_cell != begin:
        draw_cell(cur_cell[0], cur_cell[1], VISITED_IMG, start=start, gifts=gifts, door=end)

        open[cur_cell[0]][cur_cell[1]] = False
        for i in range(4):
            newX = cur_cell[0] + dx[i]
            newY = cur_cell[1] + dy[i]

            if not inGrid(newX, newY) or grid[newX][newY] == 'x':
                continue

            proposal_gScore = distance[cur_cell[0]][cur_cell[1]] + 1;
            if (proposal_gScore < distance[newX][newY]):
                distance[newX][newY] = proposal_gScore
                fScore = proposal_gScore + h(newX, newY)
                trace[newX][newY] = cur_cell
                if not open[newX][newY]:
                    heapq.heappush(heap, [fScore, [newX, newY]])

    return []


def draw_path(path, start=None, gifts=None, stops=None, tele_in=None, tele_out=None, door=None):
    pygame.time.delay(long_delay)
    for x, y in path:
        draw_cell(x, y, PATH_IMG, start=start, gifts=gifts, stops=stops, tele_in=tele_in, tele_out=tele_out, door=door)


# ---------------------------------

def main(maze_path):
    maze_data, gift_data, rows, cols = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    gifts_sort = sorted(gift_data, key=lambda point: point[2])
    start = find_start(maze_data, rows, cols)
    save_start = start
    end = find_end(maze_data, rows, cols)
    path = []
    for i in range(len(gifts_sort)):
        gift = [gifts_sort[i][0], gifts_sort[i][1]]
        path += aStarForGiftProb(maze_data, rows, cols, begin=start, start=save_start, end=gift, gifts=gift_data)
        # draw_path(path)
        draw_cell(gifts_sort[i][0], gifts_sort[i][1], GIFT_CHECKED_IMG, gifts=gift_data, start=save_start, door=end)
        start = gift
    path += aStarForGiftProb(maze_data, rows, cols, begin=start, start=save_start, end=end, gifts=gift_data)
    draw_path(path, gifts=gifts_sort, start=save_start, door=end)

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
