import torch
import torch.nn as nn
import networkx as nx


# class Model(nn.Module):

#     def __init__(self, input_features, output_features):
#         super(Model, self).__init__()
#         # Input features
#         self.input_features = input_features
#         # Output features
#         self.output_features = output_features
#         # Initialize dictionary of idx:modules in architecture
#         self.modules = {}
#         # Initialize connectivity graph
#         self.connections = nx.DiGraph()
#         self.connections.add_nodes_from(['in', 'out'])

#     def insertModule(self, idx, module_type='dense', params=None):
#         if module_type == 'conv':
#             module = nn.Conv2d(*params)

#         if module_type == 'dense':
#             module = nn.Linear(*params)

#         elif module_type == 'relu':
#             module = nn.ReLU()

#         self.modules[idx] = module
#         self.connections.add_node(idx)

#     def popModule(self, idx):
#         self.modules.pop(idx, None)
#         self.connections.remove_node(idx)

#     def addConnection(self, idx1, idx2):
#         def _inDimensions(module):
#             if

#         dim1 = self.input_features if idx1 == 'in' else self._outDimensions(
#             self.modules[idx1])
#         dim2 = self.output_features if idx2 == 'out' else self._inDimensions(
#             self.modules[idx2])

#         if dim1 == dim2:
#             self.connections.add_edge(idx1, idx2)
#         else:
#             raise Exception("Dimensions don't match")

#     def forward(self, x):
#         out = x
#         for module in self.modules:
#             out = module(out)
#         return out


class ModelGraph():

    def __init__(self, input_features, output_features):
        # Input features
        self.input_features = input_features
        # Output features
        self.output_features = output_features
        # Initialize dictionary of idx:modules in architecture
        self.modules = {}
        # Initialize connectivity graph
        self.connections = nx.DiGraph()
        self.connections.add_nodes_from(['in', 'out'])

    def insertModule(self, module_func=nn.ReLU, params=()):
        idx = 1
        while self.connections.has_node(idx):
            idx += 1

        module = module_func(*params)

        self.modules[idx] = module
        self.connections.add_node(idx)

        return idx

    def popModule(self, idx):
        if self.connections.has_node(idx):
            self.modules.pop(idx, None)
            self.connections.remove_node(idx)
        else:
            print('Missing module in graph')

    def addConnection(self, idx1, idx2):
        if self.connections.has_node(idx1) and self.connections.has_node(idx2):
            self.connections.add_edge(idx1, idx2)
        else:
            print('Missing module in graph')
        
    def checkConnection(self, idx='in'):
        if idx == 'out':
            return True
        
        dim_prev = self.getDimensions(idx)['dim_out']
        neighbors = self.connections.neighbors(idx)
        
        # Check dimensions for each layer connection
        for n in neighbors:
            dim_next = self.getDimensions(n)['dim_in']
            if dim_prev != dim_next:
                print('Dimensions issue between {} and {}'.format(idx, n))
                return False
            else:
                if not self.checkConnection(n):
                    return False
        
        return True
        
    def getDimensions(self, idx):
        if type(self.modules[idx]) == torch.nn.modules.conv.Conv2d:
            return ()
    
    def createModel(self):
        if not self.checkConnection('in'):
            print('Impossible to create model')
        else:
            pass
    
    

    
