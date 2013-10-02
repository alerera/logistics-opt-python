# Test file

import random
import math

import networkx as nx
import nearest_neighbor_simple as nns
import nearest_insertion_simple as nis
import farthest_insertion_simple as fis
import cheapest_insertion_simple as cis

# Create undirected network
G1 = nx.Graph()

# Generate a position ('pos') for each node in 2-D Euclidean space (square, 100 units per side)
n=100
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

print 'Nearest Neighbor Results'

print 'How about for four start nodes?'
for j in range(1,5):
    print 'Start node %s' % str(j)
    nn_cycle = nns.NearNeighCycle(G1, j)

print 'Nearest Insertion Results'
ni_cycle = nis.NearInsertionCycle(G1)

print 'Farthest Insertion Results'
fi_cycle = fis.FarInsertionCycle(G1)

#print 'Cheapest Insertion Results'
#ci_cycle = cis.CheapInsertionCycle(G1)
