#imports
from bauhaus import Encoding, proposition, constraint;
from bauhaus.utils import count_solutions, likelihood;
from constants import *
#PredicateObstacle, PredicateTileReachable, PredicateEnd, Theory;
from classes import *

# These two lines make sure a faster SAT solver is used.
from nnf import config;
config.sat_backend = "kissat";

#create alot of predicates
'''for x in range(WIDTH):
  for y in range(HEIGHT):
    for t in range(MAX_DEPTH):
      PredicateTileReachable(x, y, t);
      PredicateObstacle(x, y, t);'''

#set initial predicates for obstacles
if(LOAD_CUSTOM_FILE):
  #read from file
  from init import preset;

  if(len(preset) != WIDTH):
    raise Exception("Invalid preset dimensions")
    
  for x in range(WIDTH):
    if(len(preset[x]) != HEIGHT):
      raise Exception("Invalid preset dimensions")
      
    for y in range(HEIGHT):
      if(preset[x][y] == "#"):
        Theory.add_constraint(PredicateObstacle.fetch(x, y, 0))
      else:
        Theory.add_constraint(PredicateTileReachable.fetch(x, y, 0))
else:
  #generate(not complete)
  for y in range(HEIGHT):
    if(HAS_OBSTACLES):
      count = 0
      while(count < OBSTACLES_PER_ROW):
        pass
        #to be continued...


#extrapolate obstacles
for t in range(1, MAX_DEPTH):
  for x in range(WIDTH):
    for y in range(HEIGHT):
      PO = PredicateObstacle(x, y, t)
      PO.extrapolateFromPast(OBSTACLE_MOVEMENT[x], Theory)


#init chicken position
Theory.add_constraint(PredicateTileReachable.fetch(0, 0, 0))


#add constrains for reachable tiles
for t in range(1, MAX_DEPTH):
  for x in range(WIDTH):
    for y in range(HEIGHT):
      PTR = PredicateTileReachable(x, y, t)
      PTR.extrapolateUsingPast(Theory)


#construct end state(UNSAFE)
endState = PredicateEnd()
endLine = []
for x in range(WIDTH):
  endLine.append(f"PredicateTileReachable.fetch({x}, {HEIGHT - 1}, {MAX_DEPTH - 1})");
endLine = f"({1})"
eval(f"Theory.add_constraint({endLine} >> endState)")
eval(f"Theory.add_constraint(~{endLine} >> (~endState))")

if(THROW_SATIFIBILITY_ERROR):
    Theory.add_constraint(endState)

if __name__ == "__main__":

    Theory.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % Theory.satisfiable())
    print("# Solutions: %d" % count_solutions(Theory))
    print("   Solution: %s" % Theory.solve())

    '''
    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(Theory, v)))
    print()
    '''


