"""
A Standard MinCost Network Flow Problem

This version keeps all information in the header of this file
Has no ability to read data files

Authors: Alan Erera 2011
"""

# Import PuLP modeler functions
from pulp import *

# Data Section

# How many nodes?
numNodes = 10

# Create a list of the nodes
# This version uses node numbers
Nodes = range(1,numNodes+1)

# Dictionary of node demands
b     = {    1 : 1220, 
             2 : 2210, 
             3 : 150, 
             4 : 360,
	     5 : 2025,
	     6 : -1970,
	     7 : -5040,
	     8 : -1750,
	     9 : 575,
	     10 : 2220
	 }

# Create arcs as list of duples
Arcs =  (	(2,1) ,
		(3,4) ,
		(7,6) ,
		(6,8) ,
		(7,9) ,
		(6,8) ,
		(7,2) ,
		(1,3) ,
		(4,5) ,
		(6,5) ,
		(8,9) ,
		(9,10) ,
		(8,2) ,
		(2,1) ,
		(3,2) ,
		(5,4) ,
		(5,6) ,
		(9,10) ,
		(10,7) ,
		(2,1) ,
		(1,2) ,
		(4,3) ,
		(6,7) ,
		(10,6) ,
		(1,3) ,
		(2,7) ,
		(3,5) ,
		(5,6)
	)

# List of arc costs
Cost = 	( 200 ,
	  250 ,
	  800 ,
	  500 ,
	  1300 ,
	  500 ,
	  1500 ,
	  400 ,
	  450 ,
	  1100 ,
	  1100 ,
	  500 ,
	  1400 ,
	  300 ,
	  900 ,
	  1000 ,
	  300 ,
	  500 ,
	  900 ,
	  300 ,
	  200 ,
	  600 ,
	  300 ,
	  600 ,
	  400 ,
	  600 ,
	  500 ,
	  800
 	) 

# List of arc upper bounds
UpperBound = 	( 690 ,
		  1550 ,
		  50 ,
		  1105 ,
		  200 ,
		  990 ,
		  20 ,
		  550 ,
		  1440 ,
		  400 ,
		  45 ,
		  20 ,
		  300 ,
		  1220 ,
		  165 ,
		  95 ,
		  3100 ,
		  800 ,
		  390 ,
		  1200 ,
		  2820 ,
		  565 ,
		  2515 ,
		  2650 ,
		  960 ,
		  2405 ,
		  510 ,
		  1180
	) 

# List of arc indices
indArcs = range(len(Arcs))

# Create the 'prob' object to contain the problem data
prob = LpProblem("MinCost Network Flow", LpMinimize)

# Decision variables
# Build arc flow variables for each arc, lower bounds = 0
arc_flow = []
for a in indArcs:
        # Format for LpVariable("Name",Lowerbound)
	var = LpVariable("ArcFlow_(%d,%d)" % (Arcs[a][0],Arcs[a][1]), 0)
	arc_flow.append(var)

# The objective function is added to 'prob' first
prob += lpSum([Cost[a]*arc_flow[a] for a in indArcs]), "Total Cost"

# Generate a flow balance constraints for each node
for i in Nodes:
	outArcs = []
	inArcs = []
	for a in indArcs:
		if Arcs[a][0] == i:
			outArcs.append(a)
		elif Arcs[a][1] == i:
			inArcs.append(a)
	prob += lpSum([arc_flow[a] for a in outArcs]) - lpSum([arc_flow[a] for a in inArcs]) == b[i], "Node %d Balance" % i

# Generate a flow upper bound for each arc
for a in indArcs:
	prob += arc_flow[a] <= UpperBound[a], "Arc %d Upper Bound" % a

# Write out as a .LP file
prob.writeLP("MinCostFlow.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve(GUROBI())

# The status of the solution is printed to the screen
print "Status:", LpStatus[prob.status]

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print v.name, "=", v.varValue

# The optimised objective function value is printed to the screen    
print "Total Cost = ", value(prob.objective)
