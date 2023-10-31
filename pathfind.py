from maps import map
from display import displayMap

"""
Recursive function finding path to the end

args:
numCols (int) : Number of columns
numRows (int) : Number of rows
moveCount (int) : Number of moves allowed
map (2d array) : Map chicken attempts to solve
a (int) : Horizonatal (x) position of chicken
b (int) : Vertical (y) position of chicken

return:
solvable (int) : is the path solvable in the number of moves allowed. 1 is solveable
"""
#todo: rename variables
def path(numCols,numRows, moveCount, map, a, b):

    # Turn limit check
    if(moveCount <= 0):
        return 0

    # Out of bounds check
    if(a == numCols or a == -1 or b == numRows or b == -1):
        return 0
    
    # Obstacle check
    if(map[a][b] == 1):
        return 0
    
    # Chicken Reached End!
    if(b == numCols-1):
        return 1
    
    return path(numCols,numRows,moveCount-1, map, a+1, b) + path(numCols,numRows,moveCount-1, map, a-1, b) + path(numCols,numRows,moveCount-1, map, a, b + 1) + path(numCols,numRows,moveCount-1, map, a, b -1)
    
"""
Takes minimum inputs to pass to path function
Assumes chicken starts from [0, 2]

args:
n (int) : number of moves allowed
map (2d array) : Map chicken attempts to solve

return:
solvable (boolean) : is the path solvable in the number of moves allowed.
"""
def easyPath(moveCount, map):

    if(path(len(map), len(map[0]),moveCount, map, 2, 0) >= 1):
        return True
    
    return False


mapEx = [[0, 0, 1, 0, 1],
         [0, 0, 1, 0, 1],
         [0, 0, 0, 0, 1],
         [0, 0, 1, 0, 0],
         [1, 1, 1, 1, 1]]

#mapEx = map

displayMap(mapEx)

print(easyPath(11, mapEx))