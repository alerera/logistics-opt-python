# Python Code Implementing Basic Routing Tools
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
#  Flip
#
#  The basic step in a 2-exchange, where a path [a, ..., b] within
#  a cycle is reversed from end to start
#
#

import networkx as nx

# Reverse the path from a to b within the cycle
# Cycle must have b following a to be flipped: [..., a, ..., b, ...]
def Flip(cycle, a, b):
    
    # Cycle must have at least four nodes to be flipped
    if len(cycle) < 5:
        print('Cycle with fewer than 4 nodes cannot be flipped: %s' % str(cycle))
        return(cycle)
    # First, reorder the cycle as follows:
    # [pred(a), a, ..., b, ..., pred(a)]
    # Get the position in the list of a
    a_idx = cycle.index(a)
    if a_idx == 0:
        pred_a = cycle[-2]
    else:
        pred_a = cycle[a_idx-1]
    # Reorder the cycle to begin at pred_a    
    new_cycle = ReorderCycle(cycle,pred_a)
    b_idx = new_cycle.index(b)
    ba_seq = new_cycle[1:b_idx+1]
    ba_seq.reverse()
    new_cycle = new_cycle[:1] + ba_seq + new_cycle[b_idx+1:]
        
    return(new_cycle)

# Reorder cycle so that node s is the start node  
def ReorderCycle(cycle, s):
    s_idx = cycle.index(s)
    if s_idx == 0:
        return(cycle)
    else:
        return(cycle[s_idx:] + cycle[1:s_idx] + [s])
        
# Compute the cost of a cycle
def CycleCost(G, cycle):
    cycle_cost = 0
    i = cycle[0]
    for j in cycle[1:]:
        cycle_cost += G[i][j]['cost']     
        i = j
    return(cycle_cost)
 
# Find minimum cost insertion location for insert_node to cycle 
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