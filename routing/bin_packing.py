# Python Code for Bin Packing
#
# Simple heuristics and a PuLP integer programming code

# Import PuLP linear integer programming modeling tools
from pulp import *

error_tol = 0.000000001

# 
#  exact_bin_packing
#
#  a function which, given a list with tuples containing item names and
#  single dimensional sizes, returns a dictionary with the number of required bins, and the
#  contents of each bin
#

def exact_bin_packing(item_list, Q=1):

    # Number of items is length of item_list, and maximum number of bins
    n = len(item_list)
    
    # Set of bins is numbered 1 through n
    Bins = range(1,n+1)
    
    # Set of items is also numbered 1 through n (for clarity)
    Items = range(1,n+1)
    
    # Copy the item sizes into size dictionary
    size = {}
    for i in Items:
        size[i] = item_list[i-1][1]
    
    # Create the binary integer program
    prob = LpProblem("Bin Packing", LpMinimize)

    # Create a bin open binary decision variable for n bins
    is_bin_open = LpVariable.dicts("IsBinOpen", Bins, cat=LpBinary)
    
    # Create an item to bin assignment variable for n items and n bins
    x = LpVariable.dicts("ItemToBin", (Items,Bins), cat=LpBinary)
    
    # Objective function
    # The objective function is always added to 'prob' first in PuLP
    prob += lpSum([is_bin_open[b] for b in Bins]), "Number of Opened Bins"

    # Constraints
    
    # Assignment of Each Item to a Bin
    for i in Items:
        prob += lpSum([x[i][b] for b in Bins]) == 1, "Item %s Assignment" % str(item_list[i-1][0])
        
    # No Bin Exceeds Capacity Q
    for b in Bins:
        prob += lpSum([size[i]*x[i][b] for i in Items]) <= Q, "Bin %s Capacity" % str(b)
        
    # No Items in Unopened Bins
    for i in Items:
        for b in Bins:
            prob += x[i][b] <= is_bin_open[b], "Item %s Bin %s Compatibility" % (str(item_list[i-1][0]),str(b))

    # Write out as a .LP file
    prob.writeLP("BinPacking.lp")

    # The problem is solved using PuLP's choice of Solver
    prob.solve(GUROBI())
    
    # Create the final bins
    bin = nextbin = 1
    BinContents = {}
    for b in Bins:
        for i in Items:
            # If item i packed in bin b, then start adding items
            if value(x[i][b]) == 1:
                if bin not in BinContents:
                    BinContents[bin]=[]
                BinContents[bin].append(item_list[i-1][0])
                nextbin = bin+1
        bin = nextbin
    
    return(BinContents)
    

# 
#  first_fit
#
#  a function which, given a list with tuples containing item names and
#  single dimensional sizes, returns a dictionary with the number of required bins, and the
#  contents of each bin
#

def first_fit(item_list, Q=1):

    # Open bin 1, initialize its remaining size to be Q
    nbins = 1
    BinSize = {1:Q}
    BinContents = {1:[]}
    
    # Loop over the items, and pack them
    for (item,size) in item_list:
        # Pack in lowest numbered bin where item fits
        packbin = 1
        # If the size is bigger than the bin, move to the next bin
        while size > BinSize[packbin] + error_tol:
            if packbin == nbins:
                packbin = nbins = nbins+1
                BinSize[packbin]=Q
                BinContents[packbin]=[]
            else:
                packbin += 1
            
        # Now we have the bin for packing, put it in there!
        BinSize[packbin] -= size
        BinContents[packbin].append(item)
        
    return(BinContents)
    
# 
#  best_fit
#
#  a function which, given a list with tuples containing item names and
#  single dimensional sizes, returns a dictionary with the number of required bins, and the
#  contents of each bin
#

def best_fit(item_list, Q=1):

    # Open bin 1, initialize its remaining size to be Q
    nbins = 1
    BinSize = {1:Q}
    BinContents = {1:[]}
    
    # Loop over the items, and pack them
    for (item,size) in item_list:
        
        best_bin_fit = Q
        packbin = nbins+1
        
        # Pack in bin where item fits best
        for bin in BinSize.keys():
            # If item fits
            if size <= BinSize[bin] + error_tol:
                bin_fit = BinSize[bin] - size
                if bin_fit < best_bin_fit:
                    packbin = bin
                    best_bin_fit = bin_fit
                    
        # If we must pack in a new bin        
        if packbin == nbins+1:
            BinSize[packbin]=Q
            BinContents[packbin]=[]
            nbins += 1
            
        # Now we have the bin for packing, put it in there!
        BinSize[packbin] -= size
        BinContents[packbin].append(item)
        
    return(BinContents)
    

#  next_fit
#
#  a function which, given a list with tuples containing item names and
#  single dimensional sizes, returns a dictionary with the number of required bins, and the
#  contents of each bin
#

def next_fit(item_list, Q=1):

    # Open bin 1, initialize its remaining size to be Q
    nbins = packbin = 1
    BinSize = {1:Q}
    BinContents = {1:[]}
    
    # Loop over the items, and pack them
    for (item,size) in item_list:
        if size > BinSize[packbin] + error_tol:
            packbin += 1
            BinSize[packbin]=Q
            BinContents[packbin]=[]
            
        # Now we have the bin for packing, put it in there!
        BinSize[packbin] -= size
        BinContents[packbin].append(item)
        
    return(BinContents)

