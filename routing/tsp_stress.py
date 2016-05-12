# Test file for TSP Heuristics
#
# This is a python script file, which can be executed using the command "python tsp.py"
#

import random
import math

import networkx as nx
import TSP_networkdesign as tspnd
import nearest_neighbor_simple as nn
import two_opt as to

# Create undirected network with n nodes
G1 = nx.Graph()
n=150

# Generate a position ('pos') for each node in 2-D Euclidean space (square, 100 units per side)
for i in range(1,n+1):
    # Each iteration, update the position dictionary with new random coords
    pos_dict = {'pos':(100*random.random(), 100*random.random())}
    G1.add_node(i, pos_dict)

# Build arcs (i,j) for all j > i
# "range" in python: range(low, up) gives all integers >= low and < up
for i in range(1,n):
    for j in range(i+1,n+1):
        # Add the arc
        G1.add_edge(i,j)
        # Use Euclidean distance formula for cost
        delta_x = G1.node[i]['pos'][0] - G1.node[j]['pos'][0]
        delta_y = G1.node[i]['pos'][1] - G1.node[j]['pos'][1]
        G1[i][j]['cost'] = math.sqrt(delta_x**2 + delta_y**2)

#print 'Finding Optimal TSP Tour...'    
#opttsp_cycle = tspnd.TSP_networkdesign(G1)

print 'Finding Best Heuristic Tour'
nn_cycle = nn.NearNeighCycle(G1,1)
to_cycle = to.TwoOptCycle(G1,nn_cycle)




