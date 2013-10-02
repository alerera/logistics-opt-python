# Python Code for Farthest Insertion
#
# 
#  FarInsertionCycle
#
#  a function which, given a complete graph (directed or undirected) in the
#  networkx format, returns a cycle using the farthest insertion heuristic
#
#  cycles will be in node list format: [first, ..., last, first]
#

# Module imports
import networkx as nx
import find_insertion as fi

def FarInsertionCycle(G, init_cycle=None):
    
    # If initial cycle is empty, find maxcost edge
    if init_cycle == None:
        # Grab all of the edge costs into dictionary d
        d = nx.get_edge_attributes(G, 'cost')
        # A python trick to find the key with minimum value in a dictionary
        # min function returns an element (key) from d, but the one with minimum value (d.get)
        maxcost_edge = max(d, key=d.get)
        cycle = [maxcost_edge[0], maxcost_edge[1], maxcost_edge[0]]
    else:
        cycle = init_cycle[:]
        
    # Initial cost
    cycle_cost = 0
    i = cycle[0]
    for j in cycle[1:]:
        cycle_cost += G[i][j]['cost']     
        i = j
    
    # Create a list of uninserted nodes, and their costs to the cycle
    uninserted_nodes = [node for node in G.nodes() if node not in cycle]
    if not uninserted_nodes:
        return(cycle)

    # Find the cheapest costs from uninserted nodes to cycle nodes
    # and build a dictionary
    # Initial values are the cost from the first node in the cycle
    uninserted_node_costs = dict( (node, G[node][cycle[0]]['cost']) for node in uninserted_nodes)
    for i in uninserted_node_costs.keys():
        for j in cycle[1:]:
            if G[i][j]['cost'] < uninserted_node_costs[i]:
                uninserted_node_costs[i] = G[i][j]['cost']
        
    # Perform the primary nearest insertion search until all nodes inserted
    while uninserted_node_costs.keys():
        # Node j to be inserted is furthest to the current cycle
        j = max(uninserted_node_costs, key=uninserted_node_costs.get)
        # Insert j
        best_insertion = fi.FindInsertionLocation(G, cycle, j)
        # Extract predecessor i from the best_insertion dictionary
        i = best_insertion['pred']
        # Use the slice to insert j
        cycle = cycle[:cycle.index(i)+1] + [j] + cycle[cycle.index(i)+1:]
        # index(i) gives the position of i in the cycle, measured from 0
        # list(index:count) is slice notation
        cycle_cost += best_insertion['cost']
        # Remove j from uninserted_node_costs
        del(uninserted_node_costs[j])
        # Update how close all nodes are to the new cycle by
        # checking whether cost to j is less than cost to current cycle
        for i in uninserted_node_costs.keys():
            uninserted_node_costs[i] = min(uninserted_node_costs[i], G[i][j]['cost'])
        
    print('Cycle: %s, with cost:%s' % (str(cycle),str(cycle_cost)))
       
    return(cycle)
