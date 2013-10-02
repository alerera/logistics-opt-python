# Python Class Definition Module
#
# 
#  Path
#
#  a directed path class, where paths are sequences of edges (arcs)
#  This format allows support for multi digraphs where more than one
#  network arc may connect any two pair of nodes.
#
#  NodePath
#
#  a directed path class, where paths are sequences of nodes
#  This format is especially useful when the underlying network is
#  undirected
#
#  NodeCycle
#
#  a closed NodePath
#
#  Attribute 'cost' has a special designation
#
#

class Path(object):
    """ A class for storing a directed path as an edge list """
    # How the Path object represents itself to others
    def __repr__(self):
        return('Path(%s)' % (str(self.edges)))

    # Construct with a list of edges in the path, and an attributes dictionary
    def __init__(self, edges=None, attr=None):    
        if edges == None:
            self.edges = []
        else:
            # If user only supplies a single edge, turn it into a list
            if not isinstance(edges, list):
                edges = [edges]
            self.edges = edges
        if attr == None:
            self.attr = {}
        else:
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
        # Turn the supplied edge into a list
        if not isinstance(edge, list):
            edge = [edge]
        # Path + edge will modify the original path
        path.extend(edge)
    
    # Extend the path with additional edges, and delta_cost                    
    def extend(self, new_edges, delta_cost=0):
        # If edges not yet a list, turn them into a list
        if not isinstance(new_edges, list):
            new_edges = [new_edges]
        # Add the new edges
        self.edges += new_edges
        # Validate
        self.validate()
        # Reset origin, destination, cost
        self.origin = self.edges[0][0]
        self.dest = self.edges[-1][1]
        if 'cost' in self.attr:
            self.attr['cost'] += delta_cost

class NodePath(object):
    """ A class for storing a directed path as a node list """
    # How the Path object represents itself to others
    def __repr__(self):
        return('NodePath(%s)' % (str(self.nodes)))

    # Construct with a sequence of nodes in the path, and an attributes dictionary
    def __init__(self, nodes=None, attr=None):
        if nodes == None:
            self.nodes = []
        else:
            # If user passes a single node object, convert it to a list
            if not isinstance(nodes, list):
                nodes = [nodes]
            self.nodes = nodes
        if attr == None:
            self.attr = {}
        else:
            self.attr = attr
        # If initialized with nodes, set origin and destination
        if nodes:
            # Set the origin and destination
            self.origin = self.nodes[0]
            self.dest = self.nodes[-1]
    
    # Implement methods to allow NodePath to act like a list of nodes            
    # Implements the len() function to take NodePath object
    def __len__(self):
        # Return the node count in the path
        return(len(self.nodes))
        
    # Implements the attribute dictionary referencing model: NodePath[attr_key]
    def __getitem__(self, attr_key):
        return(self.attr[attr_key])
        
    def __setitem__(self, attr_key, value):
        self.attr[attr_key] = value
    
    # Implements the test: if node in NodePath    
    def __contains__(self, node):
        if node in self.nodes:
            return(True)
        return(False)
        
    # Implements the + operation to append nodes to the NodePath
    def __add__(self, new_nodes):
        # If user does not pass a list, make it a list
        if not isinstance(new_nodes, list):
            new_nodes = [new_nodes]
        # NodePath + new_nodes modifies NodePath
        self.extend(new_nodes)
        
    # Return a node's predecessor on path
    # Note: if nodes repeat, only the first predecessor returned
    def pred(self, node):
        try:
            node_idx = self.nodes.index(node)
            # First node in the path has no predecessor
            if node_idx == 0:
                return(node)
            else:
                return(self.nodes[node_idx-1])
        except:
            raise RuntimeError('Node %s not in path: %s' % (str(node),str(self.nodes)) )

    # Return a node's successor on path
    # Note: if nodes repeat, only the first successor returned
    def succ(self, node):
        try:
            node_idx = self.nodes.index(node)
            # Last node in the path has no successor
            if node_idx == len(self)-1:
                return(node)
            else:
                return(self.nodes[node_idx+1])
        except:
            raise RuntimeError('Node %s not in path: %s' % (str(node),str(self.nodes)) )
     
    # Extend the path with additional nodes, and delta_cost                    
    def extend(self, new_nodes, delta_cost=0):
        # If user does not pass a list, make it a list
        if not isinstance(new_nodes, list):
            new_nodes = [new_nodes]
        # Add the new edges
        self.nodes += new_nodes
        # Reset origin, destination, cost
        self.origin = self.nodes[0]
        self.dest = self.nodes[-1]
        if 'cost' in self.attr:
            self.attr['cost'] += delta_cost
            
    # Insert a node into a path, at delta_cost
    def insert(self, succ, node, delta_cost=0):
        # Insert node into the list immediately before succ(essor)
        try:
            succ_idx = self.nodes.index(succ)
        except:
            raise RuntimeError('Error in path insertion before %s: node %s not in path.' % (str(succ),str(succ)) )
        # With the index, perform the insert
        self.nodes.insert(succ_idx, node)
        if 'cost' in self.attr:
            self.attr['cost'] += delta_cost
    
    # Compute cost of path, with respect to a graph G    
    # Graph G assumed to be in the networkx format
    def cost(self, G):
        # Current assumes either simple graph or digraph
        # Does not handle case with multiple arcs connecting two nodes   
        cost = 0
        i = self.origin
        # Loop over all arcs in the path    
        for j in self.nodes[1:]:
            try:
                cost += G[i][j]['cost']
            except:
                raise RuntimeError('Arc (%s,%s) does not exist, or has no cost.' % (str(i),str(j)))
            # Iterate to the next arc
            i = j        
        # Set the cost attribute
        self.attr['cost'] = cost
        return(cost)
                
        
       
