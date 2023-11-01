import os

INPUT_ROOT = "../input/"


def main():
    solve(INPUT_ROOT + "level_1/")
    solve(INPUT_ROOT + "level_2/")
    solve(INPUT_ROOT + "level_3/")
    solve(INPUT_ROOT + "advance/")


def solve(prob_path):
    for f in os.listdir(prob_path):
        file_path = os.path.join(prob_path, f)
        if os.path.isfile(file_path):
            if "level_1" in prob_path:
                os.system(f"python bfs.py {file_path}")
                os.system(f"python dfs.py {file_path}")
                os.system(f"python astar_heuristic1.py {file_path}")
                os.system(f"python astar_heuristic2.py {file_path}")
                os.system(f"python gbfs_heuristic1.py {file_path}")
                os.system(f"python gbfs_heuristic2.py {file_path}")
                os.system(f"python ucs.py {file_path}")

            elif "level_2" in prob_path:
                os.system(f"python astar_greedy_gift.py {file_path}")
            elif "level_3" in prob_path:
                os.system(f"python gbfs_station.py {file_path}")
            elif "advance" in prob_path:
                os.system(f"python bfs_teleportation.py {file_path}")


if __name__ == "__main__":
    main()
