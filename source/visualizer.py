import os
import cv2
import pygame

# GAME SETUP
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.HIDDEN)
FPS = 60
DELAY = 20
LONGDELAY = 1000

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
PATH_IMG = pygame.image.load(os.path.join('..', 'Assets', 'path.jpg'))
START_CHECK_IMG = pygame.image.load(os.path.join('..', 'Assets', 'start_checked.png'))
DOOR_OPEN = pygame.image.load(os.path.join('..', 'Assets', 'door_checked.png'))
TELEPORT_IN_IMG = pygame.image.load(os.path.join('..', 'Assets', 'teleport_in.png'))
TELEPORT_OUT_IMG = pygame.image.load(os.path.join('..', 'Assets', 'teleport_out.png'))
TELEPORT_IN_VISITED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'teleport_in_visited.png'))
TELEPORT_OUT_VISITED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'teleport_out_visited.png'))
STATION_CHECK_IMG = pygame.image.load(os.path.join('..', 'Assets', 'bus_stop_checked.png'))
GIFT_IMG = pygame.image.load(os.path.join('..', 'Assets', 'gift.jpg'))
GIFT_CHECKED_IMG = pygame.image.load(os.path.join('..', 'Assets', 'gift_checked.png'))


def scale_img(CELL_WIDTH, CELL_HEIGHT):
    # Scale all icons to fit with the pygame's map

    global START_IMG, END_IMG, GIFT_IMG, GIFT_CHECKED_IMG, WALL_IMG, VISITED_IMG, PATH_IMG, START_CHECK_IMG, DOOR_OPEN
    global TELEPORT_IN_IMG, TELEPORT_IN_VISITED_IMG, TELEPORT_OUT_IMG, TELEPORT_OUT_VISITED_IMG, STATION_CHECK_IMG
    START_IMG = pygame.transform.scale(START_IMG, (CELL_WIDTH, CELL_HEIGHT))
    END_IMG = pygame.transform.scale(END_IMG, (CELL_WIDTH, CELL_HEIGHT))
    GIFT_IMG = pygame.transform.scale(GIFT_IMG, (CELL_WIDTH, CELL_HEIGHT))
    WALL_IMG = pygame.transform.scale(WALL_IMG, (CELL_WIDTH, CELL_HEIGHT))
    VISITED_IMG = pygame.transform.scale(VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    PATH_IMG = pygame.transform.scale(PATH_IMG, (CELL_WIDTH, CELL_HEIGHT))
    START_CHECK_IMG = pygame.transform.scale(START_CHECK_IMG, (CELL_WIDTH, CELL_HEIGHT))
    DOOR_OPEN = pygame.transform.scale(DOOR_OPEN, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_IN_IMG = pygame.transform.scale(TELEPORT_IN_IMG, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_IN_VISITED_IMG = pygame.transform.scale(TELEPORT_IN_VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_OUT_IMG = pygame.transform.scale(TELEPORT_OUT_IMG, (CELL_WIDTH, CELL_HEIGHT))
    TELEPORT_OUT_VISITED_IMG = pygame.transform.scale(TELEPORT_OUT_VISITED_IMG, (CELL_WIDTH, CELL_HEIGHT))
    STATION_CHECK_IMG = pygame.transform.scale(STATION_CHECK_IMG, (CELL_WIDTH, CELL_HEIGHT))
    GIFT_IMG = pygame.transform.scale(GIFT_IMG, (CELL_WIDTH, CELL_HEIGHT))
    GIFT_CHECKED_IMG = pygame.transform.scale(GIFT_CHECKED_IMG, (CELL_WIDTH, CELL_HEIGHT))

frames = []


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
    pygame.time.delay(DELAY)
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
            elif cell == 'o':
                draw_cell_no_delay(row, col, TELEPORT_IN_IMG)
            elif cell == 'O':
                draw_cell_no_delay(row, col, TELEPORT_OUT_IMG)
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
        CELL_WIDTH = CELL_HEIGHT = WIDTH / (cols + 2)
    else:
        CELL_WIDTH = CELL_HEIGHT = HEIGHT / (rows + 2)

    global X_OFFSET, Y_OFFSET
    X_OFFSET = (WIDTH - cols * CELL_WIDTH) // 2
    Y_OFFSET = (HEIGHT - rows * CELL_HEIGHT) // 2

    scale_img(CELL_WIDTH, CELL_HEIGHT)

    # Draw maze
    WIN.fill(WHITE)
    draw_maze(maze_data, rows, cols)
    pygame.display.update()
    pygame.time.delay(LONGDELAY)

    return maze_data, gift_data, rows, cols
