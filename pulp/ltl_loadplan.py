"""
Python Code for LTL Load Planning

This implementation builds from the networkx module,
which defines a useful network class

Authors: Alan Erera 2012
"""

# Module import section
import math
import networkx as nx
import pulp
from path import Path	

def main():
	
	# Data Section
	
	# List of arcs, in format (FromNode, ToNode, {Attribute Dictionary})
	arclist = [ 	('Ath','Mac',{'cost':125}) ,
			('Mac','Ath',{'cost':125}),
			('Ath','ATL',{'cost':85}) ,
			('ATL','Ath',{'cost':85}) ,
			('Mac','ATL',{'cost':70}) ,
			('ATL','Mac',{'cost':70}) ,
			('Mac','DAL',{'cost':670}) ,
			('ATL','DAL',{'cost':610}) ,
			('DAL','ATL',{'cost':610}) ,
			('ATL','CHI',{'cost':1050}) ,
			('CHI','ATL',{'cost':1050}) ,
			('DAL','CHI',{'cost':1300}) ,
			('CHI','DAL',{'cost':1300})
		  ]
	
	# Dictionary of commodities, demand and empty path sets
	commods = {	('Ath','CHI'):{'q':0.1,'paths':[]},
			('ATL','CHI'):{'q':1.6,'paths':[]}	
	}
	
	# List of paths, using the Path type (edges, path handling cost)
	paths = [	Path([('Ath','ATL'),('ATL','CHI')], {'cost':100, 'name':'Ath-Chi-1'}) ,
			Path([('Ath','ATL'),('ATL','DAL'),('DAL','CHI')], {'cost':200, 'name':'Ath-Chi-2'}) ,
			Path([('ATL','CHI')], {'cost':0, 'name':'ATL-CHI-1'}) ,
			Path([('ATL','DAL'), ('DAL','CHI')], {'cost':100, 'name':'ATL-CHI-2'})
		]
					
	# Code Section
	
	# Instantiate a directed graph for the leg network
	G = nx.DiGraph()
	
	# Add the nodes and edges, all from the arc tuple list above
	G.add_edges_from(arclist)
	
	# Attach the paths to commodities
	for p in paths:
		od_key = (p.origin,p.dest)
		# If the path (o,d) is a commodity
		if od_key in commods:
			# Add this path to the list P_k; use bracket to avoid iteration over path elements
			commods[od_key]['paths'] += [p]
		else:
			print('Found path for a non-existant (o,d) pair:' + str(p))
			
	# Validation and error checking the input data
	# Check that paths only include network arcs
	for p in paths:
		try:
			name = p['name']
			for e in p.edges:
				if e not in G.edges():
					raise RuntimeError('Arc %s in path %s not found in network arcs. ' % (str(e),str(name)))
		except:
			raise RuntimeError('Path %s is not named.' % str(p))
	
	# Check that commodity (o,d) are each nodes in the network, and
	# that each has at least one path
	for k in commods:
		dummycost = 0
		try:
			if (k[0] not in G.nodes()) or (k[1] not in G.nodes()):
				raise RuntimeError('Commodity %s connects nodes not both in network.' % str(k))
				
			dummycost += commods[k]['q']
			
			if not commods[k]['paths']:
				raise RuntimeError('At least one path must serve each commodity.  Check %s' % str(k) )
			
		except KeyError:
			raise RuntimeError('Each commodity must specify a demand value q. Check %s' % str(k) )
	
	# Check that edges have necessary attributes
	for i,j,attr in G.edges(data=True) :
		dummycost = 0
		try :
			dummycost += attr['cost']
		except KeyError :
			raise RuntimeError('Each arc must have a cost attribute. Check (%s, %s)' % (str(i),str(j)) )
					
	# Set up and run the load planning model using PuLP
	
	# Create the 'prob' object to contain the optimization problem data
	prob = pulp.LpProblem("LTL Load Planning", pulp.LpMinimize)
	
	# Decision variables initialization
	
	# Build integer trailer flow variables for each arc, lower bounds = 0
	# Build summation list for the objective function
	objFn = []
	# Loop over the arcs, pulling all of the attribute data
	for i,j,attr in G.edges(data=True) :
		# Format for LpVariable("Name",lowBound,cat)
		var = pulp.LpVariable("TrailerFlow_(%s,%s)" % (str(i),str(j)), lowBound = 0, cat=pulp.LpInteger)
			
		# Add decision variable to the edge dictionary data structure
		G[i][j]['dvTrailerFlow'] = var
			
		# Add objective function term to objFn list variable
		if attr['cost'] != 0 :
			objFn.append(attr['cost']*var)
			
	# Build path selection binary variables for each path
	# Add to objective function summation list
	for p in paths:
		# Format for LpVariable("Name",lowBound,cat)
		var = pulp.LpVariable("PathSelect_(%s)" % (str(p['name'])), cat=pulp.LpBinary)
		
		# Add decision variable to the path dictionary data structure
		p['dvPathSelect'] = var
			
		# Add objective function term to objFn list variable
		# Path handling cost * number of trailerloads
		if p['cost'] != 0 :
			o = p.origin
			d = p.dest
			objFn.append(p['cost']*commods[(o,d)]['q']*var)
			
	# Build in-tree arc selection variables	
	# Loop over all arcs in all paths, adding dictionary keys
	# Store them for each dest=d and current_node=i
	# Also add the paths needing each tree variable to a commodity list
	tree_variables = {}
	for p in paths:
		# Grab origin,destination of the path
		d = p.dest
		k = (p.origin,d)
		if d not in tree_variables:
			tree_variables[d]={}
		# Add a variable for each 
		for e in p.edges:
			# Grab the tail, head nodes of the arc
			i = e[0]
			j = e[1]
			# If this current node i not yet initialized
			if i not in tree_variables[d]:
				tree_variables[d][i]={}
			# If this arc has not had a variable generated yet
			if j not in tree_variables[d][i]:
				tree_variables[d][i][j] = {}
				
				# Create decision variable
				var = pulp.LpVariable("TreeVariable_%s_(%s,%s)" % (str(d),str(i),str(j)), cat=pulp.LpBinary)				
				tree_variables[d][i][j]['dvTreeVar'] = var
				
				# Initialize the commodity-specific path list for k=(o,d)
				tree_variables[d][i][j]['paths'] = {k:[]}
			
			# Initialize the commodity-specific path list for k=(o,d)	
			elif k not in tree_variables[d][i][j]['paths']:
				tree_variables[d][i][j]['paths'] = {k:[]}
		
			# Add this path to the list
			tree_variables[d][i][j]['paths'][k] += [p]
				

	# The objective function is added to 'prob' first
	# lpSum takes a list of coefficients*LpVariables and makes a summation
	prob += pulp.lpSum(objFn), "Total Cost"
	
	# Constraints
	# Pick one path for each commodity
	for k in commods:
		prob += pulp.lpSum(p['dvPathSelect'] for p in commods[k]['paths']) == 1, "Commodity %s Path Selection" % str(k)
		
	# Trailer counts
	for i,j in G.edges():
		pathFracTrailers = []
		# Look for paths that contain arc (i,j)
		for p in paths:
			if (i,j) in p:
				q = commods[(p.origin,p.dest)]['q']
				pathFracTrailers.append( q*p['dvPathSelect'] )
		# If any paths contain the arc (i,j), build a trailer round up constraint
		if pathFracTrailers:
			prob += pulp.lpSum(pathFracTrailers) <= G[i][j]['dvTrailerFlow'], "Arc (%s,%s) Trailer Roundup" % (str(i),str(j))
			
	# In-tree constraints
	# Destinations are the first-level keys in the tree_variables dictionary
	for d in tree_variables:
		# Current nodes i are the second-level keys
		for i in tree_variables[d]:
			# Build constraint summing the tree variables stored for each head node j
			prob += pulp.lpSum(tree_variables[d][i][j]['dvTreeVar'] for j in tree_variables[d][i]) <= 1, "Dest %s Node %s Tree Arc Selection" % (str(d),str(i))
		
	# Path-tree consistency constraints
	# Destinations are the first-level keys in the tree_variables dictionary
	for d in tree_variables:
		# Tail nodes i are the second level...
		for i in tree_variables[d]:
			# Head nodes j are the third level
			for j in tree_variables[d][i]:
				# Build a constraint for each k using this arc
				for k in tree_variables[d][i][j]['paths']:
					prob += pulp.lpSum(p['dvPathSelect'] for p in tree_variables[d][i][j]['paths'][k]) <= tree_variables[d][i][j]['dvTreeVar'], "Path-tree Consistency %s_(%s,%s)" % (str(k),str(i),str(j))		

	# Write out as a .LP file
	prob.writeLP("LTLLoadPlan.lp")

	# The problem is solved, in this case explicitly asking for Gurobi
	prob.solve(pulp.GUROBI())

	# The status of the solution is printed to the screen
	print "Status:", pulp.LpStatus[prob.status]

	# Each of the variables is printed with it's resolved optimum value
	for v in prob.variables():
		print v.name, "=", v.varValue

	# The optimised objective function value is printed to the screen    
	print "Total Cost = ", pulp.value(prob.objective)

main()
	
#try:
#	main()
	
#except Exception, err:
#	print 'ERROR: ' + str(err)
	
