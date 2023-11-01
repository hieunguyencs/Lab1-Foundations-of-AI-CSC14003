from collections import deque
from WriteOutput import *
import visualizer
from visualizer import frames,draw_cell, load_maze, dx, dy, WIN, LONGDELAY
import sys

pygame.display.set_caption("BFS")

# --- WRITE GRAPH FUNCTION HERE ---
# You can call function draw_cell(x, y, IMG) to draw IMG at cell (x, y)

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

                draw_cell(new_x, new_y, visualizer.VISITED_IMG)
 
    return []

def draw_path(path):
    if len(path) == 0: 
        return

    pygame.time.delay(LONGDELAY)
    draw_cell(path[0][0], path[0][1], visualizer.START_CHECK_IMG)
    end = path[-1]
    path = path[1:-1]
    for x, y in path:
        draw_cell(x, y, visualizer.PATH_IMG)
    draw_cell(end[0], end[1], visualizer.DOOR_OPEN)
# ---------------------------------

def main(maze_path):
    maze_data, gift_data, rows, cols = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    path = bfs(maze_data, rows, cols)
    draw_path(path)

    dir_name = generate_output_path(maze_path, "bfs")
    cost_file = dir_name + "/bfs.txt"
    writeToFile(cost_file, path, WIN=WIN, frames=frames)

    # --------------------------------
    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python bfs.py <path>")
    maze_path = "../input/level_1/input3.txt"
    main(maze_path)
else:
    maze_path = sys.argv[1]
    main(maze_path)
