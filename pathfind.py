import maps

"""
Recursive function finding path to the end

args:
x (int) : Number of columns
y (int) : Number of rows
n (int) : Number of moves allowed
m (int) : Number of moves already taken
map (2d array) : Map chicken attempts to solve
a (int) : Horizonatal (x) position of chicken
b (int) : Vertical (y) position of chicken

return:
solvable (int) : is the path solvable in the number of moves allowed. 1 is solveable
"""
def path(x, y, n, m, map, a, b):

    # Turn limit check
    if(m > n):
        return 0

    # Out of bounds check
    if(a == x or a == -1 or b == y or b == -1):
        return 0
    
    # Obstacle check
    if(map[a][b] == 1):
        return 0
    
    # Chicken Reached End!
    if(a == x-1):
        return 1
    
    return path(x, y, n, m+1, map, a+1, b) + path(x, y, n, m+1, map, a-1, b) + path(x, y, n, m+1, map, a, b + 1) + path(x, y, n, m+1, map, a, b -1)
    
"""
Takes minimum inputs to pass to path function
Assumes chicken starts from [0, 2]

args:
n (int) : number of moves allowed
map (2d array) : Map chicken attempts to solve

return:
solvable (boolean) : is the path solvable in the number of moves allowed.
"""
def easyPath(n, map):

    if(path(len(map), len(map[0]), n, 0, map, 0, 2) >= 1):
        return True
    
    return False


mapEx = [[0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0]]

print(easyPath(11, mapEx))