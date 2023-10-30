def writeToFile(file_name="output.txt", path=None):
    #Check if the path contains duplicated point?
    if path==None:
        return
    print(path)
    with open(file_name, 'w') as out:
        out.write(str(len(path)))
        out.write('\n')
        for point in path:
            out.write('({}, {}) '.format(point[0], point[1]))


