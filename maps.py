#imports
from display import *
import random
import math

#constants
ROWS, COLUMNS = 5, 5
OBSTACLES_PER_COLUMN = math.floor(COLUMNS / 2)

#variables
map = []
#create map
for i in range (ROWS):
    row = []

    #fill row with zeros(no obstacle)
    for j in range (COLUMNS):
        row.append(0)

    #add ones(obstacles)
    j = 0
    while(j < OBSTACLES_PER_COLUMN):
        pos = random.randint(0, COLUMNS - 1)
        if(not row[pos]):
            row[pos] = 1
            j += 1 

    #add row to map
    map.append(row)
