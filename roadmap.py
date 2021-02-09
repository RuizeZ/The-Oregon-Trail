# Python3 code to demonstrate 
# to generate random number list
# using random.sample()
import random
 
# using random.sample()
# to generate random number list
row = random.randint(1,10)
column = random.randint(1,10)
startx = random.randint(0, column-1)
starty = random.randint(0, row-1)
start = [startx, starty]
roadmap = []
endlist = []
for i in range(0, 3):
    endx = random.randint(0, column-1)
    endy = random.randint(0, row-1)
    endlist.append([endx, endy])
for i in range(0, row):
    res = random.sample(range(-10, 10), column)
    roadmap.append(res)
 
# printing result
print ("start is: ", start)
print ("number of end", len(endlist))
print ("end: ", endlist)
print ("row is: ", row)
print ("column is: ", column)
print ("raod map is:")
print (roadmap)