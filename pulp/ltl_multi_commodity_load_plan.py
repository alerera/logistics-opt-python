"""
Python Code for Multi-commodity network flow for load planning

This implementation introduces the idea of using
dictionaries of dictionaries in Python to easily hold
and organize lists of data of all types

A dictionary in python contains key,value pairs:

my_dictionary = {key1:value1, key2:value2, ...}

and you can always add new key,value pairs later.  What
makes them nice is that the "key" can be just about any
object, and so can the "value".  Importantly, the "value"
can be another dictionary:

my_dictionary = {key1:{key1_1:value1_1, ...}, key2:{key2_1:value2_1, ...}, ... }

Authors: Alan Erera 2012
"""

# Module import section
import math
import pulp

# Data Section
	
# List of arcs, in dictionary format (FromNode,ToNode}: {Attribute Dictionary}
# For now, the attributes are labeled with key='cost'
# But, this structure allows us to add more keys later to each arc's
# attribute dictionary
arcs =  { 	('Ath','Mac'):{'cost':125},
		('Mac','Ath'):{'cost':125},
		('Ath','ATL'):{'cost':85},
		('ATL','Ath'):{'cost':85},
		('Mac','ATL'):{'cost':70},
		('ATL','Mac'):{'cost':70},
		('Mac','DAL'):{'cost':670},
		('ATL','DAL'):{'cost':610},
		('DAL','ATL'):{'cost':610},
		('ATL','CHI'):{'cost':1050},
		('CHI','ATL'):{'cost':1050},
		('DAL','CHI'):{'cost':1300},
		('CHI','DAL'):{'cost':1300}
}

# Dictionary of commodities, (OrigNode,DestNode):{Attribute Dictionary}
# Here, we assume that commodities are distinct shipments that travel from
# an origin to a destination, and the "q" attribute gives the total flow size
commods = {	('Ath','CHI'):{'q':0.3},
		('Ath','DAL'):{'q':0.4},
		('Mac','ATL'):{'q':0.7},
		('Mac','DAL'):{'q':0.5},
		('Mac','CHI'):{'q':0.6},
		('ATL','CHI'):{'q':1.5},
		('ATL','DAL'):{'q':2.2},
		('DAL','CHI'):{'q':1.7}
}

# Code Section

# First, we build a dictionary of nodes, extracting the unique items from
# the arc dictionary; the 'for' loop considers all keys in arcs
# This way, we avoid specifying a set of nodes; all we need are arcs!
# Initialize an empty dictionary of nodes
nodes = {}
for a in arcs:
	i = a[0]
	j = a[1]
	# Check if i,j are not yet in the nodes dictionary, and if so
	# initialize empty lists of outArcs and inArcs
	if i not in nodes:
		nodes[i] = {'outArcs':[], 'inArcs':[]}
	if j not in nodes:
		nodes[j] = {'outArcs':[], 'inArcs':[]}
	# Add arc a to the outbound list for i, and the inbound list for j
	nodes[i]['outArcs'] += [a]
	nodes[j]['inArcs'] += [a]

# Check that commodity (o,d) are each nodes in the network
for k in commods:
	orig = k[0]
	dest = k[1]
	if (orig not in nodes) or (dest not in nodes):
		print('Commodity %s connects nodes not both in network.' % str(k))
		exit(1)

# Set up and run the multi-commodity flow model using PuLP
	
# Create the 'prob' object to contain the optimization problem data
prob = pulp.LpProblem("Multi-commodity Load Plan", pulp.LpMinimize)
	
# Decision variables initialization
	
# Build fractional trailer flow variables for each arc and commodity, lower bounds = 0
# and a total integer trailer flow variable
# This a data-intense approach, since many arcs may not even exist on a path
# for a specific commodity
# Build summation list for the objective function
objFn = []
# Loop over the arcs in a special way: arcs.iteritems() returns both the arcs
# a and the attribute dictionary for a (the '"value" in the pair)
for a,a_dict in arcs.iteritems():
	i = a[0]
	j = a[1]
	
	# First create a total integer trailer flow variable, and tie it to the arc
	var = pulp.LpVariable("TrailerFlow(%s,%s)" % (str(i),str(j)), lowBound = 0, cat=pulp.LpInteger)
	a_dict['dvTrailerFlow'] = var
	
	# Add objective function term to objFn list variable
	if a_dict['cost'] != 0 :
		objFn.append(a_dict['cost']*var)
	
	# Create an empty dictionary inside the arc attributes dictionary
	# to hold the fractional flow decision variables for each commodity
	a_dict['dvFlows']={}
	# Add a decision variable for each commodity k
	for k in commods:
		orig = k[0]
		dest = k[1]
		# Format for LpVariable("Name",lowBound,cat)
		# Name will list the arc first, then the commodity; e.g.
		# Arc_Flow('ATL,'DAL')_('Ath','CHI')
		var = pulp.LpVariable("ArcFlow(%s,%s)_(%s,%s)" % (str(i),str(j),str(orig),str(dest)), lowBound = 0)
			
		# Add decision variable to the dictionary data structure
		a_dict['dvFlows'][k] = var
			

# The objective function is added to 'prob' first
# lpSum takes a list of coefficients*LpVariables and makes a summation
prob += pulp.lpSum(objFn), "Total Cost"
	
# Constraints

# Flow balance at all nodes for all commodities
for k,k_dict in commods.iteritems():
	orig = k[0]
	dest = k[1]
	for i in nodes:
		# If i is the orig of the commodity, the net supply is q
		if i == orig:
			netsupply = k_dict['q']
		elif i == dest:
			netsupply = - k_dict['q']
		else:
			netsupply = 0
			
		# Create the flow balance constraint	
		prob += pulp.lpSum(arcs[a]['dvFlows'][k] for a in nodes[i]['outArcs']) - pulp.lpSum(arcs[a]['dvFlows'][k] for a in nodes[i]['inArcs']) == netsupply, "Node %s Commodity (%s,%s) Flow Balance" % (str(i),str(orig),str(dest))

# Round up the arc flows to trailer flows, across commodities
for a,a_dict in arcs.iteritems():
	i = a[0]
	j = a[1]
	# Sum over all of the commodity-specific arc flows
	prob += pulp.lpSum(a_dict['dvFlows'][k] for k in commods) <= a_dict['dvTrailerFlow'], "Arc (%s,%s) Trailer Roundup" % (str(i),str(j))

# Write out as a .LP file
prob.writeLP("LTLMCLoadPlan.lp")

# The problem is solved, in this case explicitly asking for Gurobi
prob.solve(pulp.GUROBI())

# The status of the solution is printed to the screen
print "Status:", pulp.LpStatus[prob.status]

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
	print v.name, "=", v.varValue

# The optimised objective function value is printed to the screen    
print "Total Cost = ", pulp.value(prob.objective)
	
