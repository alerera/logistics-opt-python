# Python Code to Find Best Insertion Location
#
# 
#  FindInsertionLocation
#
#  a function which, given a complete graph (directed or undirected) in the
#  networkx format and a node to be inserted, returns the predecessor i and
#  successor j that define where to insert, and the insertion cost, as
#  a dictionary:  {'pred':i, 'succ':j, 'cost':cost}
#
#  suppose input cycle = [first, ..., last, first]
#
#

import networkx as nx

def FindInsertionLocation(G, cycle, insert_node):

    # Initialize
    best_insertion = {}
    
    # Loop through the cycle
    i = cycle[0]
    for k in cycle[1:]:
        # Calculate insertion cost
        insert_cost = G[i][insert_node]['cost'] + G[insert_node][k]['cost'] - G[i][k]['cost']
        # If improved
        if not best_insertion or insert_cost <= best_insertion['cost']:
            best_insertion = {'pred':i, 'succ':k, 'cost':insert_cost}
        # Iterate forward
        i = k
        
    return(best_insertion)