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
numNodes = 4

# Create a list of the nodes
# This version uses node numbers
Nodes = range(1,numNodes+1)

# Dictionary of node demands
b     = {    1 : 40, 
             2 : -20, 
             3 : 0, 
             4 : -20 
	 }

# Create arcs as list of duples
Arcs =  (	(1,2) ,
        	(2,4) ,
		(2,3) 
	)

# List of arc costs
Cost = 	( 300 ,
          150 ,
	  200
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

# Write out as a .LP file
prob.writeLP("MinCostFlow.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print "Status:", LpStatus[prob.status]

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print v.name, "=", v.varValue

# The optimised objective function value is printed to the screen    
print "Total Cost = ", value(prob.objective)
