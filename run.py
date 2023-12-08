
import secrets
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

MAP_SIZE = 3

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

    #Stored as length 3 array
    # Index 0: x coordinate
    # Index 1: y coordinate
    # Index 2: Turn/time

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"C.{self.data}"
    
    def moveUp(self):
        self.data[1] = self.data[1] + 1
        self.data[2] = self.data[2] + 1
        return self

    def moveDown(self):
        self.data[1] = self.data[1] - 1
        self.data[2] = self.data[2] + 1
        return self
    
    def moveRight(self):
        self.data[0] = self.data[0] - 1
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
class movingSouthObjectProposition:

    #Stored as length 3 array
    # Index 0: x coordinate
    # Index 1: y coordinate
    # Index 2: Turn/time

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"M.{self.data}"
    
    def move(self):
        if (self.data[1]+1 >= MAP_SIZE):
            self.data[1] = 0
        else:
            self.data[1] = self.data[1]+1
        self.data[2] = self.data[2] + 1
        return self

    def type(self):
        return "MS"
    
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
class unoccupiedProposition:

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

#Used for creating object map.
objectList = []

# Set starting location of chicken
C = chickenProposition([0, 1, 0]) # Left Side Start
# C = chickenProposition([2, 0, 0]) # Winning Position Start
objectList.append(C)

# Set starting location of moving object
M = movingSouthObjectProposition([1, 1, 0])
objectList.append(M)

# Set starting location of stationary object
S1 = stationaryObjectProposition([2,1])
objectList.append(S1)

# Enable to block end (returns false)
S2 = stationaryObjectProposition([2,0])
S3 = stationaryObjectProposition([2,2])
objectList.append(S2)
objectList.append(S3)


U = unoccupiedProposition([0,0])
objectList.append(U)

def checkValid(C,M):

    # Check Within arraybounds, oliding with moving object, within time bounds
    if(not (C.data[0] >= 0 and C.data[1] >= 0 and C.data[0] < MAP_SIZE and C.data[1] < MAP_SIZE and C.data[2]<11 and M.data[2]<11 and C.data != M.data)):
        return False

    # Check coliding with stationary object
    for x in range(len(objectList)):
        if(objectList[x].type() == "S"):
            if( C.data[0] == objectList[x].data[0] and C.data[1] == objectList[x].data[1] ):
                return False
    
    # Otherise true
    return True
           


# Builds map with object types, filling vacant spots with unoccupiedPropositions
def buildMap():
    map = []

    for x in range(0, MAP_SIZE):
        row = []
        for y in range(0, MAP_SIZE):
            U = unoccupiedProposition([x, y])
            row.append(U)
        map.append(row)   
        
    for n in range(len(objectList)):
        map[objectList[n].data[0]][objectList[n].data[1]] = objectList[n]
    
    return map

map = buildMap()

# Converts proposition type into string for understandable printing.
def showMap():

    for x in range(len(map)):
        col = []
        for y in range(len(map)):
            col.append(map[y][x].type())
        print(col)

showMap()



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

def crossy_road():
    
    # All non chickens false
    for x in range(len(objectList)):
        if(objectList[x].type() != "C"):
            E.add_constraint(~objectList[x])



    sol = (crossy_roadRecursive(chickenProposition(C.data).moveUp(), movingSouthObjectProposition(M.data).move())
    + crossy_roadRecursive(chickenProposition(C.data).moveDown(), movingSouthObjectProposition(M.data).move())
    + crossy_roadRecursive(chickenProposition(C.data).moveRight(), movingSouthObjectProposition(M.data).move())
    + crossy_roadRecursive(chickenProposition(C.data).moveLeft(), movingSouthObjectProposition(M.data).move())
    + crossy_roadRecursive(chickenProposition(C.data).moveNone(), movingSouthObjectProposition(M.data).move()))


    # If chicken can't find path to end
    if (sol == 0):
        E.add_constraint(~C)
        return E
    else: 
        E.add_constraint(C)
        return E

def crossy_roadRecursive(C, M):

    E.add_constraint(~C)

    if (C.data[0] == -1):
        return 0
    # If within time, array bounds and not sharing spot with moving/stationary object.
    if(checkValid(C,M)):
        # If chicken is within time and at end return true (1)
        if(C.data[0] == MAP_SIZE-1):
            return 1
        # Move in all directions
        else:

            return (crossy_roadRecursive(chickenProposition(C.data).moveUp(), movingSouthObjectProposition(M.data).move())
    + crossy_roadRecursive(chickenProposition(C.data).moveDown(), movingSouthObjectProposition(M.data).move())
    + crossy_roadRecursive(chickenProposition(C.data).moveRight(), movingSouthObjectProposition(M.data).move())
    + crossy_roadRecursive(chickenProposition(C.data).moveLeft(), movingSouthObjectProposition(M.data).move())
    + crossy_roadRecursive(chickenProposition(C.data).moveNone(), movingSouthObjectProposition(M.data).move()))

    # If chicken is outside time and array bounds return false (0)
    return 0





if __name__ == "__main__":

    T = crossy_road()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    """
    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
    """
