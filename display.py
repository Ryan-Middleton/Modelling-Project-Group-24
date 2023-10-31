def displayMap(map):
    for row in map:
        for elem in row:
            print(" # " if elem else "[ ]", end = "")
        print("")