# Test file for TSP Heuristics
#
# This is a python script file, which can be executed using the command "python tsp_undergrad.py"
#

import random
import math

import networkx as nx
import TSP_networkdesign as tspnd

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

print 'Optimal Tour'
opttsp_cycle = tspnd.TSP_networkdesign(G1)

