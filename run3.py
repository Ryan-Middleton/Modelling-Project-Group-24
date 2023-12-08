# Imports.
import copy
import secrets
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from classes import *

# from nnf import config
# config.sat_backend = "kissat"

# Encoding E will store all constraints and propositions.
global objectList
E = Encoding()
MAP_SIZE = 3
TURN_LIMIT = 99
objectList = []

"""
# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"


# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"

# Call your variables whatever you want
a = BasicPropositions("a")
b = BasicPropositions("b")   
c = BasicPropositions("c")
d = BasicPropositions("d")
e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")
"""

@constraint.exactly_one(E)
@proposition(E)
class chickenProposition:

    # Stored as length 3 array
    # Index 0: x coordinate
    # Index 1: y coordinate
    # Index 2: Turn/time

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"C.{self.data}"
    
    def get_x(self):
        return self.data[0]
    
    def get_y(self):
        return self.data[1]

    def moveUp(self):
        self.data[1] = self.data[1] - 1
        self.data[2] = self.data[2] + 1
        return self

    def moveDown(self):
        self.data[1] = self.data[1] + 1
        self.data[2] = self.data[2] + 1
        return self
    
    def moveRight(self):
        self.data[0] = self.data[0] + 1
        self.data[2] = self.data[2] + 1
        return self
    
    def moveLeft(self):
        self.data[0] = self.data[0] - 1
        self.data[2] = self.data[2] + 1
        return self
    
    def moveNone(self):
        self.data[2] = self.data[2] + 1
        return self
    
    def type(self):
        return "C"
    
    def toStr(self):
        print(self.data)

    
@proposition(E)
class stationaryObjectProposition:

    #Stored as length 2 array
    # Index 0: x coordinate
    # Index 1: y coordinate

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"S.{self.data}"
    
    def type(self):
        return "S"
    
    def toStr(self):
        print(self.data)

@proposition(E)
class UnoccupiedProposition:

    #Stored as length 2 array
    # Index 0: x coordinate
    # Index 1: y coordinate

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"U.{self.data}"
    
    def type(self):
        return "U"
    
    def toStr(self):
        print(self.data)

def checkValid(C,M):

    # Check Within arraybounds, colliding with moving object, within time bounds
    if(not (C.data[0] >= 0 and C.data[1] >= 0 and C.data[0] < MAP_SIZE and C.data[1] < MAP_SIZE and C.data[2] < TURN_LIMIT 
            and M.data[2] < TURN_LIMIT and C.data != M.data)):
        return False

    # Check coliding with stationary object
    for x in range(len(objectList)):
        if(objectList[x].type() == "S"):
            if( C.data[0] == objectList[x].data[0] and C.data[1] == objectList[x].data[1] ):
                return False
    
    # Otherise true
    return True

# Builds map with object types, filling vacant spots with UnoccupiedPropositions
def buildMap():

    map = []

    for x in range(0, MAP_SIZE):
        row = []
        for y in range(0, MAP_SIZE):
            U = UnoccupiedProposition([x, y])
            row.append(U)
        map.append(row)
        
    for n in range(len(objectList)):
        map[objectList[n].data[0]][objectList[n].data[1]] = objectList[n]
    
    return map

# Converts proposition type into string for understandable printing.
def showMap():

    for x in range(len(map)):
        col = []
        for y in range(len(map)):
            col.append(map[y][x].type())
        print(col)



"""
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():

    # Add custom constraints by creating formulas with the variables you created. 
    E.add_constraint((a | b) & ~x)
    # Implication
    E.add_constraint(y >> z)
    # Negate a formula
    E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    constraint.add_exactly_one(E, a, b, c)

    return E
"""

# In its current state the game checks if the chicken is in a winning position

def crossy_road_base(C : chickenProposition, map):
    """
    Base case for checking whether the chicken can cross the road.
    Returns: Whether the chicken can cross the road.
    """

    # Create a list to use a base case for recursive exploration.
    visited = []
    for i in range(MAP_SIZE):
        row = []
        for j in range(MAP_SIZE):
            row.append(False)
        visited.append(row)

    # Depending on the reuslt add whether chicken can make it!
    result = crossy_road_recursive(C, map, visited)
    if result:
        E.add_constraint(C)
        return E
    E.add_constraint(~C)
    return E
    

def crossy_road_recursive(C : chickenProposition, map, visited):
    """
    Recursive implementation of crossy road. Checking for whether the chicken can cross the road.
    Returns: Whether the chichen can cross the road from the current location.
    """

    if (C.get_x() + 1) == MAP_SIZE:
        print("K")
        return True

    

    path_found = False
    visited[C.get_x()][C.get_y()] = True

    print(visited)
    # Go right.
    if (C.get_x() + 1) < MAP_SIZE:
        if map[C.get_y()][C.get_x() + 1].__repr__() == f"U.[{C.get_x()+1}, {C.get_y()}]":
            if not visited[C.get_x()+1][C.get_y()]:
                temp_C = copy.deepcopy(C)
                temp_C.moveRight()
                temp_map = copy.deepcopy(map)
                path_found = crossy_road_recursive(temp_C, temp_map, visited)

    # # Go up.
    # if not path_found:
    #     if (C.get_y() - 1) >= 0:
    #         if map[C.get_y() - 1][C.get_x()].__repr__() == f"U.[{C.get_x()}, {C.get_y() - 1}]":
    #             if not visited[C.get_x()][C.get_y() - 1]:
    #                 temp_C = copy.deepcopy(C)
    #                 temp_map = copy.deepcopy(map)
    #                 path_found = crossy_road_recursive(temp_C.moveUp(), temp_map, visited)
    
    # Go down.

    # Go left.

    return path_found 


if __name__ == "__main__":

    # Define variables.
    # Set starting location of chicken and obstacles.
    C = chickenProposition([0, MAP_SIZE // 2, 0])
    objectList.append(C)

    # Build the map and display it.
    map = buildMap()
    showMap()
    E.add_constraint(C) 
    T = crossy_road_base(C, map)

    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:

    print("\nSatisfiable:", T.satisfiable())

    print("# Solutions:", count_solutions(T))

    print("\tSolution: ", T.solve())

