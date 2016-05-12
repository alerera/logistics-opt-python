# Python Code for Network Design Formulation of CVRP
#
# Alan Erera, 2013
#
# 
#  VRP_networkdesign
#
#  a function which, given a complete graph (directed or undirected) in the
#  networkx format, returns an optimal multiple vehicle routing solution using
#  a "network design" style formulation: design variables select the vehicle
#  routes, and the flow variables use the selected arcs to send flow from a
#  designated depot node to all other customer nodes
#
#  Inputs:
#
#   G           - network in networkx format
#                   * each node dictionary includes 'demand' attribute
#                   * each arc dictionary includes 'cost' cost attribute
#
#   Q           - vehicle capacity
#
#   m           - optional number of vehicle routes
#

# Module imports
import networkx as nx
# Import PuLP modeler functions
from pulp import *

def VRP_networkdesign(G, Q, m=False):
    
    # Total Customer Demand
    TotalDemand = 0
    
    # Let n be the number of nodes
    n = len(G)
    
    # This version will not assume that we have a complete graph, although
    # it is recommended.  If the IP does not find a feasible region for any
    # reason, it will fail somewhat ungracefully
    
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
            # Add the demand to the node dictionary
            GD.node[i]['demand'] = G.node[i]['demand']
            # Accumulate the total demand of all nodes for the depot supply
            TotalDemand = TotalDemand + G.node[i]['demand']
            for j in GD[i]:
                GD[i][j]['cost'] = G[i][j]['cost']
                GD.add_edge(j,i,{'cost':G[i][j]['cost']})
                
    # Create the math programming problem 'prob'
    prob = LpProblem("VRP By Network Design", LpMinimize)
    
    # Create VRP arc selection variables and flow variables for each directed arc
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
    # Generate successor selection constraint (non-splittable) for each node, except the one with
    # no demand which is assumed to be the depot
    for i in GD:
        # Successors for customers
        if GD.node[i]['demand'] > 0:
            prob += lpSum([GD[i][j]['vSelect'] for j in GD.successors(i)]) == 1, "Customer %s Successor Selection" % str(i)
        # For the depot node, if m is False then allow up to n successors.  If m is specified, then
        # choose exactly m successors
        elif m == False:
            prob += lpSum([GD[i][j]['vSelect'] for j in GD.successors(i)]) <= n, "Depot %s Number of Routes Bound" % str(i)
        else:
            prob += lpSum([GD[i][j]['vSelect'] for j in GD.successors(i)]) == m, "Depot %s Number of Routes Selection" % str(i)     
    
    # Generate predecessor selection constraint for each customer node only    
    for j in GD:
        if GD.node[j]['demand'] > 0:
            prob += lpSum([GD[i][j]['vSelect'] for i in GD.predecessors(j)]) == 1, "Node %s Predecessor Selection" % str(j)

    # Flow constraints
    # Generate flow upper bound constraints for each arc, which serve the role of
    # only allowing flow on design arcs chosen and limiting vehicle capacity
    for (i,j) in GD.edges():
        prob += GD[i][j]['vFlow'] <= Q*GD[i][j]['vSelect'], "Arc %s Flow Upper Bound" % str((i,j))
   
    # Generate flow balance constraints for all nodes
    for i in GD:
        # Flow consumed at node i is the demand...
        rhs =  - GD.node[i]['demand']
        # But if the demand is 0, this is the depot node which produces TotalDemand
        if rhs == 0:
            rhs = TotalDemand
        prob += lpSum([GD[i][j]['vFlow'] for j in GD.successors(i)]) - lpSum([GD[j][i]['vFlow'] for j in GD.predecessors(i)]) == rhs, "Node %s Flow Balance" % str(i)
    
    # Write out as a .LP file
    prob.writeLP("VRPNetworkDesignIP.lp")

    # The problem is solved using PuLP's choice of Solver
    prob.solve(GUROBI())

    # The status of the solution is printed to the screen
    print "Status:", LpStatus[prob.status]

    # Each of the variables is printed with it's resolved optimum value
    #for v in prob.variables():
    #    print v.name, "=", v.varValue

    # The optimised objective function value is printed to the screen    
    print "Total Cost = ", value(prob.objective)
        
    return(1)
