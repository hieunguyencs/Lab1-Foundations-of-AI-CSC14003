def writeToFile(file_name="output.txt", path=None, bonus=0):
    if path==None:
        return
    print("Check path again:\n", path)
    with open(file_name, 'w') as out:
        leng = len(path)
        if leng == 0:
            out.write("NO")
            return
        out.write(str(leng - 1 + bonus))
        #write path
        #out.write('\n')
        #for point in path:
        #    out.write('({}, {}) '.format(point[0], point[1]))


def checkDuplicatePointInPath(path):
    s = set()
    for point in path:
        p_tuple = tuple(point)
        if p_tuple in s:
            return True
        s.add(p_tuple)
    return False

