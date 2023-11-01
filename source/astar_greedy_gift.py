import sys
import heapq
from WriteOutput import *
import visualizer
from visualizer import frames,draw_cell, load_maze, dx, dy, WIN, LONGDELAY

pygame.display.set_caption("Gift: A* - Greedy")

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


def aStarForGiftProb(grid, num_row, num_col, begin, end):
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
        draw_cell(cur_cell[0], cur_cell[1], visualizer.VISITED_IMG)

        open[cur_cell[0]][cur_cell[1]] = False
        for i in range(4):
            newX = cur_cell[0] + dx[i]
            newY = cur_cell[1] + dy[i]

            if not inGrid(newX, newY) or grid[newX][newY] == 'x':
                continue

            proposal_gScore = distance[cur_cell[0]][cur_cell[1]] + 1
            if (proposal_gScore < distance[newX][newY]):
                distance[newX][newY] = proposal_gScore
                fScore = proposal_gScore + h(newX, newY)
                trace[newX][newY] = cur_cell
                if not open[newX][newY]:
                    heapq.heappush(heap, [fScore, [newX, newY]])

    return []


def draw_path(path, start=None, gifts=None, door=None):
    pygame.time.delay(LONGDELAY)
    for x, y in path:
        if [x, y] == start:
            draw_cell(x, y, visualizer.START_CHECK_IMG)
            continue
        if [x, y] == door:
            draw_cell(x, y, visualizer.DOOR_OPEN)
            continue
        flag = False
        for gift in gifts:
            if x == gift[0] and y == gift[1]:
                draw_cell(x, y, visualizer.GIFT_CHECKED_IMG)
                flag = True
                break
        if not flag:
            draw_cell(x, y, visualizer.PATH_IMG)

# ---------------------------------

def main(maze_path):
    maze_data, gift_datas, rows, cols = load_maze(maze_path)

    sumGifts = 0
    for i in gift_datas:
        sumGifts+=i[2]
    # --- CALL GRAPH FUNCTION HERE ---
    # Ex: DFS(maze_data, gift_data, rows, cols)
    gifts_sort = sorted(gift_datas, key=lambda point: point[2])
    start = find_start(maze_data, rows, cols)
    save_start = start
    end = find_end(maze_data, rows, cols)
    path = []
    for i in range(len(gifts_sort)):
        gift = [gifts_sort[i][0], gifts_sort[i][1]]
        subPath = aStarForGiftProb(maze_data, rows, cols, begin=start, end=gift)
        if subPath is None or len(subPath)==0:
            path=[]
            break
        path += subPath
        start = gift
    lastPath = aStarForGiftProb(maze_data, rows, cols, begin=start, end=end)
    if lastPath is None or len(lastPath) == 0:
        path = []
    else:
        path += lastPath
    draw_path(path, gifts=gifts_sort, start=save_start, door=end)
    dir_name = generate_output_path(maze_path, "AStar-Greedy_gift")
    cost_file = dir_name + "/AStar-Greedy_gift.txt"
    writeToFile(file_name=cost_file, path=path, bonus=sumGifts, WIN=WIN,frames=frames)

    # --------------------------------

    pygame.quit()


if len(sys.argv) != 2:
    print("Usage: python astar_greedy_gift.py <path>")
else:
    maze_path = sys.argv[1]
    main(maze_path)
