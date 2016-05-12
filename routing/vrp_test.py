# Test file for TSP Heuristics
#
# This is a python script file, which can be executed using the command "python tsp_undergrad.py"
#

import random
import math

import networkx as nx
import VRP_networkdesign as vrpnd
import TSP_networkdesign as tspnd
import farthest_insertion_simple as fi

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

# Add demands at nodes 2 through 6
G1.node[1]['demand'] = 0
G1.node[2]['demand'] = 3
G1.node[3]['demand'] = 2
G1.node[4]['demand'] = 5
G1.node[5]['demand'] = 1
G1.node[6]['demand'] = 6

Q = 6

print 'Optimal Tours'
opt_tours = vrpnd.VRP_networkdesign(G1, Q)


# Create harder network
G2 = nx.Graph()
n=0

# Initialize empty position vector
pos = []

# Input coordinate data
pos.append({'x':6823, 'y':4674})
n=n+1
pos.append({'x':7692, 'y':2247})
n=n+1
pos.append({'x':9135, 'y':6748})
n=n+1
pos.append({'x':7721, 'y':3451})
n=n+1
pos.append({'x':8304, 'y':8580})
n=n+1
pos.append({'x':7501, 'y':5899})
n=n+1
pos.append({'x':4687, 'y':1373})
n=n+1
pos.append({'x':5429, 'y':1408})
n=n+1
pos.append({'x':7877, 'y':1716})
n=n+1
pos.append({'x':7260, 'y':2083})
n=n+1
pos.append({'x':7096, 'y':7869})
n=n+1
pos.append({'x':6539, 'y':3513})
n=n+1
pos.append({'x':6272, 'y':2992})
n=n+1
pos.append({'x':6471, 'y':4275})
n=n+1
pos.append({'x':7110, 'y':4369})
n=n+1
pos.append({'x':6462, 'y':2634})
n=n+1
pos.append({'x':8476, 'y':2874})
n=n+1
pos.append({'x':3961, 'y':1370})
n=n+1
pos.append({'x':5555, 'y':1519})
n=n+1
pos.append({'x':4422, 'y':1249})
n=n+1
pos.append({'x':5584, 'y':3081})
n=n+1
pos.append({'x':5776, 'y':4498})
n=n+1
pos.append({'x':8035, 'y':2880})
n=n+1
pos.append({'x':6963, 'y':3782})
n=n+1
pos.append({'x':6336, 'y':7348})
n=n+1
pos.append({'x':8139, 'y':8306})
n=n+1
pos.append({'x':4326, 'y':1426})
n=n+1
pos.append({'x':5164, 'y':1440})
n=n+1
pos.append({'x':8389, 'y':5804})
n=n+1
pos.append({'x':4639, 'y':1629})
n=n+1
pos.append({'x':6344, 'y':1436})
n=n+1
pos.append({'x':5840, 'y':5736})
n=n+1
pos.append({'x':5972, 'y':2555})
n=n+1
pos.append({'x':7947, 'y':4373})
n=n+1
#pos.append({'x':6929, 'y':8958})
#n=n+1
#pos.append({'x':5366, 'y':1733})
#n=n+1
#pos.append({'x':4550, 'y':1219})
#n=n+1
#pos.append({'x':6901, 'y':1589})
#n=n+1
#pos.append({'x':6316, 'y':5497})
#n=n+1
#pos.append({'x':7010, 'y':2710})
#n=n+1
#pos.append({'x':9005, 'y':3996})
#n=n+1
#pos.append({'x':7576, 'y':7065})
#n=n+1
#pos.append({'x':4246, 'y':1701})
#n=n+1
#pos.append({'x':5906, 'y':1472})
#n=n+1
#pos.append({'x':6469, 'y':8971})
#n=n+1
#pos.append({'x':6152, 'y':2174})
#n=n+1
#pos.append({'x':5887, 'y':3796})
#n=n+1
#pos.append({'x':7203, 'y':5958})
#qn=n+1

# Generate a position ('pos') for each node in 2-D Euclidean space
for i in range(1,n+1):
    # Each iteration, add the node
    G2.add_node(i, {'pos': (pos[i-1]['x'],pos[i-1]['y']), 'demand':1} )

G2.node[1]['demand'] = 0


# Build arcs (i,j) for all j > i
# "range" in python: range(low, up) gives all integers >= low and < up
for i in range(1,n):
    for j in range(i+1,n+1):
        # Add the arc
        G2.add_edge(i,j)
        # Use Euclidean distance formula for cost
        delta_x = G2.node[i]['pos'][0] - G2.node[j]['pos'][0]
        delta_y = G2.node[i]['pos'][1] - G2.node[j]['pos'][1]
        G2[i][j]['cost'] = math.sqrt(delta_x**2 + delta_y**2)

print 'Finding Optimal TSP Tour...'    
opttsp_cycle = tspnd.TSP_networkdesign(G2)

print 'Finding Farthest Insertion Tour'
fi_cycle = fi.FarInsertionCycle(G2)

print 'Finding Optimal VRP Solution'
vrpnd.VRP_networkdesign(G2, 15)
