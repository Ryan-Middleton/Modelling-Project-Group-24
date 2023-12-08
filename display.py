def displayMap(map):
    """
    Prints a 2D map to the output stream.
    """

    for row in map:
        for elem in row:
            if elem == 0:
                print(" . ", end = "")
            elif elem == 1:
                print(" # ", end = "")
            else:
                print(" X ", end = "")
        print()
