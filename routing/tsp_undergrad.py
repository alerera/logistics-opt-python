# Test file for TSP Heuristics
#
# This is a python script file, which can be executed using the command "python tsp_undergrad.py"
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

G1.add_edges_from([(1,2,{'cost':10})])
G1.add_edges_from([(1,3,{'cost':26})])
G1.add_edges_from([(1,4,{'cost':5})])
G1.add_edges_from([(1,5,{'cost':14})])
G1.add_edges_from([(1,6,{'cost':8})])

G1.add_edges_from([(2,3,{'cost':15})])
G1.add_edges_from([(2,4,{'cost':12})])
G1.add_edges_from([(2,5,{'cost':20})])
G1.add_edges_from([(2,6,{'cost':15})])

G1.add_edges_from([(3,4,{'cost':8})])
G1.add_edges_from([(3,5,{'cost':10})])
G1.add_edges_from([(3,6,{'cost':8})])

G1.add_edges_from([(4,5,{'cost':16})])
G1.add_edges_from([(4,6,{'cost':11})])

G1.add_edges_from([(5,6,{'cost':18})])

print 'Nearest Neighbor Results'

print 'How about for all start nodes?'
for j in G1.nodes():
    print 'Start node %s' % str(j)
    nn_cycle = nns.NearNeighCycle(G1, j)

#print 'Nearest Insertion Results'
#ni_cycle = nis.NearInsertionCycle(G1)

#print 'Farthest Insertion Results'
#fi_cycle = fis.FarInsertionCycle(G1)

#print 'Cheapest Insertion Results'
#ci_cycle = cis.CheapInsertionCycle(G1)

#print 'What if we start nearest insertion with the longest arc cycle?'
#ni_long_init_cycle = nis.NearInsertionCycle(G1, [4, 7, 4])

#print 'Two-Opt Results'
#for j in G1.nodes():
#    print 'Start node %s' % str(j)
#    to_cycle = to.TwoOptCycle(G1, nns.NearNeighCycle(G1, j))
    
#print 'Two-Opt on a Default Tour'
#to_cycle = to.TwoOptCycle(G1,[5,4,3,2,7,8,1,6,5])


