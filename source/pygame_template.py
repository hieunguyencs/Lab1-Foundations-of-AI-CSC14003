from WriteOutput import *
import visualizer
from visualizer import frames,draw_cell, load_maze, dx, dy, WIN, LONGDELAY, FPS
import sys

pygame.display.set_caption("BFS")
# --- WRITE GRAPH FUNCTION HERE ---
# You can call function draw_cell(x, y, IMG) to draw IMG at cell (x, y)


# ---------------------------------

def main(maze_path):
    maze_data, gift_data, rows, cols = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)


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
    print("Usage: python algorithm.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
