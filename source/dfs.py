import sys
from WriteOutput import *
import visualizer
from visualizer import frames,draw_cell, load_maze, dx, dy, WIN, LONGDELAY

pygame.display.set_caption("DFS")

# --- WRITE GRAPH FUNCTION HERE ---
# You can call function draw_cell(x, y, IMG) to draw IMG at cell (x, y)

def DFS(a, rows, cols):
    start = [-1, -1]
    end = [-1, -1]
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

                draw_cell(new_x, new_y, visualizer.VISITED_IMG)
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
    pygame.time.delay(LONGDELAY)
    draw_cell(path[0][0], path[0][1], visualizer.START_CHECK_IMG)
    end = path[-1]
    path = path[1:-1]
    for u, v in path:
        draw_cell(u, v, visualizer.PATH_IMG)
    draw_cell(end[0], end[1], visualizer.DOOR_OPEN)

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
    print("Usage: python dfs.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
