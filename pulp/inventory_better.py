#!/usr/bin/env python
"""
Inventory Problem from Winston

Authors: Alan Erera 2011
"""

# Import PuLP modeler functions
from pulp import *

# Creates a list of the quarters
Quarters = ['Q1', 'Q2', 'Q3', 'Q4']

# A dictionary of the demand for each quarter
Demand = {'Q1': 40, 
             'Q2': 60, 
             'Q3': 75, 
             'Q4': 25 }

# A dictionary of costs
Cost = {	'Reg': 400,
		'Ovt': 450,
		'Inv': 20 }

# Create the 'prob' object to contain the problem data
prob = LpProblem("Sailco Inventory", LpMinimize)

# Dictionaries created to contain the referenced Variables
reg_prod = LpVariable.dicts("RegProduction",Quarters,0)
ovt_prod = LpVariable.dicts("OverTimeProduction",Quarters,0)
inventory = LpVariable.dicts("Inventory",Quarters,0)

# The objective function is added to 'prob' first
prob += lpSum([Cost['Reg']*reg_prod[i] + Cost['Ovt']*ovt_prod[i] + Cost['Inv']*inventory[i] for i in Quarters]), "Total Cost"

# The four constraints are added to 'prob'
prob += reg_prod['Q1'] + ovt_prod['Q1'] + inventory['Q4'] - inventory['Q1'] == Demand['Q1'], "Q1Balance"
prob += reg_prod['Q2'] + ovt_prod['Q2'] + inventory['Q1'] - inventory['Q2'] == Demand['Q2'], "Q2Balance"
prob += reg_prod['Q3'] + ovt_prod['Q3'] + inventory['Q2'] - inventory['Q3'] == Demand['Q3'], "Q3Balance"
prob += reg_prod['Q4'] + ovt_prod['Q4'] + inventory['Q3'] - inventory['Q4'] == Demand['Q4'], "Q4Balance"

# Regular production upper bounds
prob += reg_prod['Q1'] <= 50, "Q1RegProductionLimit"
prob += reg_prod['Q2'] <= 50, "Q2RegProductionLimit"
prob += reg_prod['Q3'] <= 50, "Q3RegProductionLimit"
prob += reg_prod['Q4'] <= 50, "Q4RegProductionLimit"

# The problem data is written to an .lp file
prob.writeLP("SailcoInventory.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve(GUROBI())

# The status of the solution is printed to the screen
print "Status:", LpStatus[prob.status]

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print v.name, "=", v.varValue

# The optimised objective function value is printed to the screen    
print "Total Cost = ", value(prob.objective)