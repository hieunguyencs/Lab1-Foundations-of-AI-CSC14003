import os

def writeToFile(file_name="output.txt", path=None, bonus=0):
    if path is None:
        return

    # Create the directory structure if it doesn't exist
    directory = os.path.dirname(file_name)
    # print(directory)
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
    base_directory = maze_path[:-4]
    tmp = base_directory.split("/")
    tmp = tmp[2:]
    base_directory = "/".join(tmp)

    # Construct the output directory path
    output_directory = os.path.join('..', 'output', base_directory, algorithm)

    # print(output_directory)

    return output_directory


