# Python Code for 2-Opt
#
# 
#  TwoOptCycle
#
#  a function which, given a complete graph (directed or undirected) in the
#  networkx format, and an initial cycle, returns a cycle improved by a series
#  of two-exchanges.  We implement an exhaustive first-improving search
#
#  cycles will be in node list format: [first, ..., last, first]
#

# Module imports
import networkx as nx
import tsp_tools as tt

# Zero tolerance
zero = 0.000001

def TwoOptCycle(G, init_cycle=None):
    
    # If initial cycle is empty, use default node tour
    if init_cycle == None:
        cycle = G.nodes() + [G.nodes()[0]]
    else:
        cycle = init_cycle[:]
        
    # Compute initial cost
    cycle_cost = tt.CycleCost(G, cycle)
    
    # Find improving 2-exchanges
    while True:
        # Look for first improving 2-exchange
        exchange = Find2Exchange(G, cycle)
        
        # If none found, stop the search
        if exchange['savings'] <= 0:
            break
        else:
            # Implement the implied flip, and record the cost savings
            cycle = tt.Flip(cycle, exchange['leaving_arcs'][0][1], exchange['leaving_arcs'][1][0])
            cycle_cost = cycle_cost - exchange['savings']
            # print('Found a new tour with savings of: %s' % str(exchange['savings']))
            print('New tour: %s' % str(cycle))
            
    print('Cycle: %s, with cost:%s' % (str(cycle),str(cycle_cost)))
       
    return(cycle)
    
# Find first improving 2-exchange in a cycle
def Find2Exchange(G, cycle):
    
    # Initial exchange finds no savings
    exchange = {'savings':0}
    
    # Node a is the head node of (pred_a, a) = x_1 to be removed
    for a_idx in range(1, len(cycle)-3):
        pred_a = cycle[a_idx-1]
        a = cycle[a_idx]
        # Node b is the tail node of (b, succ_b) = x_2 to be removed
        for b_idx in range(a_idx+1, len(cycle)-1):
            b = cycle[b_idx]
            succ_b = cycle[b_idx+1]
            # Compute savings
            savings = G[pred_a][a]['cost'] + G[b][succ_b]['cost'] - G[pred_a][b]['cost'] - G[a][succ_b]['cost']
            # If improving, return the improving exchange
            if savings > zero:
                exchange['savings'] = savings
                exchange['leaving_arcs'] = [(pred_a,a), (b, succ_b)]
                exchange['entering_arcs'] = [(pred_a,b), (a, succ_b)]
                return(exchange)
            
    return(exchange)
