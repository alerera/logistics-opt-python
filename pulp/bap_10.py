"""
Berth Assignment Problem Model

This version uses the relative position formulation, and
minimizes only total completion time of all vessels

Authors: Alan Erera 2012
"""

# Import PuLP modeler functions
from pulp import *

# Data Section

# Berth sections
B = 12

# How many ships?
numShips = 10

# Create a list of the ships
Ships = range(1,numShips+1)

# Dictionaries containing ship information

# Arrival times
a     = {    1 : 2, 
             2 : 8, 
             3 : 7, 
             4 : 9,
	     5 : 12,
	     6 : 8,
	     7 : 9,
	     8 : 11,
	     9 : 14,
	     10 : 12
	}

# Processing times
p     = {    1 : 6, 
             2 : 3, 
             3 : 5, 
             4 : 2,
	     5 : 4,
	     6 : 3,
	     7 : 5,
	     8 : 6,
	     9 : 4,
	     10 : 5
	}

# Lengths
h     = {    1 : 5, 
             2 : 4, 
             3 : 3, 
             4 : 6,
	     5 : 2,
	     6 : 4,
	     7 : 3,
	     8 : 6,
	     9 : 5,
	     10 : 4
	 }

# Big M
M = 10000

# Create the 'prob' object to contain the problem data
# Note that "LpProblem" is used for LP, IP, or MIP
prob = LpProblem("Berth Assignment", LpMinimize)

# Decision variables

# Build primary ship berthing relations variables

# x variables model time relationships
x = LpVariable.dicts("X", (Ships,Ships), cat=LpBinary)

# y variables model space along berth relationships
y = LpVariable.dicts("Y", (Ships,Ships), cat=LpBinary)
		
# Now the ship variables
b = LpVariable.dicts("BerthPos",Ships,lowBound=1)
t = LpVariable.dicts("BerthTime",Ships,lowBound=1)
c = LpVariable.dicts("CompleteTime",Ships,lowBound=1)

# Objective function
# The objective function is always added to 'prob' first in PuLP
prob += lpSum([c[s] for s in Ships]), "Total Completion Time"

# Constraints
# Relative position constraints in time
for k in range(1,numShips):
	for l in range(k+1,numShips+1):
		prob += x[k][l] + x[l][k] <= 1, "ChooseRelTime(%d,%d)" % (k,l)

# Relative position constraints in space
for k in range(1,numShips):
	for l in range(k+1,numShips+1):
		prob += y[k][l] + y[l][k] <= 1, "ChooseRelSpace(%d,%d)" % (k,l)

# Overlap constraints
for k in range(1,numShips):
	for l in range(k+1,numShips+1):
		prob += x[k][l] + x[l][k] + y[k][l] + y[l][k] >= 1, "NoOverlap(%d,%d)" % (k,l)
		
# Berthing time and space constraints
for k in Ships:
	prob += t[k] >= a[k], "BerthTimeLowBound(%d)" % k
	prob += c[k] >= t[k] + p[k], "CompleteTimeDef(%d)" % k
	prob += b[k] <= B - h[k] + 1, "BerthPosBound(%d)" % k
	
# Conflict prevention constraints
for k in Ships:
	for l in Ships:
		if k != l:
			prob += t[l] >= c[k] + M*x[k][l] - M, "TimeConflict(%d,%d)" % (k,l)
			prob += b[l] >= b[k] + h[k] + M*y[k][l] - M, "BerthConflict(%d,%d)" % (k,l)
		
# Write out as a .LP file
prob.writeLP("BAP.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve(GUROBI())

# The status of the solution is printed to the screen
print "Status:", LpStatus[prob.status]

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print v.name, "=", v.varValue

# The optimised objective function value is printed to the screen    
print "Total Completion Time = ", value(prob.objective)
