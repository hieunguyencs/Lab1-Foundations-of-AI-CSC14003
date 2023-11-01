from collections import deque
import sys
from WriteOutput import *
import visualizer
from visualizer import frames,draw_cell, load_maze, dx, dy, WIN, LONGDELAY

pygame.display.set_caption("Teleporter: BFS")

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
                    draw_cell(new_x, new_y, visualizer.VISITED_IMG)

    return []

def draw_path(path, teleport_data):
    if len(path) == 0: 
        return
    pygame.time.delay(LONGDELAY)
    draw_cell(path[0][0], path[0][1], visualizer.START_CHECK_IMG)
    end=path[-1]
    path = path[1:-1]
    for x, y in path:
        is_teleport = False
        for teleport in teleport_data:
            x1, y1, x2, y2 = teleport
            if (x, y) == (x1, y1):
                is_teleport = True
                draw_cell(x, y, visualizer.TELEPORT_IN_VISITED_IMG)
                break
            if (x, y) == (x2, y2):
                is_teleport = True
                draw_cell(x, y, visualizer.TELEPORT_OUT_VISITED_IMG)
                break
        if not is_teleport:
            draw_cell(x, y, visualizer.PATH_IMG)
    draw_cell(end[0], end[1], visualizer.DOOR_OPEN)
# ---------------------------------

def main(maze_path):
    maze_data, teleport_data, rows, cols = load_maze(maze_path)

    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    # draw_path(maze_path, teleport_data, rows, cols)
    path = bfs(maze_data, teleport_data, rows, cols)
    draw_path(path, teleport_data)

    dir_name = generate_output_path(maze_path, "BFS_teleporter")
    cost_file = dir_name + "/teleporter.txt"

    count = 0
    for x,y in path:
        for teleport in teleport_data:
            x1,y1,x2,y2 = teleport
            if (x,y)==(x1,y1):
                count = count - 1

    writeToFile(cost_file, path, count, WIN, frames)


    # height, width, layers = frames[0].shape
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Định dạng video codec
    # out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (height, width))
    # rotated_frames = [cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) for frame in frames]
    # flipped_frames_horizontal = [cv2.flip(frame, 1) for frame in rotated_frames]
    # for frame in flipped_frames_horizontal:
    #     out.write(frame)
    # out.release()
    # --------------------------------
    pygame.quit()

if len(sys.argv) != 2:
    print("Usage: python bfs_teleportation.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)