# Python Code for Network Design Formulation of TSP
#
# Alan Erera, 2013
#
# 
#  TSP_networkdesign
#
#  a function which, given a complete graph (directed or undirected) in the
#  networkx format, returns an optimal TSP cycle using a "network design"
#  style formulation: design variables select the TSP, and the flow variables
#  use the selected arcs to send flow from an arbitrary first node to all
#  other nodes
#
#  cycles will be in node list format: [first, ..., last, first]
#
#  Inputs:
#
#   G           - network in networkx format
#

# Module imports
import networkx as nx
# Import PuLP modeler functions
from pulp import *


def TSP_networkdesign(G):
    
    # Let n be the number of nodes
    n = len(G)
    
    # This version will not assume that we have a complete graph, although
    # it is recommended.  If a TSP does not exist, it is likely that the
    # integer program will not fail gracefully.
    
    # If network is undirected, convert it to a directed network GD since we will
    # need different selection and flow variables for (i,j) and (j,i)
    if G.is_directed():
        GD = G
    else:
        GD = nx.DiGraph()
        # Add first the undirected edges
        GD.add_edges_from(G.edges())
        # Loop to add costs on the edges, and the reverse arcs with same costs
        # Careful:  once an edge is added from j to i, the original 'for' loop
        # does not consider it again
        for i in GD:
            for j in GD[i]:
                GD[i][j]['cost'] = G[i][j]['cost']
                GD.add_edge(j,i,{'cost':G[i][j]['cost']})
                
    # Create the math programming problem 'prob'
    prob = LpProblem("TSP By Network Design", LpMinimize)
    
    # Create TSP arc selection variables and flow variables for each directed arc
    # networkx format already stores arcs arranged by their "from" or "tail" nodes
    for i in GD:
        for j in GD[i]:          
            # Arc name
            a = str((i,j))
        
            # Variable generation for the "assignment" or "selection" variables
            var = LpVariable("ArcSelect_%s" % a, cat=LpBinary)
            # Add arc selection variable to the data dictionary for the arc
            GD[i][j]['vSelect'] = var
        
            # Variable generation for the "flow" variables
            var = LpVariable("ArcFlow_%s" % a, lowBound=0)
            GD[i][j]['vFlow'] = var
            
    # The objective function is added to 'prob' first
    prob += lpSum([GD[i][j]['cost']*GD[i][j]['vSelect'] for (i,j) in GD.edges()]), "Total Cost"
    
    # Assignment constraints
    # Generate successor selection constraint for each node
    for i in GD:
        prob += lpSum([GD[i][j]['vSelect'] for j in GD.successors(i)]) == 1, "Node %s Successor Selection" % str(i)
    # Generate predecessor selection constraint for each node    
    for j in GD:
        prob += lpSum([GD[i][j]['vSelect'] for i in GD.predecessors(j)]) == 1, "Node %s Predecessor Selection" % str(j)

    # Flow constraints
    # Generate flow upper bound constraints for each arc
    for (i,j) in GD.edges():
        prob += GD[i][j]['vFlow'] <= (n-1)*GD[i][j]['vSelect'], "Arc %s Successor Selection" % str((i,j))

    # Generate flow balance constraint for first node
    # In case it is not named node "1", we must use this strange form to get the first node
    first = GD.nodes()[0]
    prob += lpSum([GD[first][j]['vFlow'] for j in GD.successors(first)]) - lpSum([GD[j][first]['vFlow'] for j in GD.predecessors(first)]) == n - 1, "Node %s Flow Balance" % str(first)
    
    # Generate flow balance constraints for all but first node
    for i in GD:
        if i != first:
            prob += lpSum([GD[i][j]['vFlow'] for j in GD.successors(i)]) - lpSum([GD[j][i]['vFlow'] for j in GD.predecessors(i)]) == - 1, "Node %s Flow Balance" % str(i)
    
    # Write out as a .LP file
    prob.writeLP("TSPNetworkDesignIP.lp")

    # The problem is solved using PuLP's choice of Solver
    prob.solve(GUROBI())

    # The status of the solution is printed to the screen
    print "Status:", LpStatus[prob.status]

    # Each of the variables is printed with it's resolved optimum value
    #for v in prob.variables():
    #    print v.name, "=", v.varValue

    # The optimised objective function value is printed to the screen    
    print "Total Cost = ", value(prob.objective)
    
    # Create the optimal cycle from the optimal variable values in the solution, and return it
    # Start at the arbitrary first node, and find its successor, then the next successor, etc.
    first = GD.nodes()[0]
    current = first
    cycle = [current]
    next = []
    cycle_cost = 0
    # Break loop when successor is now the first again
    while next != first:
        # Find the successor of current
        for j in GD[current]:
            if GD[current][j]['vSelect'].varValue == 1:
                # Next is the optimal successor
                next = j
                cycle = cycle + [next]
                cycle_cost = cycle_cost + GD[current][next]['cost']
                # Let the new current node be the successor
                current = next
                # Break the 'for' loop, since we found the unique successor
                break
            
    print('Cycle: %s, with cost:%s' % (str(cycle),str(cycle_cost)))
    
    return(cycle)
