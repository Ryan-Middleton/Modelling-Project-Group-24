#imports
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from constants import WIDTH, HEIGHT, MAX_DEPTH;

#set encoding
Theory = Encoding()

@proposition(Theory)
class PredicateTileReachable:
  arr = [[[proposition for t in range(MAX_DEPTH)] for y in range(HEIGHT)] for x in range(WIDTH)]
  def __init__(self, x, y, time):
    self.x = x
    self.y = y
    self.t = time
    
    #save predicates for easy lookup
    PredicateTileReachable.arr[x][y][time] = self

  def extrapolateUsingPast(self, Theory):
    Theory.add_constraint(
      (~PredicateTileReachable.arr[self.x][self.y][self.t] &
      (PredicateTileReachable.arr[self.x + 1][self.y][self.t - 1] |
      PredicateTileReachable.arr[self.x - 1][self.y][self.t - 1] |
      PredicateTileReachable.arr[self.x][self.y + 1][self.t - 1] |
      PredicateTileReachable.arr[self.x][self.y - 1][self.t - 1] |
      PredicateTileReachable.arr[self.x][self.y][self.t - 1])) >>
      self
    )
    Theory.add_constraint(
      ~(~PredicateTileReachable.arr[self.x][self.y][self.t] &
      (PredicateTileReachable.arr[self.x + 1][self.y][self.t - 1] |
      PredicateTileReachable.arr[self.x - 1][self.y][self.t - 1] |
      PredicateTileReachable.arr[self.x][self.y + 1][self.t - 1] |
      PredicateTileReachable.arr[self.x][self.y - 1][self.t - 1] |
      PredicateTileReachable.arr[self.x][self.y][self.t - 1])) >>
      (~self.arr)
    )

  def fetch(x, y, t):
    return PredicateTileReachable.arr[x][y][t]
    
  def __repr__(self):
    return f"TileReachable.{self.x}.{self.y}.{self.t}"

@proposition(Theory)
class PredicateObstacle:
  arr = [[[proposition for t in range(MAX_DEPTH)] for y in range(HEIGHT)] for x in range(WIDTH)]
  def __init__(self, x, y, time):
    self.x = x
    self.y = y
    self.t = time

    #save predicates for easy lookup
    PredicateObstacle.arr[x][y][time] = self

  def extrapolateFromPast(self, deltaX, Theory):
    Theory.add_constraint(
      PredicateObstacle.fetch((self.x - deltaX) % WIDTH, self.y, self.t - 1) >> self.arr
    )
    Theory.add_constraint(
      (~PredicateObstacle.fetch((self.x - deltaX) % WIDTH, self.y, self.t - 1)) >> (~self)
    )
    
  def fetch(x, y, t):
    return PredicateObstacle.arr[x][y][t]

  def __repr__(self):
    return f"Obstacle.{self.x}.{self.y}.{self.t}"


#https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
class Singleton(object):
  _instance = None
  def __new__( cls, *args, **kwargs ):
      if not cls._instance:
          cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
      return cls._instance

#@Singleton
@proposition(Theory)
class PredicateEnd:
  def __init__(self):
    pass
  def __repr__(self):
    return "End"
