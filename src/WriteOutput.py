import os

def writeToFile(file_name="output.txt", path=None, bonus=0):
    if path is None:
        return

    # Create the directory structure if it doesn't exist
    directory = os.path.dirname(file_name)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(file_name, 'w') as out:
        leng = len(path)
        if leng == 0:
            out.write("NO")
            return
        out.write(str(leng - 1 + bonus))
        # Write path if needed
        # out.write('\n')
        # for point in path:
        #     out.write('({}, {}) '.format(point[0], point[1]))

def checkDuplicatePointInPath(path):
    s = set()
    for point in path:
        p_tuple = tuple(point)
        if p_tuple in s:
            return True
        s.add(p_tuple)
    return False

def generate_output_path(maze_path, algorithm):
    # Extract the directory of the input maze path
    directory = os.path.dirname(maze_path)

    # Extract the level number from the directory name
    level = os.path.basename(directory)

    # Construct the output directory path
    output_directory = os.path.join('..', 'output', level, algorithm)

    return output_directory

