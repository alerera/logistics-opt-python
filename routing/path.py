# Python Class Definition Module
#
#  Path
#
#  Define a directed path class, where paths are sequences of edges (arcs)
#  This format allows support for multi digraphs where more than one
#  network arc may connect any two pair of nodes.
#
#  Similar to networkx edges and nodes, this class supports for each
#  path a dictionary of path attributes
#
#  Attribute 'cost' has a special designation
#
#

class Path(object):
    """ A class for storing a directed path """
    # How the Path object represents itself to others
    def __repr__(self):
        return('Path(%s)' % (str(self.edges)))

    # Construct with a list of edges in the path, and an attributes dictionary
    def __init__(self, edges=[], attr={}):
        self.edges = edges
        self.attr = attr
        # If initialized with edges, ensure that we have a path
        if edges:
            self.validate()
            # Set the origin and destination
            self.origin = self.edges[0][0]
            self.dest = self.edges[-1][1]
    
    # Validator looks for errors in the structure of the path                    
    def validate(self):
        try:
            # Validate that the edge set forms a directed path
            last_head = self.edges[0][1]
            for e in self.edges[1:]:
                tail = e[0]
                if last_head != tail:
                    raise RuntimeError('Path with invalid edge set: ' + str(self.edges))
                last_head = e[1]
        except:
            raise RuntimeError('Error in path: all edges must have (tail,head) nodes.')
    
    # Implement methods to allow Path to act like a list of edges            
    # Implements the len() function to take Path object
    def __len__(self):
        return(len(self.edges))
        
    # Implements the attribute dictionary referencing model: Path[attr_key]
    def __getitem__(self, attr_key):
        return(self.attr[attr_key])
        
    def __setitem__(self, attr_key, value):
        self.attr[attr_key] = value
    
    # Implements the test: if edge in Path    
    def __contains__(self, edge):
        if edge in self.edges:
            return(True)
        return(False)
        
    # Implements the + operation to add an edge to path
    def __add__(self, edge):
        self.extend(edge)
    
    # Extend the path with additional edges, and delta_cost                    
    def extend(self, new_edges, delta_cost=0):
        # Add the new edges
        self.edges += new_edges
        # Validate
        self.validate()
        # Reset origin, destination, cost
        self.origin = self.edges[0][0]
        self.dest = self.edges[-1][1]
        if 'cost' in self.attr:
            self.attr['cost'] += delta_cost
        
