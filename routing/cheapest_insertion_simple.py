# Python Code for Cheapest Insertion
#
# 
#  CheapInsertionCycle
#
#  a function which, given a complete graph (directed or undirected) in the
#  networkx format, returns a cycle using the cheap insertion heuristic
#
#  cycles will be in node list format: [first, ..., last, first]
#

# Module imports
import networkx as nx
import find_insertion as fi

def CheapInsertionCycle(G, init_cycle=None):
    
    # If initial cycle is empty, find mincost edge
    if init_cycle == None:
        # Grab all of the edge costs into dictionary d
        d = nx.get_edge_attributes(G, 'cost')
        # A python trick to find the key with minimum value in a dictionary
        # min function returns an element (key) from d, but the one with minimum value (d.get)
        mincost_edge = min(d, key=d.get)
        cycle = [mincost_edge[0], mincost_edge[1], mincost_edge[0]]
    else:
        cycle = init_cycle[:]
        
    # Initial cost
    cycle_cost = 0
    i = cycle[0]
    for j in cycle[1:]:
        cycle_cost += G[i][j]['cost']     
        i = j
    
    # Create a list of uninserted nodes
    uninserted_nodes = [node for node in G.nodes() if node not in cycle]
    if not uninserted_nodes:
        return(cycle)
    
    # Maintain two dictionaries: cheapest_insertion contains a node,
    # insertion postion, and insertion cost for the cheapest current insertion
    # to the cycle, and node_insertion_costs contains the cheapest insertion
    # costs for the uninserted nodes
    cheapest_insertion = {}
    node_insertions = {}
    for i in uninserted_nodes:
        best_i_insertion = fi.FindInsertionLocation(G, cycle, i)
        node_insertions[i] = best_i_insertion
        if not cheapest_insertion or best_i_insertion['cost'] < cheapest_insertion['insertion']['cost']:
            cheapest_insertion = {'node':i, 'insertion':best_i_insertion}
                                  
    # Perform the primary cheapest insertion search until all nodes inserted
    while node_insertions.keys():
        # Node j to be inserted is cheapest to the current cycle
        j = cheapest_insertion['node']
        # Extract predecessor, successor i from the cheapest_insertion dictionary
        i = cheapest_insertion['insertion']['pred']
        k = cheapest_insertion['insertion']['succ']
        # Use the slice to insert j
        cycle = cycle[:cycle.index(i)+1] + [j] + cycle[cycle.index(i)+1:]
        # index(i) gives the position of i in the cycle, measured from 0
        # list(index:count) is slice notation
        cycle_cost += cheapest_insertion['insertion']['cost']
        # Remove j from node_insertion_costs dictionary
        del(node_insertions[j])
        # Update insertion costs for remaining uninserted, and find the new
        # cheapest insertion choice
        cheapest_insertion = {}
        for node in node_insertions.keys():
            # Some nodes were best inserted between i and k and must be re-evaluated
            if node_insertions[node]['pred'] == i:
                node_insertions[node] = fi.FindInsertionLocation(G,cycle,node)
            # For the others, just look at new arcs (i,j) and (j,k)
            else:
                if G[i][node]['cost'] + G[node][j]['cost'] - G[i][j]['cost'] < node_insertions[node]['cost']:
                    node_insertions[node] = {'pred':i, 'succ':j, 'cost':G[i][node]['cost'] + G[node][j]['cost'] - G[i][j]['cost']}
                if G[j][node]['cost'] + G[node][k]['cost'] - G[j][k]['cost'] < node_insertions[node]['cost']:
                    node_insertions[node] = {'pred':j, 'succ':k, 'cost':G[j][node]['cost'] + G[node][k]['cost'] - G[j][k]['cost']}
            # Update the cheapest choice                   
            if not cheapest_insertion or node_insertions[node]['cost'] < cheapest_insertion['insertion']['cost']:
                cheapest_insertion = {'node':node, 'insertion':node_insertions[node]}
        
    print('Cycle: %s, with cost:%s' % (str(cycle),str(cycle_cost)))
       
    return(cycle)
