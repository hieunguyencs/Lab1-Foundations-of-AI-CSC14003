import os

INPUT_ROOT = "../input/"
def main():
    os.system(f"cmd /c python bfs_visualizer.py ../input/level_1/input1.txt")
    os.system(f"cmd /c python dfs_visualizer.py ../input/level_1/input1.txt")
    solve(INPUT_ROOT + "level_1/")
    solve(INPUT_ROOT + "level_2/")
    solve(INPUT_ROOT + "level_3/")
    solve(INPUT_ROOT + "advance/")

def solve(prob_path):
    for f in os.listdir(prob_path):
        file_path = os.path.join(prob_path, f)
        if os.path.isfile(file_path):
            if "level_1" in prob_path:
                os.system(f"cmd /c python bfs_visualizer.py {file_path}")
                os.system(f"cmd /c python dfs_visualizer.py {file_path}")
                os.system(f"cmd /c python aStar_heuristic1_visualizer.py {file_path}")
                os.system(f"cmd /c python aStar_heuristic2_visualizer.py {file_path}")
                os.system(f"cmd /c python GBFS_heuristic1_visualizer.py {file_path}")
                os.system(f"cmd /c python GBFS_heuristic2_visualizer.py {file_path}")
                os.system(f"cmd /c python ucs_visualizer.py {file_path}")

            elif "level_2" in prob_path:
                os.system(f"cmd /c python gift_aStar.py {file_path}")
            elif "level_3" in prob_path:
                os.system(f"cmd /c python GBFS_station.py {file_path}")
            elif "advance" in prob_path:
                os.system(f"cmd /c python teleport_visualizer.py {file_path}")

if __name__ == "__main__":
    main()