# Python Code for Nearest Neighbor
#
# 
#  NearNeighCycle
#
#  a function which, given a complete graph (directed or undirected) in the
#  networkx format and a start node, returns a cycle using the
#  nearest neighbor heuristic
#
#  
#

# Module imports
import networkx as nx

def NearNeighCycle(G, start_node):

    # Initialize the path at the start node    
    nn_path = [start_node]
    path_cost = 0
    
    # Create a copy of the node list
    unreached_nodes = G.nodes()
    unreached_nodes.remove(start_node)
    
    # Grab the largest arc cost in the network
    maxcost = max(nx.get_edge_attributes(G, 'cost').values())
    
    # Prepare for search
    end_node = start_node
    
    # Perform the primary nearest neighbor search until all nodes reached
    while unreached_nodes:
        cost = maxcost
        # Find nearest node j to end_node
        for j in unreached_nodes:
            if G[end_node][j]['cost'] <= cost:
                cost = G[end_node][j]['cost']
                closest = j
        # Add the closest to the path, and the incremental cost
        nn_path = nn_path + [closest]
        path_cost += cost
        end_node = closest
        # Update the unreached nodes
        unreached_nodes.remove(closest)
    
    # Finally, reach back to the starting node
    nn_path = nn_path + [start_node]
    path_cost += G[closest][start_node]['cost']
    
    print('Cycle: %s, with cost:%s' % (str(nn_path),str(path_cost)))
       
    # Rename the path nn_cycle for clarity
    nn_cycle = nn_path
    
    return(nn_cycle)
