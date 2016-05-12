"""
A MinCost Time-Space Network Flow

This version keeps all information in the header of this file
Has no ability to read data files

Authors: Alan Erera 2013
"""

# Import PuLP modeler functions
from pulp import *

# Data Section

# Geographic Locations
Terminals = ['ATL','CHA','ORL']

# Time Periods (Assumes Uniform Discretization)
TimeStamps = [1, 2, 3]

# Dictionary of node demand dictionaries
# Blank values indicate transshipment nodes
b     = {    'ATL' : {1:3, 3:-4}, 
	     'CHA' : {1:2, 2:-1, 3:-1},
	     'ORL' : {1:2, 2:1}
	}

# Transportation options are used to generate arcs in the next step
# (From, To, TravelTime)
TransportOptions = 	(	('ATL','CHA',2),
				('CHA','ATL',2),
				('ATL','ORL',1),
				('ORL','ATL',1)
			)

# Arcs connect time-space nodes, referenced using a (Terminal,TimeStamp)
# Generate them using assuming a dispatch at all time periods
# In this formulation, we assume a flat network where no arcs are generated
# that extend beyond the final time period
Arcs=[]
Cost=[]
for (o,d,tt) in TransportOptions:
	# Generate an arc in each time period
	for t in TimeStamps:
		oNode = (o,t)
		if (t+tt) <= max(TimeStamps):
			# Assume that each t+tt refers to an available time period
			dNode = (d,t+tt)
			Arcs.append((oNode,dNode))
			Cost.append(tt)
			
# Add inventory arcs
indTime = range(len(TimeStamps)-1)
for i in Terminals:
	for it in indTime:
		oNode = (i,TimeStamps[it])
		dNode = (i,TimeStamps[it+1])
		Arcs.append((oNode,dNode))
		Cost.append(0)
			
# Add arcs from last time-space node at each terminal to a sink
for i in Terminals:
	oNode = (i,max(TimeStamps))
	dNode = ('SINK', max(TimeStamps)+1)
	Arcs.append((oNode,dNode))
	Cost.append(0)
	
# List of arc indices
indArcs = range(len(Arcs))

# Create the 'prob' object to contain the problem data
prob = LpProblem("MinCost Time Space Network Flow", LpMinimize)

# Decision variables
# Build arc flow variables for each arc, lower bounds = 0
arc_flow = []
for a in indArcs:
        # Format for LpVariable("Name",Lowerbound)
	var = LpVariable("ArcFlow_(%s,%s)_(%s,%s)" % (str(Arcs[a][0][0]),str(Arcs[a][0][1]),str(Arcs[a][1][0]),str(Arcs[a][1][1])), 0)
	arc_flow.append(var)

# The objective function is added to 'prob' first
prob += lpSum([Cost[a]*arc_flow[a] for a in indArcs]), "Total Cost"

# Generate a flow balance constraints for each non-sink node
for i in Terminals:
	for t in TimeStamps:
		outArcs = []
		inArcs = []
		for a in indArcs:
			if (Arcs[a][0][0] == i) and (Arcs[a][0][1] == t):
				outArcs.append(a)
			elif (Arcs[a][1][0] == i) and (Arcs[a][1][1] == t):
				inArcs.append(a)
		NetSupply = 0
		if i in b:
			if t in b[i]:
				NetSupply = b[i][t]
			
		prob += lpSum([arc_flow[a] for a in outArcs]) - lpSum([arc_flow[a] for a in inArcs]) == NetSupply, "Node (%s,%s) Balance" % (str(i),str(t))

# You may be wondering why no balance constraint is provided for the sink node.
# It turns out that such a constraint is redundant in this formulation, since
# the flow balance constraints at the final timed nodes for each terminal will
# determine the final inventory held, and the sum of these values must by
# definition be equal to the network-wide net supply (in this problem, +2)

# Write out as a .LP file
prob.writeLP("TSMinCostFlow.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve(GUROBI())

# The status of the solution is printed to the screen
print "Status:", LpStatus[prob.status]

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print v.name, "=", v.varValue

# The optimised objective function value is printed to the screen    
print "Total Cost = ", value(prob.objective)
