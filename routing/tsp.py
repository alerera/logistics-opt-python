# Test file for TSP Heuristics
#
# This is a python script file, which can be executed using the command "python tsp.py"
#

import random
import math

import networkx as nx
import nearest_neighbor_simple as nns
import nearest_insertion_simple as nis
import farthest_insertion_simple as fis
import cheapest_insertion_simple as cis
import two_opt as to

# Create undirected network
G1 = nx.Graph()

G1.add_edges_from([(1,2,{'cost':30})])
G1.add_edges_from([(1,3,{'cost':25})])
G1.add_edges_from([(1,4,{'cost':85})])
G1.add_edges_from([(1,5,{'cost':75})])
G1.add_edges_from([(1,6,{'cost':60})])
G1.add_edges_from([(1,7,{'cost':55})])
G1.add_edges_from([(1,8,{'cost':70})])

G1.add_edges_from([(2,3,{'cost':20})])
G1.add_edges_from([(2,4,{'cost':65})])
G1.add_edges_from([(2,5,{'cost':60})])
G1.add_edges_from([(2,6,{'cost':70})])
G1.add_edges_from([(2,7,{'cost':60})])
G1.add_edges_from([(2,8,{'cost':90})])

G1.add_edges_from([(3,4,{'cost':70})])
G1.add_edges_from([(3,5,{'cost':55})])
G1.add_edges_from([(3,6,{'cost':45})])
G1.add_edges_from([(3,7,{'cost':70})])
G1.add_edges_from([(3,8,{'cost':65})])

G1.add_edges_from([(4,5,{'cost':25})])
G1.add_edges_from([(4,6,{'cost':70})])
G1.add_edges_from([(4,7,{'cost':120})])
G1.add_edges_from([(4,8,{'cost':105})])

G1.add_edges_from([(5,6,{'cost':50})])
G1.add_edges_from([(5,7,{'cost':110})])
G1.add_edges_from([(5,8,{'cost':95})])

G1.add_edges_from([(6,7,{'cost':70})])
G1.add_edges_from([(6,8,{'cost':60})])

G1.add_edges_from([(7,8,{'cost':60})])

print 'Nearest Neighbor Results'

print 'How about for all start nodes?'
for j in G1.nodes():
    print 'Start node %s' % str(j)
    nn_cycle = nns.NearNeighCycle(G1, j)

print 'Nearest Insertion Results'
ni_cycle = nis.NearInsertionCycle(G1)

print 'Farthest Insertion Results'
fi_cycle = fis.FarInsertionCycle(G1)

print 'Cheapest Insertion Results'
ci_cycle = cis.CheapInsertionCycle(G1)

print 'What if we start nearest insertion with the longest arc cycle?'
ni_long_init_cycle = nis.NearInsertionCycle(G1, [4, 7, 4])

print 'Two-Opt Results'
for j in G1.nodes():
    print 'Start node %s' % str(j)
    to_cycle = to.TwoOptCycle(G1, nns.NearNeighCycle(G1, j))
    
print 'Two-Opt on a Default Tour'
to_cycle = to.TwoOptCycle(G1,[5,4,3,2,7,8,1,6,5])


