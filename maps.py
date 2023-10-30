#imports
from display import *
import random
import math

#constants
ROWS, COLUMNS = 5, 5
OBSTACLES_PER_COLUMN = math.floor(COLUMNS/2)

#variables
map = []
#create map
for i in range (ROWS):
    row = []

    for j in range (COLUMNS):
        row[j] = 0

    j = 0
    while(j < OBSTACLES_PER_COLUMN):
        pos = random.randInt(0, COLUMNS)
        if(not row[j]):
            row[pos] = 1
            j += 1 
    map.append(row)

displayMap(map)