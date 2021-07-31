# import numpy as np
# import torch
import torch.nn as nn
# import networkx as nx
# import time as tm


class ModelTorch(nn.Module):
    def __init__(self, modulesDict, connectivityGraph):
        super(ModelTorch, self).__init__()
        self.connectivityGraph = connectivityGraph
        self.modulesDict = modulesDict

    def computeOutput(self, moduleIdx='out', inputTensor=None):
        if moduleIdx == 'in':
            return inputTensor

        predecessorModules = self.connectivityGraph.predecessors(moduleIdx)

        if len(tuple(predecessorModules)) == 1:
            predecessor, = tuple(predecessorModules)
            return self.modulesDict[moduleIdx](
                self.computeOutput(
                    moduleIdx=predecessor,
                    inputTensor=inputTensor))

        else:
            ## TODO: check if concatenates, sums, etc.
            return None

    def forward(self, inputTensor):
        return self.computeOutput('out', inputTensor)
